"""
Multi-Protocol Support Module for PiWardrive
Support for BLE, Zigbee, Z-Wave, LoRaWAN, Cellular, and SDR
"""

import logging
import struct
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


class RadioProtocol(Enum):
    """Supported radio protocols"""

    BLE = "bluetooth_le"
    ZIGBEE = "zigbee"
    ZWAVE = "zwave"
    LORAWAN = "lorawan"
    CELLULAR_GSM = "cellular_gsm"
    CELLULAR_LTE = "cellular_lte"
    CELLULAR_5G = "cellular_5g"
    SDR_GENERIC = "sdr_generic"
    WIFI_2_4GHZ = "wifi_2_4ghz"
    WIFI_5GHZ = "wifi_5ghz"
    WIFI_6GHZ = "wifi_6ghz"


class DeviceType(Enum):
    """Device types for different protocols"""

    BLE_PERIPHERAL = "ble_peripheral"
    BLE_CENTRAL = "ble_central"
    ZIGBEE_COORDINATOR = "zigbee_coordinator"
    ZIGBEE_ROUTER = "zigbee_router"
    ZIGBEE_END_DEVICE = "zigbee_end_device"
    ZWAVE_CONTROLLER = "zwave_controller"
    ZWAVE_SLAVE = "zwave_slave"
    LORAWAN_GATEWAY = "lorawan_gateway"
    LORAWAN_NODE = "lorawan_node"
    CELLULAR_BASE_STATION = "cellular_base_station"
    CELLULAR_DEVICE = "cellular_device"


@dataclass
class RadioDevice:
    """Generic radio device representation"""

    device_id: str
    protocol: RadioProtocol
    device_type: DeviceType
    frequency: float
    rssi: float
    timestamp: datetime
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    firmware_version: Optional[str] = None
    capabilities: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BLEDevice:
    """Bluetooth Low Energy device"""

    address: str
    address_type: str  # 'public' or 'random'
    name: Optional[str] = None
    rssi: float = -100
    tx_power: Optional[int] = None
    manufacturer_data: bytes = b""
    service_uuids: List[str] = field(default_factory=list)
    advertisement_data: Dict[str, Any] = field(default_factory=dict)
    connectable: bool = True
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)


@dataclass
class ZigbeeDevice:
    """Zigbee device representation"""

    ieee_address: str
    network_address: int
    device_type: DeviceType
    manufacturer_code: Optional[int] = None
    power_source: str = "unknown"
    lqi: int = 0  # Link Quality Indicator
    rssi: float = -100
    parent_address: Optional[str] = None
    endpoint_list: List[int] = field(default_factory=list)
    cluster_list: List[int] = field(default_factory=list)
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)


@dataclass
class ZWaveDevice:
    """Z-Wave device representation"""

    node_id: int
    home_id: int
    device_type: DeviceType
    manufacturer_id: Optional[int] = None
    product_type: Optional[int] = None
    product_id: Optional[int] = None
    command_classes: List[int] = field(default_factory=list)
    security_level: str = "none"
    routing_slaves: List[int] = field(default_factory=list)
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)


@dataclass
class LoRaWANDevice:
    """LoRaWAN device representation"""

    dev_eui: str
    dev_addr: Optional[str] = None
    app_eui: Optional[str] = None
    spreading_factor: int = 7
    bandwidth: int = 125000
    frequency: float = 868000000
    rssi: float = -100
    snr: float = 0
    gateway_id: Optional[str] = None
    frame_counter: int = 0
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)


@dataclass
class CellularDevice:
    """Cellular device representation"""

    imsi: Optional[str] = None
    imei: Optional[str] = None
    cell_id: Optional[str] = None
    lac: Optional[str] = None  # Location Area Code
    mcc: Optional[str] = None  # Mobile Country Code
    mnc: Optional[str] = None  # Mobile Network Code
    technology: str = "unknown"  # GSM, LTE, 5G
    signal_strength: float = -100
    base_station_id: Optional[str] = None
    frequency_band: Optional[str] = None
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)


