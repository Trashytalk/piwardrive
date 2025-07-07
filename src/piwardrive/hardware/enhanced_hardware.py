"""
Hardware Integration Improvements for PiWardrive
Provides multi-adapter support,
    GPS enhancements,
    environmental sensors,
    power management,
    and camera integration
"""

import logging
import subprocess
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import serial

# Hardware-specific imports (conditional)
try:
    import smbus

    HAS_RPI_HARDWARE = True
except ImportError:
    HAS_RPI_HARDWARE = False

try:
    import usb.core

    HAS_USB_SUPPORT = True
except ImportError:
    HAS_USB_SUPPORT = False

try:
    import cv2

    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False

logger = logging.getLogger(__name__)


@dataclass
class AdapterInfo:
    """Information about a wireless adapter"""

    interface: str
    driver: str
    chipset: str
    capabilities: List[str]
    supported_bands: List[str]
    max_power: int
    is_monitor_capable: bool
    is_injection_capable: bool
    status: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GPSData:
    """Enhanced GPS data structure"""

    timestamp: datetime
    latitude: float
    longitude: float
    altitude: float
    speed: float
    bearing: float
    accuracy: float
    satellites: int
    hdop: float
    vdop: float
    pdop: float
    fix_type: str
    dgps_correction: bool = False
    rtk_correction: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude,
            "speed": self.speed,
            "bearing": self.bearing,
            "accuracy": self.accuracy,
            "satellites": self.satellites,
            "hdop": self.hdop,
            "vdop": self.vdop,
            "pdop": self.pdop,
            "fix_type": self.fix_type,
            "dgps_correction": self.dgps_correction,
            "rtk_correction": self.rtk_correction,
        }


@dataclass
class EnvironmentalData:
    """Environmental sensor data"""

    timestamp: datetime
    temperature: float
    humidity: float
    pressure: float
    light_level: float
    uv_index: float
    air_quality: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "temperature": self.temperature,
            "humidity": self.humidity,
            "pressure": self.pressure,
            "light_level": self.light_level,
            "uv_index": self.uv_index,
            "air_quality": self.air_quality,
        }


