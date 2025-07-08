#!/usr/bin/env python3
"""Database Schema Migration Script for PiWardrive Enhanced SchemaThis script implements the comprehensive database schema outlined in database_improvements.md"""

import asyncio
import logging
from typing import Awaitable, Callable, List

import aiosqlite

from piwardrive.core.persistence import _db_path, _get_conn

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Migration = Callable[[aiosqlite.Connection], Awaitable[None]]
:
class EnhancedSchemaManager:"""Manages enhanced database schema migrations."""

    def __init__(self):
        self.migrations: List[Migration] = [
            self._migration_5_wifi_detections,
            self._migration_6_bluetooth_detections,
            self._migration_7_cellular_detections,
            self._migration_8_gps_tracks,
            self._migration_9_network_fingerprints,
            self._migration_10_suspicious_activities,
            self._migration_11_network_analytics,
self._migration_12_performance_indexes,self._migration_13_materialized_views,self._migration_14_analysis_functions,]async def _migration_5_wifi_detections(self, conn: aiosqlite.Connection) -> None:        """Enhanced WiFi detections table with comprehensive fields."""
        logger.info("Creating enhanced wifi_detections table...")await conn.execute("""
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
                data_rates TEXT,first_seen TIMESTAMP NOT NULL,last_seen TIMESTAMP NOT NULL,detection_count INTEGER DEFAULT 1,FOREIGN KEY (scan_session_id) REFERENCES scan_sessions(id)            )        """)

        # Critical indexes for analysisindexes = ["CREATE INDEX IF NOT EXISTS idx_wifi_detections_session ON wifi_detections(scan_session_id)","CREATE INDEX IF NOT EXISTS idx_wifi_detections_bssid ON wifi_detections(bssid)","CREATE INDEX IF NOT EXISTS idx_wifi_detections_ssid ON wifi_detections(ssid)","CREATE INDEX IF NOT EXISTS idx_wifi_detections_time ON wifi_detections(detection_timestamp)","CREATE INDEX IF NOT EXISTS idx_wifi_detections_location ON wifi_detections(latitude,longitude)","CREATE INDEX IF NOT EXISTS idx_wifi_detections_signal ON wifi_detections(signal_strength_dbm)","CREATE INDEX IF NOT EXISTS idx_wifi_detections_channel ON wifi_detections(channel)","CREATE INDEX IF NOT EXISTS idx_wifi_detections_encryption ON wifi_detections(encryption_type)","CREATE INDEX IF NOT EXISTS idx_wifi_detections_vendor ON wifi_detections(vendor_name)",]
:
        for index_sql in indexes:
            await conn.execute(index_sql)logger.info("Enhanced wifi_detections table created successfully")
async def _migration_6_bluetooth_detections(self,conn: aiosqlite.Connection) -> None:"""Bluetooth detections table."""
        logger.info("Creating bluetooth_detections table...")await conn.execute("""
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
                speed_kmh REAL,first_seen TIMESTAMP NOT NULL,last_seen TIMESTAMP NOT NULL,detection_count INTEGER DEFAULT 1,FOREIGN KEY (scan_session_id) REFERENCES scan_sessions(id)            )        """)
indexes = ["CREATE INDEX IF NOT EXISTS idx_bt_detections_session ON bluetooth_detections(scan_session_id)","CREATE INDEX IF NOT EXISTS idx_bt_detections_mac ON bluetooth_detections(mac_address)","CREATE INDEX IF NOT EXISTS idx_bt_detections_time ON bluetooth_detections(detection_timestamp)","CREATE INDEX IF NOT EXISTS idx_bt_detections_location ON bluetooth_detections(latitude,longitude)","CREATE INDEX IF NOT EXISTS idx_bt_detections_rssi ON bluetooth_detections(rssi_dbm)",]
:
        for index_sql in indexes:
            await conn.execute(index_sql)
async def _migration_7_cellular_detections(self,conn: aiosqlite.Connection) -> None:"""Cellular detections table."""
        logger.info("Creating cellular_detections table...")await conn.execute("""
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
                speed_kmh REAL,first_seen TIMESTAMP NOT NULL,last_seen TIMESTAMP NOT NULL,detection_count INTEGER DEFAULT 1,FOREIGN KEY (scan_session_id) REFERENCES scan_sessions(id)            )        """)
indexes = ["CREATE INDEX IF NOT EXISTS idx_cellular_detections_session ON cellular_detections(scan_session_id)","CREATE INDEX IF NOT EXISTS idx_cellular_detections_cell ON cellular_detections(cell_id,lac)","CREATE INDEX IF NOT EXISTS idx_cellular_detections_time ON cellular_detections(detection_timestamp)","CREATE INDEX IF NOT EXISTS idx_cellular_detections_location ON cellular_detections(latitude,longitude)",]

        for index_sql in indexes:
            await conn.execute(index_sql)
async def _migration_8_gps_tracks(self, conn: aiosqlite.Connection) -> None:"""GPS tracking table with enhanced precision."""
        logger.info("Creating gps_tracks table...")await conn.execute("""
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
                hdop REAL,vdop REAL,pdop REAL,fix_type TEXT,FOREIGN KEY (scan_session_id) REFERENCES scan_sessions(id)            )        """)
