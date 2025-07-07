"""Database service wrapper for PiWardrive.

This module provides a high-level database service that wraps the persistence
layer with pluggable database backends including SQLite, MySQL, and PostgreSQL.
"""

from __future__ import annotations

from typing import Any, List

from . import persistence
from .db import (
    DatabaseAdapter,
    DatabaseManager,
    MySQLAdapter,
    PostgresAdapter,
    SQLiteAdapter,
)
from .persistence import DashboardSettings, FingerprintInfo, HealthRecord, User


class DatabaseService:
    """Wrapper around persistence with pluggable database backends."""

    def __init__(self, adapter: DatabaseAdapter | None = None) -> None:
        """Initialize database service.
        
        Args:
            adapter: Database adapter to use (defaults to SQLite).
        """
        if adapter is None:
            adapter = SQLiteAdapter(persistence._db_path())
        self.manager = DatabaseManager(adapter)

    async def connect(self) -> None:
        """Connect to the database."""
        await self.manager.connect()

    async def close(self) -> None:
        """Close database connection."""
        await self.manager.close()

    async def load_recent_health(self, limit: int = 10) -> List[HealthRecord]:
        """Load recent health records.
        
        Args:
            limit: Maximum number of records to return.
            
        Returns:
            List of health records.
        """
        return await persistence.load_recent_health(limit)

    async def load_health_history(
        self, start: str | None = None, end: str | None = None
    ) -> List[HealthRecord]:
        """Load health history within a date range.
        
        Args:
            start: Start date (optional).
            end: End date (optional).
            
        Returns:
            List of health records.
        """
        return await persistence.load_health_history(start, end)

    async def save_health_record(self, record: HealthRecord) -> None:
        """Save a health record.
        
        Args:
            record: Health record to save.
        """
        await persistence.save_health_record(record)

    async def purge_old_health(self, days: int) -> None:
        """Purge health records older than specified days.
        
        Args:
            days: Number of days to retain.
        """
        await persistence.purge_old_health(days)

    async def vacuum(self) -> None:
        """Vacuum the database to reclaim space."""
        await persistence.vacuum()

    async def load_ap_cache(self, after: float | None = None) -> List[dict[str, Any]]:
        """Load access point cache.
        
        Args:
            after: Timestamp to load cache after (optional).
            
        Returns:
            List of cached access points.
        """
        return await persistence.load_ap_cache(after)

    async def save_dashboard_settings(self, settings: DashboardSettings) -> None:
        """Save dashboard settings.
        
        Args:
            settings: Dashboard settings to save.
        """
        await persistence.save_dashboard_settings(settings)

    async def load_dashboard_settings(self) -> DashboardSettings:
        """Load dashboard settings.
        
        Returns:
            Dashboard settings.
        """
        return await persistence.load_dashboard_settings()

    async def save_fingerprint_info(self, info: FingerprintInfo) -> None:
        """Save fingerprint information.
        
        Args:
            info: Fingerprint info to save.
        """
        await persistence.save_fingerprint_info(info)

    async def load_fingerprint_info(self) -> List[FingerprintInfo]:
        """Load fingerprint information.
        
        Returns:
            List of fingerprint info.
        """
        return await persistence.load_fingerprint_info()

    async def save_gps_tracks(self, records: List[dict[str, Any]]) -> None:
        """Save GPS track records.
        
        Args:
            records: GPS track records to save.
        """
        await persistence.save_gps_tracks(records)

    async def save_suspicious_activities(self, records: List[dict[str, Any]]) -> None:
        """Save suspicious activity records.
        
        Args:
            records: Suspicious activity records to save.
        """
        await persistence.save_suspicious_activities(records)

    async def count_suspicious_activities(self, since: str | None = None) -> int:
        """Count suspicious activities since a date.
        
        Args:
            since: Date to count from (optional).
            
        Returns:
            Number of suspicious activities.
        """
        return await persistence.count_suspicious_activities(since)

    async def load_recent_suspicious(self, limit: int = 10) -> List[dict[str, Any]]:
        """Load recent suspicious activities.
        
        Args:
            limit: Maximum number of records to return.
            
        Returns:
            List of suspicious activities.
        """
        return await persistence.load_recent_suspicious(limit)

    async def get_table_counts(self) -> dict[str, int]:
        """Get counts for all tables.
        
        Returns:
            Dictionary of table names to counts.
        """
        return await persistence.get_table_counts()

    def db_path(self) -> str:
        """Get database file path.
        
        Returns:
            Path to database file.
        """
        return persistence._db_path()

    async def get_user(self, username: str) -> User | None:
        """Get user by username.
        
        Args:
            username: Username to lookup.
            
        Returns:
            User object or None if not found.
        """
        return await persistence.get_user(username)

    async def save_user(self, user: User) -> None:
        """Save user to database.
        
        Args:
            user: User object to save.
        """
        await persistence.save_user(user)

    async def update_user_token(self, username: str, token_hash: str) -> None:
        """Update user's token hash.
        
        Args:
            username: Username to update.
            token_hash: New token hash.
        """
        await persistence.update_user_token(username, token_hash)

    async def get_user_by_token(self, token_hash: str) -> User | None:
        """Get user by token hash.
        
        Args:
            token_hash: Token hash to lookup.
            
        Returns:
            User object or None if not found.
        """
        return await persistence.get_user_by_token(token_hash)

    async def fetch(self, query: str, *args: Any) -> list[dict]:
        """Run an arbitrary SELECT query using the configured adapter."""
        return await self.manager.fetchall(query, *args)


db_service = DatabaseService()
