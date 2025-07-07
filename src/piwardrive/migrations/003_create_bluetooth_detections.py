"""Migration 003: Create bluetooth detections table."""

from __future__ import annotations

from .base import BaseMigration


class Migration(BaseMigration):
    """Create bluetooth_detections table."""

    version = 3

    async def apply(self, conn) -> None:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS bluetooth_detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_session_id TEXT NOT NULL,
                detection_timestamp TIMESTAMP NOT NULL,
                mac_address TEXT NOT NULL,
                device_name TEXT,
                device_class INTEGER,
                device_type TEXT,
                manufacturer_id INTEGER,
                manufacturer_name TEXT,
                rssi_dbm INTEGER,
                tx_power_dbm INTEGER,
                bluetooth_version TEXT,
                supported_services TEXT,
                is_connectable BOOLEAN DEFAULT FALSE,
                is_paired BOOLEAN DEFAULT FALSE,
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
            "CREATE INDEX IF NOT EXISTS idx_bt_detections_session ON bluetooth_detections(scan_session_id)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_bt_detections_mac ON bluetooth_detections(mac_address)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_bt_detections_time ON bluetooth_detections(detection_timestamp)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_bt_detections_location ON bluetooth_detections(latitude, longitude)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_bt_detections_rssi ON bluetooth_detections(rssi_dbm)"
        )

    async def rollback(self, conn) -> None:
        await conn.execute("DROP INDEX IF EXISTS idx_bt_detections_rssi")
        await conn.execute("DROP INDEX IF EXISTS idx_bt_detections_location")
        await conn.execute("DROP INDEX IF EXISTS idx_bt_detections_time")
        await conn.execute("DROP INDEX IF EXISTS idx_bt_detections_mac")
        await conn.execute("DROP INDEX IF EXISTS idx_bt_detections_session")
        await conn.execute("DROP TABLE IF EXISTS bluetooth_detections")
