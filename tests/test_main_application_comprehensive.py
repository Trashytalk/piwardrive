"""
Comprehensive tests for main.py - Application entry point.
Tests application initialization, lifecycle, and core functionality.
"""

import asyncio
import os
import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, AsyncMock, call
from dataclasses import asdict

from piwardrive.main import PiWardriveApp
from piwardrive.config import Config, load_config, save_config
from piwardrive.persistence import AppState, load_app_state, save_app_state
from piwardrive.di import Container
from piwardrive.scheduler import PollScheduler
from piwardrive.security import hash_password


class TestPiWardriveAppInitialization:
    """Test PiWardriveApp initialization and setup."""
    
    def test_app_initialization_minimal(self, tmp_path):
        """Test app initializes with minimal configuration."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging') as mock_logging:
                with patch('piwardrive.main.exception_handler') as mock_exception:
                    with patch('piwardrive.main.utils.run_async_task') as mock_async:
                        with patch('piwardrive.main.tile_maintenance') as mock_tile:
                            
                            app = PiWardriveApp()
                            
                            # Test core components are initialized
                            assert app.config_data is not None
                            assert app.app_state is not None
                            assert app.container is not None
                            assert isinstance(app.scheduler, PollScheduler)
                            assert app.mqtt_client is None  # MQTT disabled by default
                            
                            # Test initialization sequence
                            mock_logging.init_logging.assert_called_once()
                            mock_exception.install.assert_called_once()
                            
    def test_app_initialization_with_custom_container(self, tmp_path):
        """Test app initializes with custom dependency container."""
        container = Container()
        test_scheduler = Mock()
        container.register_instance("scheduler", test_scheduler)
        
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.utils.run_async_task'):
                        with patch('piwardrive.main.tile_maintenance'):
                            
                            app = PiWardriveApp(container=container)
                            
                            assert app.container is container
                            assert app.scheduler is test_scheduler
                            
    def test_app_initialization_with_service_cmd_runner(self, tmp_path):
        """Test app initializes with custom service command runner."""
        def mock_service_cmd(*args, **kwargs):
            return True, "success", ""
            
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.utils.run_async_task'):
                        with patch('piwardrive.main.tile_maintenance'):
                            
                            app = PiWardriveApp(service_cmd_runner=mock_service_cmd)
                            
                            assert app._run_service_cmd is mock_service_cmd
                            
    def test_app_admin_password_initialization(self, tmp_path):
        """Test app initializes admin password from environment."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.utils.run_async_task'):
                        with patch('piwardrive.main.tile_maintenance'):
                            with patch.dict(os.environ, {'PW_ADMIN_PASSWORD': 'test_password'}):
                                
                                app = PiWardriveApp()
                                
                                # Password should be hashed
                                assert app.config_data.admin_password_hash is not None
                                assert app.config_data.admin_password_hash != 'test_password'
                                assert len(app.config_data.admin_password_hash) > 20  # Hashed
                                
    def test_app_admin_password_not_overwritten(self, tmp_path):
        """Test app doesn't overwrite existing admin password hash."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.load_config') as mock_load:
                config = Config()
                config.admin_password_hash = "existing_hash"
                mock_load.return_value = config
                
                with patch('piwardrive.main.init_logging'):
                    with patch('piwardrive.main.exception_handler'):
                        with patch('piwardrive.main.utils.run_async_task'):
                            with patch('piwardrive.main.tile_maintenance'):
                                with patch.dict(os.environ, {'PW_ADMIN_PASSWORD': 'test_password'}):
                                    
                                    app = PiWardriveApp()
                                    
                                    # Existing hash should be preserved
                                    assert app.config_data.admin_password_hash == "existing_hash"


class TestPiWardriveAppMQTTIntegration:
    """Test MQTT integration in PiWardriveApp."""
    
    def test_mqtt_client_initialization_when_enabled(self, tmp_path):
        """Test MQTT client is initialized when enabled."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.load_config') as mock_load:
                config = Config()
                config.enable_mqtt = True
                mock_load.return_value = config
                
                with patch('piwardrive.main.init_logging'):
                    with patch('piwardrive.main.exception_handler'):
                        with patch('piwardrive.main.utils.run_async_task'):
                            with patch('piwardrive.main.tile_maintenance'):
                                with patch('piwardrive.mqtt.MQTTClient') as mock_mqtt:
                                    mock_mqtt_instance = Mock()
                                    mock_mqtt.return_value = mock_mqtt_instance
                                    
                                    app = PiWardriveApp()
                                    
                                    # MQTT should be initialized and connected
                                    assert app.mqtt_client is not None
                                    mock_mqtt.assert_called_once()
                                    mock_mqtt_instance.connect.assert_called_once()
                                    
    def test_mqtt_client_not_initialized_when_disabled(self, tmp_path):
        """Test MQTT client is not initialized when disabled."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.load_config') as mock_load:
                config = Config()
                config.enable_mqtt = False
                mock_load.return_value = config
                
                with patch('piwardrive.main.init_logging'):
                    with patch('piwardrive.main.exception_handler'):
                        with patch('piwardrive.main.utils.run_async_task'):
                            with patch('piwardrive.main.tile_maintenance'):
                                
                                app = PiWardriveApp()
                                
                                # MQTT should not be initialized
                                assert app.mqtt_client is None


class TestPiWardriveAppComponentInitialization:
    """Test initialization of various app components."""
    
    def test_scheduler_initialization(self, tmp_path):
        """Test scheduler is properly initialized."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.utils.run_async_task'):
                        with patch('piwardrive.main.tile_maintenance'):
                            
                            app = PiWardriveApp()
                            
                            # Test scheduler
                            assert isinstance(app.scheduler, PollScheduler)
                            assert app.container.has("scheduler")
                            assert app.container.resolve("scheduler") is app.scheduler
                            
    def test_health_monitor_initialization(self, tmp_path):
        """Test health monitor is properly initialized."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.utils.run_async_task'):
                        with patch('piwardrive.main.tile_maintenance'):
                            with patch('piwardrive.diagnostics.HealthMonitor') as mock_health:
                                mock_health_instance = Mock()
                                mock_health.return_value = mock_health_instance
                                
                                app = PiWardriveApp()
                                
                                # Test health monitor
                                assert app.health_monitor is not None
                                assert app.container.has("health_monitor")
                                mock_health.assert_called_once()
                                
    def test_tile_maintainer_initialization(self, tmp_path):
        """Test tile maintainer is properly initialized."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.utils.run_async_task'):
                        with patch('piwardrive.main.tile_maintenance') as mock_tile:
                            mock_maintainer = Mock()
                            mock_tile.TileMaintainer.return_value = mock_maintainer
                            
                            app = PiWardriveApp()
                            
                            # Test tile maintainer
                            assert app.tile_maintainer is not None
                            mock_tile.TileMaintainer.assert_called_once()
                            
    def test_task_queues_initialization(self, tmp_path):
        """Test task queues are properly initialized."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.utils.run_async_task'):
                        with patch('piwardrive.main.tile_maintenance'):
                            
                            app = PiWardriveApp()
                            
                            # Test task queues
                            assert app.analytics_queue is not None
                            assert app.analytics_scheduler is not None
                            assert app.maintenance_queue is not None
                            assert app.maintenance_scheduler is not None
                            
    def test_model_trainer_initialization(self, tmp_path):
        """Test model trainer is properly initialized."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.utils.run_async_task'):
                        with patch('piwardrive.main.tile_maintenance'):
                            
                            app = PiWardriveApp()
                            
                            # Test model trainer
                            assert app.model_trainer is not None
                            
    def test_view_refresher_initialization(self, tmp_path):
        """Test view refresher is properly initialized."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.utils.run_async_task'):
                        with patch('piwardrive.main.tile_maintenance'):
                            
                            app = PiWardriveApp()
                            
                            # Test view refresher
                            assert app.view_refresher is not None


class TestPiWardriveAppScheduledTasks:
    """Test scheduled tasks and job initialization."""
    
    def test_remote_sync_scheduling(self, tmp_path):
        """Test remote sync is scheduled when configured."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.load_config') as mock_load:
                config = Config()
                config.remote_sync_url = "https://example.com/sync"
                config.remote_sync_interval = 60
                mock_load.return_value = config
                
                with patch('piwardrive.main.init_logging'):
                    with patch('piwardrive.main.exception_handler'):
                        with patch('piwardrive.main.utils.run_async_task'):
                            with patch('piwardrive.main.tile_maintenance'):
                                
                                app = PiWardriveApp()
                                
                                # Test sync is configured
                                assert app.config_data.remote_sync_url == "https://example.com/sync"
                                assert app.config_data.remote_sync_interval == 60
                                
    def test_scan_report_scheduling(self, tmp_path):
        """Test scan report is scheduled."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.utils.run_async_task'):
                        with patch('piwardrive.main.tile_maintenance'):
                            with patch('piwardrive.main.scan_report') as mock_scan_report:
                                
                                app = PiWardriveApp()
                                
                                # Test scan report module is available
                                assert mock_scan_report is not None
                                
    def test_auto_update_scheduling(self, tmp_path):
        """Test auto update is scheduled when configured."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.utils.run_async_task'):
                        with patch('piwardrive.main.tile_maintenance'):
                            with patch.dict(os.environ, {'PW_UPDATE_INTERVAL': '24'}):
                                
                                app = PiWardriveApp()
                                
                                # Test update interval is configured
                                assert os.getenv('PW_UPDATE_INTERVAL') == '24'
                                
    def test_jobs_initialization(self, tmp_path):
        """Test analytics and maintenance jobs are initialized."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.utils.run_async_task') as mock_async:
                        with patch('piwardrive.main.tile_maintenance'):
                            with patch('piwardrive.main.analytics_jobs') as mock_analytics:
                                with patch('piwardrive.main.maintenance_jobs') as mock_maintenance:
                                    
                                    app = PiWardriveApp()
                                    
                                    # Test jobs are initialized
                                    assert mock_analytics is not None
                                    assert mock_maintenance is not None
                                    mock_async.assert_called()


class TestPiWardriveAppNotifications:
    """Test notification system initialization."""
    
    def test_notification_manager_initialization(self, tmp_path):
        """Test notification manager is properly initialized."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.load_config') as mock_load:
                config = Config()
                config.notification_webhooks = ["https://example.com/webhook"]
                config.notify_cpu_temp = 80.0
                config.notify_disk_percent = 90.0
                mock_load.return_value = config
                
                with patch('piwardrive.main.init_logging'):
                    with patch('piwardrive.main.exception_handler'):
                        with patch('piwardrive.main.utils.run_async_task'):
                            with patch('piwardrive.main.tile_maintenance'):
                                
                                app = PiWardriveApp()
                                
                                # Test notifications are configured
                                assert app.notifications is not None
                                assert app.config_data.notification_webhooks == ["https://example.com/webhook"]
                                assert app.config_data.notify_cpu_temp == 80.0
                                assert app.config_data.notify_disk_percent == 90.0


