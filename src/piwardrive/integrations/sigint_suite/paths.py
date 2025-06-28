"""Module paths."""

import os

"""Common path constants for sigint_suite modules."""

SUITE_ROOT = os.path.abspath(os.path.dirname(__file__))

DEFAULT_EXPORT_DIR = os.path.join(SUITE_ROOT, "exports")

CONFIG_DIR = os.environ.get(
    "SIGINT_CONFIG_DIR",
    os.path.join(os.path.expanduser("~"), ".config", "piwardrive"),
)

EXPORT_DIR = os.environ.get("EXPORT_DIR", DEFAULT_EXPORT_DIR)

OUI_PATH = os.environ.get("SIGINT_OUI_PATH", os.path.join(CONFIG_DIR, "oui.csv"))

TOWER_DB_PATH = os.environ.get("SIGINT_TOWER_DB", os.path.join(CONFIG_DIR, "towers.db"))

__all__ = [
    "SUITE_ROOT",
    "DEFAULT_EXPORT_DIR",
    "EXPORT_DIR",
    "CONFIG_DIR",
    "OUI_PATH",
    "TOWER_DB_PATH",
]
