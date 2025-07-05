from __future__ import annotations

from abc import ABC, abstractmethod


class BaseMigration(ABC):
    """Abstract base class for database migrations."""

    version: int

    @abstractmethod
    async def apply(self, conn) -> None:
        """Apply the migration using ``conn``."""

    @abstractmethod
    async def rollback(self, conn) -> None:
        """Rollback the migration using ``conn``."""

    def get_version(self) -> int:
        """Return the migration version."""
        return self.version
