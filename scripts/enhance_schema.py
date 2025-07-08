#!/usr/bin/env python3
"""Enhanced table schema migration to add missing advanced features."""

import asyncio
import logging
import os
import sqlite3
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedSchemaMigration:"""Add enhanced schema features to existing tables."""

    def __init__(self, db_path: str):self.db_path = db_pathdef add_wifi_advanced_features(self):        """Add WiFi 6E/7 and advanced wireless features."""
        logger.info("Adding advanced WiFi features...")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Add WiFi 6E/7 fieldsadvanced_wifi_columns = [("wifi_standard", "TEXT"),  # 802.11a/b/g/n/ac/ax/be
            ("wifi_generation", "TEXT"),  # WiFi 4/5/6/6E/7
            ("max_data_rate_mbps", "INTEGER"),  # Maximum theoretical data rate
            ("spatial_streams", "INTEGER"),  # Number of spatial streams
            ("channel_width_mhz", "INTEGER"),  # 20/40/80/160/320 MHz
            ("band_type", "TEXT"),  # 2.4GHz/5GHz/6GHz
            ("eht_capabilities", "TEXT"),  # WiFi 7 (EHT) capabilities JSON
            ("mlo_support", "BOOLEAN"),  # Multi-Link Operation support
            ("puncturing_pattern", "TEXT"),  # Preamble puncturing pattern
            ("rtt_support", "BOOLEAN"),  # Round Trip Time measurement
            ("twt_support", "BOOLEAN"),  # Target Wake Time support
            ("ofdma_support", "BOOLEAN"),  # OFDMA support
            ("mu_mimo_support", "BOOLEAN"),  # MU-MIMO support
            ("beamforming_support", "BOOLEAN"),  # Beamforming support
            ("mesh_capabilities", "TEXT"),  # Mesh networking capabilities JSON
            ("security_protocols", "TEXT"),  # WPA3/SAE/OWE details JSON
            ("qos_support", "TEXT"),  # QoS capabilities JSON
            ("power_management", "TEXT"),  # Power management features JSON
        ]

        for column_name, column_type in advanced_wifi_columns:try:cursor.execute(f"ALTER TABLE wifi_detections ADD COLUMN {column_name} {column_type}")
                logger.info(f"Added column: {column_name}")except sqlite3.OperationalError as e:if "duplicate column name" in str(e):
                    logger.debug(f"Column {column_name} already exists")else:logger.error(f"Failed to add column {column_name}: {e}")

        conn.commit()
        conn.close()
def add_bluetooth_ble_features(self):"""Add BLE advertisement parsing and advanced Bluetooth features."""
        logger.info("Adding advanced Bluetooth features...")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Add BLE and advanced Bluetooth fieldsble_columns = [("advertisement_data", "TEXT"),  # Raw advertisement data JSON
            ("scan_response_data", "TEXT"),  # Scan response data JSON
            ("advertising_interval_ms", "INTEGER"),  # Advertising interval
            ("advertising_type", "TEXT"),  # ADV_IND, ADV_DIRECT_IND, etc.
            ("ble_appearance", "INTEGER"),  # BLE appearance value
            ("service_uuids", "TEXT"),  # Service UUIDs JSON array
            ("manufacturer_data", "TEXT"),  # Manufacturer-specific data JSON
            ("local_name", "TEXT"),  # Complete/shortened local name
("tx_power_level", "INTEGER"),  # TX power level from advertisement
            ("connection_interval", "INTEGER"),  # Preferred connection interval
            ("service_solicitation", "TEXT"),  # Service solicitation UUIDs JSON
            ("public_target_address", "TEXT"),  # Public target address
            ("random_target_address", "TEXT"),  # Random target address
            ("advertising_flags", "INTEGER"),  # Advertising flags
("uri_data", "TEXT"),  # URI data from advertisements
            ("mesh_message", "TEXT"),  # Bluetooth Mesh message data JSON
            ("ibeacon_data", "TEXT"),  # iBeacon data JSON
            ("eddystone_data", "TEXT"),  # Eddystone data JSON
            ("covid_exposure_data", "TEXT"),  # COVID exposure notification data
        ]

        for column_name, column_type in ble_columns:try:cursor.execute(f"ALTER TABLE bluetooth_detections ADD COLUMN {column_name} {column_type}")
                logger.info(f"Added column: {column_name}")except sqlite3.OperationalError as e:if "duplicate column name" in str(e):
                    logger.debug(f"Column {column_name} already exists")else:logger.error(f"Failed to add column {column_name}: {e}")

        conn.commit()
        conn.close()