indexes = ["CREATE INDEX IF NOT EXISTS idx_gps_tracks_session ON gps_tracks(scan_session_id)","CREATE INDEX IF NOT EXISTS idx_gps_tracks_time ON gps_tracks(timestamp)","CREATE INDEX IF NOT EXISTS idx_gps_tracks_location ON gps_tracks(latitude,longitude)",
                
        ]
:
        for index_sql in indexes:
            await conn.execute(index_sql)
async def _migration_9_network_fingerprints(self,conn: aiosqlite.Connection) -> None:"""Network fingerprinting and classification table."""
        logger.info("Creating network_fingerprints table...")await conn.execute("""
            CREATE TABLE IF NOT EXISTS network_fingerprints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bssid TEXT NOT NULL,
                ssid TEXT,
                fingerprint_hash TEXT NOT NULL,
                confidence_score REAL,
                device_model TEXT,
                firmware_version TEXT,
                characteristics TEXT,
                classification TEXT,risk_level TEXT,tags TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP            )        """)
indexes = ["CREATE UNIQUE INDEX IF NOT EXISTS idx_fingerprints_bssid ON network_fingerprints(bssid)","CREATE INDEX IF NOT EXISTS idx_fingerprints_hash ON network_fingerprints(fingerprint_hash)","CREATE INDEX IF NOT EXISTS idx_fingerprints_classification ON network_fingerprints(classification)","CREATE INDEX IF NOT EXISTS idx_fingerprints_risk ON network_fingerprints(risk_level)",]

        for index_sql in indexes:
            await conn.execute(index_sql)
async def _migration_10_suspicious_activities(self,conn: aiosqlite.Connection) -> None:"""Security analysis and suspicious activity detection."""
        logger.info("Creating suspicious_activities table...")await conn.execute("""
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
                latitude REAL,longitude REAL,false_positive BOOLEAN DEFAULT FALSE,analyst_notes TEXT,FOREIGN KEY (scan_session_id) REFERENCES scan_sessions(id)            )        """)
indexes = ["CREATE INDEX IF NOT EXISTS idx_suspicious_session ON suspicious_activities(scan_session_id)","CREATE INDEX IF NOT EXISTS idx_suspicious_type ON suspicious_activities(activity_type)","CREATE INDEX IF NOT EXISTS idx_suspicious_severity ON suspicious_activities(severity)","CREATE INDEX IF NOT EXISTS idx_suspicious_time ON suspicious_activities(detected_at)","CREATE INDEX IF NOT EXISTS idx_suspicious_location ON suspicious_activities(latitude,longitude)",]

        for index_sql in indexes:
            await conn.execute(index_sql)
async def _migration_11_network_analytics(self, conn: aiosqlite.Connection) -> None:"""Network analytics and intelligence table."""
        logger.info("Creating network_analytics table...")await conn.execute("""
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
                ssid_changes INTEGER,channel_changes INTEGER,suspicious_score REAL,last_analyzed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,UNIQUE(bssid, analysis_date)            )        """)
indexes = ["CREATE INDEX IF NOT EXISTS idx_analytics_bssid ON network_analytics(bssid)","CREATE INDEX IF NOT EXISTS idx_analytics_date ON network_analytics(analysis_date)","CREATE INDEX IF NOT EXISTS idx_analytics_suspicious ON network_analytics(suspicious_score)","CREATE INDEX IF NOT EXISTS idx_analytics_mobility ON network_analytics(mobility_score)",]

        for index_sql in indexes:
            await conn.execute(index_sql)
async def _migration_12_performance_indexes(self,conn: aiosqlite.Connection) -> None:"""Create composite indexes for analysis performance."""
        logger.info("Creating performance optimization indexes...")

        indexes = [# Composite indexes for common analysis queries"CREATE INDEX IF NOT EXISTS idx_wifi_time_location ON wifi_detections(detection_timestamp,latitude,longitude)","CREATE INDEX IF NOT EXISTS idx_wifi_signal_channel ON wifi_detections(signal_strength_dbm,channel)","CREATE INDEX IF NOT EXISTS idx_wifi_vendor_encryption ON wifi_detections(vendor_name,encryption_type)","CREATE INDEX IF NOT EXISTS idx_wifi_ssid_bssid ON wifi_detections(ssid,bssid)","CREATE INDEX IF NOT EXISTS idx_wifi_bssid_time ON wifi_detections(bssid,detection_timestamp)",# Bluetooth analysis indexes
            "CREATE INDEX IF NOT EXISTS idx_bt_time_location ON bluetooth_detections(detection_timestamp,
                latitude,longitude)","CREATE INDEX IF NOT EXISTS idx_bt_manufacturer_type ON bluetooth_detections(manufacturer_name,device_type)",# GPS tracking indexes
            "CREATE INDEX IF NOT EXISTS idx_gps_session_time ON gps_tracks(scan_session_id,timestamp)",# Analytics indexes
            "CREATE INDEX IF NOT EXISTS idx_analytics_score_date ON network_analytics(suspicious_score,analysis_date)",
                
        ]