class MultiAdapterManager:
    """Manager for multiple wireless adapters"""

    def __init__(self):
        self.adapters = {}
        self.active_adapters = {}
        self.scan_assignments = {}
        self.lock = threading.Lock()

    def discover_adapters(self) -> List[AdapterInfo]:
        """Discover available wireless adapters"""
        adapters = []

        try:
            # Get wireless interfaces
            _result = subprocess.run(["iwconfig"], capture_output=True, text=True)
            interfaces = self._parse_iwconfig_output(_result.stdout)

            for interface in interfaces:
                adapter_info = self._get_adapter_info(interface)
                if adapter_info:
                    adapters.append(adapter_info)

        except Exception as e:
            logger.error(f"Error discovering adapters: {e}")

        return adapters

    def _parse_iwconfig_output(self, output: str) -> List[str]:
        """Parse iwconfig output to extract wireless interfaces"""
        interfaces = []
        lines = output.split("\n")

        for line in lines:
            if "IEEE 802.11" in line or "ESSID" in line:
                interface = line.split()[0]
                if interface and interface not in interfaces:
                    interfaces.append(interface)

        return interfaces

    def _get_adapter_info(self, interface: str) -> Optional[AdapterInfo]:
        """Get detailed information about a wireless adapter"""
        try:
            # Get driver info
            driver_info = subprocess.run(
                ["ethtool", "-i", interface], capture_output=True, text=True
            )
            driver = "unknown"
            if driver_info.returncode == 0:
                for line in driver_info.stdout.split("\n"):
                    if line.startswith("driver:"):
                        driver = line.split(":", 1)[1].strip()
                        break

            # Get capabilities
            capabilities = self._get_adapter_capabilities(interface)

            # Check monitor mode support
            monitor_capable = self._check_monitor_mode_support(interface)

            # Check injection support
            injection_capable = self._check_injection_support(interface)

            # Get supported bands
            bands = self._get_supported_bands(interface)

            adapter_info = AdapterInfo(
                interface=interface,
                driver=driver,
                chipset=self._get_chipset_info(interface),
                capabilities=capabilities,
                supported_bands=bands,
                max_power=20,  # Default, should be detected
                is_monitor_capable=monitor_capable,
                is_injection_capable=injection_capable,
                status="active",
            )

            return adapter_info

        except Exception as e:
            logger.error(f"Error getting adapter info for {interface}: {e}")
            return None

    def _get_adapter_capabilities(self, interface: str) -> List[str]:
        """Get adapter capabilities"""
        capabilities = []

        try:
            # Check iwlist capabilities
            _result = subprocess.run(
                ["iwlist", interface, "freq"], capture_output=True, text=True
            )
            if "5." in _result.stdout:
                capabilities.append("5GHz")
            if "2." in _result.stdout:
                capabilities.append("2.4GHz")

        except Exception as e:
            logger.debug(f"Error getting capabilities for {interface}: {e}")

        return capabilities

    def _check_monitor_mode_support(self, interface: str) -> bool:
        """Check if adapter supports monitor mode"""
        try:
            # Try to set monitor mode temporarily
            _result = subprocess.run(
                ["iwconfig", interface, "mode", "monitor"],
                capture_output=True,
                text=True,
            )

            if _result.returncode == 0:
                # Restore managed mode
                subprocess.run(
                    ["iwconfig", interface, "mode", "managed"],
                    capture_output=True,
                    text=True,
                )
                return True

        except Exception as e:
            logger.debug(f"Error checking monitor mode for {interface}: {e}")

        return False

    def _check_injection_support(self, interface: str) -> bool:
        """Check if adapter supports packet injection"""
        try:
            # This would require more sophisticated testing
            # For now, assume monitor-capable adapters support injection
            return self._check_monitor_mode_support(interface)

        except Exception as e:
            logger.debug(f"Error checking injection support for {interface}: {e}")

        return False

    def _get_supported_bands(self, interface: str) -> List[str]:
        """Get supported frequency bands"""
        bands = []

        try:
            _result = subprocess.run(
                ["iwlist", interface, "freq"], capture_output=True, text=True
            )

            _frequencies = []
            for line in _result.stdout.split("\n"):
                if "Channel" in line and "GHz" in line:
                    if "2.4" in line or "2." in line:
                        if "2.4GHz" not in bands:
                            bands.append("2.4GHz")
                    elif "5." in line or "5GHz" in line:
                        if "5GHz" not in bands:
                            bands.append("5GHz")
                    elif "6." in line or "6GHz" in line:
                        if "6GHz" not in bands:
                            bands.append("6GHz")

        except Exception as e:
            logger.debug(f"Error getting bands for {interface}: {e}")

        return bands

    def _get_chipset_info(self, interface: str) -> str:
        """Get chipset information"""
        try:
            # Try to get chipset info from lsusb and lspci
            lsusb_result = subprocess.run(["lsusb"], capture_output=True, text=True)
            lspci_result = subprocess.run(["lspci"], capture_output=True, text=True)

            # Look for common wireless chipsets
            combined_output = lsusb_result.stdout + lspci_result.stdout

            chipsets = {
                "rtl8188": "Realtek RTL8188",
                "rtl8192": "Realtek RTL8192",
                "rtl8812": "Realtek RTL8812",
                "ath9k": "Atheros AR9xxx",
                "ath10k": "Atheros AR10xxx",
                "mt7601": "MediaTek MT7601",
                "mt7610": "MediaTek MT7610",
                "rt2800": "Ralink RT2800",
                "rt5370": "Ralink RT5370",
            }

            for chipset_key, chipset_name in chipsets.items():
                if chipset_key in combined_output.lower():
                    return chipset_name

        except Exception as e:
            logger.debug(f"Error getting chipset info: {e}")

        return "unknown"

    def assign_scanning_tasks(self, scan_config: Dict[str, Any]) -> Dict[str, str]:
        """Assign scanning tasks to different adapters"""
        assignments = {}

        with self.lock:
            _available_adapters = list(self.adapters.keys())

            # Example assignment logic
            if "2.4GHz" in scan_config.get("bands", []):
                # Assign 2.4GHz capable adapter
                for adapter_name, adapter_info in self.adapters.items():
                    if "2.4GHz" in adapter_info.supported_bands:
                        assignments["2.4GHz"] = adapter_name
                        break

            if "5GHz" in scan_config.get("bands", []):
                # Assign 5GHz capable adapter
                for adapter_name, adapter_info in self.adapters.items():
                    if (
                        "5GHz" in adapter_info.supported_bands
                        and adapter_name not in assignments.values()
                    ):
                        assignments["5GHz"] = adapter_name
                        break

        return assignments

    def configure_adapter(self, interface: str, config: Dict[str, Any]) -> bool:
        """Configure a wireless adapter"""
        try:
            # Set channel
            if "channel" in config:
                subprocess.run(
                    ["iwconfig", interface, "channel", str(config["channel"])],
                    check=True,
                )

            # Set power
            if "power" in config:
                subprocess.run(
                    ["iwconfig", interface, "txpower", str(config["power"])], check=True
                )

            # Set mode
            if "mode" in config:
                subprocess.run(
                    ["iwconfig", interface, "mode", config["mode"]], check=True
                )

            return True

        except Exception as e:
            logger.error(f"Error configuring adapter {interface}: {e}")
            return False


