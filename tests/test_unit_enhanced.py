import logging

"""
Enhanced unit tests with reduced mocking for PiWardrive.

This module contains unit tests that use real implementations where possible,
reducing reliance on mocking to catch more real-world issues.
"""

import json
import os
import shutil
import sqlite3
import tempfile
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from src.analysis import AnalysisEngine
from src.cache import CacheManager

# Import components for testing
from src.config import ConfigManager
from src.gps.client import GPSClient
from src.logging import LoggingManager
from src.network.scanner import NetworkScanner
from src.persistence import PersistenceManager
from src.security import SecurityManager
from src.utils import Utils


class RealDatabaseTestMixin:
    """Mixin for tests that use real database operations."""

    def setup_real_database(self):
        """Set up a real SQLite database for testing."""
        self.test_db_path = os.path.join(self.test_dir, "test.db")

        # Create database schema
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()

        # Create tables
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS networks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ssid TEXT NOT NULL,
                bssid TEXT NOT NULL UNIQUE,
                signal_strength INTEGER,
                frequency INTEGER,
                timestamp INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mac_address TEXT NOT NULL UNIQUE,
                manufacturer TEXT,
                device_type TEXT,
                first_seen INTEGER,
                last_seen INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                latitude REAL,
                longitude REAL,
                accuracy REAL,
                altitude REAL,
                timestamp INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_type TEXT,
                duration REAL,
                network_count INTEGER,
                device_count INTEGER,
                timestamp INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()

    def insert_test_data(self):
        """Insert test data into the database."""
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()

        # Insert test networks
        test_networks = [
            ("TestNetwork1", "00:11:22:33:44:55", -45, 2412, int(time.time())),
            ("TestNetwork2", "00:11:22:33:44:66", -55, 2437, int(time.time())),
            ("TestNetwork3", "00:11:22:33:44:77", -65, 2462, int(time.time())),
        ]

        cursor.executemany(
            """
            INSERT INTO networks (ssid, bssid, signal_strength, frequency, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """,
            test_networks,
        )

        # Insert test devices
        test_devices = [
            (
                "aa:bb:cc:dd:ee:ff",
                "Apple Inc.",
                "smartphone",
                int(time.time()),
                int(time.time()),
            ),
            (
                "bb:cc:dd:ee:ff:00",
                "Samsung",
                "smartphone",
                int(time.time()),
                int(time.time()),
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO devices (mac_address,
                manufacturer,
                device_type,
                first_seen,
                last_seen)
            VALUES (?, ?, ?, ?, ?)
        """,
            test_devices,
        )

        # Insert test locations
        test_locations = [
            (40.7128, -74.0060, 5.0, 10.0, int(time.time())),
            (40.7589, -73.9851, 3.0, 15.0, int(time.time())),
        ]

        cursor.executemany(
            """
            INSERT INTO locations (latitude, longitude, accuracy, altitude, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """,
            test_locations,
        )

        conn.commit()
        conn.close()


class TestConfigManagerReal:
    """Test ConfigManager with real configuration files."""

    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp(prefix="piwardrive_config_test_")
        self.config_path = os.path.join(self.test_dir, "config.json")

    def teardown_method(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_config_loading_real_file(self):
        """Test loading configuration from real file."""
        # Create real configuration file
        config_data = {
            "database": {"path": "/tmp/test.db", "type": "sqlite"},
            "logging": {"level": "INFO", "file": "/tmp/test.log"},
            "network": {"scan_interval": 30, "interface": "wlan0"},
        }

        with open(self.config_path, "w") as f:
            json.dump(config_data, f)

        # Test loading
        config = ConfigManager(self.config_path)
        assert config.get("database.path") == "/tmp/test.db"
        assert config.get("logging.level") == "INFO"
        assert config.get("network.scan_interval") == 30

    def test_config_validation_real_cases(self):
        """Test configuration validation with real scenarios."""
        # Test valid configuration
        valid_config = {
            "database": {"path": "/tmp/valid.db", "type": "sqlite"},
            "logging": {"level": "INFO"},
            "network": {"scan_interval": 30},
        }

        with open(self.config_path, "w") as f:
            json.dump(valid_config, f)

        config = ConfigManager(self.config_path)
        assert config.is_valid()

        # Test invalid configuration
        invalid_config = {
            "database": {"path": ""},  # Empty path
            "logging": {"level": "INVALID_LEVEL"},  # Invalid log level
            "network": {"scan_interval": -1},  # Invalid interval
        }

        invalid_config_path = os.path.join(self.test_dir, "invalid_config.json")
        with open(invalid_config_path, "w") as f:
            json.dump(invalid_config, f)

        with pytest.raises(ValueError):
            ConfigManager(invalid_config_path)

    def test_config_update_real_file(self):
        """Test updating configuration in real file."""
        # Create initial configuration
        initial_config = {
            "database": {"path": "/tmp/initial.db"},
            "logging": {"level": "INFO"},
        }

        with open(self.config_path, "w") as f:
            json.dump(initial_config, f)

        config = ConfigManager(self.config_path)

        # Update configuration
        config.set("database.path", "/tmp/updated.db")
        config.set("logging.level", "DEBUG")
        config.save()

        # Verify update persisted
        updated_config = ConfigManager(self.config_path)
        assert updated_config.get("database.path") == "/tmp/updated.db"
        assert updated_config.get("logging.level") == "DEBUG"


class TestPersistenceManagerReal(RealDatabaseTestMixin):
    """Test PersistenceManager with real database operations."""

    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp(prefix="piwardrive_persistence_test_")
        self.setup_real_database()

        # Create configuration
        config_data = {"database": {"path": self.test_db_path, "type": "sqlite"}}

        self.config_path = os.path.join(self.test_dir, "config.json")
        with open(self.config_path, "w") as f:
            json.dump(config_data, f)

        self.config = ConfigManager(self.config_path)

    def teardown_method(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_database_operations_real(self):
        """Test database operations with real database."""
        persistence = PersistenceManager(self.config)
        persistence.initialize()

        # Test network storage
        network_data = {
            "ssid": "RealTestNetwork",
            "bssid": "00:11:22:33:44:88",
            "signal_strength": -50,
            "frequency": 2412,
            "timestamp": int(time.time()),
        }

        persistence.store_network(network_data)

        # Verify storage
        networks = persistence.get_networks()
        assert len(networks) >= 1

        # Find our network
        our_network = None
        for network in networks:
            if network["bssid"] == "00:11:22:33:44:88":
                our_network = network
                break

        assert our_network is not None
        assert our_network["ssid"] == "RealTestNetwork"
        assert our_network["signal_strength"] == -50

    def test_bulk_operations_real(self):
        """Test bulk operations with real database."""
        persistence = PersistenceManager(self.config)
        persistence.initialize()

        # Prepare bulk data
        bulk_data = []
        for i in range(100):
            bulk_data.append(
                {
                    "ssid": f"BulkNetwork{i}",
                    "bssid": f"00:11:22:33:{i//10:02d}:{i%10:02d}",
                    "signal_strength": -45 - i,
                    "frequency": 2412 + (i % 13),
                    "timestamp": int(time.time()) + i,
                }
            )

        # Test bulk insert
        persistence.bulk_insert_networks(bulk_data)

        # Verify bulk insert
        networks = persistence.get_networks()
        assert len(networks) >= 100

        # Test bulk update
        update_data = []
        for i in range(50):
            update_data.append(
                {
                    "bssid": f"00:11:22:33:{i//10:02d}:{i%10:02d}",
                    "signal_strength": -30 - i,  # Updated signal strength
                }
            )

        persistence.bulk_update_networks(update_data)

        # Verify bulk update
        updated_networks = persistence.get_networks_by_bssid_list(
            [data["bssid"] for data in update_data]
        )
        for network in updated_networks:
            assert network["signal_strength"] < -30

    def test_query_performance_real(self):
        """Test query performance with real database."""
        persistence = PersistenceManager(self.config)
        persistence.initialize()

        # Insert test data
        self.insert_test_data()

        # Test various queries
        start_time = time.time()
        all_networks = persistence.get_networks()
        query_time = time.time() - start_time

        assert len(all_networks) >= 3
        assert query_time < 1.0  # Should be fast

        # Test filtered queries
        start_time = time.time()
        strong_networks = persistence.get_networks_by_signal_range(-50, 0)
        query_time = time.time() - start_time

        assert len(strong_networks) >= 1
        assert query_time < 1.0

    def test_concurrent_access_real(self):
        """Test concurrent database access with real database."""
        persistence = PersistenceManager(self.config)
        persistence.initialize()

        def worker_function(worker_id):
            """Worker function for concurrent access."""
            for i in range(10):
                network_data = {
                    "ssid": f"ConcurrentNetwork{worker_id}_{i}",
                    "bssid": f"00:11:22:33:{worker_id:02d}:{i:02d}",
                    "signal_strength": -50 - i,
                    "frequency": 2412 + i,
                    "timestamp": int(time.time()),
                }

                try:
                    persistence.store_network(network_data)
                except Exception as e:
                    print(f"Worker {worker_id} failed to store network {i}: {e}")

        # Start multiple workers
        workers = []
        for worker_id in range(5):
            worker = threading.Thread(target=worker_function, args=(worker_id,))
            workers.append(worker)
            worker.start()

        # Wait for all workers
        for worker in workers:
            worker.join()

        # Verify data from all workers
        networks = persistence.get_networks()
        assert len(networks) >= 50  # 5 workers * 10 networks each


class TestAnalysisEngineReal(RealDatabaseTestMixin):
    """Test AnalysisEngine with real data."""

    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp(prefix="piwardrive_analysis_test_")
        self.setup_real_database()

        # Create configuration
        config_data = {
            "database": {"path": self.test_db_path, "type": "sqlite"},
            "analysis": {"window_size": 3600, "min_signal_strength": -80},
        }

        self.config_path = os.path.join(self.test_dir, "config.json")
        with open(self.config_path, "w") as f:
            json.dump(config_data, f)

        self.config = ConfigManager(self.config_path)

    def teardown_method(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_network_analysis_real_data(self):
        """Test network analysis with real data."""
        # Insert comprehensive test data
        self.insert_test_data()

        # Add more diverse test data
        persistence = PersistenceManager(self.config)
        persistence.initialize()

        # Add networks with different characteristics
        diverse_networks = [
            ("StrongNetwork", "00:11:22:33:44:99", -30, 2412, int(time.time())),
            ("WeakNetwork", "00:11:22:33:44:aa", -75, 2437, int(time.time())),
            ("HighFreqNetwork", "00:11:22:33:44:bb", -45, 5180, int(time.time())),
            ("DuplicateSSID", "00:11:22:33:44:cc", -50, 2412, int(time.time())),
            ("DuplicateSSID", "00:11:22:33:44:dd", -55, 2437, int(time.time())),
        ]

        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.executemany(
            """
            INSERT INTO networks (ssid, bssid, signal_strength, frequency, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """,
            diverse_networks,
        )
        conn.commit()
        conn.close()

        # Test analysis
        analysis_engine = AnalysisEngine(self.config)

        # Test basic network analysis
        network_analysis = analysis_engine.analyze_networks()
        assert "total_networks" in network_analysis
        assert "unique_ssids" in network_analysis
        assert "signal_distribution" in network_analysis

        assert network_analysis["total_networks"] >= 8  # 3 + 5 networks
        assert network_analysis["unique_ssids"] >= 6  # Unique SSIDs

        # Test signal strength analysis
        signal_analysis = analysis_engine.analyze_signal_strength()
        assert "average_signal" in signal_analysis
        assert "signal_ranges" in signal_analysis

        # Test frequency analysis
        frequency_analysis = analysis_engine.analyze_frequency_distribution()
        assert "frequency_bands" in frequency_analysis
        assert "2.4GHz" in frequency_analysis["frequency_bands"]
        assert "5GHz" in frequency_analysis["frequency_bands"]

    def test_temporal_analysis_real_data(self):
        """Test temporal analysis with real time-based data."""
        persistence = PersistenceManager(self.config)
        persistence.initialize()

        # Insert time-series data
        base_time = int(time.time()) - 3600  # 1 hour ago

        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()

        # Insert networks over time
        for i in range(60):  # 60 data points over 1 hour
            timestamp = base_time + (i * 60)  # 1 minute intervals
            cursor.execute(
                """
                INSERT INTO networks (ssid,
                    bssid,
                    signal_strength,
                    frequency,
                    timestamp)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    f"TimeSeries{i}",
                    f"00:11:22:33:{i//10:02d}:{i%10:02d}",
                    -45 - (i % 20),
                    2412,
                    timestamp,
                ),
            )

        conn.commit()
        conn.close()

        # Test temporal analysis
        analysis_engine = AnalysisEngine(self.config)
        temporal_analysis = analysis_engine.analyze_temporal_patterns()

        assert "time_periods" in temporal_analysis
        assert "peak_activity" in temporal_analysis
        assert "activity_trend" in temporal_analysis

    def test_geolocation_analysis_real_data(self):
        """Test geolocation analysis with real location data."""
        # Insert location data
        self.insert_test_data()

        analysis_engine = AnalysisEngine(self.config)

        # Test location analysis
        location_analysis = analysis_engine.analyze_locations()
        assert "coverage_area" in location_analysis
        assert "center_point" in location_analysis
        assert "bounding_box" in location_analysis

        # Verify location calculations
        assert location_analysis["center_point"]["latitude"] > 40.0
        assert location_analysis["center_point"]["longitude"] < -70.0


class TestNetworkScannerReal:
    """Test NetworkScanner with real implementations."""

    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp(prefix="piwardrive_scanner_test_")

        # Create configuration
        config_data = {
            "network": {
                "interface": "wlan0",
                "scan_interval": 10,
                "timeout": 30,
                "mock_data": True,  # Use mock data for testing
            }
        }

        self.config_path = os.path.join(self.test_dir, "config.json")
        with open(self.config_path, "w") as f:
            json.dump(config_data, f)

        self.config = ConfigManager(self.config_path)

    def teardown_method(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_scanner_initialization_real(self):
        """Test scanner initialization with real configuration."""
        scanner = NetworkScanner(self.config)

        assert scanner.interface == "wlan0"
        assert scanner.scan_interval == 10
        assert scanner.timeout == 30

    def test_scan_execution_real(self):
        """Test scan execution with real implementation."""
        scanner = NetworkScanner(self.config)

        # Execute scan
        scan_results = scanner.execute_scan()

        # Verify results structure
        assert isinstance(scan_results, list)

        if len(scan_results) > 0:
            for result in scan_results:
                assert "ssid" in result
                assert "bssid" in result
                assert "signal_strength" in result
                assert "frequency" in result
                assert "timestamp" in result

    def test_scan_filtering_real(self):
        """Test scan result filtering with real data."""
        scanner = NetworkScanner(self.config)

        # Mock scan results for testing
        raw_results = [
            {
                "ssid": "TestNetwork1",
                "bssid": "00:11:22:33:44:55",
                "signal_strength": -30,
                "frequency": 2412,
                "timestamp": int(time.time()),
            },
            {
                "ssid": "TestNetwork2",
                "bssid": "00:11:22:33:44:66",
                "signal_strength": -80,
                "frequency": 2437,
                "timestamp": int(time.time()),
            },
            {
                "ssid": "TestNetwork3",
                "bssid": "00:11:22:33:44:77",
                "signal_strength": -45,
                "frequency": 2462,
                "timestamp": int(time.time()),
            },
        ]

        # Test signal strength filtering
        filtered_results = scanner.filter_by_signal_strength(raw_results, -50)
        assert len(filtered_results) == 2  # Only networks with signal > -50

        # Test frequency filtering
        filtered_results = scanner.filter_by_frequency_band(raw_results, "2.4GHz")
        assert len(filtered_results) == 3  # All are 2.4GHz

    def test_scan_persistence_real(self):
        """Test scan result persistence with real database."""
        # Set up database
        db_path = os.path.join(self.test_dir, "scanner_test.db")

        # Update configuration
        config_data = json.loads(open(self.config_path).read())
        config_data["database"] = {"path": db_path, "type": "sqlite"}

        with open(self.config_path, "w") as f:
            json.dump(config_data, f)

        config = ConfigManager(self.config_path)

        # Initialize components
        persistence = PersistenceManager(config)
        persistence.initialize()

        scanner = NetworkScanner(config)

        # Execute scan and store results
        scan_results = scanner.execute_scan()

        for result in scan_results:
            persistence.store_network(result)

        # Verify persistence
        stored_networks = persistence.get_networks()
        assert len(stored_networks) >= len(scan_results)


class TestGPSClientReal:
    """Test GPSClient with real implementations."""

    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp(prefix="piwardrive_gps_test_")

        # Create configuration
        config_data = {
            "gps": {
                "enabled": True,
                "port": "/dev/ttyUSB0",
                "baudrate": 9600,
                "timeout": 5,
                "mock_data": True,  # Use mock data for testing
            }
        }

        self.config_path = os.path.join(self.test_dir, "config.json")
        with open(self.config_path, "w") as f:
            json.dump(config_data, f)

        self.config = ConfigManager(self.config_path)

    def teardown_method(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_gps_initialization_real(self):
        """Test GPS client initialization with real configuration."""
        gps_client = GPSClient(self.config)

        assert gps_client.port == "/dev/ttyUSB0"
        assert gps_client.baudrate == 9600
        assert gps_client.timeout == 5

    def test_gps_data_parsing_real(self):
        """Test GPS data parsing with real NMEA sentences."""
        gps_client = GPSClient(self.config)

        # Test NMEA sentence parsing
        nmea_sentences = [
            "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47",
            "$GPGLL,4916.45,N,12311.12,W,225444,A,*1D",
            "$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A",
        ]

        for sentence in nmea_sentences:
            parsed_data = gps_client.parse_nmea_sentence(sentence)

            if parsed_data:
                assert "latitude" in parsed_data
                assert "longitude" in parsed_data
                assert "timestamp" in parsed_data

                # Verify coordinate ranges
                assert -90 <= parsed_data["latitude"] <= 90
                assert -180 <= parsed_data["longitude"] <= 180

    def test_gps_data_validation_real(self):
        """Test GPS data validation with real scenarios."""
        gps_client = GPSClient(self.config)

        # Test valid GPS data
        valid_data = {
            "latitude": 40.7128,
            "longitude": -74.0060,
            "altitude": 10.0,
            "accuracy": 5.0,
            "timestamp": int(time.time()),
        }

        assert gps_client.validate_gps_data(valid_data)

        # Test invalid GPS data
        invalid_data_sets = [
            {"latitude": 91.0, "longitude": 0.0},  # Invalid latitude
            {"latitude": 0.0, "longitude": 181.0},  # Invalid longitude
            {"latitude": "invalid", "longitude": 0.0},  # Invalid type
            {},  # Missing required fields
        ]

        for invalid_data in invalid_data_sets:
            assert not gps_client.validate_gps_data(invalid_data)


class TestUtilsReal:
    """Test utility functions with real implementations."""

    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp(prefix="piwardrive_utils_test_")

    def teardown_method(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_file_operations_real(self):
        """Test file operations with real files."""
        # Test file creation
        test_file_path = os.path.join(self.test_dir, "test_file.txt")
        test_content = "Test content for file operations"

        Utils.write_file(test_file_path, test_content)
        assert os.path.exists(test_file_path)

        # Test file reading
        read_content = Utils.read_file(test_file_path)
        assert read_content == test_content

        # Test file backup
        backup_path = Utils.backup_file(test_file_path)
        assert os.path.exists(backup_path)

        backup_content = Utils.read_file(backup_path)
        assert backup_content == test_content

    def test_json_operations_real(self):
        """Test JSON operations with real data."""
        # Test JSON writing
        test_json_path = os.path.join(self.test_dir, "test_data.json")
        test_data = {
            "networks": [
                {"ssid": "TestNetwork1", "bssid": "00:11:22:33:44:55"},
                {"ssid": "TestNetwork2", "bssid": "00:11:22:33:44:66"},
            ],
            "timestamp": int(time.time()),
            "metadata": {"version": "1.0", "format": "json"},
        }

        Utils.write_json(test_json_path, test_data)
        assert os.path.exists(test_json_path)

        # Test JSON reading
        read_data = Utils.read_json(test_json_path)
        assert read_data == test_data

        # Test JSON validation
        assert Utils.validate_json(test_json_path)

        # Test invalid JSON
        invalid_json_path = os.path.join(self.test_dir, "invalid.json")
        with open(invalid_json_path, "w") as f:
            f.write("invalid json content")

        assert not Utils.validate_json(invalid_json_path)

    def test_network_utilities_real(self):
        """Test network utilities with real implementations."""
        # Test MAC address validation
        valid_macs = [
            "00:11:22:33:44:55",
            "AA:BB:CC:DD:EE:FF",
            "aa:bb:cc:dd:ee:ff",
            "00-11-22-33-44-55",
        ]

        for mac in valid_macs:
            assert Utils.is_valid_mac_address(mac)

        # Test invalid MAC addresses
        invalid_macs = [
            "invalid",
            "00:11:22:33:44",
            "GG:HH:II:JJ:KK:LL",
            "00:11:22:33:44:55:66",
        ]

        for mac in invalid_macs:
            assert not Utils.is_valid_mac_address(mac)

        # Test SSID validation
        valid_ssids = [
            "TestNetwork",
            "Network_123",
            "My-Home-WiFi",
            "网络",  # Unicode characters
        ]

        for ssid in valid_ssids:
            assert Utils.is_valid_ssid(ssid)

        # Test invalid SSIDs
        invalid_ssids = ["", "A" * 33, None]  # Empty  # Too long  # None value

        for ssid in invalid_ssids:
            assert not Utils.is_valid_ssid(ssid)

    def test_coordinate_utilities_real(self):
        """Test coordinate utilities with real implementations."""
        # Test coordinate validation
        valid_coordinates = [
            (40.7128, -74.0060),  # New York
            (51.5074, -0.1278),  # London
            (35.6762, 139.6503),  # Tokyo
            (-33.8688, 151.2093),  # Sydney
        ]

        for lat, lon in valid_coordinates:
            assert Utils.is_valid_coordinate(lat, lon)

        # Test invalid coordinates
        invalid_coordinates = [
            (91.0, 0.0),  # Invalid latitude
            (0.0, 181.0),  # Invalid longitude
            (None, 0.0),  # None latitude
            (0.0, None),  # None longitude
            ("invalid", 0.0),  # Invalid type
        ]

        for lat, lon in invalid_coordinates:
            assert not Utils.is_valid_coordinate(lat, lon)

        # Test distance calculation
        point1 = (40.7128, -74.0060)  # New York
        point2 = (51.5074, -0.1278)  # London

        distance = Utils.calculate_distance(point1, point2)
        assert distance > 0
        assert 5500 < distance < 5600  # Approximate distance in km

    def test_time_utilities_real(self):
        """Test time utilities with real implementations."""
        # Test timestamp conversion
        current_time = int(time.time())

        # Test timestamp to datetime
        datetime_str = Utils.timestamp_to_string(current_time)
        assert isinstance(datetime_str, str)
        assert len(datetime_str) > 0

        # Test datetime to timestamp
        timestamp = Utils.string_to_timestamp(datetime_str)
        assert abs(timestamp - current_time) < 2  # Allow small difference

        # Test time range validation
        assert Utils.is_valid_time_range(current_time - 3600, current_time)
        assert not Utils.is_valid_time_range(current_time, current_time - 3600)


class TestSecurityManagerReal:
    """Test SecurityManager with real implementations."""

    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp(prefix="piwardrive_security_test_")

        # Create configuration
        config_data = {
            "security": {
                "encryption_key": "test_key_123",
                "hash_algorithm": "sha256",
                "max_login_attempts": 3,
                "session_timeout": 3600,
            }
        }

        self.config_path = os.path.join(self.test_dir, "config.json")
        with open(self.config_path, "w") as f:
            json.dump(config_data, f)

        self.config = ConfigManager(self.config_path)

    def teardown_method(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_password_hashing_real(self):
        """Test password hashing with real implementations."""
        security_manager = SecurityManager(self.config)

        # Test password hashing
        password = "test_password_123"
        hashed = security_manager.hash_password(password)

        assert hashed != password
        assert len(hashed) > 0

        # Test password verification
        assert security_manager.verify_password(password, hashed)
        assert not security_manager.verify_password("wrong_password", hashed)

    def test_data_encryption_real(self):
        """Test data encryption with real implementations."""
        security_manager = SecurityManager(self.config)

        # Test data encryption
        original_data = "sensitive_data_to_encrypt"
        encrypted_data = security_manager.encrypt_data(original_data)

        assert encrypted_data != original_data
        assert len(encrypted_data) > 0

        # Test data decryption
        decrypted_data = security_manager.decrypt_data(encrypted_data)
        assert decrypted_data == original_data

    def test_session_management_real(self):
        """Test session management with real implementations."""
        security_manager = SecurityManager(self.config)

        # Test session creation
        user_id = "test_user"
        session_token = security_manager.create_session(user_id)

        assert session_token is not None
        assert len(session_token) > 0

        # Test session validation
        assert security_manager.validate_session(session_token)

        # Test session expiration
        expired_session = security_manager.create_session(user_id)
        security_manager.expire_session(expired_session)

        assert not security_manager.validate_session(expired_session)


class TestCacheManagerReal:
    """Test CacheManager with real implementations."""

    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp(prefix="piwardrive_cache_test_")

        # Create configuration
        config_data = {"cache": {"max_size": 1000, "ttl": 300, "cleanup_interval": 60}}

        self.config_path = os.path.join(self.test_dir, "config.json")
        with open(self.config_path, "w") as f:
            json.dump(config_data, f)

        self.config = ConfigManager(self.config_path)

    def teardown_method(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_cache_operations_real(self):
        """Test cache operations with real implementations."""
        cache_manager = CacheManager(self.config)

        # Test cache set and get
        key = "test_key"
        value = {"data": "test_value", "timestamp": int(time.time())}

        cache_manager.set(key, value)
        cached_value = cache_manager.get(key)

        assert cached_value == value

        # Test cache miss
        missing_value = cache_manager.get("nonexistent_key")
        assert missing_value is None

        # Test cache deletion
        cache_manager.delete(key)
        deleted_value = cache_manager.get(key)
        assert deleted_value is None

    def test_cache_expiration_real(self):
        """Test cache expiration with real implementations."""
        # Create cache with short TTL
        config_data = json.loads(open(self.config_path).read())
        config_data["cache"]["ttl"] = 1  # 1 second TTL

        short_ttl_config_path = os.path.join(self.test_dir, "short_ttl_config.json")
        with open(short_ttl_config_path, "w") as f:
            json.dump(config_data, f)

        short_ttl_config = ConfigManager(short_ttl_config_path)
        cache_manager = CacheManager(short_ttl_config)

        # Set cache value
        key = "expiring_key"
        value = "expiring_value"

        cache_manager.set(key, value)

        # Verify immediate retrieval
        cached_value = cache_manager.get(key)
        assert cached_value == value

        # Wait for expiration
        time.sleep(2)

        # Verify expiration
        expired_value = cache_manager.get(key)
        assert expired_value is None

    def test_cache_size_limits_real(self):
        """Test cache size limits with real implementations."""
        # Create cache with small size limit
        config_data = json.loads(open(self.config_path).read())
        config_data["cache"]["max_size"] = 3  # Very small cache

        small_cache_config_path = os.path.join(self.test_dir, "small_cache_config.json")
        with open(small_cache_config_path, "w") as f:
            json.dump(config_data, f)

        small_cache_config = ConfigManager(small_cache_config_path)
        cache_manager = CacheManager(small_cache_config)

        # Fill cache beyond limit
        for i in range(5):
            cache_manager.set(f"key_{i}", f"value_{i}")

        # Verify cache eviction
        cache_size = cache_manager.size()
        assert cache_size <= 3

        # Verify some keys were evicted
        evicted_count = 0
        for i in range(5):
            if cache_manager.get(f"key_{i}") is None:
                evicted_count += 1

        assert evicted_count >= 2  # At least 2 keys should be evicted


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
