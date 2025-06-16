import json
import os
from typing import Any, List, Mapping



def _export_dir() -> str:
    """Return the directory containing SIGINT export files."""
  
    return os.getenv(
        "SIGINT_EXPORT_DIR",
        os.path.join(os.path.dirname(__file__), "sigint_suite", "exports"),
    )


def load_sigint_data(name: str) -> List[Mapping[str, Any]]:
    """Return records from ``name`` JSON file in the SIGINT export directory."""
    path = os.path.join(_export_dir(), f"{name}.json")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            if isinstance(data, list):
                return [dict(r) for r in data if isinstance(r, Mapping)]
    except Exception:
        pass
    return []

