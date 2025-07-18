"""
Fixed tests for main.py application entry point.
Tests the core application functionality without relying on problematic imports.
"""

import os
from unittest.mock import Mock, patch

import pytest


class TestPiWardriveAppCore:
    """Test core PiWardriveApp functionality."""

    def test_app_class_exists(self):
        """Test that PiWardriveApp class can be imported."""
        from piwardrive.main import PiWardriveApp

        assert PiWardriveApp is not None
        assert hasattr(PiWardriveApp, "__init__")

    @patch("piwardrive.main.init_logging")
    @patch("piwardrive.main.exception_handler.install")
    @patch("piwardrive.main.load_config")
    @patch("piwardrive.main.load_app_state")
    @patch("piwardrive.main.utils.run_async_task")
    @patch("piwardrive.main.PollScheduler")
    @patch("piwardrive.main.diagnostics.HealthMonitor")
    @patch("builtins.__import__")
    def test_app_initialization_basic(
        self,
        mock_import,
        mock_health_monitor,
        mock_poll_scheduler,
        mock_run_async_task,
        mock_load_app_state,
        mock_load_config,
        mock_install,
        mock_init_logging,
    ):
        """Test basic app initialization."""
        from piwardrive.config import Config
        from piwardrive.main import PiWardriveApp
        from piwardrive.persistence import AppState

        # Mock the config and app state
        mock_config = Mock(spec=Config)
        mock_config.admin_password_hash = ""
        mock_config.enable_mqtt = False
        mock_config.remote_sync_url = ""
        mock_config.remote_sync_interval = 0
        mock_config.notification_webhooks = []
        mock_config.notify_cpu_temp = 80.0
        mock_config.notify_disk_percent = 90.0
        mock_config.offline_tile_path = "/tmp/test.mbtiles"

        mock_app_state = Mock(spec=AppState)
        mock_app_state.last_screen = "main"

        mock_load_config.return_value = mock_config
        mock_load_app_state.return_value = mock_app_state

        # Mock scheduler
        mock_scheduler_instance = Mock()
        mock_poll_scheduler.return_value = mock_scheduler_instance

        # Mock health monitor
        mock_health_monitor_instance = Mock()
        mock_health_monitor.return_value = mock_health_monitor_instance

        # Mock tile maintenance import
        def side_effect(name, *args, **kwargs):
            if name == "tile_maintenance":
                mock_tile_maintenance = Mock()
                mock_tile_maintenance.TileMaintainer = Mock()
                return mock_tile_maintenance
            return __import__(name, *args, **kwargs)

        mock_import.side_effect = side_effect

        # Create app instance
        with patch.dict(os.environ, {"PW_ADMIN_PASSWORD": ""}, clear=False):
            app = PiWardriveApp()

        # Verify core attributes
        assert hasattr(app, "config_data")
        assert hasattr(app, "app_state")
        assert hasattr(app, "scheduler")
        assert hasattr(app, "health_monitor")
        assert hasattr(app, "container")

        # Verify initialization was called
        mock_init_logging.assert_called_once()
        mock_install.assert_called_once()
        mock_load_config.assert_called_once()

    @patch("piwardrive.main.init_logging")
    @patch("piwardrive.main.exception_handler.install")
    @patch("piwardrive.main.load_config")
    @patch("piwardrive.main.load_app_state")
    @patch("piwardrive.main.utils.run_async_task")
    @patch("piwardrive.main.tile_maintenance", create=True)
    @patch("piwardrive.main.hash_password")
    @patch("piwardrive.main.PollScheduler")
    @patch("piwardrive.main.diagnostics.HealthMonitor")
    def test_app_admin_password_setting(
        self,
        mock_health_monitor,
        mock_poll_scheduler,
        mock_hash_password,
        mock_tile_maintenance,
        mock_run_async_task,
        mock_load_app_state,
        mock_load_config,
        mock_install,
        mock_init_logging,
    ):
        """Test admin password setting during initialization."""
        from piwardrive.config import Config
        from piwardrive.main import PiWardriveApp
        from piwardrive.persistence import AppState

        # Mock the config and app state
        mock_config = Mock(spec=Config)
        mock_config.admin_password_hash = ""  # Empty initially
        mock_config.enable_mqtt = False
        mock_config.remote_sync_url = ""
        mock_config.remote_sync_interval = 0
        mock_config.notification_webhooks = []
        mock_config.notify_cpu_temp = 80.0
        mock_config.notify_disk_percent = 90.0
        mock_config.offline_tile_path = "/tmp/test.mbtiles"

        mock_app_state = Mock(spec=AppState)
        mock_app_state.last_screen = "main"

        mock_load_config.return_value = mock_config
        mock_load_app_state.return_value = mock_app_state

        # Mock scheduler
        mock_scheduler_instance = Mock()
        mock_poll_scheduler.return_value = mock_scheduler_instance

        # Mock health monitor
        mock_health_monitor_instance = Mock()
        mock_health_monitor.return_value = mock_health_monitor_instance

        # Mock tile maintenance
        mock_tile_maintenance.TileMaintainer = Mock()

        # Mock hash_password
        mock_hash_password.return_value = "hashed_password"

        # Set admin password environment variable
        with patch.dict(
            os.environ, {"PW_ADMIN_PASSWORD": "test_password"}, clear=False
        ):
            PiWardriveApp()

        # Verify password was hashed and set
        mock_hash_password.assert_called_once_with("test_password")
        assert mock_config.admin_password_hash == "hashed_password"

    @patch("piwardrive.main.init_logging")
    @patch("piwardrive.main.exception_handler.install")
    @patch("piwardrive.main.load_config")
    @patch("piwardrive.main.load_app_state")
    @patch("piwardrive.main.utils.run_async_task")
    @patch("piwardrive.main.tile_maintenance", create=True)
    @patch("piwardrive.main.PollScheduler")
    @patch("piwardrive.main.diagnostics.HealthMonitor")
    def test_app_custom_container(
        self,
        mock_health_monitor,
        mock_poll_scheduler,
        mock_tile_maintenance,
        mock_run_async_task,
        mock_load_app_state,
        mock_load_config,
        mock_install,
        mock_init_logging,
    ):
        """Test app initialization with custom container."""
        from piwardrive.config import Config
        from piwardrive.di import Container
        from piwardrive.main import PiWardriveApp
        from piwardrive.persistence import AppState

        # Mock the config and app state
        mock_config = Mock(spec=Config)
        mock_config.admin_password_hash = ""
        mock_config.enable_mqtt = False
        mock_config.remote_sync_url = ""
        mock_config.remote_sync_interval = 0
        mock_config.notification_webhooks = []
        mock_config.notify_cpu_temp = 80.0
        mock_config.notify_disk_percent = 90.0
        mock_config.offline_tile_path = "/tmp/test.mbtiles"

        mock_app_state = Mock(spec=AppState)
        mock_app_state.last_screen = "main"

        mock_load_config.return_value = mock_config
        mock_load_app_state.return_value = mock_app_state

        # Mock scheduler
        mock_scheduler_instance = Mock()
        mock_poll_scheduler.return_value = mock_scheduler_instance

        # Mock health monitor
        mock_health_monitor_instance = Mock()
        mock_health_monitor.return_value = mock_health_monitor_instance

        # Mock tile maintenance
        mock_tile_maintenance.TileMaintainer = Mock()

        # Create custom container
        custom_container = Container()

        # Create app instance with custom container
        with patch.dict(os.environ, {"PW_ADMIN_PASSWORD": ""}, clear=False):
            app = PiWardriveApp(container=custom_container)

        # Verify custom container is used
        assert app.container is custom_container

    def test_app_service_cmd_runner_customization(self):
        """Test custom service command runner."""
        from piwardrive.main import PiWardriveApp

        # Mock service command runner
        def mock_service_cmd_runner(*args, **kwargs):
            return True, "success", ""

        # This test verifies the attribute is set properly
        # without full initialization to avoid complex mocking
        with patch("piwardrive.main.load_config") as mock_load_config:
            with patch("piwardrive.main.load_app_state") as mock_load_app_state:
                with patch("piwardrive.main.init_logging"):
                    with patch("piwardrive.main.exception_handler.install"):
                        with patch("piwardrive.main.utils.run_async_task"):
                            with patch("piwardrive.main.tile_maintenance", create=True):
                                with patch("piwardrive.main.PollScheduler"):
                                    with patch(
                                        "piwardrive.main.diagnostics.HealthMonitor"
                                    ):
                                        # Set up minimal mocks
                                        mock_config = Mock()
                                        mock_config.admin_password_hash = ""
                                        mock_config.enable_mqtt = False
                                        mock_config.remote_sync_url = ""
                                        mock_config.remote_sync_interval = 0
                                        mock_config.notification_webhooks = []
                                        mock_config.notify_cpu_temp = 80.0
                                        mock_config.notify_disk_percent = 90.0
                                        mock_config.offline_tile_path = (
                                            "/tmp/test.mbtiles"
                                        )

                                        mock_app_state = Mock()
                                        mock_app_state.last_screen = "main"

                                        mock_load_config.return_value = mock_config
                                        mock_load_app_state.return_value = (
                                            mock_app_state
                                        )

                                        with patch.dict(
                                            os.environ,
                                            {"PW_ADMIN_PASSWORD": ""},
                                            clear=False,
                                        ):
                                            app = PiWardriveApp(
                                                service_cmd_runner=mock_service_cmd_runner
                                            )

                                        # Verify custom service command runner is used
                                        assert (
                                            app._run_service_cmd
                                            is mock_service_cmd_runner
                                        )


