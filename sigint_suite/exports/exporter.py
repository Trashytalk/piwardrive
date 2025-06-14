import json
from typing import Iterable, Mapping

def export_json(records: Iterable[Mapping[str, str]], path: str) -> None:
    """Export ``records`` to ``path`` in JSON format."""
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(list(records), fh, indent=2)
