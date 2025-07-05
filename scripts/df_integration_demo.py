#!/usr/bin/env python3
"""
PiWardrive Direction Finding Integration Script
Demonstrates integration of DF functionality with the main PiWardrive application.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from piwardrive.direction_finding import (
    DFConfiguration,
    DFConfigManager,
    DFAlgorithm,
    PathLossModel,
    DFEngine,
    DFMeasurement,
    RSSTriangulation,
    PathLossCalculator,
    HardwareDetector,
    DFIntegrationManager,
    initialize_df_integration,
    get_df_config,
    configure_df,
    get_df_hardware_capabilities
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PiWardriveDF:
    """Main integration class for PiWardrive DF functionality."""
    
    def __init__(self):
        self.df_manager = None
        self.config_manager = DFConfigManager()
        self.is_initialized = False
        
    async def initialize(self):
        """Initialize the DF system."""
        logger.info("Initializing PiWardrive Direction Finding system...")
        
        try:
            # Check hardware capabilities
            capabilities = get_df_hardware_capabilities()
            logger.info(f"Hardware capabilities: {capabilities}")
            
            # Initialize DF integration
            self.df_manager = initialize_df_integration()
            
            # Configure DF system
            await self._configure_system()
            
            # Start DF processing
            await self.df_manager.start()
            
            self.is_initialized = True
            logger.info("DF system initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize DF system: {e}")
            raise
    
    async def _configure_system(self):
        """Configure the DF system with optimal settings."""
        logger.info("Configuring DF system...")
        
        # Basic configuration
        config_updates = {
            'primary_algorithm': DFAlgorithm.RSS_TRIANGULATION,
            'enabled_algorithms': [DFAlgorithm.RSS_TRIANGULATION],
            'enable_logging': True,
            'log_level': 'INFO'
        }
        
        configure_df(config_updates)
        
        # Configure triangulation
        self.config_manager.update_triangulation_config(
            min_access_points=3,
            max_position_error=50.0,
            use_weighted_least_squares=True,
            outlier_rejection=True,
            confidence_threshold=0.7
        )
        
        # Configure path loss
        self.config_manager.update_path_loss_config(
            model_type=PathLossModel.FREE_SPACE,
            enable_adaptive_calibration=True,
            path_loss_exponent=2.0
        )
        
        logger.info("DF system configured")
    
    async def add_scan_result(self, scan_result):
        """Add a scan result to the DF system."""
        if not self.is_initialized:
            logger.warning("DF system not initialized")
            return
        
        try:
            # Convert scan result to DF measurement
            measurement = {
                'signal_strength': scan_result.get('signal_strength', -100),
                'frequency': scan_result.get('frequency', 2.4e9),
                'bssid': scan_result.get('bssid', ''),
                'timestamp': scan_result.get('timestamp', 0),
                'position': scan_result.get('position')
            }
            
            self.df_manager.add_measurement(measurement)
            
        except Exception as e:
            logger.error(f"Error adding scan result: {e}")
    
    def get_status(self):
        """Get DF system status."""
        if not self.is_initialized:
            return {'status': 'not_initialized'}
        
        return self.df_manager.get_integration_status()
    
    async def shutdown(self):
        """Shutdown the DF system."""
        if self.df_manager:
            await self.df_manager.stop()
        logger.info("DF system shut down")


async def demonstration():
    """Demonstrate the DF system functionality."""
    logger.info("Starting PiWardrive DF demonstration...")
    
    # Create DF system instance
    df_system = PiWardriveDF()
    
    try:
        # Initialize system
        await df_system.initialize()
        
        # Simulate scan results
        sample_scan_results = [
            {
                'bssid': '00:11:22:33:44:55',
                'signal_strength': -45.0,
                'frequency': 2.4e9,
                'timestamp': 1234567890.0,
                'position': (40.7128, -74.0060)
            },
            {
                'bssid': '00:11:22:33:44:66',
                'signal_strength': -50.0,
                'frequency': 2.4e9,
                'timestamp': 1234567890.1,
                'position': (40.7128, -74.0060)
            },
            {
                'bssid': '00:11:22:33:44:77',
                'signal_strength': -55.0,
                'frequency': 2.4e9,
                'timestamp': 1234567890.2,
                'position': (40.7128, -74.0060)
            }
        ]
        
        # Add scan results
        for scan_result in sample_scan_results:
            await df_system.add_scan_result(scan_result)
            logger.info(f"Added scan result for {scan_result['bssid']}")
        
        # Wait for processing
        await asyncio.sleep(2)
        
        # Get status
        status = df_system.get_status()
        logger.info(f"DF system status: {status}")
        
        # Run for a few seconds
        logger.info("Running demonstration for 5 seconds...")
        await asyncio.sleep(5)
        
    except Exception as e:
        logger.error(f"Demonstration failed: {e}")
        
    finally:
        # Shutdown
        await df_system.shutdown()


def test_individual_components():
    """Test individual DF components."""
    logger.info("Testing individual DF components...")
    
    # Test configuration
    logger.info("Testing configuration...")
    config = DFConfiguration()
    assert config.primary_algorithm == DFAlgorithm.RSS_TRIANGULATION
    logger.info("✓ Configuration test passed")
    
    # Test path loss calculator
    logger.info("Testing path loss calculator...")
    from piwardrive.direction_finding.config import PathLossConfig
    path_loss_config = PathLossConfig()
    calculator = PathLossCalculator(path_loss_config)
    distance = calculator.calculate_distance(-60, 20)
    assert distance > 0
    logger.info(f"✓ Path loss calculator test passed (distance: {distance:.2f}m)")
    
    # Test measurement creation
    logger.info("Testing measurement creation...")
    measurement = DFMeasurement(
        signal_strength=-60.0,
        frequency=2.4e9,
        bssid='00:11:22:33:44:55'
    )
    assert measurement.signal_strength == -60.0
    logger.info("✓ Measurement creation test passed")
    
    # Test hardware detection
    logger.info("Testing hardware detection...")
    capabilities = HardwareDetector.get_hardware_capabilities()
    assert 'wifi_adapters' in capabilities
    logger.info("✓ Hardware detection test passed")
    
    logger.info("All individual component tests passed!")


def main():
    """Main function."""
    logger.info("PiWardrive Direction Finding Integration")
    logger.info("=" * 50)
    
    # Test individual components first
    test_individual_components()
    
    # Run demonstration
    try:
        asyncio.run(demonstration())
    except KeyboardInterrupt:
        logger.info("Demonstration interrupted by user")
    except Exception as e:
        logger.error(f"Demonstration failed: {e}")
        sys.exit(1)
    
    logger.info("Demo completed successfully!")


if __name__ == "__main__":
    main()
