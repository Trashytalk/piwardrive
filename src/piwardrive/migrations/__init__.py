"""Database migration framework."""

from .base import BaseMigration

# List of migration instances in version order
MIGRATIONS: list[BaseMigration] = []

__all__ = ["BaseMigration", "MIGRATIONS"]
