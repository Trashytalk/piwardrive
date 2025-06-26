"""Interactive setup wizard for external services."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CONFIG_PATH = Path.home() / ".config" / "piwardrive" / "setup.json"


def run_wizard() -> None:
    """Prompt for service configuration options and save them."""
    config: dict[str, Any] = {}
    config["kismet_host"] = input("Kismet host [localhost]: ") or "localhost"
    config["kismet_port"] = int(input("Kismet port [2501]: ") or "2501")
    config["bettercap_iface"] = input("BetterCAP interface [wlan0]: ") or "wlan0"
    config["gpsd_port"] = int(input("GPSD port [2947]: ") or "2947")
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2))
    print(f"Configuration saved to {CONFIG_PATH}")