class BLEScanner:
    """Bluetooth Low Energy scanner"""

    def __init__(self):
        self.devices: Dict[str, BLEDevice] = {}
        self.scanning = False
        self.scan_thread = None
        self.callbacks: List[Callable] = []

    def start_scan(self, duration: Optional[int] = None):
        """Start BLE scanning"""
        if self.scanning:
            return

        self.scanning = True
        self.scan_thread = threading.Thread(target=self._scan_loop, args=(duration,))
        self.scan_thread.daemon = True
        self.scan_thread.start()
        logger.info("BLE scanning started")

    def stop_scan(self):
        """Stop BLE scanning"""
        self.scanning = False
        if self.scan_thread:
            self.scan_thread.join()
        logger.info("BLE scanning stopped")

    def _scan_loop(self, duration: Optional[int]):
        """Main scanning loop"""
        start_time = time.time()

        while self.scanning:
            if duration and (time.time() - start_time) > duration:
                break

            # Simulate BLE device discovery
            # In real implementation, this would interface with actual BLE hardware
            self._simulate_ble_discovery()
            time.sleep(1)

        self.scanning = False

    def _simulate_ble_discovery(self):
        """Simulate BLE device discovery"""
        # Simulate discovering devices
        simulated_devices = [
            {
                "address": "12:34:56:78:9A:BC",
                "name": "Fitness Tracker",
                "rssi": -55,
                "manufacturer_data": b"\x4c\x00\x02\x15",
                "service_uuids": ["180A", "180F"],
            },
            {
                "address": "AB:CD:EF:12:34:56",
                "name": "Smart Watch",
                "rssi": -70,
                "manufacturer_data": b"\x06\x00\x01\x09",
                "service_uuids": ["180A", "181A"],
            },
        ]

        for device_data in simulated_devices:
            self._process_advertisement(device_data)

    def _process_advertisement(self, adv_data: Dict[str, Any]):
        """Process BLE advertisement data"""
        address = adv_data["address"]

        if address not in self.devices:
            self.devices[address] = BLEDevice(
                address=address,
                address_type="public",
                name=adv_data.get("name"),
                rssi=adv_data.get("rssi", -100),
                manufacturer_data=adv_data.get("manufacturer_data", b""),
                service_uuids=adv_data.get("service_uuids", []),
            )
        else:
            # Update existing device
            device = self.devices[address]
            device.rssi = adv_data.get("rssi", device.rssi)
            device.last_seen = datetime.now()

        # Notify callbacks
        for callback in self.callbacks:
            callback(self.devices[address])

    def add_callback(self, callback: Callable):
        """Add device discovery callback"""
        self.callbacks.append(callback)

    def get_devices(self) -> List[BLEDevice]:
        """Get discovered BLE devices"""
        return list(self.devices.values())

    def parse_advertisement(self, data: bytes) -> Dict[str, Any]:
        """Parse BLE advertisement packet"""
        parsed = {}
        offset = 0

        while offset < len(data):
            if offset + 1 >= len(data):
                break

            length = data[offset]
            if length == 0 or offset + length >= len(data):
                break

            ad_type = data[offset + 1]
            ad_data = data[offset + 2 : offset + 1 + length]

            if ad_type == 0x01:  # Flags
                parsed["flags"] = ad_data[0] if ad_data else 0
            elif ad_type == 0x02:  # Incomplete List of 16-bit Service UUIDs
                parsed["service_uuids_16"] = self._parse_service_uuids(ad_data, 2)
            elif ad_type == 0x03:  # Complete List of 16-bit Service UUIDs
                parsed["service_uuids_16"] = self._parse_service_uuids(ad_data, 2)
            elif ad_type == 0x09:  # Complete Local Name
                parsed["name"] = ad_data.decode("utf-8", errors="ignore")
            elif ad_type == 0x0A:  # Tx Power Level
                parsed["tx_power"] = struct.unpack("b", ad_data)[0] if ad_data else 0
            elif ad_type == 0xFF:  # Manufacturer Specific Data
                parsed["manufacturer_data"] = ad_data

            offset += length + 1

        return parsed

    def _parse_service_uuids(self, data: bytes, uuid_length: int) -> List[str]:
        """Parse service UUIDs from advertisement data"""
        uuids = []
        for i in range(0, len(data), uuid_length):
            if i + uuid_length <= len(data):
                uuid_bytes = data[i : i + uuid_length]
                if uuid_length == 2:
                    uuid = f"{struct.unpack('<H', uuid_bytes)[0]:04X}"
                else:
                    uuid = uuid_bytes.hex().upper()
                uuids.append(uuid)
        return uuids


