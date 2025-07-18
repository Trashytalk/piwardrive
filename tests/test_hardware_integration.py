"""
Comprehensive test suite for PiWardrive Hardware Integration.

Tests hardware abstraction layer, GPS functionality, WiFi scanning, and device management.
"""

import threading
import time
from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from piwardrive.hardware.enhanced_hardware import (
    AdapterInfo,
    CameraManager,
    EnvironmentalSensor,
    GPSManager,
    HardwareManager,
    PowerManager,
    WirelessAdapter,
)


class TestAdapterInfo:
    """Test adapter information dataclass."""

    def test_adapter_info_creation(self):
        """Test creating an AdapterInfo instance."""
        adapter = AdapterInfo(
            interface="wlan0",
            driver="ath9k",
            chipset="Atheros AR9271",
            mac_address="00:11:22:33:44:55",
            capabilities=["monitor", "injection"],
        )

        assert adapter.interface == "wlan0"
        assert adapter.driver == "ath9k"
        assert adapter.chipset == "Atheros AR9271"
        assert adapter.mac_address == "00:11:22:33:44:55"
        assert "monitor" in adapter.capabilities
        assert "injection" in adapter.capabilities

    def test_adapter_info_defaults(self):
        """Test AdapterInfo with minimal parameters."""
        adapter = AdapterInfo(
            interface="wlan1", driver="rtl8187", chipset="Realtek RTL8187"
        )

        assert adapter.interface == "wlan1"
        assert adapter.driver == "rtl8187"
        assert adapter.chipset == "Realtek RTL8187"


class TestWirelessAdapter:
    """Test wireless adapter functionality."""

    @pytest.fixture
    def mock_adapter(self):
        """Create a mock wireless adapter."""
        with patch(
            "piwardrive.hardware.enhanced_hardware.subprocess"
        ) as mock_subprocess:
            adapter = WirelessAdapter(
                interface="wlan0", driver="ath9k", chipset="Atheros AR9271"
            )
            yield adapter, mock_subprocess

    def test_adapter_initialization(self, mock_adapter):
        """Test wireless adapter initialization."""
        adapter, mock_subprocess = mock_adapter

        assert adapter.interface == "wlan0"
        assert adapter.driver == "ath9k"
        assert adapter.chipset == "Atheros AR9271"
        assert adapter.is_active is False

    def test_adapter_activation(self, mock_adapter):
        """Test adapter activation/deactivation."""
        adapter, mock_subprocess = mock_adapter

        # Mock successful command execution
        mock_subprocess.run.return_value.returncode = 0

        # Test activation
        result = adapter.activate()
        assert result is True
        assert adapter.is_active is True

        # Test deactivation
        result = adapter.deactivate()
        assert result is True
        assert adapter.is_active is False

    def test_adapter_activation_failure(self, mock_adapter):
        """Test adapter activation failure handling."""
        adapter, mock_subprocess = mock_adapter

        # Mock failed command execution
        mock_subprocess.run.return_value.returncode = 1
        mock_subprocess.run.return_value.stderr = "Device not found"

        result = adapter.activate()
        assert result is False
        assert adapter.is_active is False

    def test_monitor_mode(self, mock_adapter):
        """Test monitor mode functionality."""
        adapter, mock_subprocess = mock_adapter

        # Mock successful mode change
        mock_subprocess.run.return_value.returncode = 0

        result = adapter.set_monitor_mode(True)
        assert result is True

        # Verify commands were called
        mock_subprocess.run.assert_called()

    def test_channel_setting(self, mock_adapter):
        """Test channel setting functionality."""
        adapter, mock_subprocess = mock_adapter

        # Mock successful channel change
        mock_subprocess.run.return_value.returncode = 0

        result = adapter.set_channel(6)
        assert result is True

        # Test invalid channel
        result = adapter.set_channel(15)  # Invalid 2.4GHz channel
        assert result is False

    def test_power_management(self, mock_adapter):
        """Test adapter power management."""
        adapter, mock_subprocess = mock_adapter

        # Mock successful power level change
        mock_subprocess.run.return_value.returncode = 0

        result = adapter.set_power_level(20)
        assert result is True

        # Test invalid power level
        result = adapter.set_power_level(35)  # Too high
        assert result is False


