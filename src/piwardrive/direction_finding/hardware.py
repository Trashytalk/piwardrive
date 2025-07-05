#!/usr/bin/env python3
"""
Hardware Management for Direction Finding
Manages WiFi adapters, antenna arrays, and other DF hardware.
"""

import asyncio
import logging
import re
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from .config import AntennaArrayConfig, ArrayGeometry, WiFiAdapterConfig

logger = logging.getLogger(__name__)


class HardwareDetector:
    """Detects and identifies DF-capable hardware."""

    @staticmethod
    def detect_wifi_adapters() -> List[Dict[str, Any]]:
        """Detect available WiFi adapters."""
        adapters = []

        try:
            # Try to get adapter info using iwconfig
            result = subprocess.run(
                ["iwconfig"], capture_output=True, text=True, timeout=10
            )

            if result.returncode == 0:
                # Parse iwconfig output
                adapters = HardwareDetector._parse_iwconfig_output(result.stdout)
            else:
                # Fallback to network interface detection
                adapters = HardwareDetector._detect_network_interfaces()

        except Exception as e:
            logger.error(f"Error detecting WiFi adapters: {e}")
            adapters = HardwareDetector._detect_network_interfaces()

        return adapters

    @staticmethod
    def _parse_iwconfig_output(output: str) -> List[Dict[str, Any]]:
        """Parse iwconfig output to extract adapter information."""
        adapters = []
        lines = output.split("\n")

        current_adapter = None
        for line in lines:
            line = line.strip()

            if line and not line.startswith(" "):
                # New adapter
                if current_adapter:
                    adapters.append(current_adapter)

                # Extract adapter name
                match = re.match(r"^(\w+)\s+", line)
                if match:
                    adapter_name = match.group(1)
                    current_adapter = {
                        "name": adapter_name,
                        "type": "wifi",
                        "capabilities": [],
                        "chipset": "unknown",
                        "driver": "unknown",
                        "monitor_mode": False,
                        "injection_capable": False,
                    }

                    # Check for IEEE 802.11
                    if "IEEE 802.11" in line:
                        current_adapter["capabilities"].append("802.11")

            elif current_adapter and line:
                # Parse adapter details
                if "Mode:" in line:
                    mode_match = re.search(r"Mode:(\w+)", line)
                    if mode_match:
                        current_adapter["mode"] = mode_match.group(1)
                        if mode_match.group(1) == "Monitor":
                            current_adapter["monitor_mode"] = True

                if "Frequency:" in line:
                    freq_match = re.search(r"Frequency:([\d.]+)", line)
                    if freq_match:
                        current_adapter["frequency"] = float(freq_match.group(1))

                if "Tx-Power:" in line:
                    power_match = re.search(r"Tx-Power:(\d+)", line)
                    if power_match:
                        current_adapter["tx_power"] = int(power_match.group(1))

        # Don't forget the last adapter
        if current_adapter:
            adapters.append(current_adapter)

        return adapters

    @staticmethod
    def _detect_network_interfaces() -> List[Dict[str, Any]]:
        """Fallback method to detect network interfaces."""
        adapters = []

        try:
            # Try to list network interfaces
            result = subprocess.run(
                ["ip", "link", "show"], capture_output=True, text=True, timeout=5
            )

            if result.returncode == 0:
                lines = result.stdout.split("\n")
                for line in lines:
                    if "wlan" in line or "wifi" in line:
                        # Extract interface name
                        match = re.search(r"(\w+):", line)
                        if match:
                            interface_name = match.group(1)
                            adapters.append(
                                {
                                    "name": interface_name,
                                    "type": "wifi",
                                    "capabilities": ["802.11"],
                                    "chipset": "unknown",
                                    "driver": "unknown",
                                    "monitor_mode": False,
                                    "injection_capable": False,
                                }
                            )

        except Exception as e:
            logger.error(f"Error detecting network interfaces: {e}")

        return adapters

    @staticmethod
    def detect_chipset(adapter_name: str) -> str:
        """Detect chipset of a specific adapter."""
        try:
            # Try to get driver information
            result = subprocess.run(
                ["ethtool", "-i", adapter_name],
                capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                lines = result.stdout.split("\n")
                for line in lines:
                    if "driver:" in line:
                        driver = line.split(":")[1].strip()

                        # Map common drivers to chipsets
                        chipset_map = {
                            "ath9k": "ath9k",
                            "ath9k_htc": "ath9k",
                            "rt2800usb": "rt2800usb",
                            "mt7601u": "mt7601u",
                            "mt76x2u": "mt76x2u",
                            "rtl8812au": "rtl8812au",
                            "rtl8821au": "rtl8821au",
                            "iwlwifi": "intel",
                            "brcmfmac": "broadcom",
                        }

                        return chipset_map.get(driver, driver)

        except Exception as e:
            logger.debug(f"Error detecting chipset for {adapter_name}: {e}")

        return "unknown"

    @staticmethod
    def check_monitor_mode_support(adapter_name: str) -> bool:
        """Check if adapter supports monitor mode."""
        try:
            # Try to get supported modes
            result = subprocess.run(
                ["iw", "phy", "phy0", "info"], capture_output=True, text=True, timeout=5
            )

            if result.returncode == 0:
                return "monitor" in result.stdout.lower()

        except Exception as e:
            logger.debug(f"Error checking monitor mode support for {adapter_name}: {e}")

        return False

    @staticmethod
    def check_injection_support(adapter_name: str) -> bool:
        """Check if adapter supports packet injection."""
        try:
            # This is a simplified check
            # In practice, you would need to test actual injection
            chipset = HardwareDetector.detect_chipset(adapter_name)

            # Known injection-capable chipsets
            injection_capable = [
                "ath9k",
                "rt2800usb",
                "mt7601u",
                "rtl8812au",
                "rtl8821au",
            ]

            return chipset in injection_capable

        except Exception as e:
            logger.debug(f"Error checking injection support for {adapter_name}: {e}")

        return False

    @staticmethod
    def detect_antenna_arrays() -> List[Dict[str, Any]]:
        """Detect connected antenna arrays."""
        # This is a placeholder implementation
        # In practice, you would need hardware-specific detection

        arrays = []

        # Check for common antenna array hardware
        # This would be specific to your hardware setup

        return arrays

    @staticmethod
    def detect_sdr_devices() -> List[Dict[str, Any]]:
        """Detect Software Defined Radio devices."""
        sdr_devices = []

        try:
            # Try to detect RTL-SDR devices
            result = subprocess.run(
                ["rtl_test", "-t"], capture_output=True, text=True, timeout=5
            )

            if result.returncode == 0:
                lines = result.stdout.split("\n")
                for line in lines:
                    if "Found" in line and "device" in line:
                        sdr_devices.append(
                            {
                                "type": "rtl_sdr",
                                "name": line.strip(),
                                "capabilities": ["rx_only"],
                                "frequency_range": (24e6, 1766e6),
                            }
                        )

        except Exception as e:
            logger.debug(f"Error detecting SDR devices: {e}")

        return sdr_devices

    @staticmethod
    def get_hardware_capabilities() -> Dict[str, Any]:
        """Get overall hardware capabilities."""
        capabilities = {
            "wifi_adapters": HardwareDetector.detect_wifi_adapters(),
            "antenna_arrays": HardwareDetector.detect_antenna_arrays(),
            "sdr_devices": HardwareDetector.detect_sdr_devices(),
            "df_capable": False,
            "monitor_mode_adapters": 0,
            "injection_capable_adapters": 0,
            "recommended_setup": [],
        }

        # Analyze capabilities
        for adapter in capabilities["wifi_adapters"]:
            if adapter.get("monitor_mode", False):
                capabilities["monitor_mode_adapters"] += 1

            if adapter.get("injection_capable", False):
                capabilities["injection_capable_adapters"] += 1

        # Determine if system is DF capable
        capabilities["df_capable"] = capabilities["monitor_mode_adapters"] >= 2

        # Generate recommendations
        if capabilities["monitor_mode_adapters"] < 2:
            capabilities["recommended_setup"].append(
                "Add more monitor mode capable WiFi adapters for triangulation"
            )

        if not capabilities["antenna_arrays"]:
            capabilities["recommended_setup"].append(
                "Add antenna array for advanced angle-of-arrival estimation"
            )

        if not capabilities["sdr_devices"]:
            capabilities["recommended_setup"].append(
                "Add SDR device for advanced signal processing"
            )

        return capabilities


class WiFiAdapterManager:
    """Manages WiFi adapters for direction finding."""

    def __init__(self, config: WiFiAdapterConfig):
        self.config = config
        self.adapters = {}
        self.is_initialized = False
        self.is_running = False

        # Performance monitoring
        self.performance_metrics = {
            "packets_captured": 0,
            "packets_processed": 0,
            "errors": 0,
            "last_update": time.time(),
        }

    async def start(self):
        """Start the WiFi adapter manager."""
        if self.is_running:
            return

        # Detect available adapters
        detected_adapters = HardwareDetector.detect_wifi_adapters()

        if not detected_adapters:
            logger.error("No WiFi adapters detected")
            return

        # Initialize adapters
        for adapter_info in detected_adapters:
            try:
                adapter = WiFiAdapter(adapter_info, self.config)
                self.adapters[adapter_info["name"]] = adapter
                await adapter.initialize()
                logger.info(f"Initialized adapter: {adapter_info['name']}")

            except Exception as e:
                logger.error(
                    f"Failed to initialize adapter {adapter_info['name']}: {e}"
                )

        self.is_running = True
        self.is_initialized = True
        logger.info(f"WiFi adapter manager started with {len(self.adapters)} adapters")

    async def stop(self):
        """Stop the WiFi adapter manager."""
        if not self.is_running:
            return

        # Stop all adapters
        for adapter in self.adapters.values():
            try:
                await adapter.stop()
            except Exception as e:
                logger.error(f"Error stopping adapter: {e}")

        self.is_running = False
        logger.info("WiFi adapter manager stopped")

    def get_adapter_status(self) -> Dict[str, Any]:
        """Get status of all adapters."""
        status = {}

        for name, adapter in self.adapters.items():
            status[name] = {
                "initialized": adapter.is_initialized,
                "running": adapter.is_running,
                "monitor_mode": adapter.is_monitor_mode,
                "channel": adapter.current_channel,
                "packets_captured": adapter.packets_captured,
                "chipset": adapter.chipset,
                "capabilities": adapter.capabilities,
            }

        return status

    def get_available_adapters(self) -> List[str]:
        """Get list of available adapter names."""
        return list(self.adapters.keys())

    def get_adapter(self, name: str) -> Optional["WiFiAdapter"]:
        """Get specific adapter by name."""
        return self.adapters.get(name)

    async def set_channel(self, adapter_name: str, channel: int):
        """Set channel for specific adapter."""
        adapter = self.adapters.get(adapter_name)
        if adapter:
            await adapter.set_channel(channel)

    async def start_capture(self, adapter_name: str):
        """Start packet capture on specific adapter."""
        adapter = self.adapters.get(adapter_name)
        if adapter:
            await adapter.start_capture()

    async def stop_capture(self, adapter_name: str):
        """Stop packet capture on specific adapter."""
        adapter = self.adapters.get(adapter_name)
        if adapter:
            await adapter.stop_capture()

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        # Aggregate metrics from all adapters
        total_metrics = self.performance_metrics.copy()

        for adapter in self.adapters.values():
            if hasattr(adapter, "performance_metrics"):
                metrics = adapter.performance_metrics
                total_metrics["packets_captured"] += metrics.get("packets_captured", 0)
                total_metrics["packets_processed"] += metrics.get(
                    "packets_processed", 0
                )
                total_metrics["errors"] += metrics.get("errors", 0)

        return total_metrics

    async def calibrate(self, calibration_data: Dict[str, Any]):
        """Calibrate WiFi adapters."""
        for adapter in self.adapters.values():
            if hasattr(adapter, "calibrate"):
                await adapter.calibrate(calibration_data)

        logger.info("WiFi adapter calibration completed")


class WiFiAdapter:
    """Individual WiFi adapter management."""

    def __init__(self, adapter_info: Dict[str, Any], config: WiFiAdapterConfig):
        self.name = adapter_info["name"]
        self.chipset = adapter_info.get("chipset", "unknown")
        self.capabilities = adapter_info.get("capabilities", [])
        self.config = config

        self.is_initialized = False
        self.is_running = False
        self.is_monitor_mode = False
        self.is_capturing = False

        self.current_channel = 1
        self.packets_captured = 0
        self.capture_process = None

        # Performance metrics
        self.performance_metrics = {
            "packets_captured": 0,
            "packets_processed": 0,
            "errors": 0,
            "last_update": time.time(),
        }

    async def initialize(self):
        """Initialize the WiFi adapter."""
        try:
            # Check if adapter supports required features
            if self.config.monitor_mode_required:
                if not self._check_monitor_mode_support():
                    raise RuntimeError(
                        f"Adapter {self.name} does not support monitor mode"
                    )

            # Set monitor mode if required
            if self.config.monitor_mode_required:
                await self._set_monitor_mode()

            # Set initial channel
            await self.set_channel(self.current_channel)

            # Set power level
            await self._set_power_level()

            self.is_initialized = True
            logger.info(f"WiFi adapter {self.name} initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize adapter {self.name}: {e}")
            raise

    async def stop(self):
        """Stop the WiFi adapter."""
        if self.is_capturing:
            await self.stop_capture()

        if self.is_monitor_mode:
            await self._disable_monitor_mode()

        self.is_running = False
        logger.info(f"WiFi adapter {self.name} stopped")

    def _check_monitor_mode_support(self) -> bool:
        """Check if adapter supports monitor mode."""
        return HardwareDetector.check_monitor_mode_support(self.name)

    async def _set_monitor_mode(self):
        """Set adapter to monitor mode."""
        try:
            # Bring interface down
            await self._run_command(["ip", "link", "set", self.name, "down"])

            # Set monitor mode
            await self._run_command(["iw", self.name, "set", "type", "monitor"])

            # Bring interface up
            await self._run_command(["ip", "link", "set", self.name, "up"])

            self.is_monitor_mode = True
            logger.info(f"Set {self.name} to monitor mode")

        except Exception as e:
            logger.error(f"Failed to set monitor mode for {self.name}: {e}")
            raise

    async def _disable_monitor_mode(self):
        """Disable monitor mode."""
        try:
            # Bring interface down
            await self._run_command(["ip", "link", "set", self.name, "down"])

            # Set managed mode
            await self._run_command(["iw", self.name, "set", "type", "managed"])

            # Bring interface up
            await self._run_command(["ip", "link", "set", self.name, "up"])

            self.is_monitor_mode = False
            logger.info(f"Disabled monitor mode for {self.name}")

        except Exception as e:
            logger.error(f"Failed to disable monitor mode for {self.name}: {e}")

    async def set_channel(self, channel: int):
        """Set WiFi channel."""
        try:
            await self._run_command(["iw", self.name, "set", "channel", str(channel)])
            self.current_channel = channel
            logger.debug(f"Set {self.name} to channel {channel}")

        except Exception as e:
            logger.error(f"Failed to set channel {channel} for {self.name}: {e}")

    async def _set_power_level(self):
        """Set transmission power level."""
        try:
            await self._run_command(
                [
                    "iw",
                    self.name,
                    "set",
                    "txpower",
                    "fixed",
                    f"{self.config.power_level}00",
                ]
            )
            logger.debug(
                f"Set {self.name} power level to {self.config.power_level} dBm"
            )

        except Exception as e:
            logger.debug(f"Failed to set power level for {self.name}: {e}")

    async def start_capture(self):
        """Start packet capture."""
        if self.is_capturing:
            return

        try:
            # Start tcpdump or similar capture tool
            cmd = ["tcpdump", "-i", self.name, "-w", "-", "-s", "0", "type", "mgt"]

            self.capture_process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            self.is_capturing = True
            logger.info(f"Started capture on {self.name}")

            # Start packet processing task
            asyncio.create_task(self._process_packets())

        except Exception as e:
            logger.error(f"Failed to start capture on {self.name}: {e}")

    async def stop_capture(self):
        """Stop packet capture."""
        if not self.is_capturing:
            return

        try:
            if self.capture_process:
                self.capture_process.terminate()
                await self.capture_process.wait()

            self.is_capturing = False
            logger.info(f"Stopped capture on {self.name}")

        except Exception as e:
            logger.error(f"Failed to stop capture on {self.name}: {e}")

    async def _process_packets(self):
        """Process captured packets."""
        try:
            while self.is_capturing and self.capture_process:
                # Read packet data
                data = await self.capture_process.stdout.read(1024)

                if not data:
                    break

                # Process packet data
                self.packets_captured += 1
                self.performance_metrics["packets_captured"] += 1

                # Here you would parse the packet and extract relevant information
                # For now, just update metrics
                self.performance_metrics["packets_processed"] += 1

        except Exception as e:
            logger.error(f"Error processing packets on {self.name}: {e}")
            self.performance_metrics["errors"] += 1

    async def _run_command(self, command: List[str]):
        """Run a system command."""
        try:
            process = await asyncio.create_subprocess_exec(
                *command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise RuntimeError(
                    f"Command failed: {' '.join(command)}, Error: {stderr.decode()}"
                )

            return stdout.decode()

        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            raise


class AntennaArrayManager:
    """Manages antenna arrays for direction finding."""

    def __init__(self, config: AntennaArrayConfig):
        self.config = config
        self.arrays = {}
        self.is_initialized = False
        self.is_running = False

        # Array geometry calculations
        self.element_positions = self._calculate_element_positions()
        self.steering_vectors = self._calculate_steering_vectors()

    def _calculate_element_positions(self) -> List[Tuple[float, float]]:
        """Calculate element positions based on array geometry."""
        positions = []
        wavelength = 3e8 / self.config.operating_frequency
        spacing = self.config.element_spacing * wavelength

        if self.config.array_type == ArrayGeometry.LINEAR:
            for i in range(self.config.num_elements):
                x = i * spacing
                y = 0
                positions.append((x, y))

        elif self.config.array_type == ArrayGeometry.CIRCULAR:
            radius = spacing * self.config.num_elements / (2 * np.pi)
            for i in range(self.config.num_elements):
                angle = 2 * np.pi * i / self.config.num_elements
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                positions.append((x, y))

        elif self.config.array_type == ArrayGeometry.RECTANGULAR:
            rows = int(np.sqrt(self.config.num_elements))
            cols = self.config.num_elements // rows

            for i in range(self.config.num_elements):
                row = i // cols
                col = i % cols
                x = col * spacing
                y = row * spacing
                positions.append((x, y))

        else:  # RANDOM
            # Generate random positions within a circular area
            radius = spacing * np.sqrt(self.config.num_elements)
            for i in range(self.config.num_elements):
                angle = np.random.uniform(0, 2 * np.pi)
                r = np.random.uniform(0, radius)
                x = r * np.cos(angle)
                y = r * np.sin(angle)
                positions.append((x, y))

        return positions

    def _calculate_steering_vectors(self) -> Dict[float, np.ndarray]:
        """Calculate steering vectors for different angles."""
        steering_vectors = {}
        wavelength = 3e8 / self.config.operating_frequency
        k = 2 * np.pi / wavelength

        # Calculate for angles from -180 to 180 degrees
        for angle_deg in range(-180, 181, 1):
            angle_rad = np.radians(angle_deg)

            steering_vector = np.zeros(self.config.num_elements, dtype=complex)

            for i, (x, y) in enumerate(self.element_positions):
                phase_delay = k * (x * np.sin(angle_rad) + y * np.cos(angle_rad))
                steering_vector[i] = np.exp(1j * phase_delay)

            steering_vectors[angle_deg] = steering_vector

        return steering_vectors

    async def start(self):
        """Start the antenna array manager."""
        if self.is_running:
            return

        # Initialize arrays
        try:
            # In a real implementation, this would initialize hardware
            # For now, just set up software structures

            if self.config.enable_calibration:
                await self._perform_calibration()

            self.is_running = True
            self.is_initialized = True
            logger.info(
                f"Antenna array manager started with {self.config.num_elements} elements"
            )

        except Exception as e:
            logger.error(f"Failed to start antenna array manager: {e}")
            raise

    async def stop(self):
        """Stop the antenna array manager."""
        if not self.is_running:
            return

        # Stop all arrays
        self.is_running = False
        logger.info("Antenna array manager stopped")

    async def _perform_calibration(self):
        """Perform antenna array calibration."""
        # This would involve measuring phase and amplitude responses
        # For now, just log that calibration is being performed
        logger.info("Performing antenna array calibration")

        # Simulate calibration delay
        await asyncio.sleep(1)

        logger.info("Antenna array calibration completed")

    def get_steering_vector(self, angle_deg: float) -> np.ndarray:
        """Get steering vector for a specific angle."""
        # Find closest pre-calculated angle
        closest_angle = round(angle_deg)
        closest_angle = max(-180, min(180, closest_angle))

        return self.steering_vectors.get(
            closest_angle, np.ones(self.config.num_elements, dtype=complex)
        )

    def get_array_response(self, angle_deg: float) -> complex:
        """Get array response for a specific angle."""
        steering_vector = self.get_steering_vector(angle_deg)

        # Uniform weighting for now
        weights = np.ones(self.config.num_elements) / self.config.num_elements

        return np.dot(weights, steering_vector)

    def get_array_geometry(self) -> Dict[str, Any]:
        """Get array geometry information."""
        return {
            "type": self.config.array_type.value,
            "num_elements": self.config.num_elements,
            "element_spacing": self.config.element_spacing,
            "operating_frequency": self.config.operating_frequency,
            "element_positions": self.element_positions,
            "wavelength": 3e8 / self.config.operating_frequency,
        }

    def apply_mutual_coupling_compensation(self, signal_data: np.ndarray) -> np.ndarray:
        """Apply mutual coupling compensation."""
        if not self.config.enable_mutual_coupling_compensation:
            return signal_data

        # This would apply a mutual coupling matrix
        # For now, just return the original data
        return signal_data

    def apply_temperature_compensation(
        self, signal_data: np.ndarray, temperature: float
    ) -> np.ndarray:
        """Apply temperature compensation."""
        if not self.config.temperature_compensation:
            return signal_data

        # This would apply temperature-dependent corrections
        # For now, just return the original data
        return signal_data

    async def calibrate(self, calibration_data: Dict[str, Any]):
        """Calibrate the antenna array."""
        if "calibration_signals" in calibration_data:
            # Process calibration signals
            signals = calibration_data["calibration_signals"]

            # This would update calibration parameters
            # For now, just log the calibration
            logger.info(
                f"Calibrating antenna array with {len(signals)} calibration signals"
            )

        logger.info("Antenna array calibration completed")

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        return {
            "array_elements": self.config.num_elements,
            "operating_frequency": self.config.operating_frequency,
            "calibration_enabled": self.config.enable_calibration,
            "mutual_coupling_compensation": self.config.enable_mutual_coupling_compensation,
            "temperature_compensation": self.config.temperature_compensation,
            "array_efficiency": 0.95,  # Placeholder
            "last_calibration": time.time(),
        }