class ZigbeeScanner:
    """Zigbee protocol scanner"""

    def __init__(self):
        self.devices: Dict[str, ZigbeeDevice] = {}
        self.scanning = False
        self.channel = 11  # Default Zigbee channel
        self.callbacks: List[Callable] = []

    def start_scan(self, channels: List[int] = None):
        """Start Zigbee scanning"""
        if not channels:
            channels = [11, 15, 20, 25]  # Common Zigbee channels

        self.scanning = True
        logger.info(f"Zigbee scanning started on channels: {channels}")

        # Simulate Zigbee device discovery
        self._simulate_zigbee_discovery()

    def stop_scan(self):
        """Stop Zigbee scanning"""
        self.scanning = False
        logger.info("Zigbee scanning stopped")

    def _simulate_zigbee_discovery(self):
        """Simulate Zigbee device discovery"""
        simulated_devices = [
            {
                "ieee_address": "00:12:4B:00:14:B2:57:D2",
                "network_address": 0x1234,
                "device_type": DeviceType.ZIGBEE_ROUTER,
                "manufacturer_code": 0x115F,
                "lqi": 254,
                "rssi": -45,
            },
            {
                "ieee_address": "00:12:4B:00:14:B2:57:D3",
                "network_address": 0x5678,
                "device_type": DeviceType.ZIGBEE_END_DEVICE,
                "manufacturer_code": 0x115F,
                "lqi": 180,
                "rssi": -60,
            },
        ]

        for device_data in simulated_devices:
            self._process_zigbee_device(device_data)

    def _process_zigbee_device(self, device_data: Dict[str, Any]):
        """Process discovered Zigbee device"""
        ieee_address = device_data["ieee_address"]

        if ieee_address not in self.devices:
            self.devices[ieee_address] = ZigbeeDevice(
                ieee_address=ieee_address,
                network_address=device_data["network_address"],
                device_type=device_data["device_type"],
                manufacturer_code=device_data.get("manufacturer_code"),
                lqi=device_data.get("lqi", 0),
                rssi=device_data.get("rssi", -100),
            )
        else:
            # Update existing device
            device = self.devices[ieee_address]
            device.lqi = device_data.get("lqi", device.lqi)
            device.rssi = device_data.get("rssi", device.rssi)
            device.last_seen = datetime.now()

        # Notify callbacks
        for callback in self.callbacks:
            callback(self.devices[ieee_address])

    def parse_zigbee_frame(self, data: bytes) -> Optional[Dict[str, Any]]:
        """Parse Zigbee frame"""
        if len(data) < 5:
            return None

        try:
            # Basic Zigbee frame parsing
            frame_control = data[0]
            sequence_number = data[1]

            # Frame type
            frame_type = frame_control & 0x07

            # Security enabled
            security_enabled = bool(frame_control & 0x08)

            # Addressing mode
            dst_addr_mode = (frame_control >> 10) & 0x03
            src_addr_mode = (frame_control >> 14) & 0x03

            return {
                "frame_control": frame_control,
                "sequence_number": sequence_number,
                "frame_type": frame_type,
                "security_enabled": security_enabled,
                "dst_addr_mode": dst_addr_mode,
                "src_addr_mode": src_addr_mode,
                "payload": data[5:],
            }
        except Exception as e:
            logger.error(f"Error parsing Zigbee frame: {e}")
            return None

    def get_devices(self) -> List[ZigbeeDevice]:
        """Get discovered Zigbee devices"""
        return list(self.devices.values())


class ZWaveScanner:
    """Z-Wave protocol scanner"""

    def __init__(self):
        self.devices: Dict[int, ZWaveDevice] = {}
        self.scanning = False
        self.home_id = 0
        self.callbacks: List[Callable] = []

    def start_scan(self):
        """Start Z-Wave scanning"""
        self.scanning = True
        logger.info("Z-Wave scanning started")

        # Simulate Z-Wave device discovery
        self._simulate_zwave_discovery()

    def stop_scan(self):
        """Stop Z-Wave scanning"""
        self.scanning = False
        logger.info("Z-Wave scanning stopped")

    def _simulate_zwave_discovery(self):
        """Simulate Z-Wave device discovery"""
        simulated_devices = [
            {
                "node_id": 2,
                "home_id": 0x12345678,
                "device_type": DeviceType.ZWAVE_SLAVE,
                "manufacturer_id": 0x0086,
                "product_type": 0x0002,
                "product_id": 0x0001,
                "command_classes": [0x20, 0x25, 0x26, 0x70],
            },
            {
                "node_id": 3,
                "home_id": 0x12345678,
                "device_type": DeviceType.ZWAVE_SLAVE,
                "manufacturer_id": 0x0086,
                "product_type": 0x0003,
                "product_id": 0x0002,
                "command_classes": [0x20, 0x25, 0x86, 0x70],
            },
        ]

        for device_data in simulated_devices:
            self._process_zwave_device(device_data)

    def _process_zwave_device(self, device_data: Dict[str, Any]):
        """Process discovered Z-Wave device"""
        node_id = device_data["node_id"]

        if node_id not in self.devices:
            self.devices[node_id] = ZWaveDevice(
                node_id=node_id,
                home_id=device_data["home_id"],
                device_type=device_data["device_type"],
                manufacturer_id=device_data.get("manufacturer_id"),
                product_type=device_data.get("product_type"),
                product_id=device_data.get("product_id"),
                command_classes=device_data.get("command_classes", []),
            )
        else:
            # Update existing device
            device = self.devices[node_id]
            device.last_seen = datetime.now()

        # Notify callbacks
        for callback in self.callbacks:
            callback(self.devices[node_id])

    def parse_zwave_frame(self, data: bytes) -> Optional[Dict[str, Any]]:
        """Parse Z-Wave frame"""
        if len(data) < 4:
            return None

        try:
            # Basic Z-Wave frame parsing
            sof = data[0]  # Start of Frame
            length = data[1]
            frame_type = data[2]
            command_class = data[3] if len(data) > 3 else 0

            return {
                "so": sof,
                "length": length,
                "frame_type": frame_type,
                "command_class": command_class,
                "payload": data[4:] if len(data) > 4 else b"",
            }
        except Exception as e:
            logger.error(f"Error parsing Z-Wave frame: {e}")
            return None

    def get_devices(self) -> List[ZWaveDevice]:
        """Get discovered Z-Wave devices"""
        return list(self.devices.values())


