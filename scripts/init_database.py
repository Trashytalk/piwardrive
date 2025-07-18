#!/usr/bin/env python3
"""Comprehensive database initialization and migration runner."""

import asyncio
import logging
import os
import sqlite3
from datetime import datetime
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseInitializer:"""Initialize database with all required tables and indexes."""
:
    def __init__(self, db_path: str):
        self.db_path = db_pathself.ensure_directory()def ensure_directory(self):        """Ensure the database directory exists."""os.makedirs(os.path.dirname(self.db_path), exist_ok=True)def create_database(self):        """Create database with all required tables and indexes."""
        logger.info(f"Creating database at {self.db_path}")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
# Set performance pragmascursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA temp_store=MEMORY")
        cursor.execute("PRAGMA cache_size=10000")
# Create schema version tablecursor.execute("""CREATE TABLE IF NOT EXISTS schema_version (version INTEGER PRIMARY KEY            )        """)
# Create migration tracking tablecursor.execute("""CREATE TABLE IF NOT EXISTS schema_migrations (version INTEGER PRIMARY KEY,applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP            )        """)
:
        # Migration 1: Core tables
        self._migration_1_core_tables(cursor)

        # Migration 2: Scan sessions
        self._migration_2_scan_sessions(cursor)

        # Migration 3: WiFi detections
        self._migration_3_wifi_detections(cursor)

        # Migration 4: Bluetooth detections
        self._migration_4_bluetooth_detections(cursor)

        # Migration 5: Cellular detections
        self._migration_5_cellular_detections(cursor)

        # Migration 6: GPS tracks
        self._migration_6_gps_tracks(cursor)

        # Migration 7: Network fingerprints
        self._migration_7_network_fingerprints(cursor)

        # Migration 8: Suspicious activities
        self._migration_8_suspicious_activities(cursor)

        # Migration 9: Network analytics
        self._migration_9_network_analytics(cursor)

        # Migration 10: Performance indexes
        self._migration_10_performance_indexes(cursor)

        # Migration 11: Materialized views
        self._migration_11_materialized_views(cursor)
# Set final schema versioncursor.execute("INSERT OR REPLACE INTO schema_version (version) VALUES (11)")

        conn.commit()conn.close()logger.info("Database initialization completed successfully")
def _migration_1_core_tables(self, cursor):"""Migration 1: Core application tables."""
        logger.info("Creating core application tables...")
