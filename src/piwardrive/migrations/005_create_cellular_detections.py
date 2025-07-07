"""Migration 005: Create cellular detections table."""

from __future__ import annotations

from .base import BaseMigration


class Migration(BaseMigration):
    """Create cellular_detections table."""

    version = 5

    async def apply(self, conn) -> None:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cellular_detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_session_id TEXT NOT NULL,
                detection_timestamp TIMESTAMP NOT NULL,
                cell_id INTEGER,
                lac INTEGER,
                mcc INTEGER,
                mnc INTEGER,
                network_name TEXT,
                technology TEXT,
                frequency_mhz INTEGER,
                band TEXT,
                channel INTEGER,
                signal_strength_dbm INTEGER,
                signal_quality INTEGER,
                timing_advance INTEGER,
                latitude REAL,
                longitude REAL,
                altitude_meters REAL,
                accuracy_meters REAL,
                heading_degrees REAL,
                speed_kmh REAL,
                first_seen TIMESTAMP NOT NULL,
                last_seen TIMESTAMP NOT NULL,
                detection_count INTEGER DEFAULT 1,
                FOREIGN KEY (scan_session_id) REFERENCES scan_sessions(id)
            )
            """
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_cellular_detections_session ",
            "ON cellular_detections(scan_session_id)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_cellular_detections_cell ",
            "ON cellular_detections(cell_id, lac)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_cellular_detections_time ",
            "ON cellular_detections(detection_timestamp)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_cellular_detections_location ",
            "ON cellular_detections(latitude, longitude)"
        )

    async def rollback(self, conn) -> None:
        await conn.execute("DROP INDEX IF EXISTS idx_cellular_detections_location")
        await conn.execute("DROP INDEX IF EXISTS idx_cellular_detections_time")
        await conn.execute("DROP INDEX IF EXISTS idx_cellular_detections_cell")
        await conn.execute("DROP INDEX IF EXISTS idx_cellular_detections_session")
        await conn.execute("DROP TABLE IF EXISTS cellular_detections")
        await conn.commit()
