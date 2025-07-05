import logging

"""
Comprehensive integration tests for PiWardrive.

This module contains end-to-end integration tests that validate the interaction
between multiple components without mocking.
"""

import asyncio
import json
import os
import shutil
import sqlite3
import tempfile
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

import pytest
import requests

from src.analysis import AnalysisEngine
from src.config import ConfigManager
from src.data.aggregation import AggregationService
from src.gps.client import GPSClient
from src.network.scanner import NetworkScanner
from src.persistence import PersistenceManager

# Import core components
from src.service import PiWardriveService
from src.webui.server import WebUIServer


class IntegrationTestFixture:
    """Base fixture for integration tests."""

    def __init__(self, test_name):
        self.test_name = test_name
        self.test_dir = None
        self.db_path = None
        self.config_path = None
        self.service = None
        self.webui_server = None
        self.cleanup_tasks = []

    def setup(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp(prefix=f"piwardrive_test_{self.test_name}_")
        self.db_path = os.path.join(self.test_dir, "test.db")
        self.config_path = os.path.join(self.test_dir, "config.json")

        # Create test configuration
        test_config = {
            "database": {"path": self.db_path, "type": "sqlite"},
            "logging": {
                "level": "INFO",
                "file": os.path.join(self.test_dir, "test.log"),
            },
            "webui": {"port": 0, "host": "127.0.0.1"},  # Let OS choose port
            "gps": {"enabled": False, "mock_data": True},  # Disable GPS for testing
            "network": {"scan_interval": 10, "mock_data": True},
        }

        with open(self.config_path, "w") as f:
            json.dump(test_config, f)

        return self

    def teardown(self):
        """Clean up test environment."""
        # Stop any running services
        if self.service:
            self.service.stop()

        if self.webui_server:
            self.webui_server.stop()

        # Execute cleanup tasks
        for task in self.cleanup_tasks:
            try:
                task()
            except Exception as e:
                print(f"Cleanup task failed: {e}")

        # Remove test directory
        if self.test_dir and os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def add_cleanup_task(self, task):
        """Add a cleanup task to be executed during teardown."""
        self.cleanup_tasks.append(task)

    @contextmanager
    def managed_service(self, service_class, *args, **kwargs):
        """Context manager for services that need cleanup."""
        service = service_class(*args, **kwargs)
        try:
            yield service
        finally:
            if hasattr(service, "stop"):
                service.stop()
            elif hasattr(service, "close"):
                service.close()


@pytest.fixture
def integration_fixture(request):
    """Pytest fixture for integration tests."""
    fixture = IntegrationTestFixture(request.node.name)
    fixture.setup()
    yield fixture
    fixture.teardown()


class TestServiceIntegration:
    """Test integration between core services."""

    def test_service_startup_and_shutdown(self, integration_fixture):
        """Test complete service lifecycle."""
        _config = ConfigManager(integration_fixture.config_path)

        # Test service initialization
        service = PiWardriveService(config)
        assert service is not None

        # Test service startup
        service.start()
        assert service.is_running()

        # Test service shutdown
        service.stop()
        assert not service.is_running()

    def test_database_initialization_and_operations(self, integration_fixture):
        """Test database setup and basic operations."""
        _config = ConfigManager(integration_fixture.config_path)
        persistence = PersistenceManager(config)

        # Test database initialization
        persistence.initialize()
        assert os.path.exists(integration_fixture.db_path)

        # Test table creation
        with sqlite3.connect(integration_fixture.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

        expected_tables = ["networks", "devices", "locations", "scans"]
        for table in expected_tables:
            assert table in tables, f"Table {table} not found in database"

    def test_config_validation_and_loading(self, integration_fixture):
        """Test configuration validation and loading."""
        # Test valid configuration
        _config = ConfigManager(integration_fixture.config_path)
        assert config.is_valid()

        # Test invalid configuration
        invalid_config_path = os.path.join(
            integration_fixture.test_dir, "invalid_config.json"
        )
        with open(invalid_config_path, "w") as f:
            json.dump({"invalid": "config"}, f)

        with pytest.raises(Exception):
            ConfigManager(invalid_config_path)

    def test_gps_data_flow(self, integration_fixture):
        """Test GPS data collection and processing."""
        _config = ConfigManager(integration_fixture.config_path)

        # Use mock GPS client
        with integration_fixture.managed_service(GPSClient, config) as gps_client:
            # Test GPS data collection
            gps_client.start()
            time.sleep(1)  # Allow some data collection

            # Verify data was collected
            data = gps_client.get_recent_data()
            assert len(data) > 0

            # Verify data format
            for point in data:
                assert "latitude" in point
                assert "longitude" in point
                assert "timestamp" in point

    def test_network_scanning_integration(self, integration_fixture):
        """Test network scanning and data storage."""
        _config = ConfigManager(integration_fixture.config_path)
        persistence = PersistenceManager(config)
        persistence.initialize()

        with integration_fixture.managed_service(NetworkScanner, config) as scanner:
            # Test network scanning
            scanner.start()
            time.sleep(2)  # Allow scanning

            # Verify scanned data was stored
            networks = persistence.get_networks()
            assert len(networks) > 0

            # Verify network data structure
            for network in networks:
                assert "ssid" in network
                assert "bssid" in network
                assert "signal_strength" in network

    def test_analysis_engine_integration(self, integration_fixture):
        """Test analysis engine with real data."""
        _config = ConfigManager(integration_fixture.config_path)
        persistence = PersistenceManager(config)
        persistence.initialize()

        # Insert test data
        test_networks = [
            {
                "ssid": "TestNetwork1",
                "bssid": "00:11:22:33:44:55",
                "signal_strength": -45,
                "frequency": 2412,
                "timestamp": int(time.time()),
            },
            {
                "ssid": "TestNetwork2",
                "bssid": "00:11:22:33:44:66",
                "signal_strength": -65,
                "frequency": 2437,
                "timestamp": int(time.time()),
            },
        ]

        for network in test_networks:
            persistence.store_network(network)

        # Test analysis engine
        with integration_fixture.managed_service(AnalysisEngine, config) as engine:
            # Test network analysis
            analysis = engine.analyze_networks()
            assert "network_count" in analysis
            assert "signal_distribution" in analysis
            assert analysis["network_count"] >= 2

            # Test location analysis
            location_analysis = engine.analyze_locations()
            assert "coverage_area" in location_analysis

    def test_webui_integration(self, integration_fixture):
        """Test WebUI server integration."""
        _config = ConfigManager(integration_fixture.config_path)

        with integration_fixture.managed_service(WebUIServer, config) as server:
            # Start server
            server.start()
            port = server.get_port()

            # Test server is responding
            response = requests.get(f"http://127.0.0.1:{port}/")
            assert response.status_code == 200

            # Test API endpoints
            api_response = requests.get(f"http://127.0.0.1:{port}/api/status")
            assert api_response.status_code == 200

            status_data = api_response.json()
            assert "uptime" in status_data
            assert "version" in status_data

    def test_data_aggregation_integration(self, integration_fixture):
        """Test data aggregation service integration."""
        _config = ConfigManager(integration_fixture.config_path)
        persistence = PersistenceManager(config)
        persistence.initialize()

        # Insert test data over time
        base_time = int(time.time()) - 3600  # 1 hour ago
        for i in range(10):
            network_data = {
                "ssid": f"TestNetwork{i}",
                "bssid": f"00:11:22:33:44:{i:02d}",
                "signal_strength": -45 - i,
                "frequency": 2412 + i,
                "timestamp": base_time + (i * 360),  # 6 minute intervals
            }
            persistence.store_network(network_data)

        # Test aggregation service
        with integration_fixture.managed_service(
            AggregationService, config
        ) as aggregator:
            # Test hourly aggregation
            hourly_data = aggregator.aggregate_hourly()
            assert len(hourly_data) > 0

            # Test daily aggregation
            daily_data = aggregator.aggregate_daily()
            assert len(daily_data) > 0

            # Verify aggregated data structure
            for data_point in hourly_data:
                assert "timestamp" in data_point
                assert "network_count" in data_point
                assert "avg_signal_strength" in data_point


class TestAsyncIntegration:
    """Test asynchronous component integration."""

    @pytest.mark.asyncio
    async def test_async_service_coordination(self, integration_fixture):
        """Test coordination between async services."""
        _config = ConfigManager(integration_fixture.config_path)

        # Test async service startup
        _tasks = []

        # Mock async GPS service
        async def mock_gps_service():
            for _ in range(5):
                await asyncio.sleep(0.1)
                yield {
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                    "timestamp": int(time.time()),
                }

        # Mock async network scanner
        async def mock_network_scanner():
            for _ in range(3):
                await asyncio.sleep(0.2)
                yield {
                    "ssid": "AsyncNetwork",
                    "bssid": "00:11:22:33:44:77",
                    "signal_strength": -50,
                    "timestamp": int(time.time()),
                }

        # Collect data from both services
        gps_data = []
        network_data = []

        async for data in mock_gps_service():
            gps_data.append(data)

        async for data in mock_network_scanner():
            network_data.append(data)

        # Verify data collection
        assert len(gps_data) == 5
        assert len(network_data) == 3

        # Verify data coordination
        assert all("timestamp" in point for point in gps_data)
        assert all("timestamp" in point for point in network_data)

    @pytest.mark.asyncio
    async def test_async_data_processing_pipeline(self, integration_fixture):
        """Test async data processing pipeline."""
        _config = ConfigManager(integration_fixture.config_path)

        # Mock async data pipeline
        async def data_generator():
            for i in range(10):
                await asyncio.sleep(0.05)
                yield {"id": i, "data": f"test_data_{i}", "timestamp": int(time.time())}

        async def data_processor(data):
            await asyncio.sleep(0.01)  # Simulate processing
            return {**data, "processed": True, "processed_at": int(time.time())}

        async def data_sink(data):
            await asyncio.sleep(0.01)  # Simulate storage
            return True

        # Test pipeline
        processed_count = 0
        stored_count = 0

        async for raw_data in data_generator():
            processed_data = await data_processor(raw_data)
            processed_count += 1

            stored = await data_sink(processed_data)
            if stored:
                stored_count += 1

        assert processed_count == 10
        assert stored_count == 10


class TestErrorHandlingIntegration:
    """Test error handling across components."""

    def test_database_connection_failure_handling(self, integration_fixture):
        """Test handling of database connection failures."""
        _config = ConfigManager(integration_fixture.config_path)

        # Test with invalid database path
        invalid_config = json.loads(open(integration_fixture.config_path).read())
        invalid_config["database"]["path"] = "/invalid/path/database.db"

        invalid_config_path = os.path.join(
            integration_fixture.test_dir, "invalid_db_config.json"
        )
        with open(invalid_config_path, "w") as f:
            json.dump(invalid_config, f)

        invalid_config_manager = ConfigManager(invalid_config_path)

        # Should handle gracefully
        with pytest.raises(Exception):
            persistence = PersistenceManager(invalid_config_manager)
            persistence.initialize()

    def test_service_recovery_after_failure(self, integration_fixture):
        """Test service recovery after component failure."""
        _config = ConfigManager(integration_fixture.config_path)

        # Test service with failing component
        service = PiWardriveService(config)

        # Mock component failure
        with patch.object(service, "_handle_component_failure") as mock_handler:
            # Simulate component failure
            service._simulate_component_failure("network_scanner")

            # Verify recovery was attempted
            mock_handler.assert_called_once()

    def test_concurrent_access_handling(self, integration_fixture):
        """Test handling of concurrent database access."""
        _config = ConfigManager(integration_fixture.config_path)
        persistence = PersistenceManager(config)
        persistence.initialize()

        # Test concurrent writes
        def write_worker(worker_id):
            for i in range(5):
                network_data = {
                    "ssid": f"ConcurrentNetwork{worker_id}_{i}",
                    "bssid": f"00:11:22:33:{worker_id:02d}:{i:02d}",
                    "signal_strength": -50 - i,
                    "frequency": 2412 + i,
                    "timestamp": int(time.time()),
                }
                persistence.store_network(network_data)

        # Start multiple workers
        workers = []
        for worker_id in range(3):
            worker = threading.Thread(target=write_worker, args=(worker_id,))
            workers.append(worker)
            worker.start()

        # Wait for all workers
        for worker in workers:
            worker.join()

        # Verify all data was stored
        networks = persistence.get_networks()
        assert len(networks) >= 15  # 3 workers * 5 networks each


class TestPerformanceIntegration:
    """Test performance characteristics of integrated components."""

    def test_high_volume_data_processing(self, integration_fixture):
        """Test processing of high-volume data."""
        _config = ConfigManager(integration_fixture.config_path)
        persistence = PersistenceManager(config)
        persistence.initialize()

        # Generate large dataset
        start_time = time.time()

        for i in range(1000):
            network_data = {
                "ssid": f"PerfTestNetwork{i}",
                "bssid": f"00:11:22:33:{i//256:02d}:{i%256:02d}",
                "signal_strength": -45 - (i % 40),
                "frequency": 2412 + (i % 13),
                "timestamp": int(time.time()) + i,
            }
            persistence.store_network(network_data)

        processing_time = time.time() - start_time

        # Performance assertions
        assert processing_time < 30  # Should complete in under 30 seconds
        assert persistence.get_network_count() >= 1000

    def test_memory_usage_under_load(self, integration_fixture):
        """Test memory usage under continuous load."""
        import os

        import psutil

        _config = ConfigManager(integration_fixture.config_path)

        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Simulate continuous operation
        service = PiWardriveService(config)
        service.start()

        # Run for a short period
        time.sleep(5)

        # Check memory usage
        current_memory = process.memory_info().rss
        memory_increase = current_memory - initial_memory

        service.stop()

        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100 * 1024 * 1024  # 100MB

    def test_concurrent_user_simulation(self, integration_fixture):
        """Test system under concurrent user load."""
        _config = ConfigManager(integration_fixture.config_path)

        with integration_fixture.managed_service(WebUIServer, config) as server:
            server.start()
            port = server.get_port()

            # Simulate concurrent users
            def simulate_user(user_id):
                for _ in range(10):
                    try:
                        response = requests.get(f"http://127.0.0.1:{port}/api/status")
                        assert response.status_code == 200
                        time.sleep(0.1)
                    except Exception as e:
                        print(f"User {user_id} request failed: {e}")

            # Start multiple user simulations
            user_threads = []
            for user_id in range(5):
                thread = threading.Thread(target=simulate_user, args=(user_id,))
                user_threads.append(thread)
                thread.start()

            # Wait for all users
            for thread in user_threads:
                thread.join()

            # Server should still be responsive
            response = requests.get(f"http://127.0.0.1:{port}/api/status")
            assert response.status_code == 200


# Test utilities
def create_test_data(persistence, count=100):
    """Create test data for integration tests."""
    for i in range(count):
        network_data = {
            "ssid": f"TestNetwork{i}",
            "bssid": f"00:11:22:33:{i//256:02d}:{i%256:02d}",
            "signal_strength": -45 - (i % 40),
            "frequency": 2412 + (i % 13),
            "timestamp": int(time.time()) + i,
        }
        persistence.store_network(network_data)


def verify_data_integrity(persistence, expected_count):
    """Verify data integrity after operations."""
    networks = persistence.get_networks()
    assert len(networks) == expected_count

    # Verify no duplicate BSSIDs
    bssids = [network["bssid"] for network in networks]
    assert len(bssids) == len(set(bssids))

    # Verify data completeness
    for network in networks:
        assert all(
            key in network
            for key in ["ssid", "bssid", "signal_strength", "frequency", "timestamp"]
        )


if __name__ == "__main__":
    pytest.main([__file__])