class EnhancedGPSManager:
    """Enhanced GPS manager with RTK and differential correction support"""

    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.running = False
        self.current_position = None
        self.dgps_corrections = {}
        self.rtk_base_station = None
        self.correction_thread = None

    def connect(self) -> bool:
        """Connect to GPS device"""
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=1)
            logger.info(f"Connected to GPS on {self.port}")
            return True

        except Exception as e:
            logger.error(f"Error connecting to GPS: {e}")
            return False

    def start_reading(self):
        """Start reading GPS data"""
        if not self.serial_connection:
            if not self.connect():
                return False

        self.running = True
        self.reading_thread = threading.Thread(target=self._read_gps_data)
        self.reading_thread.daemon = True
        self.reading_thread.start()

        return True

    def stop_reading(self):
        """Stop reading GPS data"""
        self.running = False
        if self.serial_connection:
            self.serial_connection.close()

    def _read_gps_data(self):
        """Read GPS data from serial connection"""
        while self.running:
            try:
                line = (
                    self.serial_connection.readline()
                    .decode("ascii", errors="ignore")
                    .strip()
                )

                if line.startswith("$GPGGA") or line.startswith("$GNGGA"):
                    _gpsdata = self._parse_gga_sentence(line)
                    if _gpsdata:
                        self.current_position = _gpsdata

                elif line.startswith("$GPRMC") or line.startswith("$GNRMC"):
                    self._parse_rmc_sentence(line)

            except Exception as e:
                logger.debug(f"Error reading GPS data: {e}")
                time.sleep(0.1)

    def _parse_gga_sentence(self, sentence: str) -> Optional[GPSData]:
        """Parse GGA NMEA sentence"""
        try:
            parts = sentence.split(",")

            if len(parts) < 15:
                return None

            # Extract time
            time_str = parts[1]
            if not time_str:
                return None

            # Extract coordinates
            lat_str = parts[2]
            lat_dir = parts[3]
            lon_str = parts[4]
            lon_dir = parts[5]

            if not all([lat_str, lat_dir, lon_str, lon_dir]):
                return None

            latitude = self._convert_coordinate(lat_str, lat_dir)
            longitude = self._convert_coordinate(lon_str, lon_dir)

            # Other fields
            fix_quality = int(parts[6]) if parts[6] else 0
            satellites = int(parts[7]) if parts[7] else 0
            hdop = float(parts[8]) if parts[8] else 0.0
            altitude = float(parts[9]) if parts[9] else 0.0

            # Create timestamp
            now = datetime.now()
            hour = int(time_str[:2])
            minute = int(time_str[2:4])
            second = int(time_str[4:6])

            timestamp = now.replace(
                hour=hour, minute=minute, second=second, microsecond=0
            )

            gps_data = GPSData(
                timestamp=timestamp,
                latitude=latitude,
                longitude=longitude,
                altitude=altitude,
                speed=0.0,  # Not available in GGA
                bearing=0.0,  # Not available in GGA
                accuracy=hdop * 5,  # Rough estimate
                satellites=satellites,
                hdop=hdop,
                vdop=0.0,  # Not available in GGA
                pdop=0.0,  # Not available in GGA
                fix_type=self._get_fix_type(fix_quality),
                dgps_correction=fix_quality in [2, 3, 4, 5],
                rtk_correction=fix_quality in [4, 5],
            )

            return gps_data

        except Exception as e:
            logger.debug(f"Error parsing GGA sentence: {e}")
            return None

    def _parse_rmc_sentence(self, sentence: str):
        """Parse RMC NMEA sentence for speed and bearing"""
        try:
            parts = sentence.split(",")

            if len(parts) < 10:
                return

            # Extract speed and bearing
            speed_knots = float(parts[7]) if parts[7] else 0.0
            bearing = float(parts[8]) if parts[8] else 0.0

            # Update current position if available
            if self.current_position:
                self.current_position.speed = speed_knots * 1.852  # Convert to km/h
                self.current_position.bearing = bearing

        except Exception as e:
            logger.debug(f"Error parsing RMC sentence: {e}")

    def _convert_coordinate(self, coord_str: str, direction: str) -> float:
        """Convert NMEA coordinate format to decimal degrees"""
        if not coord_str:
            return 0.0

        # NMEA format: DDMM.MMMM or DDDMM.MMMM
        if len(coord_str) > 7:  # Longitude
            degrees = int(coord_str[:3])
            minutes = float(coord_str[3:])
        else:  # Latitude
            degrees = int(coord_str[:2])
            minutes = float(coord_str[2:])

        decimal_degrees = degrees + minutes / 60.0

        if direction in ["S", "W"]:
            decimal_degrees = -decimal_degrees

        return decimal_degrees

    def _get_fix_type(self, fix_quality: int) -> str:
        """Get fix type description"""
        fix_types = {
            0: "no_fix",
            1: "gps",
            2: "dgps",
            3: "pps",
            4: "rtk_fixed",
            5: "rtk_float",
            6: "estimated",
            7: "manual",
            8: "simulation",
        }

        return fix_types.get(fix_quality, "unknown")

    def setup_rtk_base_station(self, config: Dict[str, Any]) -> bool:
        """Setup RTK base station configuration"""
        try:
            self.rtk_base_station = config

            # Configure base station if using NTRIP
            if config.get("type") == "ntrip":
                self._setup_ntrip_client(config)

            return True

        except Exception as e:
            logger.error(f"Error setting up RTK base station: {e}")
            return False

    def _setup_ntrip_client(self, config: Dict[str, Any]):
        """Setup NTRIP client for RTK corrections"""
        # This would implement NTRIP client functionality
        # For now, it's a placeholder
        logger.info("NTRIP client setup - placeholder implementation")

    def get_current_position(self) -> Optional[GPSData]:
        """Get current GPS position"""
        return self.current_position


