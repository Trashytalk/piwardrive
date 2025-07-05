#!/usr/bin/env python3
"""
Direction Finding Module for PiWardrive
Advanced, configurable direction finding functionality.
"""

from .config import (
    DFConfiguration,
    DFConfigManager,
    DFAlgorithm,
    PathLossModel,
    get_df_config,
    update_df_config,
    set_df_algorithm,
    get_algorithm_config,
    config_manager
)

from .core import (
    DFEngine,
    DFResult,
    PositionEstimate,
    AngleEstimate,
    DFMeasurement,
    DFQuality
)

from .algorithms import (
    RSSTriangulation,
    MUSICProcessor,
    BeamformingProcessor,
    PathLossCalculator,
    SignalMapper
)

from .hardware import (
    WiFiAdapterManager,
    AntennaArrayManager,
    HardwareDetector
)

from .integration import (
    DFIntegrationManager,
    get_df_integration_manager,
    initialize_df_integration,
    start_df_integration,
    stop_df_integration,
    add_df_measurement,
    get_df_status,
    configure_df,
    get_df_hardware_capabilities
)

__all__ = [
    # Configuration
    'DFConfiguration',
    'DFConfigManager',
    'DFAlgorithm',
    'PathLossModel',
    'get_df_config',
    'update_df_config',
    'set_df_algorithm',
    'get_algorithm_config',
    'config_manager',
    
    # Core engine
    'DFEngine',
    'DFResult',
    'PositionEstimate',
    'AngleEstimate',
    'DFMeasurement',
    'DFQuality',
    
    # Algorithms
    'RSSTriangulation',
    'MUSICProcessor',
    'BeamformingProcessor',
    'PathLossCalculator',
    'SignalMapper',
    
    # Hardware
    'WiFiAdapterManager',
    'AntennaArrayManager',
    'HardwareDetector',
    
    # Integration
    'DFIntegrationManager',
    'get_df_integration_manager',
    'initialize_df_integration',
    'start_df_integration',
    'stop_df_integration',
    'add_df_measurement',
    'get_df_status',
    'configure_df',
    'get_df_hardware_capabilities',
]