class LoRaWANScanner:
    """LoRaWAN protocol scanner"""

    def __init__(self):
        self.devices: Dict[str, LoRaWANDevice] = {}
        self.scanning = False
        self.frequencies = [868100000, 868300000, 868500000]  # EU868 frequencies
        self.callbacks: List[Callable] = []

    def start_scan(self, frequencies: List[float] = None):
        """Start LoRaWAN scanning"""
        if frequencies:
            self.frequencies = frequencies

        self.scanning = True
        logger.info(f"LoRaWAN scanning started on frequencies: {self.frequencies}")

        # Simulate LoRaWAN device discovery
        self._simulate_lorawan_discovery()

    def stop_scan(self):
        """Stop LoRaWAN scanning"""
        self.scanning = False
        logger.info("LoRaWAN scanning stopped")

    def _simulate_lorawan_discovery(self):
        """Simulate LoRaWAN device discovery"""
        simulated_devices = [
            {
                "dev_eui": "70B3D57ED005B420",
                "dev_addr": "12345678",
                "spreading_factor": 7,
                "bandwidth": 125000,
                "frequency": 868100000,
                "rssi": -85,
                "snr": 8.5,
            },
            {
                "dev_eui": "70B3D57ED005B421",
                "dev_addr": "12345679",
                "spreading_factor": 10,
                "bandwidth": 125000,
                "frequency": 868300000,
                "rssi": -95,
                "snr": 5.2,
            },
        ]

        for device_data in simulated_devices:
            self._process_lorawan_device(device_data)

    def _process_lorawan_device(self, device_data: Dict[str, Any]):
        """Process discovered LoRaWAN device"""
        dev_eui = device_data["dev_eui"]

        if dev_eui not in self.devices:
            self.devices[dev_eui] = LoRaWANDevice(
                dev_eui=dev_eui,
                dev_addr=device_data.get("dev_addr"),
                spreading_factor=device_data.get("spreading_factor", 7),
                bandwidth=device_data.get("bandwidth", 125000),
                frequency=device_data.get("frequency", 868100000),
                rssi=device_data.get("rssi", -100),
                snr=device_data.get("snr", 0),
            )
        else:
            # Update existing device
            device = self.devices[dev_eui]
            device.rssi = device_data.get("rssi", device.rssi)
            device.snr = device_data.get("snr", device.snr)
            device.last_seen = datetime.now()

        # Notify callbacks
        for callback in self.callbacks:
            callback(self.devices[dev_eui])

    def parse_lorawan_frame(self, data: bytes) -> Optional[Dict[str, Any]]:
        """Parse LoRaWAN frame"""
        if len(data) < 12:
            return None

        try:
            # Basic LoRaWAN frame parsing
            mhdr = data[0]

            # Message type
            mtype = (mhdr >> 5) & 0x07

            # For uplink/downlink data messages
            if mtype in [0x02, 0x03, 0x04, 0x05]:
                dev_addr = struct.unpack("<I", data[1:5])[0]
                fctrl = data[5]
                fcnt = struct.unpack("<H", data[6:8])[0]

                return {
                    "mhdr": mhdr,
                    "mtype": mtype,
                    "dev_addr": f"{dev_addr:08X}",
                    "fctrl": fctrl,
                    "fcnt": fcnt,
                    "payload": data[8:],
                }

            return {"mhdr": mhdr, "mtype": mtype, "payload": data[1:]}
        except Exception as e:
            logger.error(f"Error parsing LoRaWAN frame: {e}")
            return None

    def get_devices(self) -> List[LoRaWANDevice]:
        """Get discovered LoRaWAN devices"""
        return list(self.devices.values())


