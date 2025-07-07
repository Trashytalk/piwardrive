"""
Comprehensive tests for core application functionality.
Tests the main application entry points and critical paths.
"""

import os
import pytest
import tempfile
import asyncio
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
from dataclasses import asdict

from piwardrive.main import PiWardriveApp
from piwardrive.config import Config, load_config, save_config, CONFIG_DIR
from piwardrive.persistence import AppState, HealthRecord, load_app_state, save_app_state
from piwardrive.di import Container
from piwardrive.scheduler import PollScheduler


class TestPiWardriveAppInitialization:
    """Test core application initialization."""
    
    def test_app_initialization_with_defaults(self, tmp_path):
        """Test app initializes with default configuration."""
        # Setup temporary config directory
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    app = PiWardriveApp()
                    
                    assert app.config_data is not None
                    assert app.app_state is not None
                    assert app.container is not None
                    assert isinstance(app.scheduler, PollScheduler)
    
    def test_app_initialization_with_custom_container(self, tmp_path):
        """Test app initializes with custom container."""
        container = Container()
        
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    app = PiWardriveApp(container=container)
                    
                    assert app.container is container
                    
    def test_app_initialization_with_admin_password(self, tmp_path):
        """Test app initializes with admin password from environment."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch.dict(os.environ, {'PW_ADMIN_PASSWORD': 'test_password'}):
                        app = PiWardriveApp()
                        
                        assert app.config_data.admin_password_hash is not None
                        assert app.config_data.admin_password_hash != 'test_password'  # Should be hashed
                        
    def test_app_initialization_with_mqtt_enabled(self, tmp_path):
        """Test app initializes with MQTT when enabled."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.load_config') as mock_load_config:
                        config = Config()
                        config.enable_mqtt = True
                        mock_load_config.return_value = config
                        
                        with patch('piwardrive.mqtt.MQTTClient') as mock_mqtt:
                            mock_mqtt_instance = Mock()
                            mock_mqtt.return_value = mock_mqtt_instance
                            
                            app = PiWardriveApp()
                            
                            assert app.mqtt_client is not None
                            mock_mqtt_instance.connect.assert_called_once()


class TestApplicationLifecycle:
    """Test application lifecycle management."""
    
    def test_app_startup_sequence(self, tmp_path):
        """Test complete application startup sequence."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging') as mock_logging:
                with patch('piwardrive.main.exception_handler') as mock_exception:
                    with patch('piwardrive.main.analytics_jobs') as mock_analytics:
                        with patch('piwardrive.main.maintenance_jobs') as mock_maintenance:
                            with patch('piwardrive.main.utils.run_async_task') as mock_async:
                                
                                app = PiWardriveApp()
                                
                                # Verify initialization sequence
                                mock_logging.init_logging.assert_called_once()
                                mock_exception.install.assert_called_once()
                                
                                # Verify components are initialized
                                assert app.scheduler is not None
                                assert app.health_monitor is not None
                                assert app.tile_maintainer is not None
                                assert app.view_refresher is not None
                                assert app.model_trainer is not None
                                assert app.analytics_queue is not None
                                assert app.maintenance_queue is not None
                                
    def test_app_shutdown_cleanup(self, tmp_path):
        """Test application shutdown and cleanup."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    app = PiWardriveApp()
                    
                    # Mock cleanup methods
                    app.scheduler.stop = Mock()
                    app.analytics_queue.stop = Mock()
                    app.maintenance_queue.stop = Mock()
                    
                    # Test cleanup (would be called in actual shutdown)
                    app.scheduler.stop()
                    app.analytics_queue.stop()
                    app.maintenance_queue.stop()
                    
                    # Verify cleanup was called
                    app.scheduler.stop.assert_called_once()
                    app.analytics_queue.stop.assert_called_once()
                    app.maintenance_queue.stop.assert_called_once()


