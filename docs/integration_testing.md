# Integration Testing Guide

This guide covers comprehensive integration testing strategies for PiWardrive, including external service testing, database integration, and end-to-end testing scenarios.

## Overview

Integration testing in PiWardrive verifies that different components work together correctly:
- **Database Integration**: Testing database operations and schema evolution
- **External Service Integration**: Testing integrations with third-party APIs and services
- **Hardware Integration**: Testing hardware interfaces and sensor data
- **API Integration**: Testing REST API endpoints and WebSocket connections
- **Performance Integration**: Testing system performance under realistic conditions

## Test Environment Setup

### Docker-Based Test Environment

The test environment uses Docker containers to simulate production conditions:

```bash
# scripts/start_test_env.sh
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR}/.."

cd "$REPO_ROOT"

# Start test environment
docker-compose -f docker-compose.test.yml up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Verify services are running
docker-compose -f docker-compose.test.yml ps
```

### Test Configuration

Create a dedicated test configuration:

```python
# tests/config/test_config.py
import os
import tempfile
from pathlib import Path

class TestConfig:
    """Test configuration settings."""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test.db")
        self.log_level = "DEBUG"
        self.api_base_url = "http://localhost:8000"
        self.test_data_dir = Path(__file__).parent / "test_data"
        
    def cleanup(self):
        """Clean up test resources."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

# Global test configuration
TEST_CONFIG = TestConfig()
```

## Database Integration Testing

### Database Setup and Teardown

```python
# tests/integration/test_database_integration.py
import pytest
import asyncio
import aiosqlite
from piwardrive.core import persistence
from piwardrive.db.migrations import MigrationRunner

class TestDatabaseIntegration:
    """Test database integration scenarios."""
    
    @pytest.fixture(autouse=True)
    async def setup_database(self):
        """Set up test database."""
        self.db_path = TEST_CONFIG.db_path
        
        # Initialize database
        await persistence.init_database(self.db_path)
        
        # Apply migrations
        runner = MigrationRunner(self.db_path)
        await runner.apply_migrations()
        
        yield
        
        # Cleanup
        os.unlink(self.db_path)
    
    async def test_health_record_flow(self):
        """Test complete health record flow."""
        # Create health record
        record = persistence.HealthRecord(
            timestamp="2023-01-01T00:00:00Z",
            cpu_temp=45.0,
            cpu_percent=25.0,
            memory_percent=60.0,
            disk_percent=40.0
        )
        
        # Save record
        await persistence.save_health_record(record)
        
        # Retrieve record
        records = await persistence.load_recent_health(limit=1)
        
        assert len(records) == 1
        assert records[0].timestamp == record.timestamp
        assert records[0].cpu_temp == record.cpu_temp
    
    async def test_wifi_network_integration(self):
        """Test WiFi network data integration."""
        # Create network data
        networks = [
            {
                'bssid': '00:11:22:33:44:55',
                'ssid': 'TestNetwork1',
                'frequency': 2437,
                'signal_strength': -45,
                'encryption': 'WPA2',
                'last_seen': '2023-01-01T00:00:00Z'
            },
            {
                'bssid': 'AA:BB:CC:DD:EE:FF',
                'ssid': 'TestNetwork2',
                'frequency': 5180,
                'signal_strength': -55,
                'encryption': 'WPA3',
                'last_seen': '2023-01-01T00:01:00Z'
            }
        ]
        
        # Save networks
        await persistence.save_wifi_networks(networks)
        
        # Query networks
        saved_networks = await persistence.get_wifi_networks(limit=10)
        
        assert len(saved_networks) == 2
        assert saved_networks[0]['bssid'] == networks[0]['bssid']
        assert saved_networks[1]['bssid'] == networks[1]['bssid']
    
    async def test_database_migration_integration(self):
        """Test database migration integration."""
        # Get initial schema version
        runner = MigrationRunner(self.db_path)
        initial_version = await runner.get_current_version()
        
        # Apply a test migration
        class TestMigration:
            version = initial_version + 1
            description = "Test migration"
            
            def up(self, cursor):
                return ["ALTER TABLE wifi_networks ADD COLUMN test_column TEXT"]
            
            def down(self, cursor):
                return ["ALTER TABLE wifi_networks DROP COLUMN test_column"]
            
            def validate(self, cursor):
                cursor.execute("PRAGMA table_info(wifi_networks)")
                columns = [row[1] for row in cursor.fetchall()]
                return "test_column" in columns
        
        # Apply migration
        await runner.apply_migration(TestMigration())
        
        # Verify migration applied
        new_version = await runner.get_current_version()
        assert new_version == initial_version + 1
        
        # Verify column exists
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute("PRAGMA table_info(wifi_networks)")
            columns = [row[1] for row in cursor.fetchall()]
            assert "test_column" in columns
```

