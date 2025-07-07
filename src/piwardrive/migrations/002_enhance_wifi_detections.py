from __future__ import annotations

from datetime import datetime

from .base import BaseMigration


class Migration(BaseMigration):
    """Create wifi_detections table with enhanced schema and migrate old data."""

    version = 2

    async def apply(self, conn) -> None:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS wifi_detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_session_id TEXT NOT NULL,
                detection_timestamp TIMESTAMP NOT NULL,
                bssid TEXT NOT NULL,
                ssid TEXT,
                channel INTEGER,
                frequency_mhz INTEGER,
                signal_strength_dbm INTEGER,
                noise_floor_dbm INTEGER,
                snr_db INTEGER,
                encryption_type TEXT,
                cipher_suite TEXT,
                authentication_method TEXT,
                wps_enabled BOOLEAN DEFAULT FALSE,
                vendor_oui TEXT,
                vendor_name TEXT,
                device_type TEXT,
                latitude REAL,
                longitude REAL,
                altitude_meters REAL,
                accuracy_meters REAL,
                heading_degrees REAL,
                speed_kmh REAL,
                beacon_interval_ms INTEGER,
                dtim_period INTEGER,
                ht_capabilities TEXT,
                vht_capabilities TEXT,
                he_capabilities TEXT,
                country_code TEXT,
                regulatory_domain TEXT,
                tx_power_dbm INTEGER,
                load_percentage INTEGER,
                station_count INTEGER,
                data_rates TEXT,
                first_seen TIMESTAMP NOT NULL,
                last_seen TIMESTAMP NOT NULL,
                detection_count INTEGER DEFAULT 1,
                FOREIGN KEY (scan_session_id) REFERENCES scan_sessions(id)
            )
            """
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_detections_session ON ",
            "wifi_detections(scan_session_id)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_detections_bssid ON ",
            "wifi_detections(bssid)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_detections_ssid ON ",
            "wifi_detections(ssid)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_detections_time ON ",
            "wifi_detections(detection_timestamp)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_detections_location ON ",
            "wifi_detections(latitude, longitude)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_detections_signal ON ",
            "wifi_detections(signal_strength_dbm)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_detections_channel ON ",
            "wifi_detections(channel)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_detections_encryption ON ",
            "wifi_detections(encryption_type)"
        )
        await conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_detections_vendor ON ",
            "wifi_detections(vendor_name)"
        )

        # Migrate existing data from ap_cache if present
        cur = await conn.execute(
            "SELECT bssid, ssid, encryption, lat, lon, last_time FROM ap_cache"
        )
        rows = await cur.fetchall()
        if rows:
            now = datetime.utcnow().isoformat()
            records = []
            for bssid, ssid, enc, lat, lon, ts in rows:
                if ts is not None:
                    try:
                        dt = datetime.fromtimestamp(float(ts)).isoformat()
                    except Exception:
                        dt = now
                else:
                    dt = now
                records.append(
                    {
                        "scan_session_id": "legacy",
                        "detection_timestamp": dt,
                        "bssid": bssid,
                        "ssid": ssid,
                        "channel": None,
                        "frequency_mhz": None,
                        "signal_strength_dbm": None,
                        "noise_floor_dbm": None,
                        "snr_db": None,
                        "encryption_type": enc,
                        "cipher_suite": None,
                        "authentication_method": None,
                        "wps_enabled": False,
                        "vendor_oui": bssid[:8].upper() if bssid else None,
                        "vendor_name": None,
                        "device_type": None,
                        "latitude": lat,
                        "longitude": lon,
                        "altitude_meters": None,
                        "accuracy_meters": None,
                        "heading_degrees": None,
                        "speed_kmh": None,
                        "beacon_interval_ms": None,
                        "dtim_period": None,
                        "ht_capabilities": None,
                        "vht_capabilities": None,
                        "he_capabilities": None,
                        "country_code": None,
                        "regulatory_domain": None,
                        "tx_power_dbm": None,
                        "load_percentage": None,
                        "station_count": None,
                        "data_rates": None,
                        "first_seen": dt,
                        "last_seen": dt,
                        "detection_count": 1,
                    }
                )
            await conn.executemany(
                """
                INSERT INTO wifi_detections (
                    scan_session_id, detection_timestamp, bssid, ssid,
                    channel, frequency_mhz, signal_strength_dbm, noise_floor_dbm,
                    snr_db, encryption_type, cipher_suite, authentication_method,
                    wps_enabled, vendor_oui, vendor_name, device_type,
                    latitude, longitude, altitude_meters, accuracy_meters,
                    heading_degrees, speed_kmh, beacon_interval_ms, dtim_period,
                    ht_capabilities, vht_capabilities, he_capabilities,
                    country_code, regulatory_domain, tx_power_dbm,
                    load_percentage, station_count, data_rates,
                    first_seen, last_seen, detection_count
                ) VALUES (
                    :scan_session_id, :detection_timestamp, :bssid, :ssid,
                    :channel, :frequency_mhz, :signal_strength_dbm, :noise_floor_dbm,
                    :snr_db, :encryption_type, :cipher_suite, :authentication_method,
                    :wps_enabled, :vendor_oui, :vendor_name, :device_type,
                    :latitude, :longitude, :altitude_meters, :accuracy_meters,
                    :heading_degrees, :speed_kmh, :beacon_interval_ms, :dtim_period,
                    :ht_capabilities, :vht_capabilities, :he_capabilities,
                    :country_code, :regulatory_domain, :tx_power_dbm,
                    :load_percentage, :station_count, :data_rates,
                    :first_seen, :last_seen, :detection_count
                )
                """,
                records,
            )
        await conn.commit()

    async def rollback(self, conn) -> None:
        await conn.execute("DROP INDEX IF EXISTS idx_wifi_detections_vendor")
        await conn.execute("DROP INDEX IF EXISTS idx_wifi_detections_encryption")
        await conn.execute("DROP INDEX IF EXISTS idx_wifi_detections_channel")
        await conn.execute("DROP INDEX IF EXISTS idx_wifi_detections_signal")
        await conn.execute("DROP INDEX IF EXISTS idx_wifi_detections_location")
        await conn.execute("DROP INDEX IF EXISTS idx_wifi_detections_time")
        await conn.execute("DROP INDEX IF EXISTS idx_wifi_detections_ssid")
        await conn.execute("DROP INDEX IF EXISTS idx_wifi_detections_bssid")
        await conn.execute("DROP INDEX IF EXISTS idx_wifi_detections_session")
        await conn.execute("DROP TABLE IF EXISTS wifi_detections")
        await conn.commit()
