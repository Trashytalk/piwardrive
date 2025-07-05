from __future__ import annotations

from .base import BaseMigration


class Migration(BaseMigration):
    """Create scan_sessions table."""

    version = 1

    async def apply(self, conn) -> None:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scan_sessions (
                id TEXT PRIMARY KEY,
                device_id TEXT NOT NULL,
                scan_type TEXT NOT NULL,
                started_at TIMESTAMP NOT NULL,
                completed_at TIMESTAMP,
                duration_seconds INTEGER,
                location_start_lat REAL,
                location_start_lon REAL,
                location_end_lat REAL,
                location_end_lon REAL,
                interface_used TEXT,
                scan_parameters TEXT,
                total_detections INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_scan_sessions_device_time ON scan_sessions(device_id,
                started_at)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_scan_sessions_type ON scan_sessions(scan_type)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_scan_sessions_location ON scan_sessions(location_start_lat,
                location_start_lon)"
        )

    async def rollback(self, conn) -> None:
        await conn.execute("DROP INDEX IF EXISTS idx_scan_sessions_device_time")
        await conn.execute("DROP INDEX IF EXISTS idx_scan_sessions_type")
        await conn.execute("DROP INDEX IF EXISTS idx_scan_sessions_location")
        await conn.execute("DROP TABLE IF EXISTS scan_sessions")
