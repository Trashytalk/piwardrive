import argparse
import asyncio
import csv
import json
from dataclasses import asdict
from typing import Iterable

from persistence import load_recent_health, HealthRecord


EXPORT_FORMATS = ("csv", "json")


def _write_csv(records: Iterable[HealthRecord], path: str) -> None:
    rows = [asdict(r) for r in records]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        if rows:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


def _write_json(records: Iterable[HealthRecord], path: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump([asdict(r) for r in records], fh)


async def _load_records(limit: int) -> list[HealthRecord]:
    return await load_recent_health(limit)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Export recent health records")
    parser.add_argument("output", help="Output file path")
    parser.add_argument(
        "--format",
        "-f",
        choices=EXPORT_FORMATS,
        default="json",
        help="Output format",
    )
    parser.add_argument(
        "--limit",
        "-n",
        type=int,
        default=10,
        help="Number of records to export",
    )
    args = parser.parse_args(argv)

    records = asyncio.run(_load_records(args.limit))
    if args.format == "csv":
        _write_csv(records, args.output)
    else:
        _write_json(records, args.output)


if __name__ == "__main__":
    main()
