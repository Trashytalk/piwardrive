#!/usr/bin/env python3
"""
Direction Finding Integration for PiWardrive
Integrates DF functionality with the main PiWardrive application.
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any, Callable
import json
from pathlib import Path

from .core import DFEngine, DFMeasurement, DFResult
from .config import DFConfiguration, get_df_config, config_manager
from .hardware import HardwareDetector

logger = logging.getLogger(__name__)


class DFIntegrationManager:
    """Manages integration between DF system and PiWardrive."""
    
    def __init__(self, piwardrive_app=None):
        self.piwardrive_app = piwardrive_app
        self.df_engine = None
        self.is_running = False
        
        # Integration settings
        self.auto_start = True
        self.real_time_processing = True
        self.result_callbacks = []
        self.measurement_buffer = []
        self.buffer_size = 1000
        
        # Performance tracking
        self.integration_metrics = {
            'total_measurements': 0,
            'processed_measurements': 0,
            'successful_estimates': 0,
            'failed_estimates': 0,
            'average_processing_time': 0.0,
            'last_update': time.time()
        }
        
        # Initialize DF engine
        self._initialize_df_engine()
    
    def _initialize_df_engine(self):
        """Initialize the DF engine."""
        try:
            config = get_df_config()
            self.df_engine = DFEngine(config)
            logger.info("DF engine initialized for integration")
        except Exception as e:
            logger.error(f"Failed to initialize DF engine: {e}")
    
    async def start(self):
        """Start the DF integration."""
        if self.is_running:
            logger.warning("DF integration already running")
            return
        
        if not self.df_engine:
            logger.error("DF engine not initialized")
            return
        
        try:
            # Start DF engine
            await self.df_engine.start()
            
            # Start background processing task
            if self.real_time_processing:
                asyncio.create_task(self._process_measurements_loop())
            
            self.is_running = True
            logger.info("DF integration started")
            
            # Notify callbacks
            await self._notify_callbacks('integration_started', {})
            
        except Exception as e:
            logger.error(f"Failed to start DF integration: {e}")
            raise
    
    async def stop(self):
        """Stop the DF integration."""
        if not self.is_running:
            return
        
        try:
            # Stop DF engine
            if self.df_engine:
                await self.df_engine.stop()
            
            self.is_running = False
            logger.info("DF integration stopped")
            
            # Notify callbacks
            await self._notify_callbacks('integration_stopped', {})
            
        except Exception as e:
            logger.error(f"Error stopping DF integration: {e}")
    
    def add_measurement(self, measurement_data: Dict[str, Any]):
        """Add a measurement to the DF system."""
        try:
            # Convert measurement data to DFMeasurement
            measurement = self._create_df_measurement(measurement_data)
            
            if measurement:
                self.measurement_buffer.append(measurement)
                self.integration_metrics['total_measurements'] += 1
                
                # Limit buffer size
                if len(self.measurement_buffer) > self.buffer_size:
                    self.measurement_buffer.pop(0)
                
                # Process immediately if not in real-time mode
                if not self.real_time_processing:
                    asyncio.create_task(self._process_single_measurement(measurement))
        
        except Exception as e:
            logger.error(f"Error adding measurement: {e}")
    
    def _create_df_measurement(self, data: Dict[str, Any]) -> Optional[DFMeasurement]:
        """Create DFMeasurement from measurement data."""
        try:
            required_fields = ['signal_strength', 'frequency', 'bssid']
            
            if not all(field in data for field in required_fields):
                logger.warning(f"Measurement missing required fields: {required_fields}")
                return None
            
            measurement = DFMeasurement(
                signal_strength=data['signal_strength'],
                frequency=data['frequency'],
                bssid=data['bssid'],
                timestamp=data.get('timestamp', time.time()),
                position=data.get('position'),
                angle=data.get('angle'),
                phase=data.get('phase'),
                iq_data=data.get('iq_data')
            )
            
            return measurement
            
        except Exception as e:
            logger.error(f"Error creating DF measurement: {e}")
            return None
    
    async def _process_measurements_loop(self):
        """Background loop for processing measurements."""
        while self.is_running:
            try:
                if self.measurement_buffer:
                    # Process batch of measurements
                    batch = self.measurement_buffer.copy()
                    self.measurement_buffer.clear()
                    
                    await self._process_measurement_batch(batch)
                
                # Sleep to prevent busy waiting
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"Error in measurement processing loop: {e}")
                await asyncio.sleep(1)
    
    async def _process_measurement_batch(self, measurements: List[DFMeasurement]):
        """Process a batch of measurements."""
        if not measurements:
            return
        
        try:
            start_time = time.time()
            
            # Process measurements through DF engine
            results = await self.df_engine.process_measurements(measurements)
            
            processing_time = time.time() - start_time
            
            # Update metrics
            self.integration_metrics['processed_measurements'] += len(measurements)
            self.integration_metrics['successful_estimates'] += len(results)
            self.integration_metrics['failed_estimates'] += len(measurements) - len(results)
            
            # Update average processing time
            self._update_average_processing_time(processing_time)
            
            # Handle results
            for result in results:
                await self._handle_df_result(result)
                
        except Exception as e:
            logger.error(f"Error processing measurement batch: {e}")
            self.integration_metrics['failed_estimates'] += len(measurements)
    
    async def _process_single_measurement(self, measurement: DFMeasurement):
        """Process a single measurement."""
        await self._process_measurement_batch([measurement])
    
    async def _handle_df_result(self, result: DFResult):
        """Handle a DF result."""
        try:
            # Convert result to format expected by PiWardrive
            result_data = self._convert_df_result(result)
            
            # Notify callbacks
            await self._notify_callbacks('df_result', result_data)
            
            # Integrate with PiWardrive systems
            if self.piwardrive_app:
                await self._integrate_with_piwardrive(result_data)
                
        except Exception as e:
            logger.error(f"Error handling DF result: {e}")
    
    def _convert_df_result(self, result: DFResult) -> Dict[str, Any]:
        """Convert DFResult to dictionary format."""
        try:
            return {
                'target_bssid': result.target_bssid,
                'position': result.position.to_dict() if result.position else None,
                'angle': result.angle.to_dict() if result.angle else None,
                'processing_time': result.processing_time,
                'metadata': result.metadata,
                'timestamp': time.time()
            }
        except Exception as e:
            logger.error(f"Error converting DF result: {e}")
            return {}
    
    async def _integrate_with_piwardrive(self, result_data: Dict[str, Any]):
        """Integrate DF result with PiWardrive systems."""
        try:
            # Update database with position estimates
            if result_data.get('position'):
                await self._update_position_database(result_data)
            
            # Update visualization
            if hasattr(self.piwardrive_app, 'update_visualization'):
                await self.piwardrive_app.update_visualization(result_data)
            
            # Trigger alerts if configured
            await self._check_alerts(result_data)
            
        except Exception as e:
            logger.error(f"Error integrating with PiWardrive: {e}")
    
    async def _update_position_database(self, result_data: Dict[str, Any]):
        """Update position database with DF results."""
        try:
            # This would integrate with PiWardrive's database system
            position = result_data['position']
            
            if position and position.get('confidence', 0) > 0.5:
                # High confidence position estimate
                logger.info(f"High confidence position estimate: {position}")
                
                # Here you would update the database
                # For now, just log the position
                
        except Exception as e:
            logger.error(f"Error updating position database: {e}")
    
    async def _check_alerts(self, result_data: Dict[str, Any]):
        """Check if any alerts should be triggered."""
        try:
            # Check for geofencing alerts
            position = result_data.get('position')
            if position:
                lat = position.get('latitude')
                lon = position.get('longitude')
                
                if lat and lon:
                    # Check if position is in restricted area
                    # This would integrate with PiWardrive's geofencing system
                    pass
            
            # Check for unusual signal patterns
            # This would integrate with PiWardrive's anomaly detection
            
        except Exception as e:
            logger.error(f"Error checking alerts: {e}")
    
    def _update_average_processing_time(self, processing_time: float):
        """Update average processing time."""
        current_avg = self.integration_metrics['average_processing_time']
        total_processed = self.integration_metrics['processed_measurements']
        
        if total_processed > 0:
            self.integration_metrics['average_processing_time'] = (
                (current_avg * (total_processed - 1) + processing_time) / total_processed
            )
        else:
            self.integration_metrics['average_processing_time'] = processing_time
    
    def add_result_callback(self, callback: Callable):
        """Add a callback for DF results."""
        self.result_callbacks.append(callback)
    
    def remove_result_callback(self, callback: Callable):
        """Remove a callback for DF results."""
        if callback in self.result_callbacks:
            self.result_callbacks.remove(callback)
    
    async def _notify_callbacks(self, event_type: str, data: Dict[str, Any]):
        """Notify all registered callbacks."""
        for callback in self.result_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event_type, data)
                else:
                    callback(event_type, data)
            except Exception as e:
                logger.error(f"Error in callback: {e}")
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get integration status."""
        return {
            'running': self.is_running,
            'df_engine_status': self.df_engine.get_algorithm_status() if self.df_engine else {},
            'hardware_status': self.df_engine.get_hardware_status() if self.df_engine else {},
            'buffer_size': len(self.measurement_buffer),
            'metrics': self.integration_metrics.copy()
        }
    
    def get_integration_metrics(self) -> Dict[str, Any]:
        """Get integration performance metrics."""
        return self.integration_metrics.copy()
    
    def configure_df_system(self, config_updates: Dict[str, Any]):
        """Configure the DF system."""
        try:
            # Update configuration
            config_manager.update_config(**config_updates)
            
            # Update DF engine configuration
            if self.df_engine:
                new_config = get_df_config()
                self.df_engine.update_config(new_config)
            
            logger.info("DF system configuration updated")
            
        except Exception as e:
            logger.error(f"Error configuring DF system: {e}")
            raise
    
    def get_hardware_capabilities(self) -> Dict[str, Any]:
        """Get hardware capabilities."""
        return HardwareDetector.get_hardware_capabilities()
    
    def get_supported_algorithms(self) -> List[str]:
        """Get supported DF algorithms."""
        if self.df_engine:
            return self.df_engine.get_supported_algorithms()
        return []
    
    def get_enabled_algorithms(self) -> List[str]:
        """Get enabled DF algorithms."""
        if self.df_engine:
            return self.df_engine.get_enabled_algorithms()
        return []
    
    async def calibrate_df_system(self, calibration_data: Dict[str, Any]) -> bool:
        """Calibrate the DF system."""
        try:
            if self.df_engine:
                success = await self.df_engine.calibrate(calibration_data)
                
                if success:
                    logger.info("DF system calibration completed successfully")
                    await self._notify_callbacks('calibration_completed', {'success': True})
                else:
                    logger.error("DF system calibration failed")
                    await self._notify_callbacks('calibration_completed', {'success': False})
                
                return success
            
            return False
            
        except Exception as e:
            logger.error(f"Error calibrating DF system: {e}")
            await self._notify_callbacks('calibration_completed', {'success': False, 'error': str(e)})
            return False
    
    def clear_measurement_buffer(self):
        """Clear the measurement buffer."""
        self.measurement_buffer.clear()
        logger.info("Measurement buffer cleared")
    
    def get_recent_results(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent DF results."""
        # This would retrieve results from a results cache
        # For now, return empty list
        return []
    
    def export_configuration(self, export_path: str):
        """Export DF configuration."""
        try:
            config_manager.export_config(Path(export_path))
            logger.info(f"DF configuration exported to {export_path}")
        except Exception as e:
            logger.error(f"Error exporting configuration: {e}")
            raise
    
    def import_configuration(self, import_path: str):
        """Import DF configuration."""
        try:
            config_manager.import_config(Path(import_path))
            
            # Update DF engine with new configuration
            if self.df_engine:
                new_config = get_df_config()
                self.df_engine.update_config(new_config)
            
            logger.info(f"DF configuration imported from {import_path}")
            
        except Exception as e:
            logger.error(f"Error importing configuration: {e}")
            raise


# Global integration manager instance
integration_manager = DFIntegrationManager()


def get_df_integration_manager() -> DFIntegrationManager:
    """Get the global DF integration manager."""
    return integration_manager


def initialize_df_integration(piwardrive_app=None) -> DFIntegrationManager:
    """Initialize DF integration with PiWardrive."""
    global integration_manager
    integration_manager = DFIntegrationManager(piwardrive_app)
    return integration_manager


async def start_df_integration():
    """Start DF integration."""
    await integration_manager.start()


async def stop_df_integration():
    """Stop DF integration."""
    await integration_manager.stop()


def add_df_measurement(measurement_data: Dict[str, Any]):
    """Add a measurement to the DF system."""
    integration_manager.add_measurement(measurement_data)


def get_df_status() -> Dict[str, Any]:
    """Get DF system status."""
    return integration_manager.get_integration_status()


def configure_df(config_updates: Dict[str, Any]):
    """Configure the DF system."""
    integration_manager.configure_df_system(config_updates)


def get_df_hardware_capabilities() -> Dict[str, Any]:
    """Get DF hardware capabilities."""
    return integration_manager.get_hardware_capabilities()