class EnvironmentalSensorManager:
    """Manager for environmental sensors (temperature, humidity, pressure, etc.)"""

    def __init__(self):
        self.sensors = {}
        self.running = False
        self.current_readings = {}
        self.i2c_bus = None

        if HAS_RPI_HARDWARE:
            try:
                self.i2c_bus = smbus.SMBus(1)  # I2C bus 1
            except Exception as e:
                logger.warning(f"Could not initialize I2C bus: {e}")

    def initialize_sensors(self) -> bool:
        """Initialize environmental sensors"""
        success = True

        # Initialize BME280 (temperature, humidity, pressure)
        if self._init_bme280():
            self.sensors["bme280"] = True
            logger.info("BME280 sensor initialized")
        else:
            success = False

        # Initialize TSL2561 (light sensor)
        if self._init_tsl2561():
            self.sensors["tsl2561"] = True
            logger.info("TSL2561 light sensor initialized")
        else:
            success = False

        # Initialize UV sensor
        if self._init_uv_sensor():
            self.sensors["uv"] = True
            logger.info("UV sensor initialized")
        else:
            success = False

        return success

    def _init_bme280(self) -> bool:
        """Initialize BME280 sensor"""
        try:
            if not self.i2c_bus:
                return False

            # BME280 I2C address
            BME280_ADDR = 0x76

            # Check if sensor is present
            chip_id = self.i2c_bus.read_byte_data(BME280_ADDR, 0xD0)
            if chip_id != 0x60:
                logger.debug(f"BME280 not found, chip_id: {chip_id}")
                return False

            # Initialize sensor (basic configuration)
            self.i2c_bus.write_byte_data(
                BME280_ADDR, 0xF2, 0x01
            )  # Humidity oversampling
            self.i2c_bus.write_byte_data(
                BME280_ADDR, 0xF4, 0x27
            )  # Temperature and pressure oversampling
            self.i2c_bus.write_byte_data(BME280_ADDR, 0xF5, 0xA0)  # Configuration

            return True

        except Exception as e:
            logger.debug(f"Error initializing BME280: {e}")
            return False

    def _init_tsl2561(self) -> bool:
        """Initialize TSL2561 light sensor"""
        try:
            if not self.i2c_bus:
                return False

            # TSL2561 I2C address
            TSL2561_ADDR = 0x39

            # Check if sensor is present
            part_id = self.i2c_bus.read_byte_data(TSL2561_ADDR, 0x8A)
            if (part_id & 0xF0) != 0x10:
                logger.debug(f"TSL2561 not found, part_id: {part_id}")
                return False

            # Power up and configure
            self.i2c_bus.write_byte_data(TSL2561_ADDR, 0x80, 0x03)  # Power up
            self.i2c_bus.write_byte_data(
                TSL2561_ADDR, 0x81, 0x02
            )  # 402ms integration time

            return True

        except Exception as e:
            logger.debug(f"Error initializing TSL2561: {e}")
            return False

    def _init_uv_sensor(self) -> bool:
        """Initialize UV sensor"""
        try:
            # This would depend on the specific UV sensor being used
            # For now, assume it's connected via I2C
            return True

        except Exception as e:
            logger.debug(f"Error initializing UV sensor: {e}")
            return False

    def start_monitoring(self):
        """Start monitoring environmental sensors"""
        self.running = True
        self.monitoring_thread = threading.Thread(target=self._monitor_sensors)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

    def stop_monitoring(self):
        """Stop monitoring environmental sensors"""
        self.running = False

    def _monitor_sensors(self):
        """Monitor sensors in background thread"""
        while self.running:
            try:
                current_readings = {}

                if "bme280" in self.sensors:
                    bme_data = self._read_bme280()
                    current_readings.update(bme_data)

                if "tsl2561" in self.sensors:
                    light_data = self._read_tsl2561()
                    current_readings.update(light_data)

                if "uv" in self.sensors:
                    uv_data = self._read_uv_sensor()
                    current_readings.update(uv_data)

                # Update current readings
                self.current_readings = current_readings

                # Log readings periodically
                if time.time() % 60 < 1:  # Every minute
                    logger.info(f"Environmental readings: {current_readings}")

            except Exception as e:
                logger.debug(f"Error monitoring sensors: {e}")

            time.sleep(5)  # Read every 5 seconds

    def _read_bme280(self) -> Dict[str, float]:
        """Read BME280 sensor data"""
        try:
            if not self.i2c_bus:
                return {}

            BME280_ADDR = 0x76

            # Read raw data
            _data = self.i2c_bus.read_i2c_block_data(BME280_ADDR, 0xF7, 8)

            # Convert raw data (simplified - would need calibration coefficients)
            pressure = (_data[0] << 12) | (_data[1] << 4) | (_data[2] >> 4)
            temperature = (_data[3] << 12) | (_data[4] << 4) | (_data[5] >> 4)
            humidity = (_data[6] << 8) | _data[7]

            # Apply calibration (simplified)
            temp_c = temperature / 100.0 - 40.0  # Rough approximation
            humidity_percent = humidity / 1024.0  # Rough approximation
            pressure_hpa = pressure / 100.0  # Rough approximation

            return {
                "temperature": temp_c,
                "humidity": humidity_percent,
                "pressure": pressure_hpa,
            }

        except Exception as e:
            logger.debug(f"Error reading BME280: {e}")
            return {}

    def _read_tsl2561(self) -> Dict[str, float]:
        """Read TSL2561 light sensor data"""
        try:
            if not self.i2c_bus:
                return {}

            TSL2561_ADDR = 0x39

            # Read light data
            _data = self.i2c_bus.read_i2c_block_data(TSL2561_ADDR, 0x8C, 4)

            # Convert to lux (simplified)
            ch0 = (_data[1] << 8) | _data[0]
            ch1 = (_data[3] << 8) | _data[2]

            # Calculate lux value (simplified)
            ratio = ch1 / ch0 if ch0 > 0 else 0
            lux = ch0 * 0.39 * (1 - ratio) if ratio < 0.5 else ch0 * 0.25

            return {"light_level": lux}

        except Exception as e:
            logger.debug(f"Error reading TSL2561: {e}")
            return {}

    def _read_uv_sensor(self) -> Dict[str, float]:
        """Read UV sensor data"""
        try:
            # Placeholder for UV sensor reading
            # This would depend on the specific UV sensor
            return {"uv_index": 0.0, "air_quality": 50.0}  # Placeholder

        except Exception as e:
            logger.debug(f"Error reading UV sensor: {e}")
            return {}

    def get_current_readings(self) -> Optional[EnvironmentalData]:
        """Get current environmental readings"""
        if not self.current_readings:
            return None

        return EnvironmentalData(
            timestamp=datetime.now(),
            temperature=self.current_readings.get("temperature", 0.0),
            humidity=self.current_readings.get("humidity", 0.0),
            pressure=self.current_readings.get("pressure", 0.0),
            light_level=self.current_readings.get("light_level", 0.0),
            uv_index=self.current_readings.get("uv_index", 0.0),
            air_quality=self.current_readings.get("air_quality", 0.0),
        )


