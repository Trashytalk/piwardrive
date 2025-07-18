from __future__ import annotations

from .base import BaseMigration


class Migration(BaseMigration):
    """Create network_analytics table."""

    version = 8

    async def apply(self, conn) -> None:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS network_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bssid TEXT NOT NULL,
                analysis_date DATE NOT NULL,
                total_detections INTEGER,
                unique_locations INTEGER,
                avg_signal_strength REAL,
                max_signal_strength REAL,
                min_signal_strength REAL,
                signal_variance REAL,
                coverage_radius_meters REAL,
                mobility_score REAL,
                encryption_changes INTEGER,
                ssid_changes INTEGER,
                channel_changes INTEGER,
                suspicious_score REAL,
                last_analyzed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(bssid, analysis_date)
            )
            """
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_analytics_bssid ON network_analytics(bssid)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_analytics_date ON network_analytics(analysis_date)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_analytics_suspicious ON network_analytics(suspicious_score)"
        )

    async def rollback(self, conn) -> None:
        await conn.execute("DROP INDEX IF EXISTS idx_analytics_suspicious")
        await conn.execute("DROP INDEX IF EXISTS idx_analytics_date")
        await conn.execute("DROP INDEX IF EXISTS idx_analytics_bssid")
        await conn.execute("DROP TABLE IF EXISTS network_analytics")
        await conn.commit()
