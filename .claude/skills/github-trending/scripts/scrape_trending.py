#!/usr/bin/env python3
"""Scrape GitHub Trending (https://github.com/trending) and save results as a "raw" CSV.

This script only produces deterministically-scrapable fields (no generative AI):
rank, repository, url, description, language, stars, forks, stars gained in the
period, license, and first-commit date. Columns that require reading/understanding
a repo (overview, highlights, usage ideas) are intentionally NOT produced here --
see merge_enriched.py and SKILL.md for that step, which is delegated to a Claude
subagent.

`license` is scraped from each repo's HTML page (the "About" sidebar), same as the
trending page itself -- it is NOT subject to the GitHub REST API's rate limit.
`first_commit_date` still requires the GitHub REST API (paginating commit history
to find the oldest commit), so it remains subject to the unauthenticated 60/hour
limit.

Usage:
    python3 scrape_trending.py [--language LANG] [--since daily,weekly,monthly] [--output-dir DIR]

Examples:
    python3 scrape_trending.py
    python3 scrape_trending.py --language python --since daily
    python3 scrape_trending.py --language javascript --since daily,weekly,monthly --output-dir ./data

Set GITHUB_TOKEN (or GH_TOKEN) in the environment to raise the GitHub API rate
limit from 60/hour to 5000/hour for first_commit_date lookups on many repositories.
"""
import argparse
import csv
import datetime
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

from bs4 import BeautifulSoup

BASE_URL = "https://github.com/trending"
API_BASE = "https://api.github.com"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
VALID_SINCE = ("daily", "weekly", "monthly")

_rate_limit_warned = False


def build_url(language, since):
    url = BASE_URL
    if language and language != "all":
        url += f"/{language}"
    url += f"?since={since}"
    return url


