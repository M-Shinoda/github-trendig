#!/usr/bin/env python3
"""Assemble a github-trending analysis report from Markdown fragments written
by analysis subagents, plus a header derived from the source CSV's filename.

Each fragment file is plain Markdown, one "## owner/repo" section per
repository (see SKILL.md for the exact template subagents must follow). This
script does no research or generation itself -- it only validates coverage
against the source CSV and concatenates fragments into one report. No JSON
intermediate is produced or consumed.

Usage:
    python3 build_report.py --csv-path <original *_final.csv> \\
        --fragment analysis/daily/batch1.md --fragment analysis/daily/batch2.md \\
        [--output <path to write the .md report>]

If --output is omitted, the report is written next to a sibling "analysis"
directory that mirrors the source CSV's "final/<since>/" location, e.g.:
    .../data/final/weekly/trending_weekly_all_..._final.csv
    -> .../data/analysis/weekly/trending_weekly_all_..._analysis.md
"""
import argparse
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse_trending_csv import parse_filename  # noqa: E402

REPO_HEADING_RE = re.compile(r"^##\s+([\w.\-]+/[\w.\-]+)\s*$", re.MULTILINE)


def default_output_path(csv_path):
    csv_path = os.path.abspath(csv_path)
    parts = csv_path.split(os.sep)
    if "final" in parts:
        idx = parts.index("final")
        parts[idx] = "analysis"
    else:
        parts = parts[:-1] + ["analysis", parts[-1]]
    basename = os.path.basename(parts[-1])
    if basename.endswith("_final.csv"):
        basename = basename[: -len("_final.csv")] + "_analysis.md"
    else:
        basename = os.path.splitext(basename)[0] + "_analysis.md"
    parts[-1] = basename
    return os.sep.join(parts)


def load_repo_names(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        return [row["リポジトリ名"] for row in csv.DictReader(f)]


def build_header(csv_path, repo_count):
    filename = os.path.basename(csv_path)
    parent_dir = os.path.basename(os.path.dirname(os.path.abspath(csv_path)))
    meta = parse_filename(filename, parent_dir=parent_dir) or {}

    lines = ["# GitHub Trending 分析レポート", ""]
    if meta.get("since_label"):
        lines.append(f"- 対象期間: {meta['since_label']} (収集: {meta.get('collected_at', '不明')})")
    if meta.get("language_filter"):
        lines.append(f"- 対象言語フィルタ: {meta['language_filter']}")
    lines.append(f"- リポジトリ数: {repo_count}")
    lines.append(f"- 元データ: `{csv_path}`")
    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Assemble a Markdown trend-analysis report from subagent-written Markdown fragments.")
    parser.add_argument("--csv-path", required=True, help="Original trending *_final.csv (used for the header and coverage check)")
    parser.add_argument("--fragment", action="append", required=True, dest="fragments",
                         help="Path to a Markdown fragment file; repeat in the order they should appear")
    parser.add_argument("--output", default=None, help="Path to write the .md report (default: derived from --csv-path)")
    args = parser.parse_args()

    output_path = args.output or default_output_path(args.csv_path)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    expected_repos = load_repo_names(args.csv_path)

    fragment_texts = []
    covered_repos = []
    for path in args.fragments:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        fragment_texts.append(text.rstrip())
        covered_repos.extend(REPO_HEADING_RE.findall(text))

    header = build_header(args.csv_path, len(expected_repos))
    body = "\n\n".join(fragment_texts) + "\n"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header + "\n" + body)

    print(f"Wrote report ({len(expected_repos)} repositories in source CSV) -> {output_path}")

    missing = [r for r in expected_repos if r not in covered_repos]
    extra = [r for r in covered_repos if r not in expected_repos]
    if missing:
        print(f"WARNING: {len(missing)} repositories from the CSV have no '## owner/repo' section in any fragment: {', '.join(missing)}", file=sys.stderr)
    if extra:
        print(f"WARNING: {len(extra)} '## owner/repo' sections in fragments do not match any repository in the CSV: {', '.join(extra)}", file=sys.stderr)
    dupes = [r for r in set(covered_repos) if covered_repos.count(r) > 1]
    if dupes:
        print(f"WARNING: {len(dupes)} repositories appear in more than one fragment (possible duplicate): {', '.join(dupes)}", file=sys.stderr)


if __name__ == "__main__":
    main()
