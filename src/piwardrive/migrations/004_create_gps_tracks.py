from __future__ import annotations

from .base import BaseMigration


class Migration(BaseMigration):
    """Create gps_tracks table."""

    version = 4

    async def apply(self, conn) -> None:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS gps_tracks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_session_id TEXT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                altitude_meters REAL,
                accuracy_meters REAL,
                heading_degrees REAL,
                speed_kmh REAL,
                satellite_count INTEGER,
                hdop REAL,
                vdop REAL,
                pdop REAL,
                fix_type TEXT,
                FOREIGN KEY (scan_session_id) REFERENCES scan_sessions(id)
            )
            """
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_gps_tracks_session ON gps_tracks(scan_session_id)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_gps_tracks_time ON gps_tracks(timestamp)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_gps_tracks_location ON gps_tracks(latitude,
                longitude)"
        )

    async def rollback(self, conn) -> None:
        await conn.execute("DROP INDEX IF EXISTS idx_gps_tracks_location")
        await conn.execute("DROP INDEX IF EXISTS idx_gps_tracks_time")
        await conn.execute("DROP INDEX IF EXISTS idx_gps_tracks_session")
        await conn.execute("DROP TABLE IF EXISTS gps_tracks")
        await conn.commit()