def add_cellular_5g_features(self):"""Add 5G SA/NSA and advanced cellular features."""
        logger.info("Adding advanced cellular features...")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Add 5G and advanced cellular fieldscellular_5g_columns = [("nr_mode", "TEXT"),  # 5G SA (Standalone) or NSA (Non-Standalone)
            ("carrier_aggregation", "TEXT"),  # CA configuration JSON
            ("beam_id", "INTEGER"),  # 5G beam identifier
            ("ss_sinr", "REAL"),  # SS-SINR (Signal-to-Interference-plus-Noise Ratio)
            ("ss_rsrp", "REAL"),  # SS-RSRP (Reference Signal Received Power)
            ("ss_rsrq", "REAL"),  # SS-RSRQ (Reference Signal Received Quality)
            ("pci", "INTEGER"),  # Physical Cell ID
            ("tac", "INTEGER"),  # Tracking Area Code
            ("plmn_id", "TEXT"),  # Public Land Mobile Network ID
            ("slice_info", "TEXT"),  # Network slicing information JSON
            ("bandwidth_mhz", "INTEGER"),  # Channel bandwidth
            ("mimo_layers", "INTEGER"),  # MIMO layer count
            ("modulation_scheme", "TEXT"),  # Modulation scheme (QPSK, 16QAM, etc.)
            ("duplex_mode", "TEXT"),  # FDD/TDD
            ("subcarrier_spacing", "INTEGER"),  # Subcarrier spacing (kHz)
            ("numerology", "INTEGER"),  # 5G numerology
            ("frame_structure", "TEXT"),  # Frame structure configuration
            ("beamforming_info", "TEXT"),  # Beamforming configuration JSON
            ("network_capabilities", "TEXT"),  # Network capabilities JSON
        ]

        for column_name, column_type in cellular_5g_columns:try:cursor.execute(f"ALTER TABLE cellular_detections ADD COLUMN {column_name} {column_type}")
                logger.info(f"Added column: {column_name}")except sqlite3.OperationalError as e:if "duplicate column name" in str(e):
                    logger.debug(f"Column {column_name} already exists")else:logger.error(f"Failed to add column {column_name}: {e}")

        conn.commit()
        conn.close()
def add_gps_gnss_features(self):"""Add GNSS constellation and advanced GPS features."""
        logger.info("Adding advanced GNSS features...")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Add GNSS constellation and advanced GPS fieldsgnss_columns = [("gnss_constellations", "TEXT"),  # GPS, GLONASS, Galileo, BeiDou JSON
            ("satellite_details", "TEXT"),  # Per-satellite data JSON
            ("dgps_station_id", "INTEGER"),  # DGPS reference station ID
            ("rtk_mode", "TEXT"),  # RTK mode (fixed, float, etc.)
            ("baseline_length_m", "REAL"),  # RTK baseline length
            ("age_of_corrections", "INTEGER"),  # Age of differential corrections
            ("geoid_height_m", "REAL"),  # Geoid height
            ("magnetic_declination", "REAL"),  # Magnetic declination
            ("grid_convergence", "REAL"),  # Grid convergence
            ("coordinate_system", "TEXT"),  # WGS84, NAD83, etc.
            ("utm_zone", "TEXT"),  # UTM zone if applicable
            ("multipath_indicator", "INTEGER"),  # Multipath detection level
            ("carrier_phase_measurements", "TEXT"),  # Carrier phase data JSON
            ("pseudorange_measurements", "TEXT"),  # Pseudorange data JSON
            ("doppler_measurements", "TEXT"),  # Doppler shift data JSON
            ("ionospheric_delay", "REAL"),  # Ionospheric delay estimate
            ("tropospheric_delay", "REAL"),  # Tropospheric delay estimate
            ("clock_bias", "REAL"),  # Receiver clock bias
            ("antenna_height_m", "REAL"),  # Antenna height above ground
        ]