### Database Performance Integration

```python
class TestDatabasePerformance:
    """Test database performance under realistic conditions."""
    
    async def test_bulk_insert_performance(self):
        """Test bulk insert performance."""
        import time
        
        # Generate test data
        test_networks = []
        for i in range(10000):
            test_networks.append({
                'bssid': f"00:11:22:33:44:{i:02x}",
                'ssid': f"Network_{i}",
                'frequency': 2437 + (i % 100),
                'signal_strength': -30 - (i % 70),
                'encryption': 'WPA2',
                'last_seen': f"2023-01-01T{i%24:02d}:00:00Z"
            })
        
        # Measure insert time
        start_time = time.perf_counter()
        await persistence.save_wifi_networks(test_networks)
        end_time = time.perf_counter()
        
        insert_time = end_time - start_time
        rate = len(test_networks) / insert_time
        
        # Assert performance meets requirements
        assert rate > 1000  # At least 1000 records per second
        assert insert_time < 10  # Less than 10 seconds total
    
    async def test_query_performance(self):
        """Test query performance with realistic data."""
        # Insert test data
        await self.insert_test_data()
        
        # Test various query patterns
        queries = [
            "SELECT * FROM wifi_networks WHERE signal_strength > -50",
            "SELECT bssid, ssid, signal_strength FROM wifi_networks ORDER BY last_seen DESC LIMIT 100",
            "SELECT COUNT(*) FROM wifi_networks WHERE encryption = 'WPA2'",
            "SELECT * FROM wifi_networks WHERE gps_lat BETWEEN 40.0 AND 41.0 AND gps_lon BETWEEN -74.0 AND -73.0"
        ]
        
        for query in queries:
            start_time = time.perf_counter()
            
            async with aiosqlite.connect(self.db_path) as conn:
                cursor = await conn.execute(query)
                results = await cursor.fetchall()
            
            end_time = time.perf_counter()
            query_time = end_time - start_time
            
            # Assert query performance
            assert query_time < 1.0  # Less than 1 second
            assert len(results) >= 0  # Valid results
```

## External Service Integration Testing

### Mock External Services

```python
# tests/integration/test_external_services.py
import pytest
import aiohttp
from aioresponses import aioresponses
from piwardrive.integrations import wigle_api, weather_api

class TestExternalServiceIntegration:
    """Test external service integrations."""
    
    @pytest.fixture
    def mock_wigle_api(self):
        """Mock WiGLE API responses."""
        with aioresponses() as m:
            m.get(
                'https://api.wigle.net/api/v2/network/search',
                payload={
                    'success': True,
                    'results': [
                        {
                            'netid': '00:11:22:33:44:55',
                            'ssid': 'TestNetwork',
                            'trilat': 40.7128,
                            'trilong': -74.0060,
                            'encryption': 'WPA2'
                        }
                    ]
                }
            )
            yield m
    
    async def test_wigle_integration(self, mock_wigle_api):
        """Test WiGLE API integration."""
        # Configure API credentials
        api_key = "test_api_key"
        api_name = "test_user"
        
        # Test API call
        results = await wigle_api.search_networks(
            api_key=api_key,
            api_name=api_name,
            lat=40.7128,
            lon=-74.0060,
            radius=1000
        )
        
        assert len(results) == 1
        assert results[0]['netid'] == '00:11:22:33:44:55'
        assert results[0]['ssid'] == 'TestNetwork'
    
    async def test_weather_integration(self):
        """Test weather API integration."""
        with aioresponses() as m:
            m.get(
                'https://api.openweathermap.org/data/2.5/weather',
                payload={
                    'main': {
                        'temp': 22.5,
                        'humidity': 65,
                        'pressure': 1013
                    },
                    'weather': [
                        {
                            'main': 'Clear',
                            'description': 'clear sky'
                        }
                    ]
                }
            )
            
            weather_data = await weather_api.get_weather(
                lat=40.7128,
                lon=-74.0060,
                api_key="test_key"
            )
            
            assert weather_data['main']['temp'] == 22.5
            assert weather_data['weather'][0]['main'] == 'Clear'
```

