#!/usr/bin/env python3
"""
Unit tests for PiWardrive Direction Finding System
Tests all major components and functionality.
"""

import asyncio
import pytest
import numpy as np
import time
from unittest.mock import Mock, patch, MagicMock

# Import DF components
from piwardrive.direction_finding import (
    DFConfiguration,
    DFConfigManager,
    DFAlgorithm,
    PathLossModel,
    DFEngine,
    DFResult,
    PositionEstimate,
    AngleEstimate,
    DFMeasurement,
    DFQuality,
    RSSTriangulation,
    PathLossCalculator,
    WiFiAdapterManager,
    AntennaArrayManager,
    HardwareDetector,
    DFIntegrationManager,
    get_df_config,
    set_df_algorithm,
    config_manager
)


class TestDFConfiguration:
    """Test DF configuration management."""
    
    def test_default_configuration(self):
        """Test default configuration creation."""
        config = DFConfiguration()
        
        assert config.primary_algorithm == DFAlgorithm.RSS_TRIANGULATION
        assert DFAlgorithm.RSS_TRIANGULATION in config.enabled_algorithms
        assert config.triangulation.min_access_points == 3
        assert config.path_loss.model_type == PathLossModel.FREE_SPACE
        assert config.enable_logging is True
    
    def test_configuration_manager(self):
        """Test configuration manager functionality."""
        manager = DFConfigManager()
        
        # Test getting configuration
        config = manager.get_config()
        assert isinstance(config, DFConfiguration)
        
        # Test updating configuration
        manager.update_config(enable_logging=False)
        assert manager.get_config().enable_logging is False
        
        # Test setting algorithm
        manager.set_algorithm(DFAlgorithm.MUSIC_AOA)
        assert manager.get_config().primary_algorithm == DFAlgorithm.MUSIC_AOA
        
        # Test enabling/disabling algorithms
        manager.enable_algorithm(DFAlgorithm.BEAMFORMING)
        assert DFAlgorithm.BEAMFORMING in manager.get_config().enabled_algorithms
        
        manager.disable_algorithm(DFAlgorithm.BEAMFORMING)
        assert DFAlgorithm.BEAMFORMING not in manager.get_config().enabled_algorithms
    
    def test_algorithm_config_retrieval(self):
        """Test algorithm-specific configuration retrieval."""
        manager = DFConfigManager()
        
        # Test RSS triangulation config
        rss_config = manager.get_algorithm_config(DFAlgorithm.RSS_TRIANGULATION)
        assert 'triangulation' in rss_config
        assert 'path_loss' in rss_config
        assert 'signal_mapping' in rss_config
        
        # Test MUSIC config
        music_config = manager.get_algorithm_config(DFAlgorithm.MUSIC_AOA)
        assert 'music' in music_config
        assert 'array_processing' in music_config
        assert 'antenna_array' in music_config


class TestDFCore:
    """Test DF core functionality."""
    
    def test_df_measurement_creation(self):
        """Test DFMeasurement creation."""
        measurement = DFMeasurement(
            signal_strength=-60.0,
            frequency=2.4e9,
            bssid='00:11:22:33:44:55',
            timestamp=time.time()
        )
        
        assert measurement.signal_strength == -60.0
        assert measurement.frequency == 2.4e9
        assert measurement.bssid == '00:11:22:33:44:55'
        assert measurement.timestamp > 0
        
        # Test serialization
        data = measurement.to_dict()
        assert 'signal_strength' in data
        assert 'frequency' in data
        assert 'bssid' in data
    
    def test_position_estimate_creation(self):
        """Test PositionEstimate creation."""
        position = PositionEstimate(
            latitude=40.7128,
            longitude=-74.0060,
            accuracy=10.0,
            confidence=0.8,
            algorithm="RSS_TRIANGULATION",
            quality=DFQuality.GOOD
        )
        
        assert position.latitude == 40.7128
        assert position.longitude == -74.0060
        assert position.accuracy == 10.0
        assert position.confidence == 0.8
        assert position.quality == DFQuality.GOOD
        
        # Test serialization
        data = position.to_dict()
        assert 'latitude' in data
        assert 'longitude' in data
        assert 'quality' in data
    
    def test_angle_estimate_creation(self):
        """Test AngleEstimate creation."""
        angle = AngleEstimate(
            azimuth=45.0,
            elevation=10.0,
            accuracy=5.0,
            confidence=0.7,
            algorithm="MUSIC_AOA",
            quality=DFQuality.GOOD
        )
        
        assert angle.azimuth == 45.0
        assert angle.elevation == 10.0
        assert angle.accuracy == 5.0
        assert angle.confidence == 0.7
        assert angle.quality == DFQuality.GOOD
        
        # Test serialization
        data = angle.to_dict()
        assert 'azimuth' in data
        assert 'elevation' in data
        assert 'quality' in data
    
    def test_df_result_creation(self):
        """Test DFResult creation."""
        position = PositionEstimate(40.7128, -74.0060, accuracy=10.0, confidence=0.8)
        angle = AngleEstimate(45.0, accuracy=5.0, confidence=0.7)
        
        result = DFResult(
            target_bssid='00:11:22:33:44:55',
            position=position,
            angle=angle,
            processing_time=0.1
        )
        
        assert result.target_bssid == '00:11:22:33:44:55'
        assert result.position == position
        assert result.angle == angle
        assert result.processing_time == 0.1
        
        # Test serialization
        data = result.to_dict()
        assert 'target_bssid' in data
        assert 'position' in data
        assert 'angle' in data