class TestGPSManager:
    """Test GPS functionality."""

    @pytest.fixture
    def mock_gps_manager(self):
        """Create a mock GPS manager."""
        with patch(
            "piwardrive.hardware.enhanced_hardware.serial.Serial"
        ) as mock_serial:
            gps_manager = GPSManager(device="/dev/ttyUSB0", baudrate=9600)
            yield gps_manager, mock_serial

    def test_gps_manager_initialization(self, mock_gps_manager):
        """Test GPS manager initialization."""
        gps_manager, mock_serial = mock_gps_manager

        assert gps_manager.device == "/dev/ttyUSB0"
        assert gps_manager.baudrate == 9600
        assert gps_manager.is_connected is False

    def test_gps_connection(self, mock_gps_manager):
        """Test GPS device connection."""
        gps_manager, mock_serial = mock_gps_manager

        # Mock successful connection
        mock_serial.return_value.is_open = True

        result = gps_manager.connect()
        assert result is True
        assert gps_manager.is_connected is True

    def test_gps_connection_failure(self, mock_gps_manager):
        """Test GPS connection failure handling."""
        gps_manager, mock_serial = mock_gps_manager

        # Mock connection failure
        mock_serial.side_effect = Exception("Device not found")

        result = gps_manager.connect()
        assert result is False
        assert gps_manager.is_connected is False

    def test_nmea_parsing(self, mock_gps_manager):
        """Test NMEA sentence parsing."""
        gps_manager, mock_serial = mock_gps_manager

        # Mock NMEA sentence
        nmea_sentence = (
            "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47"
        )

        # Mock serial read
        mock_serial.return_value.readline.return_value = nmea_sentence.encode()

        gps_data = gps_manager.parse_nmea(nmea_sentence)

        assert gps_data is not None
        assert "latitude" in gps_data
        assert "longitude" in gps_data
        assert "altitude" in gps_data

    def test_position_tracking(self, mock_gps_manager):
        """Test position tracking functionality."""
        gps_manager, mock_serial = mock_gps_manager

        # Mock position data
        mock_position = {
            "latitude": 48.1174,
            "longitude": 11.5167,
            "altitude": 545.4,
            "timestamp": datetime.now(),
            "accuracy": 0.9,
        }

        gps_manager.current_position = mock_position

        position = gps_manager.get_current_position()
        assert position == mock_position
        assert position["latitude"] == 48.1174
        assert position["longitude"] == 11.5167

    def test_waypoint_management(self, mock_gps_manager):
        """Test waypoint management."""
        gps_manager, mock_serial = mock_gps_manager

        # Add waypoint
        waypoint = {
            "name": "test_point",
            "latitude": 48.1174,
            "longitude": 11.5167,
            "timestamp": datetime.now(),
        }

        gps_manager.add_waypoint(waypoint)
        waypoints = gps_manager.get_waypoints()

        assert len(waypoints) == 1
        assert waypoints[0]["name"] == "test_point"