### Real External Service Testing

```python
class TestRealExternalServices:
    """Test real external service integrations (with rate limiting)."""
    
    @pytest.mark.integration
    @pytest.mark.slow
    async def test_real_wigle_api(self):
        """Test real WiGLE API (requires valid credentials)."""
        # Skip if credentials not provided
        api_key = os.getenv('WIGLE_API_KEY')
        api_name = os.getenv('WIGLE_API_NAME')
        
        if not api_key or not api_name:
            pytest.skip("WiGLE API credentials not provided")
        
        # Test with rate limiting
        async with aiohttp.ClientSession() as session:
            # Add rate limiting
            await asyncio.sleep(1)  # Respect API rate limits
            
            results = await wigle_api.search_networks(
                api_key=api_key,
                api_name=api_name,
                lat=40.7128,
                lon=-74.0060,
                radius=1000,
                session=session
            )
            
            assert isinstance(results, list)
            # Don't assert specific results since they may vary
    
    @pytest.mark.integration
    async def test_gps_service_integration(self):
        """Test GPS service integration."""
        # Test with mock GPS data
        from unittest.mock import patch
        
        with patch('piwardrive.gps.get_position') as mock_gps:
            mock_gps.return_value = (40.7128, -74.0060, 5.0)  # lat, lon, accuracy
            
            position = await gps_service.get_current_position()
            
            assert position['lat'] == 40.7128
            assert position['lon'] == -74.0060
            assert position['accuracy'] == 5.0
```

## API Integration Testing

### REST API Testing

```python
# tests/integration/test_api_integration.py
import pytest
import httpx
from fastapi.testclient import TestClient
from piwardrive.service import app

class TestAPIIntegration:
    """Test REST API integration."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    @pytest.fixture
    def authenticated_client(self, client):
        """Create authenticated test client."""
        # Login and get token
        response = client.post(
            "/auth/login",
            data={"username": "admin", "password": "password"}
        )
        assert response.status_code == 200
        token = response.json()["access_token"]
        
        # Add authorization header
        client.headers.update({"Authorization": f"Bearer {token}"})
        return client
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_wifi_networks_endpoint(self, authenticated_client):
        """Test WiFi networks endpoint."""
        # Add test data
        self.add_test_wifi_networks()
        
        # Test endpoint
        response = authenticated_client.get("/api/wifi/networks")
        assert response.status_code == 200
        
        data = response.json()
        assert "networks" in data
        assert len(data["networks"]) > 0
    
    def test_bluetooth_devices_endpoint(self, authenticated_client):
        """Test Bluetooth devices endpoint."""
        # Add test data
        self.add_test_bluetooth_devices()
        
        # Test endpoint
        response = authenticated_client.get("/api/bluetooth/devices")
        assert response.status_code == 200
        
        data = response.json()
        assert "devices" in data
        assert len(data["devices"]) > 0
    
    def test_configuration_endpoint(self, authenticated_client):
        """Test configuration endpoint."""
        # Get current configuration
        response = authenticated_client.get("/api/config")
        assert response.status_code == 200
        
        config = response.json()
        original_value = config.get("scan_interval", 60)
        
        # Update configuration
        new_value = original_value + 10
        response = authenticated_client.put(
            "/api/config",
            json={"scan_interval": new_value}
        )
        assert response.status_code == 200
        
        # Verify update
        response = authenticated_client.get("/api/config")
        assert response.status_code == 200
        assert response.json()["scan_interval"] == new_value
    
    def add_test_wifi_networks(self):
        """Add test WiFi networks."""
        # Implementation depends on your data layer
        pass
    
    def add_test_bluetooth_devices(self):
        """Add test Bluetooth devices."""
        # Implementation depends on your data layer
        pass
```

