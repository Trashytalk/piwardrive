"""Database migration framework."""

from importlib import import_module

from .base import BaseMigration

Migration001 = import_module(f"{__name__}.001_create_scan_sessions").Migration
Migration002 = import_module(f"{__name__}.002_enhance_wifi_detections").Migration
Migration003 = import_module(f"{__name__}.003_create_bluetooth_detections").Migration

# List of migration instances in version order
MIGRATIONS: list[BaseMigration] = [Migration001(), Migration002(), Migration003()]

__all__ = ["BaseMigration", "MIGRATIONS"]