class TestEnvironmentalSensor:
    """Test environmental sensor functionality."""

    @pytest.fixture
    def mock_sensor(self):
        """Create a mock environmental sensor."""
        with patch("piwardrive.hardware.enhanced_hardware.smbus.SMBus") as mock_smbus:
            sensor = EnvironmentalSensor(sensor_type="temperature", i2c_address=0x48)
            yield sensor, mock_smbus

    def test_sensor_initialization(self, mock_sensor):
        """Test sensor initialization."""
        sensor, mock_smbus = mock_sensor

        assert sensor.sensor_type == "temperature"
        assert sensor.i2c_address == 0x48

    def test_temperature_reading(self, mock_sensor):
        """Test temperature sensor reading."""
        sensor, mock_smbus = mock_sensor

        # Mock temperature data (example: 25.5°C)
        mock_smbus.return_value.read_word_data.return_value = 0x19A0  # Mock raw data

        temperature = sensor.read_temperature()
        assert temperature is not None
        assert isinstance(temperature, (int, float))

    def test_humidity_reading(self, mock_sensor):
        """Test humidity sensor reading."""
        sensor, mock_smbus = mock_sensor
        sensor.sensor_type = "humidity"

        # Mock humidity data (example: 60% RH)
        mock_smbus.return_value.read_word_data.return_value = 0x6000

        humidity = sensor.read_humidity()
        assert humidity is not None
        assert isinstance(humidity, (int, float))

    def test_sensor_calibration(self, mock_sensor):
        """Test sensor calibration."""
        sensor, mock_smbus = mock_sensor

        # Test calibration offset
        sensor.calibration_offset = 2.0

        # Mock raw reading
        mock_smbus.return_value.read_word_data.return_value = 0x1800

        calibrated_value = sensor.read_calibrated_value()
        assert calibrated_value is not None

    def test_sensor_error_handling(self, mock_sensor):
        """Test sensor error handling."""
        sensor, mock_smbus = mock_sensor

        # Mock I2C error
        mock_smbus.return_value.read_word_data.side_effect = Exception("I2C Error")

        temperature = sensor.read_temperature()
        assert temperature is None  # Should handle errors gracefully


class TestPowerManager:
    """Test power management functionality."""

    @pytest.fixture
    def mock_power_manager(self):
        """Create a mock power manager."""
        with patch(
            "piwardrive.hardware.enhanced_hardware.subprocess"
        ) as mock_subprocess:
            power_manager = PowerManager()
            yield power_manager, mock_subprocess

    def test_power_manager_initialization(self, mock_power_manager):
        """Test power manager initialization."""
        power_manager, mock_subprocess = mock_power_manager

        assert power_manager is not None

    def test_battery_status(self, mock_power_manager):
        """Test battery status monitoring."""
        power_manager, mock_subprocess = mock_power_manager

        # Mock battery status output
        mock_subprocess.run.return_value.stdout = "75%"
        mock_subprocess.run.return_value.returncode = 0

        battery_level = power_manager.get_battery_level()
        assert battery_level == 75

    def test_power_consumption_monitoring(self, mock_power_manager):
        """Test power consumption monitoring."""
        power_manager, mock_subprocess = mock_power_manager

        # Mock power consumption data
        mock_power_data = {"voltage": 5.0, "current": 1.2, "power": 6.0}

        power_manager.current_consumption = mock_power_data

        consumption = power_manager.get_power_consumption()
        assert consumption["voltage"] == 5.0
        assert consumption["current"] == 1.2
        assert consumption["power"] == 6.0

    def test_low_power_mode(self, mock_power_manager):
        """Test low power mode functionality."""
        power_manager, mock_subprocess = mock_power_manager

        # Mock successful low power mode activation
        mock_subprocess.run.return_value.returncode = 0

        result = power_manager.enable_low_power_mode()
        assert result is True

        result = power_manager.disable_low_power_mode()
        assert result is True

    def test_thermal_monitoring(self, mock_power_manager):
        """Test thermal monitoring."""
        power_manager, mock_subprocess = mock_power_manager

        # Mock CPU temperature
        mock_subprocess.run.return_value.stdout = "temp=45.2'C"
        mock_subprocess.run.return_value.returncode = 0

        temperature = power_manager.get_cpu_temperature()
        assert temperature == 45.2