### WebSocket Integration Testing

```python
class TestWebSocketIntegration:
    """Test WebSocket integration."""
    
    def test_websocket_connection(self, client):
        """Test WebSocket connection."""
        with client.websocket_connect("/ws/status") as websocket:
            # Send test message
            websocket.send_json({"type": "ping"})
            
            # Receive response
            data = websocket.receive_json()
            assert data["type"] == "pong"
    
    def test_websocket_data_stream(self, client):
        """Test WebSocket data streaming."""
        with client.websocket_connect("/ws/data") as websocket:
            # Receive initial data
            data = websocket.receive_json()
            
            assert "timestamp" in data
            assert "data" in data
            
            # Verify data structure
            assert isinstance(data["data"], dict)
    
    def test_websocket_reconnection(self, client):
        """Test WebSocket reconnection handling."""
        # Test connection drop and reconnection
        with client.websocket_connect("/ws/status") as websocket:
            # Send message
            websocket.send_json({"type": "ping"})
            
            # Simulate connection drop
            websocket.close()
            
            # Reconnect
            with client.websocket_connect("/ws/status") as new_websocket:
                new_websocket.send_json({"type": "ping"})
                response = new_websocket.receive_json()
                assert response["type"] == "pong"
```

## Hardware Integration Testing

### Sensor Integration Testing

```python
# tests/integration/test_hardware_integration.py
import pytest
from unittest.mock import patch, MagicMock
from piwardrive.hardware import sensors, gps, bluetooth

class TestHardwareIntegration:
    """Test hardware integration."""
    
    @pytest.mark.hardware
    def test_gps_integration(self):
        """Test GPS integration."""
        with patch('piwardrive.hardware.gps.GPSClient') as mock_gps:
            # Mock GPS client
            mock_instance = MagicMock()
            mock_instance.get_position.return_value = (40.7128, -74.0060, 5.0)
            mock_gps.return_value = mock_instance
            
            # Test GPS functionality
            position = gps.get_current_position()
            
            assert position[0] == 40.7128  # latitude
            assert position[1] == -74.0060  # longitude
            assert position[2] == 5.0       # accuracy
    
    @pytest.mark.hardware
    def test_bluetooth_scanning(self):
        """Test Bluetooth scanning integration."""
        with patch('piwardrive.hardware.bluetooth.BluetoothScanner') as mock_scanner:
            # Mock scanner
            mock_instance = MagicMock()
            mock_instance.scan.return_value = [
                {
                    'address': '00:11:22:33:44:55',
                    'name': 'Test Device',
                    'rssi': -45,
                    'device_type': 'smartphone'
                }
            ]
            mock_scanner.return_value = mock_instance
            
            # Test scanning
            scanner = bluetooth.BluetoothScanner()
            devices = scanner.scan(timeout=10)
            
            assert len(devices) == 1
            assert devices[0]['address'] == '00:11:22:33:44:55'
            assert devices[0]['name'] == 'Test Device'
    
    @pytest.mark.hardware
    def test_sensor_data_collection(self):
        """Test sensor data collection."""
        with patch('piwardrive.hardware.sensors.get_cpu_temperature') as mock_temp:
            with patch('piwardrive.hardware.sensors.get_cpu_usage') as mock_cpu:
                # Mock sensor readings
                mock_temp.return_value = 45.5
                mock_cpu.return_value = 25.0
                
                # Test sensor data collection
                sensor_data = sensors.collect_sensor_data()
                
                assert sensor_data['cpu_temperature'] == 45.5
                assert sensor_data['cpu_usage'] == 25.0
                assert 'timestamp' in sensor_data
```

### Hardware Simulation

