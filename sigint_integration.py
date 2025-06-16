import json
import os
from typing import Any, List, Mapping


_DEFAULT_EXPORT_DIR = os.path.join(os.path.dirname(__file__), "sigint_suite", "exports")


def load_sigint_data(name: str) -> List[Mapping[str, Any]]:
    """Return records from ``name`` JSON file in the SIGINT export directory."""
    export_dir = os.getenv("SIGINT_EXPORT_DIR", _DEFAULT_EXPORT_DIR)
    path = os.path.join(export_dir, f"{name}.json")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            if isinstance(data, list):
                return [dict(r) for r in data if isinstance(r, Mapping)]
    except Exception:
        pass
    return []