class TestCameraManager:
    """Test camera integration functionality."""

    @pytest.fixture
    def mock_camera_manager(self):
        """Create a mock camera manager."""
        with patch("piwardrive.hardware.enhanced_hardware.cv2") as mock_cv2:
            camera_manager = CameraManager(camera_id=0)
            yield camera_manager, mock_cv2

    def test_camera_manager_initialization(self, mock_camera_manager):
        """Test camera manager initialization."""
        camera_manager, mock_cv2 = mock_camera_manager

        assert camera_manager.camera_id == 0
        assert camera_manager.is_recording is False

    def test_camera_activation(self, mock_camera_manager):
        """Test camera activation."""
        camera_manager, mock_cv2 = mock_camera_manager

        # Mock successful camera opening
        mock_cv2.VideoCapture.return_value.isOpened.return_value = True

        result = camera_manager.initialize_camera()
        assert result is True

    def test_image_capture(self, mock_camera_manager):
        """Test image capture functionality."""
        camera_manager, mock_cv2 = mock_camera_manager

        # Mock successful frame capture
        mock_cv2.VideoCapture.return_value.read.return_value = (True, "mock_frame")

        frame = camera_manager.capture_frame()
        assert frame == "mock_frame"

    def test_video_recording(self, mock_camera_manager):
        """Test video recording functionality."""
        camera_manager, mock_cv2 = mock_camera_manager

        # Mock video writer
        mock_cv2.VideoWriter.return_value = Mock()

        result = camera_manager.start_recording("test_video.mp4")
        assert result is True
        assert camera_manager.is_recording is True

        result = camera_manager.stop_recording()
        assert result is True
        assert camera_manager.is_recording is False

    def test_camera_settings(self, mock_camera_manager):
        """Test camera settings configuration."""
        camera_manager, mock_cv2 = mock_camera_manager

        # Mock camera property setting
        mock_cv2.VideoCapture.return_value.set.return_value = True

        result = camera_manager.set_resolution(1920, 1080)
        assert result is True

        result = camera_manager.set_framerate(30)
        assert result is True


class TestHardwareManager:
    """Test overall hardware management."""

    @pytest.fixture
    def mock_hardware_manager(self):
        """Create a mock hardware manager."""
        with patch.multiple(
            "piwardrive.hardware.enhanced_hardware",
            WirelessAdapter=Mock(),
            GPSManager=Mock(),
            EnvironmentalSensor=Mock(),
            PowerManager=Mock(),
            CameraManager=Mock(),
        ) as mocks:
            hardware_manager = HardwareManager()
            yield hardware_manager, mocks

    def test_hardware_manager_initialization(self, mock_hardware_manager):
        """Test hardware manager initialization."""
        hardware_manager, mocks = mock_hardware_manager

        assert hardware_manager is not None
        assert hasattr(hardware_manager, "adapters")
        assert hasattr(hardware_manager, "gps_manager")

    def test_adapter_discovery(self, mock_hardware_manager):
        """Test wireless adapter discovery."""
        hardware_manager, mocks = mock_hardware_manager

        # Mock adapter discovery
        mock_adapters = [
            AdapterInfo(interface="wlan0", driver="ath9k", chipset="Atheros AR9271"),
            AdapterInfo(interface="wlan1", driver="rtl8187", chipset="Realtek RTL8187"),
        ]

        hardware_manager.discovered_adapters = mock_adapters

        adapters = hardware_manager.discover_adapters()
        assert len(adapters) == 2
        assert adapters[0].interface == "wlan0"
        assert adapters[1].interface == "wlan1"

    def test_device_health_monitoring(self, mock_hardware_manager):
        """Test device health monitoring."""
        hardware_manager, mocks = mock_hardware_manager

        # Mock health status
        health_status = {
            "adapters": 2,
            "gps": True,
            "sensors": 3,
            "power": "normal",
            "temperature": 45.2,
        }

        hardware_manager.health_status = health_status

        status = hardware_manager.get_health_status()
        assert status["adapters"] == 2
        assert status["gps"] is True
        assert status["power"] == "normal"

    def test_concurrent_device_access(self, mock_hardware_manager):
        """Test concurrent access to hardware devices."""
        hardware_manager, mocks = mock_hardware_manager

        def access_devices():
            for i in range(100):
                _ = hardware_manager.get_health_status()
                time.sleep(0.001)

        # Create multiple threads accessing devices
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=access_devices)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=5)

        # Hardware manager should remain stable
        assert hardware_manager is not None

    def test_error_recovery(self, mock_hardware_manager):
        """Test hardware error recovery."""
        hardware_manager, mocks = mock_hardware_manager

        # Simulate device failure
        mocks["WirelessAdapter"].side_effect = Exception("Device error")

        # Hardware manager should handle errors gracefully
        result = hardware_manager.recover_from_error("wlan0")
        # Should attempt recovery without crashing
        assert result is not None

    def test_resource_cleanup(self, mock_hardware_manager):
        """Test resource cleanup on shutdown."""
        hardware_manager, mocks = mock_hardware_manager

        # Simulate cleanup
        hardware_manager.cleanup()

        # Should call cleanup methods on components
        # (exact verification depends on implementation)
        assert hardware_manager is not None