class CellularScanner:
    """Cellular protocol scanner"""

    def __init__(self):
        self.devices: Dict[str, CellularDevice] = {}
        self.base_stations: Dict[str, CellularDevice] = {}
        self.scanning = False
        self.technologies = ["GSM", "LTE", "5G"]
        self.callbacks: List[Callable] = []

    def start_scan(self, technologies: List[str] = None):
        """Start cellular scanning"""
        if technologies:
            self.technologies = technologies

        self.scanning = True
        logger.info(f"Cellular scanning started for: {self.technologies}")

        # Simulate cellular device discovery
        self._simulate_cellular_discovery()

    def stop_scan(self):
        """Stop cellular scanning"""
        self.scanning = False
        logger.info("Cellular scanning stopped")

    def _simulate_cellular_discovery(self):
        """Simulate cellular device discovery"""
        # Base stations
        simulated_base_stations = [
            {
                "cell_id": "Cell_12345",
                "lac": "LAC_001",
                "mcc": "310",
                "mnc": "260",
                "technology": "LTE",
                "signal_strength": -75,
                "frequency_band": "Band 2 (1900 MHz)",
            },
            {
                "cell_id": "Cell_67890",
                "lac": "LAC_002",
                "mcc": "310",
                "mnc": "260",
                "technology": "5G",
                "signal_strength": -65,
                "frequency_band": "Band n41 (2500 MHz)",
            },
        ]

        # Mobile devices
        simulated_devices = [
            {
                "imsi": "310260123456789",
                "imei": "123456789012345",
                "cell_id": "Cell_12345",
                "technology": "LTE",
                "signal_strength": -85,
            },
            {
                "imsi": "310260987654321",
                "imei": "543210987654321",
                "cell_id": "Cell_67890",
                "technology": "5G",
                "signal_strength": -78,
            },
        ]

        for bs_data in simulated_base_stations:
            self._process_base_station(bs_data)

        for device_data in simulated_devices:
            self._process_cellular_device(device_data)

    def _process_base_station(self, bs_data: Dict[str, Any]):
        """Process discovered base station"""
        cell_id = bs_data["cell_id"]

        if cell_id not in self.base_stations:
            self.base_stations[cell_id] = CellularDevice(
                cell_id=cell_id,
                lac=bs_data.get("lac"),
                mcc=bs_data.get("mcc"),
                mnc=bs_data.get("mnc"),
                technology=bs_data.get("technology", "unknown"),
                signal_strength=bs_data.get("signal_strength", -100),
                frequency_band=bs_data.get("frequency_band"),
            )
        else:
            # Update existing base station
            bs = self.base_stations[cell_id]
            bs.signal_strength = bs_data.get("signal_strength", bs.signal_strength)
            bs.last_seen = datetime.now()

    def _process_cellular_device(self, device_data: Dict[str, Any]):
        """Process discovered cellular device"""
        device_id = device_data.get("imsi") or device_data.get("imei", "unknown")

        if device_id not in self.devices:
            self.devices[device_id] = CellularDevice(
                imsi=device_data.get("imsi"),
                imei=device_data.get("imei"),
                cell_id=device_data.get("cell_id"),
                technology=device_data.get("technology", "unknown"),
                signal_strength=device_data.get("signal_strength", -100),
            )
        else:
            # Update existing device
            device = self.devices[device_id]
            device.signal_strength = device_data.get(
                "signal_strength", device.signal_strength
            )
            device.last_seen = datetime.now()

        # Notify callbacks
        for callback in self.callbacks:
            callback(self.devices[device_id])

    def get_devices(self) -> List[CellularDevice]:
        """Get discovered cellular devices"""
        return list(self.devices.values())

    def get_base_stations(self) -> List[CellularDevice]:
        """Get discovered base stations"""
        return list(self.base_stations.values())


class SDRInterface:
    """Software Defined Radio interface"""

    def __init__(self):
        self.center_frequency = 2.4e9
        self.sample_rate = 2e6
        self.gain = 20
        self.running = False
        self.callbacks: List[Callable] = []

    def configure(self, center_frequency: float, sample_rate: float, gain: float):
        """Configure SDR parameters"""
        self.center_frequency = center_frequency
        self.sample_rate = sample_rate
        self.gain = gain
        logger.info(
            f"SDR configured: {center_frequency/1e6:.1f} MHz, {sample_rate/1e6:.1f} MS/s, {gain} dB"
        )

    def start_capture(self):
        """Start SDR capture"""
        self.running = True
        logger.info("SDR capture started")

        # Simulate SDR capture
        self._simulate_sdr_capture()

    def stop_capture(self):
        """Stop SDR capture"""
        self.running = False
        logger.info("SDR capture stopped")

    def _simulate_sdr_capture(self):
        """Simulate SDR capture"""
        # Generate sample IQ data
        import numpy as np

        duration = 0.001  # 1ms
        t = np.linspace(0, duration, int(self.sample_rate * duration))

        # Simulate multiple signals
        signal1 = np.exp(1j * 2 * np.pi * 1e6 * t)  # 1 MHz offset
        signal2 = 0.5 * np.exp(1j * 2 * np.pi * 5e6 * t)  # 5 MHz offset
        noise = 0.1 * (np.random.randn(len(t)) + 1j * np.random.randn(len(t)))

        iq_data = signal1 + signal2 + noise

        # Notify callbacks with IQ data
        for callback in self.callbacks:
            callback(iq_data, self.center_frequency, self.sample_rate)

    def add_callback(self, callback: Callable):
        """Add IQ data callback"""
        self.callbacks.append(callback)

    def get_spectrum(self, iq_data, nfft: int = 1024):
        """Compute power spectrum from IQ data"""
        import numpy as np

        # Compute FFT
        fft_data = np.fft.fft(iq_data, nfft)
        freqs = np.fft.fftfreq(nfft, 1 / self.sample_rate)

        # Compute power spectrum
        power_spectrum = 20 * np.log10(np.abs(fft_data) + 1e-12)

        # Shift to center frequency
        freqs_shifted = freqs + self.center_frequency

        return freqs_shifted, power_spectrum