```python
class HardwareSimulator:
    """Simulate hardware for testing."""
    
    def __init__(self):
        self.gps_position = (40.7128, -74.0060, 5.0)
        self.bluetooth_devices = []
        self.wifi_networks = []
    
    def simulate_gps_movement(self, start_pos, end_pos, steps=10):
        """Simulate GPS movement."""
        lat_step = (end_pos[0] - start_pos[0]) / steps
        lon_step = (end_pos[1] - start_pos[1]) / steps
        
        positions = []
        for i in range(steps + 1):
            lat = start_pos[0] + (lat_step * i)
            lon = start_pos[1] + (lon_step * i)
            positions.append((lat, lon, 5.0))
        
        return positions
    
    def simulate_wifi_scan(self, count=10):
        """Simulate WiFi scan results."""
        import random
        
        networks = []
        for i in range(count):
            networks.append({
                'bssid': f"00:11:22:33:{i:02x}:{random.randint(0, 255):02x}",
                'ssid': f"Network_{i}",
                'frequency': random.choice([2437, 2462, 5180, 5200]),
                'signal_strength': random.randint(-80, -30),
                'encryption': random.choice(['WPA2', 'WPA3', 'WEP', 'Open'])
            })
        
        return networks
    
    def simulate_bluetooth_scan(self, count=5):
        """Simulate Bluetooth scan results."""
        import random
        
        devices = []
        device_types = ['smartphone', 'laptop', 'tablet', 'smartwatch', 'headphones']
        
        for i in range(count):
            devices.append({
                'address': f"AA:BB:CC:DD:{i:02x}:{random.randint(0, 255):02x}",
                'name': f"Device_{i}",
                'rssi': random.randint(-80, -30),
                'device_type': random.choice(device_types)
            })
        
        return devices
```

## End-to-End Testing

### Complete Workflow Testing

```python
class TestEndToEndWorkflows:
    """Test complete end-to-end workflows."""
    
    @pytest.mark.e2e
    async def test_complete_scan_workflow(self):
        """Test complete scanning workflow."""
        # Setup
        simulator = HardwareSimulator()
        
        # Simulate scan process
        with patch('piwardrive.hardware.wifi.scan') as mock_wifi:
            with patch('piwardrive.hardware.bluetooth.scan') as mock_bt:
                with patch('piwardrive.hardware.gps.get_position') as mock_gps:
                    # Mock hardware responses
                    mock_wifi.return_value = simulator.simulate_wifi_scan(20)
                    mock_bt.return_value = simulator.simulate_bluetooth_scan(10)
                    mock_gps.return_value = (40.7128, -74.0060, 5.0)
                    
                    # Run scan workflow
                    from piwardrive.workflows import scan_workflow
                    results = await scan_workflow.run_complete_scan()
                    
                    # Verify results
                    assert 'wifi_networks' in results
                    assert 'bluetooth_devices' in results
                    assert 'gps_position' in results
                    
                    assert len(results['wifi_networks']) == 20
                    assert len(results['bluetooth_devices']) == 10
                    assert results['gps_position'] == (40.7128, -74.0060, 5.0)
    
    @pytest.mark.e2e
    async def test_data_persistence_workflow(self):
        """Test data persistence workflow."""
        # Generate test data
        test_data = {
            'wifi_networks': [
                {
                    'bssid': '00:11:22:33:44:55',
                    'ssid': 'TestNetwork',
                    'frequency': 2437,
                    'signal_strength': -45,
                    'encryption': 'WPA2',
                    'timestamp': '2023-01-01T00:00:00Z'
                }
            ],
            'bluetooth_devices': [
                {
                    'address': 'AA:BB:CC:DD:EE:FF',
                    'name': 'TestDevice',
                    'rssi': -50,
                    'device_type': 'smartphone',
                    'timestamp': '2023-01-01T00:00:00Z'
                }
            ],
            'gps_position': (40.7128, -74.0060, 5.0)
        }
        
        # Save data
        await persistence.save_scan_results(test_data)
        
        # Verify data saved
        wifi_networks = await persistence.get_wifi_networks(limit=10)
        bluetooth_devices = await persistence.get_bluetooth_devices(limit=10)
        
        assert len(wifi_networks) == 1
        assert len(bluetooth_devices) == 1
        assert wifi_networks[0]['bssid'] == '00:11:22:33:44:55'
        assert bluetooth_devices[0]['address'] == 'AA:BB:CC:DD:EE:FF'
    
    @pytest.mark.e2e
    async def test_api_data_flow(self):
        """Test complete API data flow."""
        # Setup test client
        client = TestClient(app)
        
        # Add test data
        await self.add_test_scan_data()
        
        # Test API endpoints
        response = client.get("/api/wifi/networks")
        assert response.status_code == 200
        wifi_data = response.json()
        
        response = client.get("/api/bluetooth/devices")
        assert response.status_code == 200
        bluetooth_data = response.json()
        
        response = client.get("/api/status")
        assert response.status_code == 200
        status_data = response.json()
        
        # Verify data flow
        assert len(wifi_data['networks']) > 0
        assert len(bluetooth_data['devices']) > 0
        assert status_data['status'] == 'active'
```

