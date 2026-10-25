#!/usr/bin/env python3
"""Summarize recorded usability session outcomes by task."""

from __future__ import annotations

import argparse
import csv
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import TextIO

REQUIRED_COLUMNS = {"session_id", "task", "outcome", "duration_seconds"}
VALID_OUTCOMES = {"complete", "blocked", "abandoned"}


def summarize(stream: TextIO) -> list[dict[str, object]]:
    reader = csv.DictReader(stream)
    fields = set(reader.fieldnames or ())
    missing = REQUIRED_COLUMNS - fields
    if missing:
        raise ValueError("Missing CSV columns: " + ", ".join(sorted(missing)))

    rows: dict[str, list[tuple[str, float | None]]] = defaultdict(list)
    seen_records: set[tuple[str, str]] = set()
    for line_number, row in enumerate(reader, start=2):
        session_id = (row.get("session_id") or "").strip()
        task = (row.get("task") or "").strip()
        outcome = (row.get("outcome") or "").strip().lower()
        raw_duration = (row.get("duration_seconds") or "").strip()
        if not session_id or not task:
            raise ValueError(f"Line {line_number}: session_id and task are required")
        record_key = (session_id, task)
        if record_key in seen_records:
            raise ValueError(f"Line {line_number}: session_id and task must be unique")
        seen_records.add(record_key)
        if outcome not in VALID_OUTCOMES:
            raise ValueError(f"Line {line_number}: outcome must be one of {sorted(VALID_OUTCOMES)}")
        try:
            duration = float(raw_duration) if raw_duration else None
        except ValueError as error:
            raise ValueError(f"Line {line_number}: duration_seconds must be numeric") from error
        if duration is not None and duration < 0:
            raise ValueError(f"Line {line_number}: duration_seconds cannot be negative")
        rows[task].append((outcome, duration))

    result: list[dict[str, object]] = []
    for task in sorted(rows):
        task_rows = rows[task]
        times = [duration for _, duration in task_rows if duration is not None]
        result.append({
            "task": task,
            "sessions": len(task_rows),
            "complete": sum(outcome == "complete" for outcome, _ in task_rows),
            "blocked": sum(outcome == "blocked" for outcome, _ in task_rows),
            "abandoned": sum(outcome == "abandoned" for outcome, _ in task_rows),
            "median_seconds": statistics.median(times) if times else None,
        })
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path, help="CSV file of session observations")
    args = parser.parse_args()
    try:
        with args.csv_file.open("r", encoding="utf-8", newline="") as stream:
            summaries = summarize(stream)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=["task", "sessions", "complete", "blocked", "abandoned", "median_seconds"],
    )
    writer.writeheader()
    writer.writerows(summaries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