:
        for index_sql in indexes:
            await conn.execute(index_sql)
async def _migration_13_materialized_views(self,conn: aiosqlite.Connection) -> None:"""Create materialized views for analysis (SQLite doesn't support materialized views,so we'll create tables)."""
        logger.info("Creating analysis summary tables...")
# Daily detection stats table (acts as materialized view)await conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_detection_stats (
                detection_date DATE,
                scan_session_id TEXT,
                total_detections INTEGER,
                unique_networks INTEGER,
                avg_signal REAL,
                min_signal REAL,
                max_signal REAL,
                channels_used INTEGER,
                open_networks INTEGER,wep_networks INTEGER,wpa_networks INTEGER,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (detection_date, scan_session_id)            )        """)
# Network coverage grid tableawait conn.execute("""
            CREATE TABLE IF NOT EXISTS network_coverage_grid (
                lat_grid REAL,
                lon_grid REAL,
                detection_count INTEGER,
                unique_networks INTEGER,avg_signal REAL,max_signal REAL,last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (lat_grid, lon_grid)            )        """)
indexes = ["CREATE INDEX IF NOT EXISTS idx_daily_stats_date ON daily_detection_stats(detection_date)","CREATE INDEX IF NOT EXISTS idx_coverage_grid_location ON network_coverage_grid(lat_grid,lon_grid)",
                
        ]
:
        for index_sql in indexes:
            await conn.execute(index_sql)
async def _migration_14_analysis_functions(self,conn: aiosqlite.Connection) -> None:"""Create database triggers and views for automated analysis."""
        logger.info("Creating analysis triggers and views...")
# Trigger to update detection counts automaticallyawait conn.execute("""
            CREATE TRIGGER IF NOT EXISTS update_wifi_detection_count
            AFTER INSERT ON wifi_detections
            BEGIN
                UPDATE wifi_detections
                SET detection_count = detection_count + 1,last_seen = NEW.detection_timestamp
                WHERE bssid = NEW.bssidAND id != NEW.idAND ABS(julianday(NEW.detection_timestamp) - julianday(last_seen)) < 1;            END        """)
# View for recent suspicious activitiesawait conn.execute("""
            CREATE VIEW IF NOT EXISTS recent_suspicious_activities AS
            SELECT
                sa.*,
                ss.device_id,ss.scan_type,CASE
                    WHEN sa.severity = 'critical' THEN 4
                    WHEN sa.severity = 'high' THEN 3
                    WHEN sa.severity = 'medium' THEN 2
                    ELSE 1
                END as severity_score
            FROM suspicious_activities sa
            JOIN scan_sessions ss ON sa.scan_session_id = ss.idWHERE sa.detected_at >= datetime('now', '-7 days')AND sa.false_positive = FALSE            ORDER BY severity_score DESC, sa.detected_at DESC        """)
# View for network security overviewawait conn.execute("""
            CREATE VIEW IF NOT EXISTS network_security_overview AS
            SELECT
                wd.encryption_type,
                COUNT(*) as network_count,
                COUNT(DISTINCT wd.vendor_name) as vendor_count,
                AVG(wd.signal_strength_dbm) as avg_signal,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM wifi_detections),
                    2) as percentage,COUNT(CASE WHEN nf.risk_level = 'high' THEN 1 END) as high_risk_count,COUNT(CASE WHEN nf.risk_level = 'critical' THEN 1 END) as critical_risk_count
            FROM wifi_detections wdLEFT JOIN network_fingerprints nf ON wd.bssid = nf.bssidGROUP BY wd.encryption_type            ORDER BY network_count DESC        """):
async def get_current_version(self, conn: aiosqlite.Connection) -> int:"""Get current schema version."""try:cursor = await conn.execute("PRAGMA user_version")
            result = await cursor.fetchone()
            return result[0] if result else 0:
        except Exception:
            return 0
async def set_version(self, conn: aiosqlite.Connection, version: int) -> None:"""Set schema version."""
        await conn.execute(f"PRAGMA user_version = {version}")
async def migrate(self) -> None:"""Run all pending migrations."""
        async with _get_conn() as conn:current_version = await self.get_current_version(conn)logger.info(f"Current schema version: {current_version}")

            # Start from migration 5 since the base system has migrations 1-4
            start_migration = max(0, current_version - 4)
            target_version = 4 + len(self.migrations)
if current_version >= target_version:logger.info("Schema is already up to date")
returnlogger.info(f"Upgrading schema from version {current_version} to {target_version}")

            # Run migrations
            for i,migration in enumerate(self.migrations[start_migration:],start=start_migration):migration_version = 5 + ilogger.info(f"Running migration {migration_version}...")

                try:
                    await migration(conn)
                    await self.set_version(conn, migration_version)await conn.commit()logger.info(f"Migration {migration_version} completed successfully")except Exception as e:logger.error(f"Migration {migration_version} failed: {e}")
                    await conn.rollback()
                    raiselogger.info("All migrations completed successfully")
async def main():"""Run schema migrations."""
    manager = EnhancedSchemaManager()
await manager.migrate()if __name__ == "__main__":
    asyncio.run(main())