## Performance Integration Testing

### Load Testing Integration

```python
class TestPerformanceIntegration:
    """Test performance under realistic conditions."""
    
    @pytest.mark.performance
    async def test_concurrent_api_requests(self):
        """Test API performance under concurrent load."""
        import asyncio
        import aiohttp
        
        async def make_request(session, url):
            async with session.get(url) as response:
                return await response.json()
        
        # Test concurrent requests
        async with aiohttp.ClientSession() as session:
            tasks = []
            
            # Create concurrent requests
            for _ in range(100):
                tasks.append(make_request(session, f"{TEST_CONFIG.api_base_url}/api/wifi/networks"))
            
            # Execute requests
            start_time = time.perf_counter()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            end_time = time.perf_counter()
            
            # Verify performance
            total_time = end_time - start_time
            success_count = sum(1 for r in results if not isinstance(r, Exception))
            
            assert success_count >= 90  # At least 90% success rate
            assert total_time < 10      # Complete within 10 seconds
    
    @pytest.mark.performance
    async def test_database_performance_integration(self):
        """Test database performance with realistic workload."""
        # Generate realistic test data
        import random
        
        # Create large dataset
        wifi_networks = []
        for i in range(50000):
            wifi_networks.append({
                'bssid': f"00:11:22:{i//256:02x}:{i%256:02x}:{random.randint(0, 255):02x}",
                'ssid': f"Network_{i}",
                'frequency': random.choice([2437, 2462, 5180, 5200]),
                'signal_strength': random.randint(-80, -30),
                'encryption': random.choice(['WPA2', 'WPA3', 'WEP', 'Open']),
                'timestamp': f"2023-01-01T{i%24:02d}:{i%60:02d}:{i%60:02d}Z"
            })
        
        # Test bulk insert performance
        start_time = time.perf_counter()
        await persistence.save_wifi_networks(wifi_networks)
        insert_time = time.perf_counter() - start_time
        
        # Test query performance
        start_time = time.perf_counter()
        results = await persistence.get_wifi_networks(limit=1000)
        query_time = time.perf_counter() - start_time
        
        # Verify performance requirements
        assert insert_time < 30  # Insert 50k records in under 30 seconds
        assert query_time < 1    # Query 1k records in under 1 second
        assert len(results) == 1000
```

## Test Data Management

### Test Data Fixtures