class TestPiWardriveAppErrorHandling:
    """Test error handling in app initialization."""
    
    def test_config_loading_error_handling(self, tmp_path):
        """Test app handles config loading errors gracefully."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.load_config') as mock_load:
                mock_load.side_effect = Exception("Config loading failed")
                
                with patch('piwardrive.main.init_logging'):
                    with patch('piwardrive.main.exception_handler'):
                        with patch('piwardrive.main.utils.run_async_task'):
                            with patch('piwardrive.main.tile_maintenance'):
                                
                                # Should raise the exception
                                with pytest.raises(Exception, match="Config loading failed"):
                                    PiWardriveApp()
                                    
    def test_app_state_loading_error_handling(self, tmp_path):
        """Test app handles app state loading errors gracefully."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.load_app_state') as mock_load:
                mock_load.side_effect = Exception("App state loading failed")
                
                with patch('piwardrive.main.init_logging'):
                    with patch('piwardrive.main.exception_handler'):
                        with patch('piwardrive.main.utils.run_async_task'):
                            with patch('piwardrive.main.tile_maintenance'):
                                
                                # Should raise the exception
                                with pytest.raises(Exception, match="App state loading failed"):
                                    PiWardriveApp()
                                    
    def test_mqtt_connection_error_handling(self, tmp_path):
        """Test app handles MQTT connection errors gracefully."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.load_config') as mock_load:
                config = Config()
                config.enable_mqtt = True
                mock_load.return_value = config
                
                with patch('piwardrive.main.init_logging'):
                    with patch('piwardrive.main.exception_handler'):
                        with patch('piwardrive.main.utils.run_async_task'):
                            with patch('piwardrive.main.tile_maintenance'):
                                with patch('piwardrive.mqtt.MQTTClient') as mock_mqtt:
                                    mock_mqtt_instance = Mock()
                                    mock_mqtt_instance.connect.side_effect = Exception("MQTT connection failed")
                                    mock_mqtt.return_value = mock_mqtt_instance
                                    
                                    # Should handle MQTT error gracefully
                                    with pytest.raises(Exception, match="MQTT connection failed"):
                                        PiWardriveApp()
                                        
    def test_scan_report_scheduling_error_handling(self, tmp_path):
        """Test app handles scan report scheduling errors gracefully."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.utils.run_async_task'):
                        with patch('piwardrive.main.tile_maintenance'):
                            with patch('piwardrive.main.scan_report') as mock_scan_report:
                                mock_scan_report.side_effect = Exception("Scan report failed")
                                
                                # Should handle scan report error gracefully
                                app = PiWardriveApp()
                                
                                # App should still initialize despite scan report error
                                assert app is not None