class PowerManagementSystem:
    """Power management system for battery monitoring and optimization"""

    def __init__(self):
        self.battery_level = 100.0
        self.power_mode = "normal"
        self.power_profiles = {
            "power_save": {"cpu_freq": 600, "wifi_power": 10, "scan_interval": 30},
            "normal": {"cpu_freq": 1000, "wifi_power": 20, "scan_interval": 5},
            "performance": {"cpu_freq": 1400, "wifi_power": 30, "scan_interval": 1},
        }
        self.monitoring_active = False

    def get_battery_status(self) -> Dict[str, Any]:
        """Get battery status information"""
        try:
            # Try to read from standard battery interfaces
            battery_info = {}

            # Check for UPS/battery via I2C
            if HAS_RPI_HARDWARE and hasattr(self, "i2c_bus"):
                battery_info = self._read_battery_i2c()

            # Check for USB power monitoring
            if not battery_info:
                battery_info = self._read_system_power()

            return battery_info

        except Exception as e:
            logger.debug(f"Error getting battery status: {e}")
            return {
                "level": 100.0,
                "charging": False,
                "time_remaining": 0,
                "health": "unknown",
            }

    def _read_battery_i2c(self) -> Dict[str, Any]:
        """Read battery information via I2C"""
        # This would implement specific battery monitoring chip communication
        # For now, return simulated data
        return {
            "level": self.battery_level,
            "charging": False,
            "time_remaining": 120,  # minutes
            "health": "good",
        }

    def _read_system_power(self) -> Dict[str, Any]:
        """Read system power information"""
        try:
            # Check for power supply information
            power_supply_path = Path("/sys/class/power_supply")

            if power_supply_path.exists():
                for supply in power_supply_path.iterdir():
                    if supply.is_dir():
                        capacity_file = supply / "capacity"
                        if capacity_file.exists():
                            with open(capacity_file, "r") as f:
                                capacity = int(f.read().strip())

                            return {
                                "level": capacity,
                                "charging": False,
                                "time_remaining": 0,
                                "health": "good",
                            }

        except Exception as e:
            logger.debug(f"Error reading system power: {e}")

        return {}

    def set_power_mode(self, mode: str) -> bool:
        """Set power management mode"""
        if mode not in self.power_profiles:
            return False

        try:
            profile = self.power_profiles[mode]

            # Set CPU frequency
            if HAS_RPI_HARDWARE:
                self._set_cpu_frequency(profile["cpu_freq"])

            # Set WiFi power
            self._set_wifi_power(profile["wifi_power"])

            self.power_mode = mode
            logger.info(f"Power mode set to {mode}")

            return True

        except Exception as e:
            logger.error(f"Error setting power mode: {e}")
            return False

    def _set_cpu_frequency(self, freq_mhz: int):
        """Set CPU frequency"""
        try:
            with open(
                "/sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq", "w"
            ) as f:
                f.write(str(freq_mhz * 1000))

        except Exception as e:
            logger.debug(f"Error setting CPU frequency: {e}")

    def _set_wifi_power(self, power_dbm: int):
        """Set WiFi power level"""
        try:
            # This would set power for all WiFi interfaces
            _result = subprocess.run(["iwconfig"], capture_output=True, text=True)

            for line in _result.stdout.split("\n"):
                if "IEEE 802.11" in line:
                    interface = line.split()[0]
                    subprocess.run(
                        ["iwconfig", interface, "txpower", str(power_dbm)],
                        capture_output=True,
                    )

        except Exception as e:
            logger.debug(f"Error setting WiFi power: {e}")

    def start_monitoring(self):
        """Start power monitoring"""
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitor_power)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()

    def stop_monitoring(self):
        """Stop power monitoring"""
        self.monitoring_active = False

    def _monitor_power(self):
        """Monitor power status and adjust accordingly"""
        while self.monitoring_active:
            try:
                battery_status = self.get_battery_status()
                battery_level = battery_status.get("level", 100)

                # Auto-adjust power mode based on battery level
                if battery_level < 20 and self.power_mode != "power_save":
                    self.set_power_mode("power_save")
                    logger.info("Auto-switched to power save mode")
                elif battery_level > 50 and self.power_mode == "power_save":
                    self.set_power_mode("normal")
                    logger.info("Auto-switched to normal power mode")

                self.battery_level = battery_level

            except Exception as e:
                logger.debug(f"Error in power monitoring: {e}")

            time.sleep(30)  # Check every 30 seconds


