#!/usr/bin/env python3
"""Merge a raw trending CSV (from scrape_trending.py) with an AI-generated
enrichment JSON into the final CSV requested by the user.

The enrichment JSON must map "owner/repo" -> {"overview": str, "highlights": str,
"usage_ideas": str}. It is produced by a Claude subagent (see SKILL.md) -- this
script does no generation itself, it only merges and formats.

The base CSV is expected under a <root>/intermediate/<since>/... directory (as
written by scrape_trending.py). If --output is omitted, the final CSV is placed
under the sibling <root>/final/<since>/... directory automatically, keeping
intermediate and final data -- and daily/weekly/monthly -- in separate folders.

Usage:
    python3 merge_enriched.py --base-csv data/intermediate/daily/trending_daily_python_..._raw.csv \\
        --enrichment-json data/intermediate/daily/enrichment_daily_python_....json
    # -> writes data/final/daily/trending_daily_python_..._final.csv

    # Or specify the output path explicitly:
    python3 merge_enriched.py --base-csv data/intermediate/daily/trending_daily_python_..._raw.csv \\
        --enrichment-json data/intermediate/daily/enrichment_daily_python_....json \\
        --output data/final/daily/trending_daily_python_..._final.csv
"""
import argparse
import csv
import json
import os
import sys

FINAL_HEADER = [
    "リポジトリ名",
    "主要言語",
    "概要",
    "GitHubURL",
    "Star増分",
    "注目ポイント/要約",
    "活用アイデア/関連性/所感",
    "ライセンス",
    "first commit日",
]


def default_output_path(base_csv_path):
    """Mirror <root>/intermediate/<since>/name_raw.csv -> <root>/final/<since>/name_final.csv."""
    since_dir = os.path.dirname(base_csv_path)
    since = os.path.basename(since_dir)
    root = os.path.dirname(os.path.dirname(since_dir))
    basename = os.path.basename(base_csv_path)
    if basename.endswith("_raw.csv"):
        basename = basename[: -len("_raw.csv")] + "_final.csv"
    else:
        basename = os.path.splitext(basename)[0] + "_final.csv"
    return os.path.join(root, "final", since, basename)


def load_base_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_enrichment(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Merge raw trending CSV with AI-generated enrichment JSON.")
    parser.add_argument("--base-csv", required=True, help="Raw CSV produced by scrape_trending.py")
    parser.add_argument("--enrichment-json", required=True, help="JSON mapping owner/repo -> {overview, highlights, usage_ideas}")
    parser.add_argument("--output", default=None, help="Path to write the final CSV (default: derived from --base-csv, see module docstring)")
    args = parser.parse_args()

    output_path = args.output or default_output_path(args.base_csv)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    base_rows = load_base_rows(args.base_csv)
    enrichment = load_enrichment(args.enrichment_json)

    missing = []
    final_rows = []
    for row in base_rows:
        repo = row["repository"]
        info = enrichment.get(repo)
        if info is None:
            missing.append(repo)
            info = {}
        final_rows.append([
            repo,
            row.get("language", ""),
            info.get("overview", ""),
            row.get("url", ""),
            row.get("stars_period", ""),
            info.get("highlights", ""),
            info.get("usage_ideas", ""),
            row.get("license", ""),
            row.get("first_commit_date", ""),
        ])

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(FINAL_HEADER)
        writer.writerows(final_rows)

    print(f"Wrote {len(final_rows)} rows -> {output_path}")
    if missing:
        print(
            f"WARNING: {len(missing)} repositories had no entry in the enrichment JSON "
            f"and were left blank: {', '.join(missing)}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
