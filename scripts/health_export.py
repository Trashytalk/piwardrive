"""Module health_export."""
import argparse
import asyncio
import csv
import json
from dataclasses import asdict
from typing import Iterable

try:
    from persistence import HealthRecord, load_recent_health  # type: ignore
except Exception:  # pragma: no cover - fall back if tests replaced module
    from piwardrive.persistence import HealthRecord, load_recent_health


EXPORT_FORMATS = ("csv", "json")


def _write_csv(records: Iterable[HealthRecord], path: str) -> None:
    it = iter(records)
    try:
        first = next(it)
    except StopIteration:
        open(path, "w", newline="", encoding="utf-8").close()
        return

    first_row = asdict(first)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(first_row.keys()))
        writer.writeheader()
        writer.writerow(first_row)
        for rec in it:
            writer.writerow(asdict(rec))


def _write_json(records: Iterable[HealthRecord], path: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("[")
        first = True
        for r in records:
            if not first:
                fh.write(",")
            json.dump(asdict(r), fh)
            first = False
        fh.write("]")


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
