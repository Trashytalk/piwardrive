from __future__ import annotations

from .base import BaseMigration


class Migration(BaseMigration):
    """Add performance indexes for analysis queries."""

    version = 10

    async def apply(self, conn) -> None:
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_time_location ON wifi_detections(detection_timestamp,
                latitude,
                longitude)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_signal_channel ON wifi_detections(signal_strength_dbm,
                channel)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_vendor_encryption ON wifi_detections(vendor_name,
                encryption_type)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_ssid_bssid ON wifi_detections(ssid,
                bssid)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_ssid_fts ON wifi_detections(ssid)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_bt_name_fts ON bluetooth_detections(device_name)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_location_spatial ON wifi_detections(longitude,
                latitude)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_gps_location_spatial ON gps_tracks(longitude,
                latitude)"
        )

    async def rollback(self, conn) -> None:
        await conn.execute("DROP INDEX IF EXISTS idx_gps_location_spatial")
        await conn.execute("DROP INDEX IF EXISTS idx_wifi_location_spatial")
        await conn.execute("DROP INDEX IF EXISTS idx_bt_name_fts")
        await conn.execute("DROP INDEX IF EXISTS idx_wifi_ssid_fts")
        await conn.execute("DROP INDEX IF EXISTS idx_wifi_ssid_bssid")
        await conn.execute("DROP INDEX IF EXISTS idx_wifi_vendor_encryption")
        await conn.execute("DROP INDEX IF EXISTS idx_wifi_signal_channel")
        await conn.execute("DROP INDEX IF EXISTS idx_wifi_time_location")
        await conn.commit()