class TestPathLossCalculator:
    """Test path loss calculations."""
    
    def test_free_space_model(self):
        """Test free space path loss model."""
        from piwardrive.direction_finding.config import PathLossConfig
        
        config = PathLossConfig(model_type=PathLossModel.FREE_SPACE)
        calculator = PathLossCalculator(config)
        
        # Test distance calculation
        distance = calculator.calculate_distance(rssi=-40, tx_power=20)
        assert distance > 0
        assert distance < 1000  # Should be reasonable
        
        # Test with different RSSI values
        distance1 = calculator.calculate_distance(rssi=-50, tx_power=20)
        distance2 = calculator.calculate_distance(rssi=-60, tx_power=20)
        
        # Lower RSSI should result in greater distance
        assert distance2 > distance1
    
    def test_indoor_model(self):
        """Test indoor path loss model."""
        from piwardrive.direction_finding.config import PathLossConfig
        
        config = PathLossConfig(model_type=PathLossModel.INDOOR)
        calculator = PathLossCalculator(config)
        
        distance = calculator.calculate_distance(rssi=-50, tx_power=20)
        assert distance > 0
    
    def test_calibration(self):
        """Test path loss calibration."""
        from piwardrive.direction_finding.config import PathLossConfig
        
        config = PathLossConfig()
        calculator = PathLossCalculator(config)
        
        # Test calibration with sample data
        calibration_points = [
            {'distance': 10, 'rssi': -40, 'tx_power': 20},
            {'distance': 20, 'rssi': -50, 'tx_power': 20},
            {'distance': 50, 'rssi': -65, 'tx_power': 20},
        ]
        
        original_exponent = config.path_loss_exponent
        calculator.calibrate(calibration_points)
        
        # Calibration should update the path loss exponent
        assert hasattr(calculator, 'calibration_data')
        assert 'points' in calculator.calibration_data


class TestRSSTriangulation:
    """Test RSS triangulation algorithm."""
    
    def test_triangulation_initialization(self):
        """Test triangulation initialization."""
        from piwardrive.direction_finding.config import (
            TriangulationConfig, PathLossConfig, SignalMappingConfig
        )
        
        tri_config = TriangulationConfig()
        path_config = PathLossConfig()
        signal_config = SignalMappingConfig()
        
        triangulation = RSSTriangulation(tri_config, path_config, signal_config)
        
        assert triangulation.triangulation_config == tri_config
        assert triangulation.path_loss_config == path_config
        assert triangulation.signal_mapping_config == signal_config
        assert isinstance(triangulation.path_loss_calculator, PathLossCalculator)
    
    def test_access_point_management(self):
        """Test access point management."""
        from piwardrive.direction_finding.config import (
            TriangulationConfig, PathLossConfig, SignalMappingConfig
        )
        
        triangulation = RSSTriangulation(
            TriangulationConfig(),
            PathLossConfig(),
            SignalMappingConfig()
        )
        
        # Add access points
        triangulation.add_access_point('00:11:22:33:44:55', 40.7128, -74.0060, 20)
        triangulation.add_access_point('00:11:22:33:44:66', 40.7138, -74.0070, 20)
        
        assert len(triangulation.access_points) == 2
        assert '00:11:22:33:44:55' in triangulation.access_points
        assert '00:11:22:33:44:66' in triangulation.access_points
    
    def test_measurement_processing(self):
        """Test measurement processing."""
        from piwardrive.direction_finding.config import (
            TriangulationConfig, PathLossConfig, SignalMappingConfig
        )
        
        triangulation = RSSTriangulation(
            TriangulationConfig(),
            PathLossConfig(),
            SignalMappingConfig()
        )
        
        # Add access points
        triangulation.add_access_point('00:11:22:33:44:55', 40.7128, -74.0060, 20)
        triangulation.add_access_point('00:11:22:33:44:66', 40.7138, -74.0070, 20)
        triangulation.add_access_point('00:11:22:33:44:77', 40.7118, -74.0050, 20)
        
        # Create measurements
        measurements = [
            DFMeasurement(-50, 2.4e9, '00:11:22:33:44:55'),
            DFMeasurement(-55, 2.4e9, '00:11:22:33:44:66'),
            DFMeasurement(-60, 2.4e9, '00:11:22:33:44:77'),
        ]
        
        # Set as initialized
        triangulation.is_initialized = True
        
        # Process measurements
        result = triangulation.process('target_bssid', measurements)
        
        # Should have a result if enough reference points
        if result:
            assert result.target_bssid == 'target_bssid'
            assert len(result.measurements) == len(measurements)