class MultiProtocolManager:
    """Multi-protocol scanning and management"""

    def __init__(self):
        self.ble_scanner = BLEScanner()
        self.zigbee_scanner = ZigbeeScanner()
        self.zwave_scanner = ZWaveScanner()
        self.lorawan_scanner = LoRaWANScanner()
        self.cellular_scanner = CellularScanner()
        self.sdr_interface = SDRInterface()

        self.active_protocols: Set[RadioProtocol] = set()
        self.device_callbacks: List[Callable] = []
        self.all_devices: Dict[str, RadioDevice] = {}

    def start_protocol_scan(self, protocol: RadioProtocol, **kwargs):
        """Start scanning for specific protocol"""
        if protocol == RadioProtocol.BLE:
            self.ble_scanner.add_callback(self._handle_ble_device)
            self.ble_scanner.start_scan(kwargs.get("duration"))
        elif protocol == RadioProtocol.ZIGBEE:
            self.zigbee_scanner.callbacks.append(self._handle_zigbee_device)
            self.zigbee_scanner.start_scan(kwargs.get("channels"))
        elif protocol == RadioProtocol.ZWAVE:
            self.zwave_scanner.callbacks.append(self._handle_zwave_device)
            self.zwave_scanner.start_scan()
        elif protocol == RadioProtocol.LORAWAN:
            self.lorawan_scanner.callbacks.append(self._handle_lorawan_device)
            self.lorawan_scanner.start_scan(kwargs.get("frequencies"))
        elif protocol in [
            RadioProtocol.CELLULAR_GSM,
            RadioProtocol.CELLULAR_LTE,
            RadioProtocol.CELLULAR_5G,
        ]:
            self.cellular_scanner.callbacks.append(self._handle_cellular_device)
            self.cellular_scanner.start_scan(kwargs.get("technologies"))
        elif protocol == RadioProtocol.SDR_GENERIC:
            self.sdr_interface.add_callback(self._handle_sdr_data)
            self.sdr_interface.configure(
                kwargs.get("center_frequency", 2.4e9),
                kwargs.get("sample_rate", 2e6),
                kwargs.get("gain", 20),
            )
            self.sdr_interface.start_capture()

        self.active_protocols.add(protocol)
        logger.info(f"Started scanning for protocol: {protocol.value}")

    def stop_protocol_scan(self, protocol: RadioProtocol):
        """Stop scanning for specific protocol"""
        if protocol == RadioProtocol.BLE:
            self.ble_scanner.stop_scan()
        elif protocol == RadioProtocol.ZIGBEE:
            self.zigbee_scanner.stop_scan()
        elif protocol == RadioProtocol.ZWAVE:
            self.zwave_scanner.stop_scan()
        elif protocol == RadioProtocol.LORAWAN:
            self.lorawan_scanner.stop_scan()
        elif protocol in [
            RadioProtocol.CELLULAR_GSM,
            RadioProtocol.CELLULAR_LTE,
            RadioProtocol.CELLULAR_5G,
        ]:
            self.cellular_scanner.stop_scan()
        elif protocol == RadioProtocol.SDR_GENERIC:
            self.sdr_interface.stop_capture()

        self.active_protocols.discard(protocol)
        logger.info(f"Stopped scanning for protocol: {protocol.value}")

    def start_all_protocols(self):
        """Start scanning for all supported protocols"""
        for protocol in RadioProtocol:
            self.start_protocol_scan(protocol)

    def stop_all_protocols(self):
        """Stop scanning for all protocols"""
        for protocol in list(self.active_protocols):
            self.stop_protocol_scan(protocol)

    def _handle_ble_device(self, device: BLEDevice):
        """Handle discovered BLE device"""
        radio_device = RadioDevice(
            device_id=device.address,
            protocol=RadioProtocol.BLE,
            device_type=DeviceType.BLE_PERIPHERAL,
            frequency=2.4e9,
            rssi=device.rssi,
            timestamp=device.last_seen,
            metadata={
                "name": device.name,
                "address_type": device.address_type,
                "service_uuids": device.service_uuids,
                "manufacturer_data": device.manufacturer_data.hex(),
            },
        )

        self.all_devices[device.address] = radio_device
        self._notify_device_callbacks(radio_device)

    def _handle_zigbee_device(self, device: ZigbeeDevice):
        """Handle discovered Zigbee device"""
        radio_device = RadioDevice(
            device_id=device.ieee_address,
            protocol=RadioProtocol.ZIGBEE,
            device_type=device.device_type,
            frequency=2.4e9,  # Zigbee operates in 2.4 GHz
            rssi=device.rssi,
            timestamp=device.last_seen,
            metadata={
                "network_address": device.network_address,
                "manufacturer_code": device.manufacturer_code,
                "lqi": device.lqi,
                "endpoint_list": device.endpoint_list,
            },
        )

        self.all_devices[device.ieee_address] = radio_device
        self._notify_device_callbacks(radio_device)

    def _handle_zwave_device(self, device: ZWaveDevice):
        """Handle discovered Z-Wave device"""
        radio_device = RadioDevice(
            device_id=str(device.node_id),
            protocol=RadioProtocol.ZWAVE,
            device_type=device.device_type,
            frequency=868e6,  # Z-Wave frequency (EU)
            rssi=-60,  # Z-Wave doesn't typically report RSSI
            timestamp=device.last_seen,
            metadata={
                "home_id": device.home_id,
                "manufacturer_id": device.manufacturer_id,
                "product_type": device.product_type,
                "command_classes": device.command_classes,
            },
        )

        self.all_devices[str(device.node_id)] = radio_device
        self._notify_device_callbacks(radio_device)

    def _handle_lorawan_device(self, device: LoRaWANDevice):
        """Handle discovered LoRaWAN device"""
        radio_device = RadioDevice(
            device_id=device.dev_eui,
            protocol=RadioProtocol.LORAWAN,
            device_type=DeviceType.LORAWAN_NODE,
            frequency=device.frequency,
            rssi=device.rssi,
            timestamp=device.last_seen,
            metadata={
                "dev_addr": device.dev_addr,
                "spreading_factor": device.spreading_factor,
                "bandwidth": device.bandwidth,
                "snr": device.snr,
            },
        )

        self.all_devices[device.dev_eui] = radio_device
        self._notify_device_callbacks(radio_device)

    def _handle_cellular_device(self, device: CellularDevice):
        """Handle discovered cellular device"""
        device_id = device.imsi or device.imei or "unknown"
        radio_device = RadioDevice(
            device_id=device_id,
            protocol=RadioProtocol.CELLULAR_LTE,  # Default to LTE
            device_type=DeviceType.CELLULAR_DEVICE,
            frequency=1900e6,  # Default frequency
            rssi=device.signal_strength,
            timestamp=device.last_seen,
            metadata={
                "imsi": device.imsi,
                "imei": device.imei,
                "cell_id": device.cell_id,
                "technology": device.technology,
                "mcc": device.mcc,
                "mnc": device.mnc,
            },
        )

        self.all_devices[device_id] = radio_device
        self._notify_device_callbacks(radio_device)

    def _handle_sdr_data(self, iq_data, center_freq: float, sample_rate: float):
        """Handle SDR IQ data"""
        # Analyze IQ data for signals
        freqs, power_spectrum = self.sdr_interface.get_spectrum(iq_data)

        # Simple peak detection
        import numpy as np

        # Find peaks in spectrum
        threshold = np.mean(power_spectrum) + 10  # 10 dB above mean
        peaks = np.where(power_spectrum > threshold)[0]

        for peak_idx in peaks:
            freq = freqs[peak_idx]
            power = power_spectrum[peak_idx]

            # Create generic SDR device
            device_id = f"SDR_{freq/1e6:.1f}MHz"
            radio_device = RadioDevice(
                device_id=device_id,
                protocol=RadioProtocol.SDR_GENERIC,
                device_type=DeviceType.CELLULAR_DEVICE,  # Generic
                frequency=freq,
                rssi=power,
                timestamp=datetime.now(),
                metadata={
                    "center_frequency": center_freq,
                    "sample_rate": sample_rate,
                    "peak_frequency": freq,
                    "power_dbm": power,
                },
            )

            self.all_devices[device_id] = radio_device
            self._notify_device_callbacks(radio_device)

    def _notify_device_callbacks(self, device: RadioDevice):
        """Notify device discovery callbacks"""
        for callback in self.device_callbacks:
            callback(device)

    def add_device_callback(self, callback: Callable):
        """Add device discovery callback"""
        self.device_callbacks.append(callback)

    def get_all_devices(self) -> List[RadioDevice]:
        """Get all discovered devices"""
        return list(self.all_devices.values())

    def get_devices_by_protocol(self, protocol: RadioProtocol) -> List[RadioDevice]:
        """Get devices by protocol"""
        return [
            device
            for device in self.all_devices.values()
            if device.protocol == protocol
        ]

    def get_protocol_statistics(self) -> Dict[str, Any]:
        """Get protocol statistics"""
        stats = {
            "active_protocols": list(self.active_protocols),
            "total_devices": len(self.all_devices),
            "protocol_distribution": {},
        }

        # Count devices by protocol
        for device in self.all_devices.values():
            protocol = device.protocol.value
            stats["protocol_distribution"][protocol] = (
                stats["protocol_distribution"].get(protocol, 0) + 1
            )

        # Individual protocol stats
        stats["ble_devices"] = len(self.ble_scanner.get_devices())
        stats["zigbee_devices"] = len(self.zigbee_scanner.get_devices())
        stats["zwave_devices"] = len(self.zwave_scanner.get_devices())
        stats["lorawan_devices"] = len(self.lorawan_scanner.get_devices())
        stats["cellular_devices"] = len(self.cellular_scanner.get_devices())
        stats["cellular_base_stations"] = len(self.cellular_scanner.get_base_stations())

        return stats


