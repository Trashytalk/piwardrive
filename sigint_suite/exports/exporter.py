import json
from typing import Iterable, Mapping, Any


def export_json(records: Iterable[Any], path: str) -> None:
    """Export ``records`` to ``path`` in JSON format."""
    data = []
    for rec in records:
        if hasattr(rec, "model_dump"):
            data.append(rec.model_dump())
        elif isinstance(rec, Mapping):
            data.append(dict(rec))
        else:
            data.append(rec)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
