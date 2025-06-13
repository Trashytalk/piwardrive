import json
import os
from typing import Any, Dict

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "piwardrive")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG: Dict[str, Any] = {
    "theme": "Dark",
    "map_poll_gps": 10,
    "map_poll_aps": 60,
    "map_show_gps": True,
    "map_show_aps": True,
    "map_cluster_aps": False,
}


def load_config() -> Dict[str, Any]:
    """Load configuration from ``CONFIG_PATH``.

    Returns defaults merged with values from the JSON file. Invalid or missing
    files return only the defaults.
    """
    data: Dict[str, Any] = {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        pass
    merged = {**DEFAULT_CONFIG, **data}
    return merged


def save_config(config: Dict[str, Any]) -> None:
    """Persist ``config`` dictionary to ``CONFIG_PATH``."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
