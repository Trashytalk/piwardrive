import csv
import json
from typing import Iterable, Mapping


def export_json(records: Iterable[Mapping[str, str]], path: str) -> None:
    """Export ``records`` to ``path`` in JSON format."""
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(list(records), fh, indent=2)


def export_csv(records: Iterable[Mapping[str, str]], path: str) -> None:
    """Export ``records`` to ``path`` in CSV format."""
    rows = list(records)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        if rows:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