def fetch_html(url, retries=3, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_err = None
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8")
        except (urllib.error.URLError, urllib.error.HTTPError) as err:
            last_err = err
            if attempt < retries:
                time.sleep(2 * attempt)
    raise RuntimeError(f"Failed to fetch {url}: {last_err}")


def parse_int(text):
    if not text:
        return 0
    text = text.strip().replace(",", "")
    match = re.match(r"(\d+(?:\.\d+)?)(k)?", text, re.IGNORECASE)
    if not match:
        return 0
    value = float(match.group(1))
    if match.group(2):
        value *= 1000
    return int(value)


def parse_trending_html(html, since, language):
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.select("article.Box-row")
    results = []
    scraped_at = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")

    for rank, row in enumerate(rows, start=1):
        title_link = row.select_one("h2 a")
        if not title_link:
            continue
        full_name = re.sub(r"\s+", "", title_link.get_text())
        repo_path = title_link.get("href", "").strip("/")
        url = f"https://github.com/{repo_path}" if repo_path else ""

        desc_el = row.select_one("p.col-9")
        description = desc_el.get_text(strip=True) if desc_el else ""

        lang_el = row.select_one("span[itemprop='programmingLanguage']")
        repo_language = lang_el.get_text(strip=True) if lang_el else ""

        star_links = row.select("a[href$='/stargazers']")
        stars_total = parse_int(star_links[0].get_text()) if star_links else 0

        fork_links = row.select("a[href$='/forks']")
        forks_total = parse_int(fork_links[0].get_text()) if fork_links else 0

        period_el = row.select_one("span.d-inline-block.float-sm-right")
        stars_period_text = period_el.get_text(strip=True) if period_el else ""
        stars_period = parse_int(stars_period_text)

        results.append({
            "rank": rank,
            "repository": full_name or repo_path,
            "url": url,
            "description": description,
            "language": repo_language,
            "stars_total": stars_total,
            "forks_total": forks_total,
            "stars_period": stars_period,
            "since": since,
            "language_filter": language or "all",
            "scraped_at": scraped_at,
        })

    return results


def build_api_headers():
    headers = {"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _api_get(url, headers, timeout=15):
    global _rate_limit_warned
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body, resp.headers.get("Link")
    except urllib.error.HTTPError as err:
        if err.code in (403, 429) and not _rate_limit_warned:
            _rate_limit_warned = True
            print(
                "WARNING: GitHub API rate limit hit. Set GITHUB_TOKEN (or GH_TOKEN) "
                "in the environment for a higher limit (60/hr -> 5000/hr). "
                "first_commit_date will be left blank for remaining repos "
                "(license is unaffected -- it's scraped from the page, not the API).",
                file=sys.stderr,
            )
        return None, None
    except urllib.error.URLError:
        return None, None


def fetch_license(repo_path, headers=None):
    """Scrape the license off the repo's HTML page (About sidebar), not the API.

    This avoids the GitHub REST API's 60/hour unauthenticated rate limit entirely --
    it's a plain page fetch, same as the trending page itself. The About sidebar
    renders the license next to a "law" icon, e.g.:
        <a ...><svg class="octicon octicon-law" ...></svg>
          <span data-component="text" data-content="MIT license">MIT license</span></a>
    """
    try:
        html = fetch_html(f"https://github.com/{repo_path}")
    except RuntimeError:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    icon = soup.select_one("svg.octicon-law")
    if not icon:
        return ""
    link = icon.find_parent("a")
    if not link:
        return ""
    text_el = link.select_one('span[data-component="text"]') or link
    text = text_el.get_text(strip=True)
    return re.sub(r"\s*license$", "", text, flags=re.IGNORECASE).strip()


def _last_page_url(link_header):
    if not link_header:
        return None
    match = re.search(r'<([^>]+)>;\s*rel="last"', link_header)
    return match.group(1) if match else None


def fetch_first_commit_date(repo_path, headers):
    data, link = _api_get(f"{API_BASE}/repos/{repo_path}/commits?per_page=1", headers)
    if data is None:
        return ""
    last_url = _last_page_url(link)
    commit = None
    if last_url:
        last_data, _ = _api_get(last_url, headers)
        if last_data:
            commit = last_data[-1]
    if commit is None and data:
        commit = data[0]
    if not commit:
        return ""
    commit_info = commit.get("commit", {})
    date = (commit_info.get("author") or {}).get("date") or (commit_info.get("committer") or {}).get("date")
    return date or ""


def enrich_with_metadata(rows, skip_first_commit=False):
    """Attach license / first_commit_date to each row, fetching each unique repo once.

    license: scraped from the repo's HTML page (no rate limit beyond normal fetches).
    first_commit_date: still needs the GitHub REST API (commit history pagination),
    so it remains subject to the unauthenticated 60/hour limit. Pass
    skip_first_commit=True to leave it blank without spending any API calls on it.
    """
    headers = build_api_headers()
    cache = {}
    unique_repos = sorted({row["repository"] for row in rows if row["repository"]})
    for repo_path in unique_repos:
        print(f"Fetching metadata for {repo_path} ...", file=sys.stderr)
        cache[repo_path] = {
            "license": fetch_license(repo_path),
            "first_commit_date": "" if skip_first_commit else fetch_first_commit_date(repo_path, headers),
        }
    for row in rows:
        meta = cache.get(row["repository"], {})
        row["license"] = meta.get("license", "")
        row["first_commit_date"] = meta.get("first_commit_date", "")


FIELDNAMES = [
    "rank", "repository", "url", "description", "language",
    "stars_total", "forks_total", "stars_period", "since",
    "language_filter", "scraped_at", "license", "first_commit_date",
]


def write_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description="Scrape GitHub Trending into a raw CSV (no AI-generated fields).")
    parser.add_argument("--language", default=None, help="Language filter, e.g. python, javascript. Omit for all languages.")
    parser.add_argument("--since", default="daily,weekly,monthly", help="Comma-separated list among daily,weekly,monthly (default: all three).")
    parser.add_argument("--output-dir", default="data", help="Directory to write CSV files into (default: ./data).")
    parser.add_argument("--skip-api-enrich", action="store_true", help="Skip license (page scrape) and first_commit_date (API) lookups entirely.")
    parser.add_argument("--skip-first-commit", action="store_true", help="Skip only first_commit_date (GitHub API); license is still scraped from the page.")
    args = parser.parse_args()

    since_list = [s.strip().lower() for s in args.since.split(",") if s.strip()]
    for s in since_list:
        if s not in VALID_SINCE:
            parser.error(f"Invalid --since value '{s}'. Must be one of {VALID_SINCE}.")

    now = datetime.datetime.now()
    # Include the time (not just the date) since the script can be run multiple times per day.
    timestamp = now.strftime("%Y-%m-%d_%H%M%S")
    lang_tag = args.language if args.language else "all"

    rows_by_since = {}
    for since in since_list:
        url = build_url(args.language, since)
        print(f"Fetching {url} ...", file=sys.stderr)
        html = fetch_html(url)
        rows_by_since[since] = parse_trending_html(html, since, args.language)

    if not args.skip_api_enrich:
        all_rows = [row for rows in rows_by_since.values() for row in rows]
        enrich_with_metadata(all_rows, skip_first_commit=args.skip_first_commit)
    else:
        for rows in rows_by_since.values():
            for row in rows:
                row["license"] = ""
                row["first_commit_date"] = ""

    for since, rows in rows_by_since.items():
        # Intermediate (raw) data is kept separate from final output, split by period.
        since_dir = os.path.join(args.output_dir, "intermediate", since)
        os.makedirs(since_dir, exist_ok=True)
        filename = f"trending_{since}_{lang_tag}_{timestamp}_raw.csv"
        path = os.path.join(since_dir, filename)
        write_csv(rows, path)
        print(f"Saved {len(rows)} repositories -> {path}")


if __name__ == "__main__":
    main()
