import argparse
import asyncio
import csv
import json
from typing import Iterable

from persistence import HealthRecord, save_health_record

IMPORT_FORMATS = ("csv", "json")


def _parse_json(path: str) -> list[HealthRecord]:
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    records = []
    for row in data:
        if not isinstance(row, dict):
            continue
        records.append(
            HealthRecord(
                timestamp=str(row.get("timestamp", "")),
                cpu_temp=row.get("cpu_temp"),
                cpu_percent=float(row.get("cpu_percent", 0.0)),
                memory_percent=float(row.get("memory_percent", 0.0)),
                disk_percent=float(row.get("disk_percent", 0.0)),
            )
        )
    return records


def _parse_csv(path: str) -> list[HealthRecord]:
    records = []
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            cpu_temp = row.get("cpu_temp")
            records.append(
                HealthRecord(
                    timestamp=row.get("timestamp", ""),
                    cpu_temp=float(cpu_temp) if cpu_temp not in (None, "") else None,
                    cpu_percent=float(row.get("cpu_percent", 0.0)),
                    memory_percent=float(row.get("memory_percent", 0.0)),
                    disk_percent=float(row.get("disk_percent", 0.0)),
                )
            )
    return records


async def _save_records(records: Iterable[HealthRecord]) -> None:
    for rec in records:
        await save_health_record(rec)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Import HealthRecord data")
    parser.add_argument("input", help="Input file path")
    parser.add_argument(
        "--format",
        "-f",
        choices=IMPORT_FORMATS,
        help="Input format (guessed from extension if omitted)",
    )
    args = parser.parse_args(argv)

    fmt = args.format
    if fmt is None:
        ext = args.input.rsplit(".", 1)[-1].lower()
        fmt = ext if ext in IMPORT_FORMATS else "json"

    if fmt == "csv":
        records = _parse_csv(args.input)
    else:
        records = _parse_json(args.input)

    asyncio.run(_save_records(records))


if __name__ == "__main__":
    main()
