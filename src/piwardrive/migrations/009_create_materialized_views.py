from __future__ import annotations

from .base import BaseMigration


class Migration(BaseMigration):
    """Create materialized view tables for analytics."""

    version = 9

    async def apply(self, conn) -> None:
        await conn.execute("DROP TABLE IF EXISTS daily_detection_stats")
        await conn.execute(
            """
            CREATE TABLE daily_detection_stats AS
            SELECT
                DATE(detection_timestamp) AS detection_date,
                scan_session_id,
                COUNT(*) AS total_detections,
                COUNT(DISTINCT bssid) AS unique_networks,
                AVG(signal_strength_dbm) AS avg_signal,
                MIN(signal_strength_dbm) AS min_signal,
                MAX(signal_strength_dbm) AS max_signal,
                COUNT(DISTINCT channel) AS channels_used,
                COUNT(
                    CASE WHEN encryption_type = 'OPEN' THEN 1 END
                ) AS open_networks,
                COUNT(
                    CASE WHEN encryption_type LIKE '%WEP%' THEN 1 END
                ) AS wep_networks,
                COUNT(
                    CASE WHEN encryption_type LIKE '%WPA%' THEN 1 END
                ) AS wpa_networks
            FROM wifi_detections
            GROUP BY DATE(detection_timestamp), scan_session_id
            """
        )
        await conn.execute("DROP TABLE IF EXISTS network_coverage_grid")
        await conn.execute(
            """
            CREATE TABLE network_coverage_grid AS
            SELECT
                ROUND(latitude, 4) AS lat_grid,
                ROUND(longitude, 4) AS lon_grid,
                COUNT(*) AS detection_count,
                COUNT(DISTINCT bssid) AS unique_networks,
                AVG(signal_strength_dbm) AS avg_signal,
                MAX(signal_strength_dbm) AS max_signal
            FROM wifi_detections
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            GROUP BY ROUND(latitude, 4), ROUND(longitude, 4)
            """
        )
        await conn.commit()

    async def rollback(self, conn) -> None:
        await conn.execute("DROP TABLE IF EXISTS network_coverage_grid")
        await conn.execute("DROP TABLE IF EXISTS daily_detection_stats")
        await conn.commit()
