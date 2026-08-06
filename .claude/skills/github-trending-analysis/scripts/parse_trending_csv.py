#!/usr/bin/env python3
"""Parse a github-trending "final" CSV (see ../github-trending skill) and print
its period metadata + rows as JSON.

This is a read-only, deterministic helper: it does no analysis or generation.
Its only job is to make the period (since/language/timestamp) and the existing
per-repo data machine-readable so it can be handed to analysis subagents.

Usage:
    python3 parse_trending_csv.py --csv-path <path to *_final.csv>

Expected filename pattern (as produced by the github-trending skill):
    trending_{since}_{language}_{YYYY-MM-DD}_{HHMMSS}_final.csv
e.g. trending_weekly_all_2026-07-29_103249_final.csv
"""
import argparse
import csv
import json
import os
import re
import sys

FILENAME_RE = re.compile(
    r"^trending_(?P<since>daily|weekly|monthly)_(?P<language>[^_]+)_"
    r"(?P<date>\d{4}-\d{2}-\d{2})_(?P<time>\d{6})_final\.csv$"
)
# Fallback for older files saved before timestamps were added to filenames,
# e.g. trending_daily_all_2026-07-29_final.csv (no HHMMSS component).
LEGACY_FILENAME_RE = re.compile(
    r"^trending_(?P<since>daily|weekly|monthly)_(?P<language>[^_]+)_"
    r"(?P<date>\d{4}-\d{2}-\d{2})_final\.csv$"
)

PERIOD_LABELS = {
    "daily": "1日間(daily)",
    "weekly": "1週間(weekly)",
    "monthly": "1か月間(monthly)",
}


def parse_filename(filename, parent_dir=None):
    match = FILENAME_RE.match(filename)
    if match:
        d = match.groupdict()
        date, time = d["date"], d["time"]
        return {
            "since": d["since"],
            "since_label": PERIOD_LABELS.get(d["since"], d["since"]),
            "language_filter": d["language"],
            "collected_date": date,
            "collected_at": f"{date} {time[0:2]}:{time[2:4]}:{time[4:6]}",
        }

    match = LEGACY_FILENAME_RE.match(filename)
    if match:
        d = match.groupdict()
        return {
            "since": d["since"],
            "since_label": PERIOD_LABELS.get(d["since"], d["since"]),
            "language_filter": d["language"],
            "collected_date": d["date"],
            "collected_at": f"{d['date']} (時刻不明: ファイル名に時刻情報なし)",
        }

    # Last resort: infer `since` from the parent directory name (daily/weekly/monthly)
    # and pull any YYYY-MM-DD found in the filename for the date.
    if parent_dir in PERIOD_LABELS:
        date_match = re.search(r"\d{4}-\d{2}-\d{2}", filename)
        return {
            "since": parent_dir,
            "since_label": PERIOD_LABELS[parent_dir],
            "language_filter": None,
            "collected_date": date_match.group(0) if date_match else None,
            "collected_at": (date_match.group(0) if date_match else "不明") + " (時刻不明: ファイル名から推定できず)",
        }

    return None


def main():
    parser = argparse.ArgumentParser(description="Parse a github-trending final CSV into JSON (metadata + rows).")
    parser.add_argument("--csv-path", required=True, help="Path to a trending_{since}_{lang}_{date}_{time}_final.csv file")
    args = parser.parse_args()

    if not os.path.isfile(args.csv_path):
        parser.error(f"File not found: {args.csv_path}")

    filename = os.path.basename(args.csv_path)
    parent_dir = os.path.basename(os.path.dirname(os.path.abspath(args.csv_path)))
    meta = parse_filename(filename, parent_dir=parent_dir)
    if meta is None:
        print(
            f"WARNING: filename '{filename}' does not match the expected "
            "trending_{since}_{language}_{date}_{time}_final.csv pattern; "
            "period metadata could not be inferred.",
            file=sys.stderr,
        )
        meta = {
            "since": None, "since_label": None,
            "language_filter": None, "collected_date": None, "collected_at": None,
        }

    with open(args.csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    result = {
        "csv_path": args.csv_path,
        **meta,
        "repo_count": len(rows),
        "rows": rows,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