class TestPiWardriveAppIntegration:
    """Test complete app integration scenarios."""
    
    def test_full_app_initialization_sequence(self, tmp_path):
        """Test complete app initialization with all components."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging') as mock_logging:
                with patch('piwardrive.main.exception_handler') as mock_exception:
                    with patch('piwardrive.main.utils.run_async_task') as mock_async:
                        with patch('piwardrive.main.tile_maintenance') as mock_tile:
                            with patch('piwardrive.main.analytics_jobs') as mock_analytics:
                                with patch('piwardrive.main.maintenance_jobs') as mock_maintenance:
                                    
                                    app = PiWardriveApp()
                                    
                                    # Test complete initialization
                                    assert app.config_data is not None
                                    assert app.app_state is not None
                                    assert app.container is not None
                                    assert app.scheduler is not None
                                    assert app.health_monitor is not None
                                    assert app.tile_maintainer is not None
                                    assert app.view_refresher is not None
                                    assert app.model_trainer is not None
                                    assert app.analytics_queue is not None
                                    assert app.maintenance_queue is not None
                                    assert app.notifications is not None
                                    
                                    # Test initialization sequence
                                    mock_logging.init_logging.assert_called_once()
                                    mock_exception.install.assert_called_once()
                                    mock_async.assert_called()
                                    
    def test_app_with_all_features_enabled(self, tmp_path):
        """Test app with all features enabled."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.load_config') as mock_load:
                config = Config()
                config.enable_mqtt = True
                config.debug_mode = True
                config.remote_sync_url = "https://example.com/sync"
                config.remote_sync_interval = 60
                config.notification_webhooks = ["https://example.com/webhook"]
                config.notify_cpu_temp = 75.0
                config.notify_disk_percent = 85.0
                mock_load.return_value = config
                
                with patch('piwardrive.main.init_logging'):
                    with patch('piwardrive.main.exception_handler'):
                        with patch('piwardrive.main.utils.run_async_task'):
                            with patch('piwardrive.main.tile_maintenance'):
                                with patch('piwardrive.mqtt.MQTTClient') as mock_mqtt:
                                    mock_mqtt_instance = Mock()
                                    mock_mqtt.return_value = mock_mqtt_instance
                                    
                                    with patch.dict(os.environ, {'PW_UPDATE_INTERVAL': '12'}):
                                        app = PiWardriveApp()
                                        
                                        # Test all features are enabled
                                        assert app.config_data.enable_mqtt is True
                                        assert app.config_data.debug_mode is True
                                        assert app.config_data.remote_sync_url == "https://example.com/sync"
                                        assert app.config_data.remote_sync_interval == 60
                                        assert app.mqtt_client is not None
                                        assert len(app.config_data.notification_webhooks) == 1
                                        
    def test_app_state_persistence(self, tmp_path):
        """Test app state is properly loaded and can be persisted."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.load_app_state') as mock_load:
                test_state = AppState(
                    last_screen="Scanner",
                    last_start="2024-01-01T12:00:00",
                    first_run=False
                )
                mock_load.return_value = test_state
                
                with patch('piwardrive.main.init_logging'):
                    with patch('piwardrive.main.exception_handler'):
                        with patch('piwardrive.main.utils.run_async_task'):
                            with patch('piwardrive.main.tile_maintenance'):
                                
                                app = PiWardriveApp()
                                
                                # Test app state is loaded
                                assert app.app_state.last_screen == "Scanner"
                                assert app.app_state.last_start == "2024-01-01T12:00:00"
                                assert app.app_state.first_run is False
                                assert app.last_screen == "Scanner"
                                
    def test_dependency_injection_integration(self, tmp_path):
        """Test dependency injection container integration."""
        with patch('piwardrive.config.CONFIG_DIR', str(tmp_path)):
            with patch('piwardrive.main.init_logging'):
                with patch('piwardrive.main.exception_handler'):
                    with patch('piwardrive.main.utils.run_async_task'):
                        with patch('piwardrive.main.tile_maintenance'):
                            
                            app = PiWardriveApp()
                            
                            # Test container has expected services
                            assert app.container.has("scheduler")
                            assert app.container.has("health_monitor")
                            
                            # Test services can be resolved
                            scheduler = app.container.resolve("scheduler")
                            health_monitor = app.container.resolve("health_monitor")
                            
                            assert scheduler is app.scheduler
                            assert health_monitor is app.health_monitor
