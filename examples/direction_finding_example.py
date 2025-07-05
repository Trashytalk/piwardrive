#!/usr/bin/env python3
"""
Example usage of PiWardrive Direction Finding System
Demonstrates basic setup and usage of the DF functionality.
"""

import asyncio
import logging
import time
from typing import Any, Dict

import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import DF components
from piwardrive.direction_finding import (
    DFAlgorithm,
    PathLossModel,
    add_df_measurement,
    configure_df,
    get_df_hardware_capabilities,
    get_df_status,
    initialize_df_integration,
    start_df_integration,
    stop_df_integration,
)


async def main():
    """Main example function."""
    logger.info("Starting PiWardrive Direction Finding Example")

    # Initialize DF integration
    _df_manager = initialize_df_integration()

    # Configure DF system
    configure_df_system()

    # Check hardware capabilities
    check_hardware_capabilities()

    # Start DF integration
    await start_df_integration()

    try:
        # Add example measurements
        await add_example_measurements()

        # Wait for processing
        await asyncio.sleep(2)

        # Check status
        status = get_df_status()
        logger.info(f"DF Status: {status}")

        # Demonstrate configuration changes
        await demonstrate_configuration_changes()

        # Run for a while to see processing
        logger.info("Running DF system for 10 seconds...")
        await asyncio.sleep(10)

    finally:
        # Stop DF integration
        await stop_df_integration()
        logger.info("DF system stopped")


def configure_df_system():
    """Configure the DF system."""
    logger.info("Configuring DF system...")

    # Basic configuration
    config_updates = {
        'primary_algorithm': DFAlgorithm.RSS_TRIANGULATION,
        'enabled_algorithms': [DFAlgorithm.RSS_TRIANGULATION],
        'enable_logging': True,
        'log_level': 'INFO'
    }

    try:
        configure_df(config_updates)
        logger.info("DF system configured successfully")
    except Exception as e:
        logger.error(f"Error configuring DF system: {e}")


def check_hardware_capabilities():
    """Check hardware capabilities."""
    logger.info("Checking hardware capabilities...")

    try:
        capabilities = get_df_hardware_capabilities()

        logger.info(f"WiFi Adapters: {len(capabilities.get('wifi_adapters', []))}")
        logger.info(f"Monitor Mode Adapters: {capabilities.get('monitor_mode_adapters',
            0)}")
        logger.info(f"DF Capable: {capabilities.get('df_capable', False)}")

        if capabilities.get('recommended_setup'):
            logger.info("Recommendations:")
            for rec in capabilities['recommended_setup']:
                logger.info(f"  - {rec}")

    except Exception as e:
        logger.error(f"Error checking hardware capabilities: {e}")

async def add_example_measurements():
    """Add example measurements to the DF system."""
    logger.info("Adding example measurements...")

    # Example access points (would come from actual WiFi scanning)
    access_points = [
        {'bssid': '00:11:22:33:44:55', 'tx_power': 20, 'position': (40.7128, -74.0060)},
        {'bssid': '00:11:22:33:44:66', 'tx_power': 20, 'position': (40.7138, -74.0070)},
        {'bssid': '00:11:22:33:44:77', 'tx_power': 20, 'position': (40.7118, -74.0050)},
        {'bssid': '00:11:22:33:44:88', 'tx_power': 20, 'position': (40.7148, -74.0080)},
    ]

    # Simulate measurements from different positions
    measurement_positions = [
        (40.7130, -74.0065),  # Position 1
        (40.7125, -74.0062),  # Position 2
        (40.7135, -74.0068),  # Position 3
    ]

    for pos_idx, position in enumerate(measurement_positions):
        logger.info(f"Adding measurements from position {pos_idx + 1}")

        for ap in access_points:
            # Calculate distance for realistic RSSI
            distance = calculate_distance(position, ap['position'])

            # Simulate path loss
            rssi = simulate_rssi(ap['tx_power'], distance)

            # Add some noise
            rssi += np.random.normal(0, 2)

            # Create measurement
            measurement = {
                'signal_strength': rssi,
                'frequency': 2.4e9,
                'bssid': ap['bssid'],
                'position': position,
                'timestamp': time.time()
            }

            add_df_measurement(measurement)

            # Small delay between measurements
            await asyncio.sleep(0.1)