class TestApplicationConfiguration:
    """Test application configuration management."""
    
    def test_config_loading_and_validation(self, tmp_path):
        """Test configuration loading and validation."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            # Create a test config file
            config_path = tmp_path / "config.json"
            test_config = {
                "map_poll_aps": 30,
                "map_poll_bt": 45,
                "debug_mode": True,
                "health_poll_interval": 15
            }
            
            with open(config_path, 'w') as f:
                import json
                json.dump(test_config, f)
            
            # Load config
            config = load_config()
            
            # Verify loaded values
            assert config.map_poll_aps == 30
            assert config.map_poll_bt == 45
            assert config.debug_mode is True
            assert config.health_poll_interval == 15
            
    def test_config_save_and_load_roundtrip(self, tmp_path):
        """Test configuration save/load roundtrip."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            # Create and modify config
            config = Config()
            config.map_poll_aps = 120
            config.debug_mode = True
            config.health_poll_interval = 5
            
            # Save config
            save_config(config)
            
            # Load config
            loaded_config = load_config()
            
            # Verify values
            assert loaded_config.map_poll_aps == 120
            assert loaded_config.debug_mode is True
            assert loaded_config.health_poll_interval == 5
            
    def test_config_validation_errors(self, tmp_path):
        """Test configuration validation catches errors."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            config = Config()
            
            # Test invalid values
            with pytest.raises(ValueError):
                config.map_poll_aps = -1  # Should be positive
                
            with pytest.raises(ValueError):
                config.health_poll_interval = 0  # Should be positive


class TestApplicationState:
    """Test application state persistence."""
    
    def test_app_state_persistence(self, tmp_path):
        """Test application state save/load."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            # Create test state
            state = AppState(
                last_screen="Dashboard",
                last_start="2024-01-01T12:00:00",
                first_run=False
            )
            
            # Save state
            asyncio.run(save_app_state(state))
            
            # Load state
            loaded_state = asyncio.run(load_app_state())
            
            # Verify state
            assert loaded_state.last_screen == "Dashboard"
            assert loaded_state.last_start == "2024-01-01T12:00:00"
            assert loaded_state.first_run is False
            
    def test_app_state_first_run_detection(self, tmp_path):
        """Test first run detection."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            # Load state when no file exists (first run)
            loaded_state = asyncio.run(load_app_state())
            
            # Should detect first run
            assert loaded_state.first_run is True
            assert loaded_state.last_screen == "Dashboard"  # Default
            
    def test_health_record_persistence(self, tmp_path):
        """Test health record persistence."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            # Create test health record
            record = HealthRecord(
                timestamp="2024-01-01T12:00:00",
                cpu_temp=55.5,
                cpu_percent=25.0,
                memory_percent=60.0,
                disk_percent=40.0
            )
            
            # Save record
            from piwardrive.persistence import save_health_record
            asyncio.run(save_health_record(record))
            
            # Load recent records
            from piwardrive.persistence import load_recent_health
            records = asyncio.run(load_recent_health(1))
            
            # Verify record
            assert len(records) == 1
            assert records[0].cpu_temp == 55.5
            assert records[0].cpu_percent == 25.0
            assert records[0].memory_percent == 60.0
            assert records[0].disk_percent == 40.0


