"""Interactive setup wizard for external services."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import questionary

CONFIG_PATH = Path.home() / ".config" / "piwardrive" / "setup.json"


def run_wizard() -> None:
    """Prompt for service configuration options and save them."""
    config: dict[str, Any] = {}
    try:
        config["kismet_host"] = questionary.text(
            "Kismet host", default="localhost"
        ).ask()
        config["kismet_port"] = int(
            questionary.text("Kismet port", default="2501").ask()
        )
        config["bettercap_iface"] = questionary.text(
            "BetterCAP interface", default="wlan0"
        ).ask()
        config["gpsd_port"] = int(questionary.text("GPSD port", default="2947").ask())
    except Exception as exc:
        logging.error("Invalid input: %s", exc)
        return
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        CONFIG_PATH.write_text(json.dumps(config, indent=2))
    except OSError as exc:
        logging.error("Failed to write config: %s", exc)
        return
    print(f"Configuration saved to {CONFIG_PATH}")