# Example usage and testing
def test_multi_protocol_support():
    """Test multi-protocol support functionality"""
    print("Testing Multi-Protocol Support...")

    # Create multi-protocol manager
    manager = MultiProtocolManager()

    # Add device discovery callback
    def device_discovered(device: RadioDevice):
        print(f"Device discovered: {device.protocol.value} - {device.device_id}")
        print(f"  Frequency: {device.frequency/1e6:.1f} MHz")
        print(f"  RSSI: {device.rssi} dBm")
        print(f"  Type: {device.device_type.value}")

    manager.add_device_callback(device_discovered)

    # Test individual protocol scanning
    print("\nTesting BLE scanning...")
    manager.start_protocol_scan(RadioProtocol.BLE, duration=2)
    time.sleep(3)
    manager.stop_protocol_scan(RadioProtocol.BLE)

    print("\nTesting Zigbee scanning...")
    manager.start_protocol_scan(RadioProtocol.ZIGBEE, channels=[11, 15, 20])
    time.sleep(2)
    manager.stop_protocol_scan(RadioProtocol.ZIGBEE)

    print("\nTesting Z-Wave scanning...")
    manager.start_protocol_scan(RadioProtocol.ZWAVE)
    time.sleep(2)
    manager.stop_protocol_scan(RadioProtocol.ZWAVE)

    print("\nTesting LoRaWAN scanning...")
    manager.start_protocol_scan(RadioProtocol.LORAWAN)
    time.sleep(2)
    manager.stop_protocol_scan(RadioProtocol.LORAWAN)

    print("\nTesting Cellular scanning...")
    manager.start_protocol_scan(RadioProtocol.CELLULAR_LTE)
    time.sleep(2)
    manager.stop_protocol_scan(RadioProtocol.CELLULAR_LTE)

    print("\nTesting SDR interface...")
    manager.start_protocol_scan(
        RadioProtocol.SDR_GENERIC, center_frequency=2.4e9, sample_rate=2e6, gain=20
    )
    time.sleep(2)
    manager.stop_protocol_scan(RadioProtocol.SDR_GENERIC)

    # Get statistics
    stats = manager.get_protocol_statistics()
    print("\nProtocol Statistics:")
    print(f"  Total devices: {stats['total_devices']}")
    print(f"  Active protocols: {stats['active_protocols']}")
    print(f"  Protocol distribution: {stats['protocol_distribution']}")
    print(f"  BLE devices: {stats['ble_devices']}")
    print(f"  Zigbee devices: {stats['zigbee_devices']}")
    print(f"  Z-Wave devices: {stats['zwave_devices']}")
    print(f"  LoRaWAN devices: {stats['lorawan_devices']}")
    print(f"  Cellular devices: {stats['cellular_devices']}")

    # Test getting devices by protocol
    ble_devices = manager.get_devices_by_protocol(RadioProtocol.BLE)
    print(f"\nBLE devices found: {len(ble_devices)}")
    for device in ble_devices:
        print(f"  {device.device_id}: {device.metadata.get('name', 'Unknown')}")

    print("Multi-Protocol Support test completed!")


if __name__ == "__main__":
    test_multi_protocol_support()
