from __future__ import annotations

from typing import Any, List

from . import persistence
from .persistence import DashboardSettings, FingerprintInfo, HealthRecord, User


class DatabaseService:
    """Wrapper around :mod:`piwardrive.persistence` functions."""

    async def load_recent_health(self, limit: int = 10) -> List[HealthRecord]:
        return await persistence.load_recent_health(limit)

    async def load_health_history(
        self, start: str | None = None, end: str | None = None
    ) -> List[HealthRecord]:
        return await persistence.load_health_history(start, end)

    async def save_health_record(self, record: HealthRecord) -> None:
        await persistence.save_health_record(record)

    async def purge_old_health(self, days: int) -> None:
        await persistence.purge_old_health(days)

    async def vacuum(self) -> None:
        await persistence.vacuum()

    async def load_ap_cache(self, after: float | None = None) -> List[dict[str, Any]]:
        return await persistence.load_ap_cache(after)

    async def save_dashboard_settings(self, settings: DashboardSettings) -> None:
        await persistence.save_dashboard_settings(settings)

    async def load_dashboard_settings(self) -> DashboardSettings:
        return await persistence.load_dashboard_settings()

    async def save_fingerprint_info(self, info: FingerprintInfo) -> None:
        await persistence.save_fingerprint_info(info)

    async def load_fingerprint_info(self) -> List[FingerprintInfo]:
        return await persistence.load_fingerprint_info()

    async def get_table_counts(self) -> dict[str, int]:
        return await persistence.get_table_counts()

    def db_path(self) -> str:
        return persistence._db_path()

    async def get_user(self, username: str) -> User | None:
        return await persistence.get_user(username)

    async def save_user(self, user: User) -> None:
        await persistence.save_user(user)

    async def update_user_token(self, username: str, token_hash: str) -> None:
        await persistence.update_user_token(username, token_hash)

    async def get_user_by_token(self, token_hash: str) -> User | None:
        return await persistence.get_user_by_token(token_hash)


db_service = DatabaseService()