```python
# tests/fixtures/test_data.py
import json
from pathlib import Path

class TestDataManager:
    """Manage test data for integration tests."""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent / "data"
        self.data_dir.mkdir(exist_ok=True)
    
    def load_wifi_networks(self, dataset="default"):
        """Load WiFi network test data."""
        file_path = self.data_dir / f"wifi_networks_{dataset}.json"
        
        if not file_path.exists():
            # Generate default data
            return self.generate_wifi_networks()
        
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def load_bluetooth_devices(self, dataset="default"):
        """Load Bluetooth device test data."""
        file_path = self.data_dir / f"bluetooth_devices_{dataset}.json"
        
        if not file_path.exists():
            return self.generate_bluetooth_devices()
        
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def generate_wifi_networks(self, count=100):
        """Generate realistic WiFi network data."""
        import random
        
        networks = []
        ssid_patterns = ["Home", "Guest", "Office", "Cafe", "Hotel"]
        
        for i in range(count):
            networks.append({
                'bssid': f"00:11:22:{i//256:02x}:{i%256:02x}:{random.randint(0, 255):02x}",
                'ssid': f"{random.choice(ssid_patterns)}_{i}",
                'frequency': random.choice([2437, 2462, 5180, 5200]),
                'signal_strength': random.randint(-80, -30),
                'encryption': random.choice(['WPA2', 'WPA3', 'WEP', 'Open']),
                'channel': random.choice([1, 6, 11, 36, 40, 44, 48]),
                'vendor': random.choice(['Cisco', 'Netgear', 'Linksys', 'TP-Link']),
                'timestamp': f"2023-01-01T{i%24:02d}:{i%60:02d}:{i%60:02d}Z"
            })
        
        return networks
    
    def generate_bluetooth_devices(self, count=50):
        """Generate realistic Bluetooth device data."""
        import random
        
        devices = []
        device_names = ["iPhone", "Samsung", "MacBook", "AirPods", "Watch"]
        device_types = ["smartphone", "laptop", "tablet", "smartwatch", "headphones"]
        
        for i in range(count):
            devices.append({
                'address': f"AA:BB:CC:{i//256:02x}:{i%256:02x}:{random.randint(0, 255):02x}",
                'name': f"{random.choice(device_names)}_{i}",
                'rssi': random.randint(-80, -30),
                'device_type': random.choice(device_types),
                'manufacturer': random.choice(['Apple', 'Samsung', 'Google', 'Microsoft']),
                'timestamp': f"2023-01-01T{i%24:02d}:{i%60:02d}:{i%60:02d}Z"
            })
        
        return devices

# Global test data manager
TEST_DATA = TestDataManager()
```

## Test Automation and CI Integration

### GitHub Actions Integration

```yaml
# .github/workflows/integration-tests.yml
name: Integration Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  integration-tests:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
        pip install -e .
    
    - name: Start test services
      run: |
        docker-compose -f docker-compose.test.yml up -d
        sleep 30  # Wait for services to start
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ -v --tb=short
    
    - name: Run performance tests
      run: |
        pytest tests/integration/ -m performance -v --tb=short
    
    - name: Stop test services
      if: always()
      run: |
        docker-compose -f docker-compose.test.yml down
```

## Best Practices

### Integration Test Design

1. **Isolated Tests**: Each test should be independent and not rely on other tests
2. **Realistic Data**: Use realistic test data that matches production patterns
3. **Environment Consistency**: Ensure test environments match production
4. **Proper Cleanup**: Always clean up test data and resources
5. **Error Handling**: Test both success and failure scenarios

### Performance Testing

1. **Baseline Measurements**: Establish performance baselines
2. **Realistic Load**: Use realistic load patterns and data volumes
3. **Resource Monitoring**: Monitor CPU, memory, and I/O during tests
4. **Regression Testing**: Detect performance regressions early
5. **Scalability Testing**: Test system scalability limits

### External Service Testing

1. **Mock Services**: Use mocks for reliable and fast testing
2. **Contract Testing**: Verify API contracts with external services
3. **Rate Limiting**: Respect external service rate limits
4. **Fallback Testing**: Test fallback mechanisms when services are unavailable
5. **Authentication Testing**: Test authentication and authorization flows

## Troubleshooting Integration Tests

### Common Issues

1. **Test Data Conflicts**: Ensure proper test data isolation
2. **Service Dependencies**: Verify all required services are running
3. **Network Issues**: Check network connectivity and firewall rules
4. **Resource Limitations**: Monitor system resources during tests
5. **Timing Issues**: Add appropriate waits for asynchronous operations

### Debugging Strategies

1. **Detailed Logging**: Enable detailed logging for troubleshooting
2. **Test Isolation**: Run tests individually to identify issues
3. **Environment Verification**: Verify test environment setup
4. **Data Inspection**: Inspect test data and database state
5. **Service Health**: Check health of dependent services

For more information on testing strategies, see the [Testing Guide](testing_guide.md) and [Performance Testing](performance_testing.md) documentation.