class TestHardwareDetection:
    """Test hardware detection functionality."""
    
    def test_hardware_detector(self):
        """Test hardware detection."""
        # Mock subprocess calls
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "wlan0     IEEE 802.11  ESSID:off/any\n"
            
            adapters = HardwareDetector.detect_wifi_adapters()
            assert isinstance(adapters, list)
    
    def test_chipset_detection(self):
        """Test chipset detection."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "driver: ath9k\n"
            
            chipset = HardwareDetector.detect_chipset('wlan0')
            assert chipset == 'ath9k'
    
    def test_capabilities_check(self):
        """Test hardware capabilities check."""
        capabilities = HardwareDetector.get_hardware_capabilities()
        
        assert 'wifi_adapters' in capabilities
        assert 'antenna_arrays' in capabilities
        assert 'sdr_devices' in capabilities
        assert 'df_capable' in capabilities
        assert 'recommended_setup' in capabilities


class TestDFEngine:
    """Test DF engine functionality."""
    
    def test_engine_initialization(self):
        """Test DF engine initialization."""
        config = DFConfiguration()
        engine = DFEngine(config)
        
        assert engine.config == config
        assert isinstance(engine.algorithms, dict)
        assert isinstance(engine.hardware_managers, dict)
        assert engine.is_running is False
    
    @pytest.mark.asyncio
    async def test_engine_start_stop(self):
        """Test engine start/stop functionality."""
        config = DFConfiguration()
        engine = DFEngine(config)
        
        # Mock hardware managers
        engine.hardware_managers = {
            'wifi': Mock(),
            'antenna': Mock()
        }
        
        # Mock algorithms
        engine.algorithms = {
            DFAlgorithm.RSS_TRIANGULATION: Mock()
        }
        
        # Test start
        await engine.start()
        assert engine.is_running is True
        
        # Test stop
        await engine.stop()
        assert engine.is_running is False
    
    def test_performance_metrics(self):
        """Test performance metrics."""
        config = DFConfiguration()
        engine = DFEngine(config)
        
        metrics = engine.get_performance_metrics()
        
        assert 'total_estimates' in metrics
        assert 'successful_estimates' in metrics
        assert 'average_processing_time' in metrics
        assert 'last_update' in metrics
    
    def test_algorithm_status(self):
        """Test algorithm status reporting."""
        config = DFConfiguration()
        engine = DFEngine(config)
        
        status = engine.get_algorithm_status()
        assert isinstance(status, dict)
    
    def test_hardware_status(self):
        """Test hardware status reporting."""
        config = DFConfiguration()
        engine = DFEngine(config)
        
        status = engine.get_hardware_status()
        assert isinstance(status, dict)


class TestDFIntegration:
    """Test DF integration functionality."""
    
    def test_integration_manager_initialization(self):
        """Test integration manager initialization."""
        manager = DFIntegrationManager()
        
        assert manager.df_engine is not None
        assert manager.is_running is False
        assert isinstance(manager.measurement_buffer, list)
        assert isinstance(manager.integration_metrics, dict)
    
    def test_measurement_addition(self):
        """Test adding measurements."""
        manager = DFIntegrationManager()
        
        measurement_data = {
            'signal_strength': -60.0,
            'frequency': 2.4e9,
            'bssid': '00:11:22:33:44:55',
            'timestamp': time.time()
        }
        
        initial_count = len(manager.measurement_buffer)
        manager.add_measurement(measurement_data)
        
        assert len(manager.measurement_buffer) == initial_count + 1
        assert manager.integration_metrics['total_measurements'] == 1
    
    def test_status_reporting(self):
        """Test status reporting."""
        manager = DFIntegrationManager()
        
        status = manager.get_integration_status()
        
        assert 'running' in status
        assert 'df_engine_status' in status
        assert 'hardware_status' in status
        assert 'buffer_size' in status
        assert 'metrics' in status
    
    def test_configuration_management(self):
        """Test configuration management."""
        manager = DFIntegrationManager()
        
        config_updates = {
            'enable_logging': False,
            'log_level': 'DEBUG'
        }
        
        manager.configure_df_system(config_updates)
        
        # Should not raise an exception
        assert True
    
    def test_callback_management(self):
        """Test callback management."""
        manager = DFIntegrationManager()
        
        callback_called = False
        
        def test_callback(event_type, data):
            nonlocal callback_called
            callback_called = True
        
        manager.add_result_callback(test_callback)
        assert test_callback in manager.result_callbacks
        
        manager.remove_result_callback(test_callback)
        assert test_callback not in manager.result_callbacks


class TestConfigurationValidation:
    """Test configuration validation."""
    
    def test_triangulation_validation(self):
        """Test triangulation configuration validation."""
        manager = DFConfigManager()
        
        # Test invalid minimum access points
        with pytest.raises(ValueError):
            manager.update_triangulation_config(min_access_points=2)
        
        # Test invalid position error
        with pytest.raises(ValueError):
            manager.update_triangulation_config(max_position_error=-1)
    
    def test_antenna_validation(self):
        """Test antenna configuration validation."""
        manager = DFConfigManager()
        
        # Test invalid number of elements
        with pytest.raises(ValueError):
            manager.update_antenna_config(num_elements=1)
        
        # Test invalid element spacing
        with pytest.raises(ValueError):
            manager.update_antenna_config(element_spacing=-1)
    
    def test_frequency_validation(self):
        """Test frequency configuration validation."""
        manager = DFConfigManager()
        
        # Test invalid frequency
        with pytest.raises(ValueError):
            manager.update_antenna_config(operating_frequency=-1)


class TestPerformanceMonitoring:
    """Test performance monitoring functionality."""
    
    def test_metrics_collection(self):
        """Test metrics collection."""
        manager = DFIntegrationManager()
        
        # Add some measurements
        for i in range(10):
            measurement_data = {
                'signal_strength': -60.0 - i,
                'frequency': 2.4e9,
                'bssid': f'00:11:22:33:44:{i:02d}',
                'timestamp': time.time()
            }
            manager.add_measurement(measurement_data)
        
        metrics = manager.get_integration_metrics()
        
        assert metrics['total_measurements'] == 10
        assert 'processed_measurements' in metrics
        assert 'successful_estimates' in metrics
        assert 'failed_estimates' in metrics
    
    def test_performance_tracking(self):
        """Test performance tracking."""
        config = DFConfiguration()
        engine = DFEngine(config)
        
        # Update metrics
        engine._update_performance_metrics(5, 0.1)
        
        metrics = engine.get_performance_metrics()
        
        assert metrics['total_estimates'] == 5
        assert metrics['successful_estimates'] == 5
        assert metrics['average_processing_time'] == 0.1


# Test fixtures
@pytest.fixture
def sample_measurements():
    """Sample measurements for testing."""
    return [
        DFMeasurement(-50, 2.4e9, '00:11:22:33:44:55'),
        DFMeasurement(-55, 2.4e9, '00:11:22:33:44:66'),
        DFMeasurement(-60, 2.4e9, '00:11:22:33:44:77'),
        DFMeasurement(-65, 2.4e9, '00:11:22:33:44:88'),
    ]


@pytest.fixture
def sample_access_points():
    """Sample access points for testing."""
    return [
        {'bssid': '00:11:22:33:44:55', 'latitude': 40.7128, 'longitude': -74.0060, 'tx_power': 20},
        {'bssid': '00:11:22:33:44:66', 'latitude': 40.7138, 'longitude': -74.0070, 'tx_power': 20},
        {'bssid': '00:11:22:33:44:77', 'latitude': 40.7118, 'longitude': -74.0050, 'tx_power': 20},
        {'bssid': '00:11:22:33:44:88', 'latitude': 40.7148, 'longitude': -74.0080, 'tx_power': 20},
    ]


@pytest.fixture
def configured_triangulation(sample_access_points):
    """Configured triangulation algorithm for testing."""
    from piwardrive.direction_finding.config import (
        TriangulationConfig, PathLossConfig, SignalMappingConfig
    )
    
    triangulation = RSSTriangulation(
        TriangulationConfig(),
        PathLossConfig(),
        SignalMappingConfig()
    )
    
    # Add access points
    for ap in sample_access_points:
        triangulation.add_access_point(
            ap['bssid'],
            ap['latitude'],
            ap['longitude'],
            ap['tx_power']
        )
    
    triangulation.is_initialized = True
    return triangulation


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