class TestMainModuleFunctions:
    """Test standalone functions in main module."""

    def test_main_module_imports(self):
        """Test that main module imports work correctly."""
        try:
            import piwardrive.main

            assert hasattr(piwardrive.main, "PiWardriveApp")
        except ImportError as e:
            pytest.fail(f"Failed to import piwardrive.main: {e}")

    def test_main_module_constants(self):
        """Test main module constants and attributes."""
        import piwardrive.main

        # Check that the module has expected attributes
        assert hasattr(piwardrive.main, "PiWardriveApp")
        assert hasattr(piwardrive.main, "logging")
        assert hasattr(piwardrive.main, "asyncio")
        assert hasattr(piwardrive.main, "os")
        assert hasattr(piwardrive.main, "Path")

    def test_main_module_logging_setup(self):
        """Test logging setup in main module."""

        # Test that urllib3 logging level is set
        import logging

        logger = logging.getLogger("urllib3")
        assert logger.level == logging.WARNING


class TestMainModuleIntegration:
    """Test integration scenarios for main module."""

    @patch("piwardrive.main.load_config")
    @patch("piwardrive.main.load_app_state")
    @patch("piwardrive.main.PollScheduler")
    @patch("piwardrive.main.diagnostics.HealthMonitor")
    def test_config_and_state_loading(
        self,
        mock_health_monitor,
        mock_poll_scheduler,
        mock_load_app_state,
        mock_load_config,
    ):
        """Test config and state loading integration."""
        from piwardrive.config import Config
        from piwardrive.persistence import AppState

        # Mock config
        mock_config = Mock(spec=Config)
        mock_config.admin_password_hash = "existing_hash"
        mock_config.enable_mqtt = False
        mock_config.remote_sync_url = None
        mock_config.remote_sync_interval = 0
        mock_config.notification_webhooks = []
        mock_config.notify_cpu_temp = 80.0
        mock_config.notify_disk_percent = 90.0
        mock_config.offline_tile_path = "/tmp/test.mbtiles"

        # Mock app state
        mock_app_state = Mock(spec=AppState)
        mock_app_state.last_screen = "dashboard"

        mock_load_config.return_value = mock_config
        mock_load_app_state.return_value = mock_app_state

        # Mock scheduler
        mock_scheduler_instance = Mock()
        mock_poll_scheduler.return_value = mock_scheduler_instance

        # Mock health monitor
        mock_health_monitor_instance = Mock()
        mock_health_monitor.return_value = mock_health_monitor_instance

        # Test that config and state are loaded correctly
        with patch("piwardrive.main.init_logging"):
            with patch("piwardrive.main.exception_handler.install"):
                with patch("piwardrive.main.utils.run_async_task"):
                    with patch("piwardrive.main.tile_maintenance", create=True):
                        with patch.dict(
                            os.environ, {"PW_ADMIN_PASSWORD": ""}, clear=False
                        ):
                            from piwardrive.main import PiWardriveApp

                            app = PiWardriveApp()

                            # Verify config and state are loaded
                            assert app.config_data is mock_config
                            assert app.app_state is mock_app_state
                            assert app.last_screen == "dashboard"

                            # Verify loading functions were called
                            mock_load_config.assert_called_once()
                            mock_load_app_state.assert_called_once()

    @patch("piwardrive.main.load_config")
    @patch("piwardrive.main.load_app_state")
    def test_mqtt_client_initialization(self, mock_load_app_state, mock_load_config):
        """Test MQTT client initialization when enabled."""
        from piwardrive.config import Config
        from piwardrive.persistence import AppState

        # Mock config with MQTT enabled
        mock_config = Mock(spec=Config)
        mock_config.admin_password_hash = ""
        mock_config.enable_mqtt = True
        mock_config.remote_sync_url = ""
        mock_config.remote_sync_interval = 0
        mock_config.notification_webhooks = []
        mock_config.notify_cpu_temp = 80.0
        mock_config.notify_disk_percent = 90.0
        mock_config.offline_tile_path = "/tmp/test.mbtiles"

        mock_app_state = Mock(spec=AppState)
        mock_app_state.last_screen = "main"

        mock_load_config.return_value = mock_config
        mock_load_app_state.return_value = mock_app_state

        # Mock MQTT client
        mock_mqtt_client = Mock()
        mock_mqtt_client.connect.return_value = None

        with patch("piwardrive.main.init_logging"):
            with patch("piwardrive.main.exception_handler.install"):
                with patch("piwardrive.main.utils.run_async_task"):
                    with patch("piwardrive.main.tile_maintenance", create=True):
                        with patch(
                            "piwardrive.mqtt.MQTTClient", return_value=mock_mqtt_client
                        ):
                            with patch.dict(
                                os.environ, {"PW_ADMIN_PASSWORD": ""}, clear=False
                            ):
                                from piwardrive.main import PiWardriveApp

                                app = PiWardriveApp()

                                # Verify MQTT client was initialized
                                assert app.mqtt_client is mock_mqtt_client
                                mock_mqtt_client.connect.assert_called_once()

    def test_environment_variable_handling(self):
        """Test handling of environment variables."""

        # Test PW_UPDATE_INTERVAL environment variable
        with patch.dict(os.environ, {"PW_UPDATE_INTERVAL": "24"}, clear=False):
            update_hours = int(os.getenv("PW_UPDATE_INTERVAL", "0"))
            assert update_hours == 24

        # Test PW_ADMIN_PASSWORD environment variable
        with patch.dict(os.environ, {"PW_ADMIN_PASSWORD": "test_pass"}, clear=False):
            admin_password = os.getenv("PW_ADMIN_PASSWORD")
            assert admin_password == "test_pass"

        # Test default values
        with patch.dict(os.environ, {}, clear=True):
            update_hours = int(os.getenv("PW_UPDATE_INTERVAL", "0"))
            admin_password = os.getenv("PW_ADMIN_PASSWORD")
            assert update_hours == 0
            assert admin_password is None


