"""Summarize rows in health monitor databases."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
from typing import Dict

KEY_TABLES = ("health_records", "ap_cache")


def summarize(path: str) -> Dict[str, int]:
    """Return row counts for ``KEY_TABLES`` in ``path``."""
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    counts: Dict[str, int] = {}
    with sqlite3.connect(path) as db:
        for table in KEY_TABLES:
            try:
                row = db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
            except sqlite3.DatabaseError:
                counts[table] = 0
            else:
                counts[table] = int(row[0]) if row else 0
    return counts


def main(argv: list[str] | None = None) -> None:
    """Print row counts for tables in a health.db file."""
    parser = argparse.ArgumentParser(
        description="Show row counts for health monitor tables"
    )
    parser.add_argument("db", help="path to health.db")
    parser.add_argument("--json", action="store_true", help="output JSON")
    args = parser.parse_args(argv)

    counts = summarize(args.db)
    if args.json:
        print(json.dumps(counts))
    else:
        for name, count in counts.items():
            print(f"{name}: {count}")


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
