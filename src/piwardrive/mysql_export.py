from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable, List, Sequence

import aiomysql

from .persistence import HealthRecord


@dataclass
class MySQLConfig:
    """Connection information for a MySQL or MariaDB server."""

    host: str = "localhost"
    port: int = 3306
    user: str = "piwardrive"
    password: str = ""
    database: str = "piwardrive"


async def connect(config: MySQLConfig) -> aiomysql.Connection:
    """Return an ``aiomysql`` connection using ``config``."""

    return await aiomysql.connect(
        host=config.host,
        port=config.port,
        user=config.user,
        password=config.password,
        db=config.database,
        autocommit=False,
    )


async def init_schema(conn: aiomysql.Connection) -> None:
    """Create database tables if they do not exist."""

    async with conn.cursor() as cur:
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS health_records (
                timestamp VARCHAR(32) PRIMARY KEY,
                cpu_temp DOUBLE,
                cpu_percent DOUBLE,
                memory_percent DOUBLE,
                disk_percent DOUBLE
            )
            """
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_health_time ON health_records(timestamp)"
        )
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS wifi_observations (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                bssid VARCHAR(32),
                ssid VARCHAR(255),
                lat DOUBLE,
                lon DOUBLE,
                timestamp BIGINT
            )
            """
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_bssid ON wifi_observations(bssid)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_time ON wifi_observations(timestamp)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_loc ON wifi_observations(lat, lon)"
        )
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS bluetooth_observations (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                address VARCHAR(64),
                name VARCHAR(255),
                lat DOUBLE,
                lon DOUBLE,
                timestamp BIGINT
            )
            """
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_bt_addr ON bluetooth_observations(address)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_bt_time ON bluetooth_observations(timestamp)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_bt_loc ON bluetooth_observations(lat, lon)"
        )
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tower_observations (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                tower_id VARCHAR(32),
                rssi VARCHAR(32),
                lat DOUBLE,
                lon DOUBLE,
                timestamp BIGINT
            )
            """
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_tower_id ON tower_observations(tower_id)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_tower_time ON tower_observations(timestamp)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_tower_loc ON tower_observations(lat, lon)"
        )
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS scan_sessions (
                id VARCHAR(64) PRIMARY KEY,
                device_id VARCHAR(64) NOT NULL,
                scan_type VARCHAR(16) NOT NULL,
                started_at TIMESTAMP NOT NULL,
                completed_at TIMESTAMP,
                duration_seconds INTEGER,
                location_start_lat DOUBLE,
                location_start_lon DOUBLE,
                location_end_lat DOUBLE,
                location_end_lon DOUBLE,
                interface_used VARCHAR(64),
                scan_parameters TEXT,
                total_detections INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_scan_sessions_device_time ON scan_sessions(device_id, started_at)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_scan_sessions_type ON scan_sessions(scan_type)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_scan_sessions_location ON scan_sessions(location_start_lat, location_start_lon)"
        )
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS wifi_detections (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                scan_session_id VARCHAR(64) NOT NULL,
                detection_timestamp TIMESTAMP NOT NULL,
                bssid VARCHAR(32) NOT NULL,
                ssid VARCHAR(255),
                channel INTEGER,
                frequency_mhz INTEGER,
                signal_strength_dbm INTEGER,
                noise_floor_dbm INTEGER,
                snr_db INTEGER,
                encryption_type VARCHAR(64),
                cipher_suite VARCHAR(64),
                authentication_method VARCHAR(64),
                wps_enabled BOOLEAN DEFAULT FALSE,
                vendor_oui VARCHAR(16),
                vendor_name VARCHAR(255),
                device_type VARCHAR(64),
                latitude DOUBLE,
                longitude DOUBLE,
                altitude_meters DOUBLE,
                accuracy_meters DOUBLE,
                heading_degrees DOUBLE,
                speed_kmh DOUBLE,
                beacon_interval_ms INTEGER,
                dtim_period INTEGER,
                ht_capabilities TEXT,
                vht_capabilities TEXT,
                he_capabilities TEXT,
                country_code VARCHAR(8),
                regulatory_domain VARCHAR(8),
                tx_power_dbm INTEGER,
                load_percentage INTEGER,
                station_count INTEGER,
                data_rates TEXT,
                first_seen TIMESTAMP NOT NULL,
                last_seen TIMESTAMP NOT NULL,
                detection_count INTEGER DEFAULT 1
            )
            """
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_detections_session ON wifi_detections(scan_session_id)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_detections_bssid ON wifi_detections(bssid)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_detections_ssid ON wifi_detections(ssid)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_detections_time ON wifi_detections(detection_timestamp)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_wifi_detections_location ON wifi_detections(latitude, longitude)"
        )
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS bluetooth_detections (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                scan_session_id VARCHAR(64) NOT NULL,
                detection_timestamp TIMESTAMP NOT NULL,
                mac_address VARCHAR(64) NOT NULL,
                device_name VARCHAR(255),
                device_class INTEGER,
                device_type VARCHAR(64),
                manufacturer_id INTEGER,
                manufacturer_name VARCHAR(255),
                rssi_dbm INTEGER,
                tx_power_dbm INTEGER,
                bluetooth_version VARCHAR(32),
                supported_services TEXT,
                is_connectable BOOLEAN DEFAULT FALSE,
                is_paired BOOLEAN DEFAULT FALSE,
                latitude DOUBLE,
                longitude DOUBLE,
                altitude_meters DOUBLE,
                accuracy_meters DOUBLE,
                heading_degrees DOUBLE,
                speed_kmh DOUBLE,
                first_seen TIMESTAMP NOT NULL,
                last_seen TIMESTAMP NOT NULL,
                detection_count INTEGER DEFAULT 1
            )
            """
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_bt_detections_session ON bluetooth_detections(scan_session_id)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_bt_detections_mac ON bluetooth_detections(mac_address)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_bt_detections_time ON bluetooth_detections(detection_timestamp)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_bt_detections_location ON bluetooth_detections(latitude, longitude)"
        )
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS cellular_detections (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                scan_session_id VARCHAR(64) NOT NULL,
                detection_timestamp TIMESTAMP NOT NULL,
                cell_id INTEGER,
                lac INTEGER,
                mcc INTEGER,
                mnc INTEGER,
                network_name VARCHAR(255),
                technology VARCHAR(32),
                frequency_mhz INTEGER,
                band VARCHAR(32),
                channel INTEGER,
                signal_strength_dbm INTEGER,
                signal_quality INTEGER,
                timing_advance INTEGER,
                latitude DOUBLE,
                longitude DOUBLE,
                altitude_meters DOUBLE,
                accuracy_meters DOUBLE,
                heading_degrees DOUBLE,
                speed_kmh DOUBLE,
                first_seen TIMESTAMP NOT NULL,
                last_seen TIMESTAMP NOT NULL,
                detection_count INTEGER DEFAULT 1
            )
            """
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_cellular_detections_session ON cellular_detections(scan_session_id)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_cellular_detections_cell ON cellular_detections(cell_id, lac)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_cellular_detections_time ON cellular_detections(detection_timestamp)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_cellular_detections_location ON cellular_detections(latitude, longitude)"
        )
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS gps_tracks (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                scan_session_id VARCHAR(64) NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                latitude DOUBLE NOT NULL,
                longitude DOUBLE NOT NULL,
                altitude_meters DOUBLE,
                accuracy_meters DOUBLE,
                heading_degrees DOUBLE,
                speed_kmh DOUBLE,
                satellite_count INTEGER,
                hdop DOUBLE,
                vdop DOUBLE,
                pdop DOUBLE,
                fix_type VARCHAR(16)
            )
            """
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_gps_tracks_session ON gps_tracks(scan_session_id)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_gps_tracks_time ON gps_tracks(timestamp)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_gps_tracks_location ON gps_tracks(latitude, longitude)"
        )
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS network_fingerprints (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                bssid VARCHAR(32) NOT NULL,
                ssid VARCHAR(255),
                fingerprint_hash VARCHAR(64) NOT NULL,
                confidence_score DOUBLE,
                device_model VARCHAR(255),
                firmware_version VARCHAR(64),
                characteristics TEXT,
                classification VARCHAR(32),
                risk_level VARCHAR(32),
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        await cur.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_fingerprints_bssid ON network_fingerprints(bssid)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_fingerprints_hash ON network_fingerprints(fingerprint_hash)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_fingerprints_classification ON network_fingerprints(classification)"
        )
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS suspicious_activities (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                scan_session_id VARCHAR(64) NOT NULL,
                activity_type VARCHAR(64) NOT NULL,
                severity VARCHAR(32) NOT NULL,
                target_bssid VARCHAR(32),
                target_ssid VARCHAR(255),
                evidence TEXT,
                description TEXT,
                detected_at TIMESTAMP NOT NULL,
                latitude DOUBLE,
                longitude DOUBLE,
                false_positive BOOLEAN DEFAULT FALSE,
                analyst_notes TEXT
            )
            """
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_suspicious_session ON suspicious_activities(scan_session_id)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_suspicious_type ON suspicious_activities(activity_type)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_suspicious_severity ON suspicious_activities(severity)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_suspicious_time ON suspicious_activities(detected_at)"
        )
        await cur.execute(
            """
            CREATE TABLE IF NOT EXISTS network_analytics (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                bssid VARCHAR(32) NOT NULL,
                analysis_date DATE NOT NULL,
                total_detections INTEGER,
                unique_locations INTEGER,
                avg_signal_strength DOUBLE,
                max_signal_strength DOUBLE,
                min_signal_strength DOUBLE,
                signal_variance DOUBLE,
                coverage_radius_meters DOUBLE,
                mobility_score DOUBLE,
                encryption_changes INTEGER,
                ssid_changes INTEGER,
                channel_changes INTEGER,
                suspicious_score DOUBLE,
                last_analyzed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY uniq_bssid_date (bssid, analysis_date)
            )
            """
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_analytics_bssid ON network_analytics(bssid)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_analytics_date ON network_analytics(analysis_date)"
        )
        await cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_analytics_suspicious ON network_analytics(suspicious_score)"
        )
    await conn.commit()


async def insert_health_records(
    conn: aiomysql.Connection, records: Iterable[HealthRecord]
) -> None:
    """Insert ``records`` into ``health_records``."""

    rows = [
        (
            r.timestamp,
            r.cpu_temp,
            r.cpu_percent,
            r.memory_percent,
            r.disk_percent,
        )
        for r in records
    ]
    if not rows:
        return
    async with conn.cursor() as cur:
        await cur.executemany(
            """
            INSERT INTO health_records
            (timestamp, cpu_temp, cpu_percent, memory_percent, disk_percent)
            VALUES (%s, %s, %s, %s, %s)
            """,
            rows,
        )
    await conn.commit()


async def insert_wifi_observations(
    conn: aiomysql.Connection, records: Iterable[dict[str, Any]]
) -> None:
    """Insert Wi-Fi observation ``records``."""

    rows: List[Sequence[Any]] = [
        (
            r.get("bssid"),
            r.get("ssid"),
            r.get("lat"),
            r.get("lon"),
            r.get("timestamp") or r.get("last_time"),
        )
        for r in records
    ]
    if not rows:
        return
    async with conn.cursor() as cur:
        await cur.executemany(
            """
            INSERT INTO wifi_observations (bssid, ssid, lat, lon, timestamp)
            VALUES (%s, %s, %s, %s, %s)
            """,
            rows,
        )
    await conn.commit()


async def _bulk_insert(
    conn: aiomysql.Connection,
    table: str,
    columns: Sequence[str],
    records: Iterable[dict[str, Any]],
) -> None:
    rows = [tuple(r.get(c) for c in columns) for r in records]
    if not rows:
        return
    placeholders = ", ".join(["%s"] * len(columns))
    col_str = ", ".join(columns)
    async with conn.cursor() as cur:
        await cur.executemany(
            f"INSERT INTO {table} ({col_str}) VALUES ({placeholders})",
            rows,
        )
    await conn.commit()


async def insert_scan_sessions(
    conn: aiomysql.Connection, records: Iterable[dict[str, Any]]
) -> None:
    cols = [
        "id",
        "device_id",
        "scan_type",
        "started_at",
        "completed_at",
        "duration_seconds",
        "location_start_lat",
        "location_start_lon",
        "location_end_lat",
        "location_end_lon",
        "interface_used",
        "scan_parameters",
        "total_detections",
        "created_at",
    ]
    await _bulk_insert(conn, "scan_sessions", cols, records)


async def insert_wifi_detections(
    conn: aiomysql.Connection, records: Iterable[dict[str, Any]]
) -> None:
    cols = [
        "scan_session_id",
        "detection_timestamp",
        "bssid",
        "ssid",
        "channel",
        "frequency_mhz",
        "signal_strength_dbm",
        "noise_floor_dbm",
        "snr_db",
        "encryption_type",
        "cipher_suite",
        "authentication_method",
        "wps_enabled",
        "vendor_oui",
        "vendor_name",
        "device_type",
        "latitude",
        "longitude",
        "altitude_meters",
        "accuracy_meters",
        "heading_degrees",
        "speed_kmh",
        "beacon_interval_ms",
        "dtim_period",
        "ht_capabilities",
        "vht_capabilities",
        "he_capabilities",
        "country_code",
        "regulatory_domain",
        "tx_power_dbm",
        "load_percentage",
        "station_count",
        "data_rates",
        "first_seen",
        "last_seen",
        "detection_count",
    ]
    await _bulk_insert(conn, "wifi_detections", cols, records)


async def insert_bluetooth_detections(
    conn: aiomysql.Connection, records: Iterable[dict[str, Any]]
) -> None:
    cols = [
        "scan_session_id",
        "detection_timestamp",
        "mac_address",
        "device_name",
        "device_class",
        "device_type",
        "manufacturer_id",
        "manufacturer_name",
        "rssi_dbm",
        "tx_power_dbm",
        "bluetooth_version",
        "supported_services",
        "is_connectable",
        "is_paired",
        "latitude",
        "longitude",
        "altitude_meters",
        "accuracy_meters",
        "heading_degrees",
        "speed_kmh",
        "first_seen",
        "last_seen",
        "detection_count",
    ]
    await _bulk_insert(conn, "bluetooth_detections", cols, records)


async def insert_cellular_detections(
    conn: aiomysql.Connection, records: Iterable[dict[str, Any]]
) -> None:
    cols = [
        "scan_session_id",
        "detection_timestamp",
        "cell_id",
        "lac",
        "mcc",
        "mnc",
        "network_name",
        "technology",
        "frequency_mhz",
        "band",
        "channel",
        "signal_strength_dbm",
        "signal_quality",
        "timing_advance",
        "latitude",
        "longitude",
        "altitude_meters",
        "accuracy_meters",
        "heading_degrees",
        "speed_kmh",
        "first_seen",
        "last_seen",
        "detection_count",
    ]
    await _bulk_insert(conn, "cellular_detections", cols, records)


async def insert_gps_tracks(
    conn: aiomysql.Connection, records: Iterable[dict[str, Any]]
) -> None:
    cols = [
        "scan_session_id",
        "timestamp",
        "latitude",
        "longitude",
        "altitude_meters",
        "accuracy_meters",
        "heading_degrees",
        "speed_kmh",
        "satellite_count",
        "hdop",
        "vdop",
        "pdop",
        "fix_type",
    ]
    await _bulk_insert(conn, "gps_tracks", cols, records)


async def insert_network_fingerprints(
    conn: aiomysql.Connection, records: Iterable[dict[str, Any]]
) -> None:
    cols = [
        "bssid",
        "ssid",
        "fingerprint_hash",
        "confidence_score",
        "device_model",
        "firmware_version",
        "characteristics",
        "classification",
        "risk_level",
        "tags",
        "created_at",
        "updated_at",
    ]
    await _bulk_insert(conn, "network_fingerprints", cols, records)


async def insert_suspicious_activities(
    conn: aiomysql.Connection, records: Iterable[dict[str, Any]]
) -> None:
    cols = [
        "scan_session_id",
        "activity_type",
        "severity",
        "target_bssid",
        "target_ssid",
        "evidence",
        "description",
        "detected_at",
        "latitude",
        "longitude",
        "false_positive",
        "analyst_notes",
    ]
    await _bulk_insert(conn, "suspicious_activities", cols, records)


async def insert_network_analytics(
    conn: aiomysql.Connection, records: Iterable[dict[str, Any]]
) -> None:
    cols = [
        "bssid",
        "analysis_date",
        "total_detections",
        "unique_locations",
        "avg_signal_strength",
        "max_signal_strength",
        "min_signal_strength",
        "signal_variance",
        "coverage_radius_meters",
        "mobility_score",
        "encryption_changes",
        "ssid_changes",
        "channel_changes",
        "suspicious_score",
        "last_analyzed",
    ]
    await _bulk_insert(conn, "network_analytics", cols, records)


async def export_data(
    config: MySQLConfig,
    health: Iterable[HealthRecord],
    wifi: Iterable[dict[str, Any]],
    *,
    sessions: Iterable[dict[str, Any]] = (),
    wifi_dets: Iterable[dict[str, Any]] = (),
    bt_dets: Iterable[dict[str, Any]] = (),
    cell_dets: Iterable[dict[str, Any]] = (),
    gps_tracks: Iterable[dict[str, Any]] = (),
    fingerprints: Iterable[dict[str, Any]] = (),
    suspicious: Iterable[dict[str, Any]] = (),
    analytics: Iterable[dict[str, Any]] = (),
) -> None:
    """Create schema and export provided records."""

    conn = await connect(config)
    try:
        await init_schema(conn)
        await insert_health_records(conn, health)
        await insert_wifi_observations(conn, wifi)
        await insert_scan_sessions(conn, sessions)
        await insert_wifi_detections(conn, wifi_dets)
        await insert_bluetooth_detections(conn, bt_dets)
        await insert_cellular_detections(conn, cell_dets)
        await insert_gps_tracks(conn, gps_tracks)
        await insert_network_fingerprints(conn, fingerprints)
        await insert_suspicious_activities(conn, suspicious)
        await insert_network_analytics(conn, analytics)
    finally:
        conn.close()
        await conn.wait_closed()
