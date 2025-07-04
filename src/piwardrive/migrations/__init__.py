"""Database migration framework."""

from importlib import import_module

from .base import BaseMigration

Migration001 = import_module(f"{__name__}.001_create_scan_sessions").Migration
Migration002 = import_module(f"{__name__}.002_enhance_wifi_detections").Migration
Migration003 = import_module(f"{__name__}.003_create_bluetooth_detections").Migration
Migration004 = import_module(f"{__name__}.004_create_gps_tracks").Migration
Migration005 = import_module(f"{__name__}.005_create_cellular_detections").Migration
Migration006 = import_module(f"{__name__}.006_create_network_fingerprints").Migration
Migration007 = import_module(f"{__name__}.007_create_suspicious_activities").Migration

# List of migration instances in version order
MIGRATIONS: list[BaseMigration] = [
    Migration001(),
    Migration002(),
    Migration003(),
    Migration004(),
    Migration005(),
    Migration006(),
    Migration007(),
]

__all__ = ["BaseMigration", "MIGRATIONS"]
