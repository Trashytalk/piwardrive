"""Module exporter."""
import csv
import json
from dataclasses import asdict, is_dataclass
from typing import Any, Iterable, Mapping


def export_json(records: Iterable[Any], path: str) -> None:
    """Export ``records`` to ``path`` in JSON format."""

    def normalise(record: Any) -> Any:
        if hasattr(record, "model_dump"):
            return record.model_dump()
        if is_dataclass(record):
            return asdict(record)
        if isinstance(record, Mapping):
            return dict(record)
        return record

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("[\n")
        first = True
        for rec in records:
            if not first:
                fh.write(",\n")
            json.dump(normalise(rec), fh, indent=2)
            first = False
        if not first:
            fh.write("\n")
        fh.write("]")


def export_csv(records: Iterable[Mapping[str, str]], path: str) -> None:
    """Export ``records`` to ``path`` in CSV format."""
    it = iter(records)
    try:
        first = next(it)
    except StopIteration:
        open(path, "w", newline="", encoding="utf-8").close()
        return

    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(first.keys()))
        writer.writeheader()
        writer.writerow(first)
        for rec in it:
            writer.writerow(rec)


def export_yaml(records: Iterable[Any], path: str) -> None:
    """Export ``records`` to ``path`` in YAML format."""
    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover - optional dep
        raise RuntimeError("PyYAML required for YAML export") from exc

    data = []
    for rec in records:
        if hasattr(rec, "model_dump"):
            data.append(rec.model_dump())
        elif isinstance(rec, Mapping):
            data.append(dict(rec))
        else:
            data.append(rec)
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh, sort_keys=False)