def calculate_distance(pos1, pos2):
    """Calculate distance between two positions (simplified)."""
    lat1, lon1 = pos1
    lat2, lon2 = pos2

    # Simple Euclidean distance (not accurate for real GPS coordinates)
    return np.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2) * 111320  # Rough conversion to meters


def simulate_rssi(tx_power, distance):
    """Simulate RSSI based on distance."""
    if distance <= 0:
        return tx_power

    # Free space path loss model
    frequency = 2.4e9
    path_loss = 20 * np.log10(distance) + 20 * np.log10(frequency) + 20 * np.log10(4 * np.pi / 3e8)

    return tx_power - path_loss

async def demonstrate_configuration_changes():
    """Demonstrate dynamic configuration changes."""
    logger.info("Demonstrating configuration changes...")

    # Change to different path loss model
    config_updates = {
        'path_loss': {
            'model_type': PathLossModel.INDOOR
        }
    }

    try:
        configure_df(config_updates)
        logger.info("Changed path loss model to INDOOR")

        # Wait a bit
        await asyncio.sleep(1)

        # Change triangulation settings
        config_updates = {
            'triangulation': {
                'min_access_points': 4,
                'max_position_error': 25.0
            }
        }

        configure_df(config_updates)
        logger.info("Updated triangulation settings")

    except Exception as e:
        logger.error(f"Error changing configuration: {e}")


class DFResultHandler:
    """Example result handler for DF results."""

    def __init__(self):
        self.results_received = 0
        self.positions_estimated = 0
        self.angles_estimated = 0

    async def handle_result(self, event_type: str, data: Dict[str, Any]):
        """Handle DF results."""
        if event_type == 'df_result':
            self.results_received += 1

            if data.get('position'):
                self.positions_estimated += 1
                position = data['position']
                logger.info(f"Position estimate: {position['latitude']:.6f},
                    {position['longitude']:.6f} "
                           f"(accuracy: {position['accuracy']:.1f}m,
                               confidence: {position['confidence']:.2f})")

            if data.get('angle'):
                self.angles_estimated += 1
                angle = data['angle']
                logger.info(f"Angle estimate: {angle['azimuth']:.1f}° "
                           f"(accuracy: {angle['accuracy']:.1f}°,
                               confidence: {angle['confidence']:.2f})")

        elif event_type == 'integration_started':
            logger.info("DF integration started")

        elif event_type == 'integration_stopped':
            logger.info("DF integration stopped")

        elif event_type == 'calibration_completed':
            success = data.get('success', False)
            logger.info(f"Calibration completed: {'Success' if success else 'Failed'}")

    def get_statistics(self) -> Dict[str, int]:
        """Get statistics."""
        return {
            'results_received': self.results_received,
            'positions_estimated': self.positions_estimated,
            'angles_estimated': self.angles_estimated
        }

async def demonstrate_advanced_features():
    """Demonstrate advanced DF features."""
    logger.info("Demonstrating advanced DF features...")

    # Setup result handler
    result_handler = DFResultHandler()

    # Get DF manager and add callback
    _df_manager = initialize_df_integration()
    df_manager.add_result_callback(result_handler.handle_result)

    # Demonstrate calibration
    calibration_data = {
        'access_points': [
            {'bssid': '00:11:22:33:44:55',
                'latitude': 40.7128,
                'longitude': -74.0060,
                'tx_power': 20},
                
            {'bssid': '00:11:22:33:44:66',
                'latitude': 40.7138,
                'longitude': -74.0070,
                'tx_power': 20},
                
            {'bssid': '00:11:22:33:44:77',
                'latitude': 40.7118,
                'longitude': -74.0050,
                'tx_power': 20},
                
        ],
        'path_loss_points': [
            {'distance': 10, 'rssi': -40, 'tx_power': 20},
            {'distance': 20, 'rssi': -50, 'tx_power': 20},
            {'distance': 50, 'rssi': -65, 'tx_power': 20},
        ]
    }

    logger.info("Starting calibration...")
    success = await df_manager.calibrate_df_system(calibration_data)
    logger.info(f"Calibration result: {'Success' if success else 'Failed'}")

    # Wait for results
    await asyncio.sleep(2)

    # Show statistics
    stats = result_handler.get_statistics()
    logger.info(f"Result handler statistics: {stats}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Example interrupted by user")
    except Exception as e:
        logger.error(f"Example failed: {e}")
        raise
