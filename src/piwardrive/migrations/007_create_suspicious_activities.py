from __future__ import annotations

from .base import BaseMigration


class Migration(BaseMigration):
    """Create suspicious_activities table."""

    version = 7

    async def apply(self, conn) -> None:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS suspicious_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_session_id TEXT NOT NULL,
                activity_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                target_bssid TEXT,
                target_ssid TEXT,
                evidence TEXT,
                description TEXT,
                detected_at TIMESTAMP NOT NULL,
                latitude REAL,
                longitude REAL,
                false_positive BOOLEAN DEFAULT FALSE,
                analyst_notes TEXT,
                FOREIGN KEY (scan_session_id) REFERENCES scan_sessions(id)
            )
            """
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_suspicious_session ON suspicious_activities(scan_session_id)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_suspicious_type ON suspicious_activities(activity_type)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_suspicious_severity ON suspicious_activities(severity)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_suspicious_time ON suspicious_activities(detected_at)"
        )

    async def rollback(self, conn) -> None:
        await conn.execute("DROP INDEX IF EXISTS idx_suspicious_time")
        await conn.execute("DROP INDEX IF EXISTS idx_suspicious_severity")
        await conn.execute("DROP INDEX IF EXISTS idx_suspicious_type")
        await conn.execute("DROP INDEX IF EXISTS idx_suspicious_session")
        await conn.execute("DROP TABLE IF EXISTS suspicious_activities")
        await conn.commit()