# Health records tablecursor.execute("""
            CREATE TABLE IF NOT EXISTS health_records (
                timestamp TEXT PRIMARY KEY,cpu_temp REAL,cpu_percent REAL,memory_percent REAL,disk_percent REAL            )        """)
# App state tablecursor.execute("""
            CREATE TABLE IF NOT EXISTS app_state (id INTEGER PRIMARY KEY CHECK (id = 1),last_screen TEXT,last_start TEXT,first_run INTEGER            )        """)
# Access point cachecursor.execute("""
            CREATE TABLE IF NOT EXISTS ap_cache (
                bssid TEXT PRIMARY KEY,
                ssid TEXT,encryption TEXT,lat REAL,lon REAL,last_time INTEGER            )        """)
# Dashboard settingscursor.execute("""CREATE TABLE IF NOT EXISTS dashboard_settings (id INTEGER PRIMARY KEY CHECK (id = 1),layout TEXT,widgets TEXT            )        """)
# Users tablecursor.execute("""
            CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY,password_hash TEXT NOT NULL,token_hash TEXT,token_created INTEGER            )        """)
# Basic indexescursor.execute("CREATE INDEX IF NOT EXISTS idx_health_time ON health_records(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_apcache_time ON ap_cache(last_time)")
# Record migrationcursor.execute("INSERT OR REPLACE INTO schema_migrations (version) VALUES (1)")
def _migration_2_scan_sessions(self, cursor):"""Migration 2: Scan sessions table."""
        logger.info("Creating scan sessions table...")cursor.execute("""
            CREATE TABLE IF NOT EXISTS scan_sessions (
                id TEXT PRIMARY KEY,
                device_id TEXT NOT NULL,
                scan_type TEXT NOT NULL,
                started_at TIMESTAMP NOT NULL,
                completed_at TIMESTAMP,
                duration_seconds INTEGER,
                location_start_lat REAL,
                location_start_lon REAL,
                location_end_lat REAL,
                location_end_lon REAL,interface_used TEXT,scan_parameters TEXT,total_detections INTEGER DEFAULT 0,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP            )        """)
# Indexescursor.execute("CREATE INDEX IF NOT EXISTS idx_scan_sessions_device_time ON scan_sessions(device_id,started_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_scan_sessions_type ON scan_sessions(scan_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_scan_sessions_location ON scan_sessions(location_start_lat,location_start_lon)")cursor.execute("INSERT OR REPLACE INTO schema_migrations (version) VALUES (2)")
def _migration_3_wifi_detections(self, cursor):"""Migration 3: Enhanced WiFi detections table."""
        logger.info("Creating WiFi detections table...")cursor.execute("""
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
# Critical indexescursor.execute("CREATE INDEX IF NOT EXISTS idx_wifi_detections_session ON wifi_detections(scan_session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_wifi_detections_bssid ON wifi_detections(bssid)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_wifi_detections_ssid ON wifi_detections(ssid)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_wifi_detections_time ON wifi_detections(detection_timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_wifi_detections_location ON wifi_detections(latitude,longitude)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_wifi_detections_signal ON wifi_detections(signal_strength_dbm)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_wifi_detections_channel ON wifi_detections(channel)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_wifi_detections_encryption ON wifi_detections(encryption_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_wifi_detections_vendor ON wifi_detections(vendor_name)")cursor.execute("INSERT OR REPLACE INTO schema_migrations (version) VALUES (3)")
def _migration_4_bluetooth_detections(self, cursor):"""Migration 4: Bluetooth detections table."""
        logger.info("Creating Bluetooth detections table...")cursor.execute("""
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
# Indexescursor.execute("CREATE INDEX IF NOT EXISTS idx_bt_detections_session ON bluetooth_detections(scan_session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_bt_detections_mac ON bluetooth_detections(mac_address)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_bt_detections_time ON bluetooth_detections(detection_timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_bt_detections_location ON bluetooth_detections(latitude,longitude)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_bt_detections_rssi ON bluetooth_detections(rssi_dbm)")cursor.execute("INSERT OR REPLACE INTO schema_migrations (version) VALUES (4)"):
def _migration_5_cellular_detections(self, cursor):"""Migration 5: Cellular detections table."""
        logger.info("Creating cellular detections table...")cursor.execute("""
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
# Indexescursor.execute("CREATE INDEX IF NOT EXISTS idx_cellular_detections_session ON cellular_detections(scan_session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cellular_detections_cell ON cellular_detections(cell_id,lac)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cellular_detections_time ON cellular_detections(detection_timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cellular_detections_location ON cellular_detections(latitude,longitude)")cursor.execute("INSERT OR REPLACE INTO schema_migrations (version) VALUES (5)")
def _migration_6_gps_tracks(self, cursor):"""Migration 6: GPS tracks table."""
        logger.info("Creating GPS tracks table...")cursor.execute("""
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
# Indexescursor.execute("CREATE INDEX IF NOT EXISTS idx_gps_tracks_session ON gps_tracks(scan_session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_gps_tracks_time ON gps_tracks(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_gps_tracks_location ON gps_tracks(latitude,longitude)")cursor.execute("INSERT OR REPLACE INTO schema_migrations (version) VALUES (6)")
def _migration_7_network_fingerprints(self, cursor):"""Migration 7: Network fingerprints table."""
        logger.info("Creating network fingerprints table...")cursor.execute("""
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
# Indexescursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_fingerprints_bssid ON network_fingerprints(bssid)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fingerprints_hash ON network_fingerprints(fingerprint_hash)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fingerprints_classification ON network_fingerprints(classification)")cursor.execute("INSERT OR REPLACE INTO schema_migrations (version) VALUES (7)")
def _migration_8_suspicious_activities(self, cursor):"""Migration 8: Suspicious activities table."""
        logger.info("Creating suspicious activities table...")cursor.execute("""
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
# Indexescursor.execute("CREATE INDEX IF NOT EXISTS idx_suspicious_session ON suspicious_activities(scan_session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_suspicious_type ON suspicious_activities(activity_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_suspicious_severity ON suspicious_activities(severity)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_suspicious_time ON suspicious_activities(detected_at)")cursor.execute("INSERT OR REPLACE INTO schema_migrations (version) VALUES (8)")
def _migration_9_network_analytics(self, cursor):"""Migration 9: Network analytics table."""
        logger.info("Creating network analytics table...")cursor.execute("""
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
            )        """)
# Indexescursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_bssid ON network_analytics(bssid)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_date ON network_analytics(analysis_date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_suspicious ON network_analytics(suspicious_score)")cursor.execute("INSERT OR REPLACE INTO schema_migrations (version) VALUES (9)")
def _migration_10_performance_indexes(self, cursor):"""Migration 10: Additional performance indexes."""
        logger.info("Creating performance indexes...")
# Compound indexes for common queriescursor.execute("CREATE INDEX IF NOT EXISTS idx_wifi_time_location ON wifi_detections(detection_timestamp,latitude,longitude)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_wifi_signal_channel ON wifi_detections(signal_strength_dbm,channel)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_wifi_vendor_encryption ON wifi_detections(vendor_name,encryption_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_wifi_ssid_bssid ON wifi_detections(ssid,bssid)")
# Additional bluetooth indexescursor.execute("CREATE INDEX IF NOT EXISTS idx_bt_manufacturer_type ON bluetooth_detections(manufacturer_name,device_type)")
# Additional cellular indexescursor.execute("CREATE INDEX IF NOT EXISTS idx_cellular_network_tech ON cellular_detections(network_name,technology)")cursor.execute("INSERT OR REPLACE INTO schema_migrations (version) VALUES (10)"):
def _migration_11_materialized_views(self, cursor):"""Migration 11: Materialized views as tables."""
        logger.info("Creating materialized view tables...")
# Daily detection statscursor.execute("DROP TABLE IF EXISTS daily_detection_stats")
        cursor.execute("""
            CREATE TABLE daily_detection_stats (
                detection_date DATE,
                scan_session_id TEXT,
                total_detections INTEGER,
                unique_networks INTEGER,
                avg_signal REAL,
                min_signal REAL,
                max_signal REAL,
                channels_used INTEGER,
                open_networks INTEGER,wep_networks INTEGER,wpa_networks INTEGER,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (detection_date, scan_session_id)            )        """)
# Network coverage gridcursor.execute("DROP TABLE IF EXISTS network_coverage_grid")
        cursor.execute("""
            CREATE TABLE network_coverage_grid (
                lat_grid REAL,
                lon_grid REAL,
                detection_count INTEGER,
                unique_networks INTEGER,avg_signal REAL,max_signal REAL,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (lat_grid, lon_grid)            )        """)cursor.execute("INSERT OR REPLACE INTO schema_migrations (version) VALUES (11)")
async def main():"""Initialize the database."""
    print("=== PiWardrive Database Initialization ===\n")
# Default database pathdb_path = os.path.expanduser("~/.config/piwardrive/app.db")print(f"Initializing database at: {db_path}")

    initializer = DatabaseInitializer(db_path)
    initializer.create_database()print("\n✅ Database initialization completed successfully!")
    print(f"Database created at: {db_path}")
# Run status checkprint("\n=== Post-initialization Status ===")
from simple_db_check import check_database_status
status = await check_database_status(db_path)print(f"Tables Present ({len(status['tables_present'])}): {','.join(status['tables_present'])}")
    print(f"Indexes Present ({len(status['indexes_present'])}): {','.join(status['indexes_present'])}")if status["recommendations"]:
        print(f"\nRemaining recommendations:")
        for rec in status["recommendations"]:
            print(f"  - {rec['description']}")else:print("\n✅ No additional recommendations - database is ready!")if __name__ == "__main__":
    asyncio.run(main())