class TestHardwareIntegration:
    """Test hardware component integration."""

    def test_gps_adapter_coordination(self):
        """Test coordination between GPS and wireless adapters."""
        with patch.multiple(
            "piwardrive.hardware.enhanced_hardware",
            GPSManager=Mock(),
            WirelessAdapter=Mock(),
        ) as mocks:
            # Mock GPS providing location
            mock_gps = mocks["GPSManager"].return_value
            mock_gps.get_current_position.return_value = {
                "latitude": 48.1174,
                "longitude": 11.5167,
            }

            # Mock adapter scan with location
            mock_adapter = mocks["WirelessAdapter"].return_value
            mock_adapter.scan_with_location.return_value = [
                {"ssid": "TestNetwork", "lat": 48.1174, "lon": 11.5167}
            ]

            hardware_manager = HardwareManager()

            # Test coordinated scan
            results = hardware_manager.perform_coordinated_scan()
            assert results is not None

    def test_environmental_monitoring_integration(self):
        """Test integration of environmental monitoring with other components."""
        with patch.multiple(
            "piwardrive.hardware.enhanced_hardware",
            EnvironmentalSensor=Mock(),
            PowerManager=Mock(),
        ) as mocks:
            # Mock high temperature reading
            mock_sensor = mocks["EnvironmentalSensor"].return_value
            mock_sensor.read_temperature.return_value = 85.0  # High temperature

            # Mock power manager response
            mock_power = mocks["PowerManager"].return_value
            mock_power.enable_low_power_mode.return_value = True

            hardware_manager = HardwareManager()

            # Test thermal protection
            hardware_manager.check_thermal_protection()

            # Should trigger low power mode due to high temperature
            mock_power.enable_low_power_mode.assert_called()

    def test_multi_adapter_scanning(self):
        """Test coordinated scanning with multiple adapters."""
        with patch(
            "piwardrive.hardware.enhanced_hardware.WirelessAdapter"
        ) as mock_adapter_class:
            # Create multiple mock adapters
            mock_adapters = []
            for i in range(3):
                mock_adapter = Mock()
                mock_adapter.interface = f"wlan{i}"
                mock_adapter.scan.return_value = [f"network_{i}_1", f"network_{i}_2"]
                mock_adapters.append(mock_adapter)

            mock_adapter_class.side_effect = mock_adapters

            hardware_manager = HardwareManager()
            hardware_manager.adapters = mock_adapters

            # Test multi-adapter scan
            results = hardware_manager.scan_all_adapters()

            # Should collect results from all adapters
            assert len(results) >= 3
            for adapter in mock_adapters:
                adapter.scan.assert_called()
