#!/usr/bin/env python3

"""
Comprehensive test suite for api_models.py module.
Tests all Pydantic models for API request/response validation.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import pytest
from pydantic import ValidationError

# Add source directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from piwardrive.models.api_models import (
    WiFiScanRequest,
    AccessPoint,
    WiFiScanResponse,
    BluetoothScanRequest,
    BluetoothDevice,
    BluetoothScanResponse,
    SystemStats,
    ErrorResponse,
    CellularScanRequest,
    CellTower,
    CellularScanResponse,
    BluetoothDetection,
    CellularDetection,
    NetworkFingerprint,
    SuspiciousActivity,
    NetworkAnalyticsRecord,
)


class TestWiFiModels:
    """Test Wi-Fi related API models."""

    def test_wifi_scan_request_defaults(self):
        """Test WiFiScanRequest with default values."""
        request = WiFiScanRequest()
        assert request.interface == "wlan0"
        assert request.timeout is None

    def test_wifi_scan_request_custom_values(self):
        """Test WiFiScanRequest with custom values."""
        request = WiFiScanRequest(interface="wlan1", timeout=30)
        assert request.interface == "wlan1"
        assert request.timeout == 30

    def test_wifi_scan_request_validation(self):
        """Test WiFiScanRequest validation."""
        # Should accept valid timeout
        request = WiFiScanRequest(timeout=10)
        assert request.timeout == 10
        
        # Should accept None timeout
        request = WiFiScanRequest(timeout=None)
        assert request.timeout is None

    def test_access_point_full_data(self):
        """Test AccessPoint with all fields populated."""
        ap_data = {
            "ssid": "TestNetwork",
            "bssid": "AA:BB:CC:DD:EE:FF",
            "frequency": "2.437",
            "channel": "6",
            "quality": "70/100",
            "encryption": "WPA2",
            "vendor": "RaspberryPi",
            "heading": 180.0,
        }
        
        ap = AccessPoint(**ap_data)
        assert ap.ssid == "TestNetwork"
        assert ap.bssid == "AA:BB:CC:DD:EE:FF"
        assert ap.frequency == "2.437"
        assert ap.channel == "6"
        assert ap.quality == "70/100"
        assert ap.encryption == "WPA2"
        assert ap.vendor == "RaspberryPi"
        assert ap.heading == 180.0

    def test_access_point_minimal_data(self):
        """Test AccessPoint with minimal required data."""
        ap = AccessPoint()
        assert ap.ssid is None
        assert ap.bssid is None
        assert ap.frequency is None
        assert ap.channel is None
        assert ap.quality is None
        assert ap.encryption is None
        assert ap.vendor is None
        assert ap.heading is None

    def test_access_point_partial_data(self):
        """Test AccessPoint with some fields populated."""
        ap = AccessPoint(ssid="TestNet", bssid="AA:BB:CC:DD:EE:FF", encryption="WPA2")
        assert ap.ssid == "TestNet"
        assert ap.bssid == "AA:BB:CC:DD:EE:FF"
        assert ap.encryption == "WPA2"
        assert ap.frequency is None

    def test_wifi_scan_response_empty(self):
        """Test WiFiScanResponse with no access points."""
        response = WiFiScanResponse()
        assert response.access_points == []

    def test_wifi_scan_response_with_aps(self):
        """Test WiFiScanResponse with access points."""
        ap1 = AccessPoint(ssid="Net1", bssid="AA:BB:CC:DD:EE:01")
        ap2 = AccessPoint(ssid="Net2", bssid="AA:BB:CC:DD:EE:02")
        
        response = WiFiScanResponse(access_points=[ap1, ap2])
        assert len(response.access_points) == 2
        assert response.access_points[0].ssid == "Net1"
        assert response.access_points[1].ssid == "Net2"


class TestBluetoothModels:
    """Test Bluetooth related API models."""

    def test_bluetooth_scan_request_defaults(self):
        """Test BluetoothScanRequest with default values."""
        request = BluetoothScanRequest()
        assert request.timeout is None

    def test_bluetooth_scan_request_custom_timeout(self):
        """Test BluetoothScanRequest with custom timeout."""
        request = BluetoothScanRequest(timeout=15)
        assert request.timeout == 15

    def test_bluetooth_device_required_fields(self):
        """Test BluetoothDevice with required fields."""
        device = BluetoothDevice(address="AA:BB:CC:DD:EE:FF")
        assert device.address == "AA:BB:CC:DD:EE:FF"
        assert device.name is None

    def test_bluetooth_device_with_name(self):
        """Test BluetoothDevice with name."""
        device = BluetoothDevice(address="AA:BB:CC:DD:EE:FF", name="My Phone")
        assert device.address == "AA:BB:CC:DD:EE:FF"
        assert device.name == "My Phone"

    def test_bluetooth_device_validation_missing_address(self):
        """Test BluetoothDevice validation fails without address."""
        with pytest.raises(ValidationError):
            BluetoothDevice()

    def test_bluetooth_scan_response_empty(self):
        """Test BluetoothScanResponse with no devices."""
        response = BluetoothScanResponse()
        assert response.devices == []

    def test_bluetooth_scan_response_with_devices(self):
        """Test BluetoothScanResponse with devices."""
        device1 = BluetoothDevice(address="AA:BB:CC:DD:EE:01", name="Device1")
        device2 = BluetoothDevice(address="AA:BB:CC:DD:EE:02")
        
        response = BluetoothScanResponse(devices=[device1, device2])
        assert len(response.devices) == 2
        assert response.devices[0].name == "Device1"
        assert response.devices[1].name is None


class TestCellularModels:
    """Test Cellular related API models."""

    def test_cellular_scan_request_defaults(self):
        """Test CellularScanRequest with default values."""
        request = CellularScanRequest()
        assert request.timeout is None

    def test_cellular_scan_request_custom_timeout(self):
        """Test CellularScanRequest with custom timeout."""
        request = CellularScanRequest(timeout=20)
        assert request.timeout == 20

    def test_cell_tower_required_fields(self):
        """Test CellTower with required fields."""
        tower = CellTower(tower_id="12345")
        assert tower.tower_id == "12345"
        assert tower.rssi is None
        assert tower.lat is None
        assert tower.lon is None

    def test_cell_tower_full_data(self):
        """Test CellTower with all fields."""
        tower = CellTower(
            tower_id="12345",
            rssi="-60",
            lat=51.5,
            lon=-0.1
        )
        assert tower.tower_id == "12345"
        assert tower.rssi == "-60"
        assert tower.lat == 51.5
        assert tower.lon == -0.1

    def test_cell_tower_validation_missing_id(self):
        """Test CellTower validation fails without tower_id."""
        with pytest.raises(ValidationError):
            CellTower()

    def test_cellular_scan_response_empty(self):
        """Test CellularScanResponse with no towers."""
        response = CellularScanResponse()
        assert response.towers == []

    def test_cellular_scan_response_with_towers(self):
        """Test CellularScanResponse with towers."""
        tower1 = CellTower(tower_id="123", rssi="-60")
        tower2 = CellTower(tower_id="456", rssi="-70")
        
        response = CellularScanResponse(towers=[tower1, tower2])
        assert len(response.towers) == 2
        assert response.towers[0].tower_id == "123"
        assert response.towers[1].tower_id == "456"


class TestSystemModels:
    """Test System related API models."""

    def test_system_stats_required_fields(self):
        """Test SystemStats with required fields."""
        stats = SystemStats(
            cpu_percent=15.5,
            memory_percent=45.2,
            disk_percent=70.1
        )
        assert stats.cpu_percent == 15.5
        assert stats.memory_percent == 45.2
        assert stats.disk_percent == 70.1
        assert stats.temp_celsius is None

    def test_system_stats_with_temperature(self):
        """Test SystemStats with temperature."""
        stats = SystemStats(
            cpu_percent=15.5,
            memory_percent=45.2,
            disk_percent=70.1,
            temp_celsius=52.3
        )
        assert stats.temp_celsius == 52.3

    def test_system_stats_validation_missing_required(self):
        """Test SystemStats validation fails without required fields."""
        with pytest.raises(ValidationError):
            SystemStats()
        
        with pytest.raises(ValidationError):
            SystemStats(cpu_percent=15.5)  # Missing other required fields

    def test_error_response_required_fields(self):
        """Test ErrorResponse with required fields."""
        error = ErrorResponse(code="404", message="Not found")
        assert error.code == "404"
        assert error.message == "Not found"

    def test_error_response_validation_missing_fields(self):
        """Test ErrorResponse validation fails without required fields."""
        with pytest.raises(ValidationError):
            ErrorResponse()
        
        with pytest.raises(ValidationError):
            ErrorResponse(code="404")  # Missing message


class TestDatabaseModels:
    """Test database record models."""

    def test_bluetooth_detection_required_fields(self):
        """Test BluetoothDetection with required fields."""
        detection = BluetoothDetection(
            scan_session_id="session123",
            detection_timestamp="2023-12-01T10:00:00Z",
            mac_address="AA:BB:CC:DD:EE:FF"
        )
        assert detection.scan_session_id == "session123"
        assert detection.detection_timestamp == "2023-12-01T10:00:00Z"
        assert detection.mac_address == "AA:BB:CC:DD:EE:FF"
        assert detection.id is None
        assert detection.device_name is None

    def test_bluetooth_detection_full_data(self):
        """Test BluetoothDetection with all fields."""
        detection = BluetoothDetection(
            id=1,
            scan_session_id="session123",
            detection_timestamp="2023-12-01T10:00:00Z",
            mac_address="AA:BB:CC:DD:EE:FF",
            device_name="Phone",
            rssi_dbm=-50,
            latitude=51.5,
            longitude=-0.1
        )
        assert detection.id == 1
        assert detection.device_name == "Phone"
        assert detection.rssi_dbm == -50
        assert detection.latitude == 51.5
        assert detection.longitude == -0.1

    def test_cellular_detection_required_fields(self):
        """Test CellularDetection with required fields."""
        detection = CellularDetection(
            scan_session_id="session123",
            detection_timestamp="2023-12-01T10:00:00Z"
        )
        assert detection.scan_session_id == "session123"
        assert detection.detection_timestamp == "2023-12-01T10:00:00Z"
        assert detection.id is None
        assert detection.cell_id is None

    def test_cellular_detection_full_data(self):
        """Test CellularDetection with all fields."""
        detection = CellularDetection(
            id=1,
            scan_session_id="session123",
            detection_timestamp="2023-12-01T10:00:00Z",
            cell_id=12345,
            lac=100,
            mcc=234,
            mnc=10,
            signal_strength_dbm=-80,
            latitude=51.5,
            longitude=-0.1
        )
        assert detection.id == 1
        assert detection.cell_id == 12345
        assert detection.lac == 100
        assert detection.mcc == 234
        assert detection.mnc == 10
        assert detection.signal_strength_dbm == -80

    def test_network_fingerprint_required_fields(self):
        """Test NetworkFingerprint with required fields."""
        fingerprint = NetworkFingerprint(
            bssid="AA:BB:CC:DD:EE:FF",
            fingerprint_hash="abc123def456"
        )
        assert fingerprint.bssid == "AA:BB:CC:DD:EE:FF"
        assert fingerprint.fingerprint_hash == "abc123def456"
        assert fingerprint.id is None
        assert fingerprint.classification is None

    def test_suspicious_activity_required_fields(self):
        """Test SuspiciousActivity with required fields."""
        activity = SuspiciousActivity(
            scan_session_id="session123",
            activity_type="rogue_ap",
            severity="high",
            detected_at="2023-12-01T10:00:00Z"
        )
        assert activity.scan_session_id == "session123"
        assert activity.activity_type == "rogue_ap"
        assert activity.severity == "high"
        assert activity.detected_at == "2023-12-01T10:00:00Z"

    def test_network_analytics_record_required_fields(self):
        """Test NetworkAnalyticsRecord with required fields."""
        record = NetworkAnalyticsRecord(
            bssid="AA:BB:CC:DD:EE:FF",
            analysis_date="2023-12-01"
        )
        assert record.bssid == "AA:BB:CC:DD:EE:FF"
        assert record.analysis_date == "2023-12-01"
        assert record.total_detections is None
        assert record.suspicious_score is None


class TestSerialization:
    """Test JSON serialization and deserialization of models."""

    def test_wifi_scan_response_json_serialization(self):
        """Test WiFiScanResponse JSON serialization."""
        ap = AccessPoint(ssid="TestNet", bssid="AA:BB:CC:DD:EE:FF")
        response = WiFiScanResponse(access_points=[ap])
        
        # Test serialization
        json_data = response.model_dump()
        assert "access_points" in json_data
        assert len(json_data["access_points"]) == 1
        assert json_data["access_points"][0]["ssid"] == "TestNet"
        
        # Test JSON string serialization
        json_str = response.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["access_points"][0]["ssid"] == "TestNet"

    def test_bluetooth_scan_response_json_serialization(self):
        """Test BluetoothScanResponse JSON serialization."""
        device = BluetoothDevice(address="AA:BB:CC:DD:EE:FF", name="Phone")
        response = BluetoothScanResponse(devices=[device])
        
        json_data = response.model_dump()
        assert json_data["devices"][0]["address"] == "AA:BB:CC:DD:EE:FF"
        assert json_data["devices"][0]["name"] == "Phone"

    def test_system_stats_json_serialization(self):
        """Test SystemStats JSON serialization."""
        stats = SystemStats(
            cpu_percent=15.5,
            memory_percent=45.2,
            disk_percent=70.1,
            temp_celsius=52.3
        )
        
        json_data = stats.model_dump()
        assert json_data["cpu_percent"] == 15.5
        assert json_data["temp_celsius"] == 52.3

    def test_error_response_json_serialization(self):
        """Test ErrorResponse JSON serialization."""
        error = ErrorResponse(code="404", message="Not found")
        
        json_data = error.model_dump()
        assert json_data["code"] == "404"
        assert json_data["message"] == "Not found"


class TestModelConfig:
    """Test model configuration and validation behavior."""

    def test_from_attributes_config(self):
        """Test that models can be created from object attributes."""
        # Create a simple object with attributes
        class SimpleObject:
            def __init__(self):
                self.address = "AA:BB:CC:DD:EE:FF"
                self.name = "Test Device"
        
        obj = SimpleObject()
        device = BluetoothDevice.model_validate(obj)
        assert device.address == "AA:BB:CC:DD:EE:FF"
        assert device.name == "Test Device"

    def test_field_validation_and_defaults(self):
        """Test field validation and default value behavior."""
        # Test that optional fields accept None
        ap = AccessPoint(ssid=None, bssid=None)
        assert ap.ssid is None
        assert ap.bssid is None
        
        # Test default factory for lists
        wifi_response = WiFiScanResponse()
        assert wifi_response.access_points == []
        
        bluetooth_response = BluetoothScanResponse()
        assert bluetooth_response.devices == []

    def test_field_descriptions_and_examples(self):
        """Test that field descriptions and examples are properly set."""
        # This tests that the Pydantic schema generation works correctly
        wifi_schema = WiFiScanRequest.model_json_schema()
        assert "properties" in wifi_schema
        assert "interface" in wifi_schema["properties"]
        assert "description" in wifi_schema["properties"]["interface"]

    def test_model_examples_in_schema(self):
        """Test that model examples are included in JSON schema."""
        access_point_schema = AccessPoint.model_json_schema()
        bluetooth_device_schema = BluetoothDevice.model_json_schema()
        
        # Should have examples defined in the schema (checking for 'example' which is Pydantic's format)
        assert "example" in access_point_schema or "examples" in access_point_schema or "$defs" in access_point_schema
        assert "example" in bluetooth_device_schema or "examples" in bluetooth_device_schema or "$defs" in bluetooth_device_schema


if __name__ == "__main__":
    pytest.main([__file__])