class TestMainModuleErrorHandling:
    """Test error handling in main module."""

    @patch("piwardrive.main.load_config")
    @patch("piwardrive.main.load_app_state")
    def test_scan_report_error_handling(self, mock_load_app_state, mock_load_config):
        """Test error handling in scan report scheduling."""
        from piwardrive.config import Config
        from piwardrive.persistence import AppState

        mock_config = Mock(spec=Config)
        mock_config.admin_password_hash = ""
        mock_config.enable_mqtt = False
        mock_config.remote_sync_url = ""
        mock_config.remote_sync_interval = 0
        mock_config.notification_webhooks = []
        mock_config.notify_cpu_temp = 80.0
        mock_config.notify_disk_percent = 90.0
        mock_config.offline_tile_path = "/tmp/test.mbtiles"

        mock_app_state = Mock(spec=AppState)
        mock_app_state.last_screen = "main"

        mock_load_config.return_value = mock_config
        mock_load_app_state.return_value = mock_app_state

        # Mock scan_report to raise an exception
        with patch("piwardrive.main.init_logging"):
            with patch("piwardrive.main.exception_handler.install"):
                with patch("piwardrive.main.utils.run_async_task"):
                    with patch("piwardrive.main.tile_maintenance", create=True):
                        with patch(
                            "piwardrive.scan_report",
                            side_effect=ImportError("Module not found"),
                        ):
                            with patch("logging.exception") as mock_log_exception:
                                with patch.dict(
                                    os.environ, {"PW_ADMIN_PASSWORD": ""}, clear=False
                                ):
                                    from piwardrive.main import PiWardriveApp

                                    app = PiWardriveApp()

                                    # Verify that exception was caught and logged
                                    mock_log_exception.assert_called_once_with(
                                        "Failed to schedule scan report"
                                    )

                                    # Verify app still initializes despite error
                                    assert app is not None
                                    assert hasattr(app, "scheduler")

    def test_password_hash_preservation(self):
        """Test that existing password hash is not overwritten."""
        from piwardrive.config import Config
        from piwardrive.main import PiWardriveApp
        from piwardrive.persistence import AppState

        # Mock config with existing password hash
        mock_config = Mock(spec=Config)
        mock_config.admin_password_hash = "existing_hash"
        mock_config.enable_mqtt = False
        mock_config.remote_sync_url = ""
        mock_config.remote_sync_interval = 0
        mock_config.notification_webhooks = []
        mock_config.notify_cpu_temp = 80.0
        mock_config.notify_disk_percent = 90.0
        mock_config.offline_tile_path = "/tmp/test.mbtiles"

        mock_app_state = Mock(spec=AppState)
        mock_app_state.last_screen = "main"

        with patch("piwardrive.main.load_config", return_value=mock_config):
            with patch("piwardrive.main.load_app_state", return_value=mock_app_state):
                with patch("piwardrive.main.init_logging"):
                    with patch("piwardrive.main.exception_handler.install"):
                        with patch("piwardrive.main.utils.run_async_task"):
                            with patch("piwardrive.main.tile_maintenance", create=True):
                                with patch(
                                    "piwardrive.main.hash_password"
                                ) as mock_hash_password:
                                    # Set environment variable but config already has hash
                                    with patch.dict(
                                        os.environ,
                                        {"PW_ADMIN_PASSWORD": "new_password"},
                                        clear=False,
                                    ):
                                        PiWardriveApp()

                                        # Verify existing hash is preserved
                                        assert (
                                            mock_config.admin_password_hash
                                            == "existing_hash"
                                        )
                                        # Verify hash_password was not called
                                        mock_hash_password.assert_not_called()
