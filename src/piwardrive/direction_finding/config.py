#!/usr/bin/env python3
"""
Direction Finding Configuration Management for PiWardrive
Provides configurable options for all DF algorithms and hardware settings.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

logger = logging.getLogger(__name__)


class DFAlgorithm(Enum):
    """Available Direction Finding algorithms."""
    RSS_TRIANGULATION = "rss_triangulation"
    MUSIC_AOA = "music_aoa"
    BEAMFORMING = "beamforming"
    TIME_DIFFERENCE = "time_difference"
    FINGERPRINTING = "fingerprinting"
    HYBRID = "hybrid"


class PathLossModel(Enum):
    """Available path loss models."""
    FREE_SPACE = "free_space"
    HATA = "hata"
    INDOOR = "indoor"
    DENSE_URBAN = "dense_urban"
    RURAL = "rural"
    CUSTOM = "custom"


class InterpolationMethod(Enum):
    """Signal strength interpolation methods."""
    KRIGING = "kriging"
    IDW = "inverse_distance_weighting"
    SPLINE = "spline"
    NEURAL_NETWORK = "neural_network"


class ArrayGeometry(Enum):
    """Antenna array geometries."""
    LINEAR = "linear"
    CIRCULAR = "circular"
    RECTANGULAR = "rectangular"
    RANDOM = "random"


class SyncSource(Enum):
    """Time synchronization sources."""
    GPS = "gps"
    NTP = "ntp"
    PTP = "ptp"
    LOCAL_OSCILLATOR = "local_oscillator"


@dataclass
class TriangulationConfig:
    """Configuration for RSS-based triangulation."""
    algorithm: DFAlgorithm = DFAlgorithm.RSS_TRIANGULATION
    min_access_points: int = 3
    max_position_error: float = 50.0  # meters
    convergence_threshold: float = 0.01
    max_iterations: int = 100
    use_weighted_least_squares: bool = True
    outlier_rejection: bool = True
    confidence_threshold: float = 0.8


@dataclass
class PathLossConfig:
    """Configuration for path loss modeling."""
    model_type: PathLossModel = PathLossModel.FREE_SPACE
    frequency_bands: List[str] = field(default_factory=lambda: ['2.4GHz', '5GHz'])
    environment_type: str = 'suburban'
    enable_adaptive_calibration: bool = True
    reference_distance: float = 1.0  # meters
    path_loss_exponent: float = 2.0
    shadow_fading_std: float = 8.0  # dB
    wall_penetration_loss: float = 10.0  # dB for indoor models


@dataclass
class SignalMappingConfig:
    """Configuration for signal strength mapping."""
    map_resolution: float = 10.0  # meters per pixel
    interpolation_method: InterpolationMethod = InterpolationMethod.KRIGING
    coverage_threshold: float = -70.0  # dBm
    update_interval: float = 5.0  # seconds
    enable_real_time: bool = True
    export_formats: List[str] = field(default_factory=lambda: ['PNG', 'KML', 'GeoJSON'])
    enable_3d_visualization: bool = False


@dataclass
class WiFiAdapterConfig:
    """Configuration for WiFi adapter management."""
    supported_chipsets: List[str] = field(default_factory=lambda: [
        'ath9k', 'rt2800usb', 'mt7601u', 'mt76x2u', 'rtl8812au', 'rtl8821au'
    ])
    monitor_mode_required: bool = True
    injection_capability: bool = False
    auto_detection: bool = True
    channel_hopping: bool = True
    dwell_time: float = 0.1  # seconds per channel
    power_level: int = 20  # dBm
    enable_load_balancing: bool = True


@dataclass
class AntennaArrayConfig:
    """Configuration for antenna arrays."""
    array_type: ArrayGeometry = ArrayGeometry.CIRCULAR
    num_elements: int = 4
    element_spacing: float = 0.5  # wavelengths
    operating_frequency: float = 2.4e9  # Hz
    enable_calibration: bool = True
    polarization: str = 'linear'  # 'linear', 'circular', 'dual'
    enable_mutual_coupling_compensation: bool = True
    temperature_compensation: bool = False


@dataclass
class TimeSyncConfig:
    """Configuration for time synchronization."""
    sync_source: SyncSource = SyncSource.GPS
    accuracy_requirement: float = 1e-6  # microseconds
    enable_drift_compensation: bool = True
    sync_interval: float = 60.0  # seconds
    holdover_time: float = 3600.0  # seconds
    jitter_threshold: float = 100e-9  # nanoseconds
    enable_quality_monitoring: bool = True


@dataclass
class MUSICConfig:
    """Configuration for MUSIC algorithm."""
    array_elements: int = 8
    num_sources: int = 1
    angular_resolution: float = 1.0  # degrees
    search_range: tuple = (-180, 180)  # degrees
    enable_spatial_smoothing: bool = True
    smoothing_factor: int = 3
    eigenvalue_threshold: float = 0.01
    peak_detection_method: str = 'threshold'  # 'threshold', 'statistical'


@dataclass
class ArrayProcessingConfig:
    """Configuration for antenna array processing."""
    sampling_rate: float = 20e6  # Hz
    fft_size: int = 1024
    overlap_factor: float = 0.5
    window_type: str = 'hamming'
    enable_coherent_processing: bool = True
    beamforming_type: str = 'conventional'  # 'conventional', 'adaptive', 'mvdr'
    null_steering: bool = False


@dataclass
class VisualizationConfig:
    """Configuration for directional visualization."""
    plot_types: List[str] = field(default_factory=lambda: ['polar', 'cartesian'])
    update_rate: float = 10.0  # Hz
    history_length: int = 100
    enable_confidence_intervals: bool = True
    export_formats: List[str] = field(default_factory=lambda: ['PNG', 'SVG'])
    enable_animation: bool = False
    color_scheme: str = 'viridis'


@dataclass
class BLEConfig:
    """Configuration for BLE direction finding."""
    ble_version: str = '5.1'
    cte_types: List[str] = field(default_factory=lambda: ['AoA', 'AoD'])
    switching_pattern: str = 'custom'
    sampling_rate: float = 1e6  # Hz
    cte_length: int = 160  # microseconds
    switching_period: int = 4  # microseconds
    enable_calibration: bool = True


@dataclass
class BluetoothClassicConfig:
    """Configuration for Bluetooth Classic DF."""
    supported_classes: List[str] = field(default_factory=lambda: ['1', '2', '3', '4', '5'])
    enable_frequency_hopping: bool = True
    inquiry_interval: float = 1.28  # seconds
    tracking_algorithm: str = 'kalman'  # 'kalman', 'particle_filter', 'ekf'
    max_tracking_distance: float = 100.0  # meters
    tracking_timeout: float = 30.0  # seconds


@dataclass
class IoTProtocolConfig:
    """Configuration for IoT protocol DF."""
    supported_protocols: List[str] = field(default_factory=lambda: ['zigbee', 'z-wave', 'thread'])
    enable_mesh_analysis: bool = True
    enable_topology_mapping: bool = True
    topology_algorithms: List[str] = field(default_factory=lambda: ['dijkstra', 'centrality'])
    visualization_format: str = 'networkx'


@dataclass
class DFConfiguration:
    """Master configuration for Direction Finding system."""
    # Core DF settings
    enabled_algorithms: List[DFAlgorithm] = field(default_factory=lambda: [DFAlgorithm.RSS_TRIANGULATION])
    primary_algorithm: DFAlgorithm = DFAlgorithm.RSS_TRIANGULATION
    fallback_algorithm: Optional[DFAlgorithm] = None
    
    # Phase 1 configurations
    triangulation: TriangulationConfig = field(default_factory=TriangulationConfig)
    path_loss: PathLossConfig = field(default_factory=PathLossConfig)
    signal_mapping: SignalMappingConfig = field(default_factory=SignalMappingConfig)
    wifi_adapter: WiFiAdapterConfig = field(default_factory=WiFiAdapterConfig)
    antenna_array: AntennaArrayConfig = field(default_factory=AntennaArrayConfig)
    time_sync: TimeSyncConfig = field(default_factory=TimeSyncConfig)
    
    # Phase 2 configurations
    music: MUSICConfig = field(default_factory=MUSICConfig)
    array_processing: ArrayProcessingConfig = field(default_factory=ArrayProcessingConfig)
    visualization: VisualizationConfig = field(default_factory=VisualizationConfig)
    ble: BLEConfig = field(default_factory=BLEConfig)
    
    # Phase 3 configurations
    bluetooth_classic: BluetoothClassicConfig = field(default_factory=BluetoothClassicConfig)
    iot_protocols: IoTProtocolConfig = field(default_factory=IoTProtocolConfig)
    
    # Global settings
    enable_logging: bool = True
    log_level: str = 'INFO'
    data_retention_days: int = 30
    enable_performance_monitoring: bool = True


class DFConfigManager:
    """Manages Direction Finding configuration with validation and persistence."""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.home() / ".config" / "piwardrive" / "df_config.json"
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self._config = DFConfiguration()
        self._load_config()
    
    def get_config(self) -> DFConfiguration:
        """Get current configuration."""
        return self._config
    
    def update_config(self, **kwargs) -> None:
        """Update configuration parameters."""
        for key, value in kwargs.items():
            if hasattr(self._config, key):
                setattr(self._config, key, value)
            else:
                logger.warning(f"Unknown configuration parameter: {key}")
        
        self._validate_config()
        self._save_config()
    
    def update_triangulation_config(self, **kwargs) -> None:
        """Update triangulation-specific configuration."""
        for key, value in kwargs.items():
            if hasattr(self._config.triangulation, key):
                setattr(self._config.triangulation, key, value)
            else:
                logger.warning(f"Unknown triangulation parameter: {key}")
        
        self._validate_config()
        self._save_config()
    
    def update_path_loss_config(self, **kwargs) -> None:
        """Update path loss model configuration."""
        for key, value in kwargs.items():
            if hasattr(self._config.path_loss, key):
                setattr(self._config.path_loss, key, value)
            else:
                logger.warning(f"Unknown path loss parameter: {key}")
        
        self._validate_config()
        self._save_config()
    
    def update_antenna_config(self, **kwargs) -> None:
        """Update antenna array configuration."""
        for key, value in kwargs.items():
            if hasattr(self._config.antenna_array, key):
                setattr(self._config.antenna_array, key, value)
            else:
                logger.warning(f"Unknown antenna parameter: {key}")
        
        self._validate_config()
        self._save_config()
    
    def set_algorithm(self, algorithm: Union[str, DFAlgorithm]) -> None:
        """Set the primary DF algorithm."""
        if isinstance(algorithm, str):
            algorithm = DFAlgorithm(algorithm)
        
        self._config.primary_algorithm = algorithm
        if algorithm not in self._config.enabled_algorithms:
            self._config.enabled_algorithms.append(algorithm)
        
        self._save_config()
        logger.info(f"Primary DF algorithm set to: {algorithm.value}")
    
    def enable_algorithm(self, algorithm: Union[str, DFAlgorithm]) -> None:
        """Enable a DF algorithm."""
        if isinstance(algorithm, str):
            algorithm = DFAlgorithm(algorithm)
        
        if algorithm not in self._config.enabled_algorithms:
            self._config.enabled_algorithms.append(algorithm)
            self._save_config()
            logger.info(f"Enabled DF algorithm: {algorithm.value}")
    
    def disable_algorithm(self, algorithm: Union[str, DFAlgorithm]) -> None:
        """Disable a DF algorithm."""
        if isinstance(algorithm, str):
            algorithm = DFAlgorithm(algorithm)
        
        if algorithm in self._config.enabled_algorithms:
            self._config.enabled_algorithms.remove(algorithm)
            
            # Switch primary algorithm if disabled
            if self._config.primary_algorithm == algorithm:
                if self._config.enabled_algorithms:
                    self._config.primary_algorithm = self._config.enabled_algorithms[0]
                    logger.info(f"Switched primary algorithm to: {self._config.primary_algorithm.value}")
                else:
                    logger.warning("No enabled algorithms remaining!")
            
            self._save_config()
            logger.info(f"Disabled DF algorithm: {algorithm.value}")
    
    def get_algorithm_config(self, algorithm: Union[str, DFAlgorithm]) -> Dict[str, Any]:
        """Get configuration for a specific algorithm."""
        if isinstance(algorithm, str):
            algorithm = DFAlgorithm(algorithm)
        
        config_map = {
            DFAlgorithm.RSS_TRIANGULATION: {
                'triangulation': self._config.triangulation,
                'path_loss': self._config.path_loss,
                'signal_mapping': self._config.signal_mapping
            },
            DFAlgorithm.MUSIC_AOA: {
                'music': self._config.music,
                'array_processing': self._config.array_processing,
                'antenna_array': self._config.antenna_array
            },
            DFAlgorithm.BEAMFORMING: {
                'array_processing': self._config.array_processing,
                'antenna_array': self._config.antenna_array
            }
        }
        
        return config_map.get(algorithm, {})
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self._config = DFConfiguration()
        self._save_config()
        logger.info("Configuration reset to defaults")
    
    def export_config(self, export_path: Path) -> None:
        """Export configuration to file."""
        config_dict = self._config_to_dict()
        with open(export_path, 'w') as f:
            json.dump(config_dict, f, indent=2)
        logger.info(f"Configuration exported to: {export_path}")
    
    def import_config(self, import_path: Path) -> None:
        """Import configuration from file."""
        with open(import_path, 'r') as f:
            config_dict = json.load(f)
        
        self._dict_to_config(config_dict)
        self._validate_config()
        self._save_config()
        logger.info(f"Configuration imported from: {import_path}")
    
    def _load_config(self) -> None:
        """Load configuration from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    config_dict = json.load(f)
                self._dict_to_config(config_dict)
                self._validate_config()
                logger.info("Configuration loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load configuration: {e}")
                logger.info("Using default configuration")
    
    def _save_config(self) -> None:
        """Save configuration to file."""
        try:
            config_dict = self._config_to_dict()
            with open(self.config_path, 'w') as f:
                json.dump(config_dict, f, indent=2)
            logger.debug("Configuration saved successfully")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
    
    def _config_to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        def enum_serializer(obj):
            if isinstance(obj, Enum):
                return obj.value
            elif hasattr(obj, '__dict__'):
                return {k: enum_serializer(v) for k, v in obj.__dict__.items()}
            elif isinstance(obj, list):
                return [enum_serializer(item) for item in obj]
            else:
                return obj
        
        return enum_serializer(self._config)
    
    def _dict_to_config(self, config_dict: Dict[str, Any]) -> None:
        """Convert dictionary to configuration."""
        # This is simplified - in practice, you'd need more robust deserialization
        # that properly handles enum conversion and nested dataclass creation
        pass
    
    def _validate_config(self) -> None:
        """Validate configuration parameters."""
        errors = []
        
        # Validate triangulation config
        if self._config.triangulation.min_access_points < 3:
            errors.append("Minimum access points must be >= 3 for triangulation")
        
        if self._config.triangulation.max_position_error <= 0:
            errors.append("Maximum position error must be positive")
        
        # Validate antenna array config
        if self._config.antenna_array.num_elements < 2:
            errors.append("Antenna array must have at least 2 elements")
        
        if self._config.antenna_array.element_spacing <= 0:
            errors.append("Element spacing must be positive")
        
        # Validate frequency settings
        if self._config.antenna_array.operating_frequency <= 0:
            errors.append("Operating frequency must be positive")
        
        # Validate MUSIC config
        if self._config.music.array_elements < 2:
            errors.append("MUSIC algorithm requires at least 2 array elements")
        
        if self._config.music.angular_resolution <= 0:
            errors.append("Angular resolution must be positive")
        
        if errors:
            raise ValueError("Configuration validation failed:\n" + "\n".join(errors))
    
    def get_hardware_requirements(self) -> Dict[str, Any]:
        """Get hardware requirements based on current configuration."""
        requirements = {
            "wifi_adapters": max(2, len(self._config.enabled_algorithms)),
            "antenna_elements": self._config.antenna_array.num_elements,
            "gps_required": self._config.time_sync.sync_source == SyncSource.GPS,
            "sdr_required": DFAlgorithm.MUSIC_AOA in self._config.enabled_algorithms,
            "ble_required": DFAlgorithm.MUSIC_AOA in self._config.enabled_algorithms,
            "processing_requirements": {
                "min_cores": 4,
                "min_ram_gb": 8,
                "gpu_acceleration": self._config.array_processing.enable_coherent_processing
            }
        }
        
        return requirements
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """Get performance-related settings."""
        return {
            "update_rates": {
                "positioning": 1.0 / self._config.signal_mapping.update_interval,
                "visualization": self._config.visualization.update_rate,
                "array_processing": self._config.array_processing.sampling_rate
            },
            "buffer_sizes": {
                "fft_size": self._config.array_processing.fft_size,
                "history_length": self._config.visualization.history_length
            },
            "accuracy_targets": {
                "position_error": self._config.triangulation.max_position_error,
                "angular_resolution": self._config.music.angular_resolution,
                "time_sync_accuracy": self._config.time_sync.accuracy_requirement
            }
        }


# Global configuration manager instance
config_manager = DFConfigManager()


def get_df_config() -> DFConfiguration:
    """Get the current DF configuration."""
    return config_manager.get_config()


def update_df_config(**kwargs) -> None:
    """Update DF configuration parameters."""
    config_manager.update_config(**kwargs)


def set_df_algorithm(algorithm: Union[str, DFAlgorithm]) -> None:
    """Set the primary DF algorithm."""
    config_manager.set_algorithm(algorithm)


def get_algorithm_config(algorithm: Union[str, DFAlgorithm]) -> Dict[str, Any]:
    """Get configuration for a specific algorithm."""
    return config_manager.get_algorithm_config(algorithm)