:
        for column_name, column_type in gnss_columns:try:cursor.execute(f"ALTER TABLE gps_tracks ADD COLUMN {column_name} {column_type}")
                logger.info(f"Added column: {column_name}")except sqlite3.OperationalError as e:if "duplicate column name" in str(e):
                    logger.debug(f"Column {column_name} already exists")else:logger.error(f"Failed to add column {column_name}: {e}")

        conn.commit()
        conn.close()
def create_advanced_indexes(self):"""Create indexes for the new advanced fields."""
        logger.info("Creating indexes for advanced fields...")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        advanced_indexes = [# WiFi advanced indexes("idx_wifi_standard_generation","wifi_detections","wifi_standard,wifi_generation"),("idx_wifi_band_channel_width","wifi_detections","band_type,channel_width_mhz"),("idx_wifi_data_rate", "wifi_detections", "max_data_rate_mbps DESC"),("idx_wifi_security_protocols", "wifi_detections", "security_protocols"),# Bluetooth/BLE advanced indexes
            ("idx_ble_advertisement_type", "bluetooth_detections", "advertising_type"),("idx_ble_service_uuids", "bluetooth_detections", "service_uuids"),("idx_ble_beacon_type","bluetooth_detections","ibeacon_data,eddystone_data"),# Cellular 5G indexes
            ("idx_cellular_nr_mode", "cellular_detections", "nr_mode, technology"),("idx_cellular_5g_quality","cellular_detections","ss_sinr DESC,ss_rsrp DESC"),("idx_cellular_pci_tac", "cellular_detections", "pci, tac"),# GNSS advanced indexes
            ("idx_gnss_constellations", "gps_tracks", "gnss_constellations"),("idx_gnss_accuracy_mode", "gps_tracks", "rtk_mode, accuracy_meters"),("idx_gnss_coordinate_system", "gps_tracks", "coordinate_system, utm_zone"),]
:
        for index_name, table_name, columns in advanced_indexes:
            try:# Check if table and columns existcursor.execute(f"PRAGMA table_info({table_name})")
                table_columns = [row[1] for row in cursor.fetchall()]

                # Check if all columns in the index exist:
                index_columns = [col.strip() for col in columns.split(',')]if all(col.split()[0] in table_columns for col in index_columns):cursor.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name}({columns})")
                    logger.info(f"Created index: {index_name}")else:logger.warning(f"Skipping index {index_name} - missing columns")
except Exception as e:logger.error(f"Failed to create index {index_name}: {e}")

        conn.commit()
        conn.close()
def run_all_enhancements(self) -> Dict[str, Any]:"""Run all schema enhancements."""
        logger.info("Running all schema enhancements...")
results = {"timestamp": "2025-07-04T00:00:00","enhancements_applied": []
        }

        try:self.add_wifi_advanced_features()results["enhancements_applied"].append("wifi_advanced_features")
self.add_bluetooth_ble_features()results["enhancements_applied"].append("bluetooth_ble_features")
self.add_cellular_5g_features()results["enhancements_applied"].append("cellular_5g_features")
self.add_gps_gnss_features()results["enhancements_applied"].append("gps_gnss_features")
self.create_advanced_indexes()results["enhancements_applied"].append("advanced_indexes")results["success"] = "True"
            logger.info("All schema enhancements completed successfully")
except Exception as e:results["error"] = str(e)
            results["success"] = "False"
            logger.error(f"Schema enhancement failed: {e}")

        return results
async def main():"""Main enhancement function."""
    print("=== PiWardrive Enhanced Schema Migration ===\n")
# Find databasedb_path = os.path.expanduser("~/.config/piwardrive/app.db")
if not os.path.exists(db_path):print(f"❌ Database not found at {db_path}")
        print("Please run the database initialization script first.")
        returnprint(f"Enhancing database schema: {db_path}")

    enhancer = EnhancedSchemaMigration(db_path)
    results = enhancer.run_all_enhancements()print("\n=== Enhancement Results ===")
    if results["success"]:
        print("✅ Schema enhancements completed successfully")
print(f"Applied enhancements: {', '.join(results['enhancements_applied'])}")else:print(f"❌ Schema enhancement failed: {results.get('error', 'Unknown error')}")print("\n=== Schema enhancement completed! ===")if __name__ == "__main__":
    asyncio.run(main())
