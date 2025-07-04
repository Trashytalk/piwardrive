"""Database migration framework."""

from .base import BaseMigration
from .001_create_scan_sessions import Migration as Migration001

# List of migration instances in version order
MIGRATIONS: list[BaseMigration] = [Migration001()]

__all__ = ["BaseMigration", "MIGRATIONS"]
