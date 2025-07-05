#!/usr/bin/env python3
"""
Direction Finding Module for PiWardrive
Advanced, configurable direction finding functionality.
"""

from .algorithms import (
    BeamformingProcessor,
    MUSICProcessor,
    PathLossCalculator,
    RSSTriangulation,
    SignalMapper,
)
from .config import (
    DFAlgorithm,
    DFConfigManager,
    DFConfiguration,
    PathLossModel,
    config_manager,
    get_algorithm_config,
    get_df_config,
    set_df_algorithm,
    update_df_config,
)
from .core import (
    AngleEstimate,
    DFEngine,
    DFMeasurement,
    DFQuality,
    DFResult,
    PositionEstimate,
)
from .hardware import AntennaArrayManager, HardwareDetector, WiFiAdapterManager
from .integration import (
    DFIntegrationManager,
    add_df_measurement,
    configure_df,
    get_df_hardware_capabilities,
    get_df_integration_manager,
    get_df_status,
    initialize_df_integration,
    start_df_integration,
    stop_df_integration,
)

__all__ = [
    # Configuration
    "DFConfiguration",
    "DFConfigManager",
    "DFAlgorithm",
    "PathLossModel",
    "get_df_config",
    "update_df_config",
    "set_df_algorithm",
    "get_algorithm_config",
    "config_manager",
    # Core engine
    "DFEngine",
    "DFResult",
    "PositionEstimate",
    "AngleEstimate",
    "DFMeasurement",
    "DFQuality",
    # Algorithms
    "RSSTriangulation",
    "MUSICProcessor",
    "BeamformingProcessor",
    "PathLossCalculator",
    "SignalMapper",
    # Hardware
    "WiFiAdapterManager",
    "AntennaArrayManager",
    "HardwareDetector",
    # Integration
    "DFIntegrationManager",
    "get_df_integration_manager",
    "initialize_df_integration",
    "start_df_integration",
    "stop_df_integration",
    "add_df_measurement",
    "get_df_status",
    "configure_d",
    "get_df_hardware_capabilities",
]