class CameraIntegration:
    """Camera integration for visual documentation"""

    def __init__(self):
        self.camera = None
        self.recording = False
        self.photo_count = 0
        self.video_count = 0

    def initialize_camera(self) -> bool:
        """Initialize camera system"""
        try:
            if HAS_RPI_HARDWARE:
                # Try PiCamera first
                try:

                    self.camera = picamera.PiCamera()
                    self.camera.resolution = (1920, 1080)
                    self.camera.framerate = 30
                    logger.info("PiCamera initialized")
                    return True
                except ImportError:
                    pass

            # Try OpenCV camera
            if HAS_OPENCV:
                self.camera = cv2.VideoCapture(0)
                if self.camera.isOpened():
                    logger.info("OpenCV camera initialized")
                    return True

        except Exception as e:
            logger.error(f"Error initializing camera: {e}")

        return False

    def take_photo(self, filename: str = None) -> Optional[str]:
        """Take a photo"""
        if not self.camera:
            return None

        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"photo_{timestamp}_{self.photo_count:04d}.jpg"

            if HAS_RPI_HARDWARE and hasattr(self.camera, "capture"):
                self.camera.capture(filename)
            elif HAS_OPENCV:
                ret, frame = self.camera.read()
                if ret:
                    cv2.imwrite(filename, frame)

            self.photo_count += 1
            logger.info(f"Photo saved: {filename}")

            return filename

        except Exception as e:
            logger.error(f"Error taking photo: {e}")
            return None

    def start_video_recording(self, filename: str = None) -> Optional[str]:
        """Start video recording"""
        if not self.camera or self.recording:
            return None

        try:
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"video_{timestamp}_{self.video_count:04d}.mp4"

            if HAS_RPI_HARDWARE and hasattr(self.camera, "start_recording"):
                self.camera.start_recording(filename)
            elif HAS_OPENCV:
                # Setup video writer
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                self.video_writer = cv2.VideoWriter(filename, fourcc, 30.0, (640, 480))
                self.video_filename = filename

            self.recording = True
            self.video_count += 1
            logger.info(f"Video recording started: {filename}")

            return filename

        except Exception as e:
            logger.error(f"Error starting video recording: {e}")
            return None

    def stop_video_recording(self):
        """Stop video recording"""
        if not self.recording:
            return

        try:
            if HAS_RPI_HARDWARE and hasattr(self.camera, "stop_recording"):
                self.camera.stop_recording()
            elif HAS_OPENCV and hasattr(self, "video_writer"):
                self.video_writer.release()

            self.recording = False
            logger.info("Video recording stopped")

        except Exception as e:
            logger.error(f"Error stopping video recording: {e}")

    def get_camera_info(self) -> Dict[str, Any]:
        """Get camera information"""
        if not self.camera:
            return {}

        info = {
            "initialized": True,
            "recording": self.recording,
            "photo_count": self.photo_count,
            "video_count": self.video_count,
        }

        if HAS_RPI_HARDWARE and hasattr(self.camera, "resolution"):
            info["resolution"] = self.camera.resolution
            info["framerate"] = self.camera.framerate

        return info


# Example usage functions
def example_multi_adapter():
    """Example of multi-adapter management"""
    manager = MultiAdapterManager()

    # Discover adapters
    adapters = manager.discover_adapters()

    for adapter in adapters:
        logger.info(f"Found adapter: {adapter.interface} ({adapter.chipset})")

    # Configure scanning assignments
    scan_config = {"bands": ["2.4GHz", "5GHz"]}
    assignments = manager.assign_scanning_tasks(scan_config)

    logger.info(f"Scanning assignments: {assignments}")

    return manager


def example_enhanced_gps():
    """Example of enhanced GPS functionality"""
    gps_manager = EnhancedGPSManager()

    if gps_manager.start_reading():
        logger.info("GPS reading started")

        # Wait for position fix
        for _ in range(60):  # Wait up to 60 seconds
            position = gps_manager.get_current_position()
            if position:
                logger.info(f"GPS Position: {position.to_dict()}")
                break
            time.sleep(1)

        gps_manager.stop_reading()

    return gps_manager


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Run examples
    example_multi_adapter()
    example_enhanced_gps()
