import argparse
import csv
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from piwardrive import export


def _load_json(path: str) -> list[Mapping[str, Any]]:
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, Mapping):
        return [data]
    if isinstance(data, Iterable):
        return [r for r in data if isinstance(r, Mapping)]
    return []


def _load_csv(path: str) -> list[Mapping[str, Any]]:
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader)


def main(argv: list[str] | None = None) -> None:
    """Convert JSON or CSV records to GPX format."""
    parser = argparse.ArgumentParser(description="Export records to GPX")
    parser.add_argument("input", help="input file (CSV or JSON)")
    parser.add_argument("output", help="destination GPX file")
    parser.add_argument(
        "--format",
        "-f",
        choices=["csv", "json"],
        help="input format (guessed from extension)",
    )
    args = parser.parse_args(argv)

    fmt = args.format
    if fmt is None:
        ext = Path(args.input).suffix.lower().lstrip(".")
        fmt = ext if ext in {"csv", "json"} else "json"

    if fmt == "csv":
        records = _load_csv(args.input)
    else:
        records = _load_json(args.input)

    export.export_gpx(records, args.output, None)


if __name__ == "__main__":  # pragma: no cover - manual invocation
    main()