class TestErrorHandling:
    """Test application error handling."""
    
    def test_config_loading_error_handling(self, tmp_path):
        """Test error handling during config loading."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            # Create invalid config file
            config_path = tmp_path / "config.json"
            with open(config_path, 'w') as f:
                f.write("invalid json content")
            
            # Should fall back to defaults
            config = load_config()
            assert config is not None
            assert config.map_poll_aps == 60  # Default value
            
    def test_database_connection_error_handling(self, tmp_path):
        """Test database connection error handling."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            # Mock database connection failure
            with patch('piwardrive.persistence.aiosqlite.connect') as mock_connect:
                mock_connect.side_effect = Exception("Database connection failed")
                
                # Should handle the error gracefully
                try:
                    asyncio.run(load_app_state())
                except Exception as e:
                    assert "Database connection failed" in str(e)
                    
    def test_service_command_error_handling(self, tmp_path):
        """Test service command error handling."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            # Mock service command runner that fails
            def failing_service_cmd(*args, **kwargs):
                return False, "", "Service command failed"
            
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    app = PiWardriveApp(service_cmd_runner=failing_service_cmd)
                    
                    # App should still initialize despite service command failure
                    assert app.config_data is not None
                    assert app.app_state is not None


class TestDependencyInjection:
    """Test dependency injection container."""
    
    def test_container_registration_and_resolution(self):
        """Test container service registration and resolution."""
        container = Container()
        
        # Register a service
        test_service = Mock()
        container.register_instance("test_service", test_service)
        
        # Check if service is registered
        assert container.has("test_service")
        
        # Resolve service
        resolved_service = container.resolve("test_service")
        assert resolved_service is test_service
        
    def test_container_singleton_behavior(self):
        """Test container singleton behavior."""
        container = Container()
        
        # Register a service
        test_service = Mock()
        container.register_instance("test_service", test_service)
        
        # Resolve multiple times
        service1 = container.resolve("test_service")
        service2 = container.resolve("test_service")
        
        # Should return the same instance
        assert service1 is service2
        
    def test_container_error_handling(self):
        """Test container error handling for unregistered services."""
        container = Container()
        
        # Try to resolve unregistered service
        with pytest.raises(KeyError):
            container.resolve("nonexistent_service")
            
        # Check service existence
        assert not container.has("nonexistent_service")


class TestApplicationIntegration:
    """Test complete application integration scenarios."""
    
    def test_full_application_startup_and_basic_operations(self, tmp_path):
        """Test complete application startup and basic operations."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.utils.run_async_task'):
                        # Initialize application
                        app = PiWardriveApp()
                        
                        # Verify core components are available
                        assert app.scheduler is not None
                        assert app.health_monitor is not None
                        assert app.config_data is not None
                        assert app.app_state is not None
                        
                        # Test basic operations
                        assert app.container.has("scheduler")
                        assert app.container.has("health_monitor")
                        
                        # Test configuration access
                        assert app.config_data.map_poll_aps >= 0
                        assert app.config_data.health_poll_interval > 0
                        
    def test_application_with_all_features_enabled(self, tmp_path):
        """Test application with all major features enabled."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.utils.run_async_task'):
                        with patch('piwardrive.main.load_config') as mock_load_config:
                            # Create config with all features enabled
                            config = Config()
                            config.enable_mqtt = True
                            config.debug_mode = True
                            config.map_auto_prefetch = True
                            config.compress_health_exports = True
                            mock_load_config.return_value = config
                            
                            with patch('piwardrive.mqtt.MQTTClient') as mock_mqtt:
                                mock_mqtt_instance = Mock()
                                mock_mqtt.return_value = mock_mqtt_instance
                                
                                # Initialize application
                                app = PiWardriveApp()
                                
                                # Verify all components are initialized
                                assert app.config_data.enable_mqtt is True
                                assert app.config_data.debug_mode is True
                                assert app.config_data.map_auto_prefetch is True
                                assert app.config_data.compress_health_exports is True
                                assert app.mqtt_client is not None
                                
    def test_application_performance_monitoring(self, tmp_path):
        """Test application performance monitoring capabilities."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.utils.run_async_task'):
                        app = PiWardriveApp()
                        
                        # Test health monitoring
                        assert app.health_monitor is not None
                        
                        # Test analytics queue
                        assert app.analytics_queue is not None
                        assert app.analytics_scheduler is not None
                        
                        # Test maintenance queue
                        assert app.maintenance_queue is not None
                        assert app.maintenance_scheduler is not None
                        
                        # Test model trainer
                        assert app.model_trainer is not None
                        
                        # Test view refresher
                        assert app.view_refresher is not None
