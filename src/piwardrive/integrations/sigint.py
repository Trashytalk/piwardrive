"""Module sigint_integration."""
import json
import os
from typing import Any, List, Mapping

from piwardrive.sigint_suite import paths


def load_sigint_data(name: str) -> List[Mapping[str, Any]]:
    """
    Load and return a list of mapping records from a JSON file in the SIGINT export directory.
    
    The function constructs the file path using the provided name and attempts to read and parse the corresponding JSON file. Only elements that are mappings (dictionaries) are included in the returned list. If the file cannot be read, parsed, or does not contain a list of mappings, an empty list is returned.
    
    Parameters:
        name (str): The base name of the JSON file (without extension) to load.
    
    Returns:
        List[Mapping[str, Any]]: A list of mapping records from the JSON file, or an empty list if loading fails.
    """
    export_dir = os.getenv("SIGINT_EXPORT_DIR", paths.EXPORT_DIR)
    path = os.path.join(export_dir, f"{name}.json")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            if isinstance(data, list):
                return [dict(r) for r in data if isinstance(r, Mapping)]
    except Exception:
        pass
    return []
