"""
Tests for the main application entry point and core startup functionality.
"""

import os
import sys
from unittest.mock import Mock, patch

import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from piwardrive.errors import ConfigError
from piwardrive.main import PiWardriveApp
from piwardrive.main import main as main_func


class TestPiWardriveApp:
    """Test core PiWardrive application class."""

    def test_app_initialization(self):
        """Test basic app initialization."""
        app = PiWardriveApp()
        assert app is not None
        assert hasattr(app, "config")
        assert hasattr(app, "scheduler")

    @patch("piwardrive.main.load_config")
    def test_app_with_config(self, mock_load_config):
        """Test app initialization with configuration."""
        mock_config = {
            "debug": False,
            "logging": {"level": "INFO"},
            "database": {"path": ":memory:"},
        }
        mock_load_config.return_value = mock_config

        app = PiWardriveApp()
        assert app.config is not None

    @patch("piwardrive.main.setup_logging")
    @patch("piwardrive.main.load_config")
    def test_app_logging_setup(self, mock_load_config, mock_setup_logging):
        """Test logging setup during app initialization."""
        mock_config = {
            "debug": True,
            "logging": {"level": "DEBUG"},
            "database": {"path": ":memory:"},
        }
        mock_load_config.return_value = mock_config

        PiWardriveApp()
        mock_setup_logging.assert_called_once()

    def test_app_start_stop(self):
        """Test app start and stop functionality."""
        app = PiWardriveApp()

        # Mock scheduler to avoid actual hardware dependencies
        app.scheduler = Mock()
        app.scheduler.start = Mock()
        app.scheduler.stop = Mock()

        # Test start
        app.start()
        app.scheduler.start.assert_called_once()

        # Test stop
        app.stop()
        app.scheduler.stop.assert_called_once()

    @patch("piwardrive.main.load_config")
    def test_app_config_error_handling(self, mock_load_config):
        """Test handling of configuration errors."""
        mock_load_config.side_effect = ConfigError("Invalid config")

        with pytest.raises(ConfigError):
            PiWardriveApp()

    @patch("piwardrive.main.DatabaseManager")
    @patch("piwardrive.main.load_config")
    def test_app_database_initialization(self, mock_load_config, mock_db_manager):
        """Test database initialization."""
        mock_config = {
            "debug": False,
            "logging": {"level": "INFO"},
            "database": {"path": "/tmp/test.db"},
        }
        mock_load_config.return_value = mock_config

        PiWardriveApp()
        mock_db_manager.assert_called_once()

    def test_app_scheduler_initialization(self):
        """Test scheduler initialization."""
        app = PiWardriveApp()
        assert app.scheduler is not None
        assert hasattr(app.scheduler, "start")
        assert hasattr(app.scheduler, "stop")

    @patch("piwardrive.main.WidgetManager")
    def test_app_widget_manager_initialization(self, mock_widget_manager):
        """Test widget manager initialization."""
        PiWardriveApp()
        mock_widget_manager.assert_called_once()

    def test_app_context_manager(self):
        """Test app as context manager."""
        app = PiWardriveApp()
        app.scheduler = Mock()

        with app:
            app.scheduler.start.assert_called_once()

        app.scheduler.stop.assert_called_once()

    def test_app_signal_handlers(self):
        """Test signal handler registration."""
        app = PiWardriveApp()

        # Test that signal handlers are set up
        assert hasattr(app, "_setup_signal_handlers")

        # Mock signal handling
        with patch("signal.signal") as mock_signal:
            app._setup_signal_handlers()
            assert mock_signal.call_count > 0


class TestMainFunction:
    """Test main application entry point function."""

    @patch("piwardrive.main.PiWardriveApp")
    @patch("sys.argv", ["main.py"])
    def test_main_basic(self, mock_app_class):
        """Test basic main function execution."""
        mock_app = Mock()
        mock_app_class.return_value = mock_app

        with patch("piwardrive.main.parse_arguments") as mock_parse:
            mock_parse.return_value = Mock(
                config=None, debug=False, daemon=False, profile=None
            )

            main_func()
            mock_app_class.assert_called_once()
            mock_app.start.assert_called_once()

    @patch("piwardrive.main.PiWardriveApp")
    @patch("sys.argv", ["main.py", "--debug"])
    def test_main_with_debug(self, mock_app_class):
        """Test main function with debug flag."""
        mock_app = Mock()
        mock_app_class.return_value = mock_app

        with patch("piwardrive.main.parse_arguments") as mock_parse:
            mock_parse.return_value = Mock(
                config=None, debug=True, daemon=False, profile=None
            )

            main_func()
            mock_app_class.assert_called_once()

    @patch("piwardrive.main.PiWardriveApp")
    @patch("sys.argv", ["main.py", "--config", "custom.json"])
    def test_main_with_config(self, mock_app_class):
        """Test main function with custom config."""
        mock_app = Mock()
        mock_app_class.return_value = mock_app

        with patch("piwardrive.main.parse_arguments") as mock_parse:
            mock_parse.return_value = Mock(
                config="custom.json", debug=False, daemon=False, profile=None
            )

            main_func()
            mock_app_class.assert_called_once()

    @patch("piwardrive.main.PiWardriveApp")
    def test_main_keyboard_interrupt(self, mock_app_class):
        """Test main function handling keyboard interrupt."""
        mock_app = Mock()
        mock_app.start.side_effect = KeyboardInterrupt()
        mock_app_class.return_value = mock_app

        with patch("piwardrive.main.parse_arguments") as mock_parse:
            mock_parse.return_value = Mock(
                config=None, debug=False, daemon=False, profile=None
            )

            with pytest.raises(SystemExit):
                main_func()

    @patch("piwardrive.main.PiWardriveApp")
    def test_main_exception_handling(self, mock_app_class):
        """Test main function exception handling."""
        mock_app = Mock()
        mock_app.start.side_effect = Exception("Test error")
        mock_app_class.return_value = mock_app

        with patch("piwardrive.main.parse_arguments") as mock_parse:
            mock_parse.return_value = Mock(
                config=None, debug=False, daemon=False, profile=None
            )

            with pytest.raises(SystemExit):
                main_func()

    @patch("piwardrive.main.PiWardriveApp")
    def test_main_daemon_mode(self, mock_app_class):
        """Test main function in daemon mode."""
        mock_app = Mock()
        mock_app_class.return_value = mock_app

        with patch("piwardrive.main.parse_arguments") as mock_parse:
            mock_parse.return_value = Mock(
                config=None, debug=False, daemon=True, profile=None
            )

            with patch("piwardrive.main.daemonize") as mock_daemonize:
                main_func()
                mock_daemonize.assert_called_once()

    @patch("piwardrive.main.PiWardriveApp")
    def test_main_profiling(self, mock_app_class):
        """Test main function with profiling enabled."""
        mock_app = Mock()
        mock_app_class.return_value = mock_app

        with patch("piwardrive.main.parse_arguments") as mock_parse:
            mock_parse.return_value = Mock(
                config=None, debug=False, daemon=False, profile="profile.out"
            )

            with patch("cProfile.Profile") as mock_profile:
                main_func()
                mock_profile.assert_called_once()


class TestApplicationState:
    """Test application state management."""

    def test_app_state_persistence(self):
        """Test application state saving and loading."""
        app = PiWardriveApp()

        # Mock state persistence
        with patch("piwardrive.main.save_app_state") as mock_save:
            with patch("piwardrive.main.load_app_state") as mock_load:
                mock_load.return_value = {"last_screen": "dashboard"}

                state = app._load_app_state()
                assert state["last_screen"] == "dashboard"

                app._save_app_state({"last_screen": "settings"})
                mock_save.assert_called_once()

    def test_app_state_recovery(self):
        """Test application state recovery after crash."""
        app = PiWardriveApp()

        # Mock crash recovery
        with patch("piwardrive.main.detect_crash") as mock_detect:
            mock_detect.return_value = True

            with patch("piwardrive.main.recover_from_crash") as mock_recover:
                app._handle_crash_recovery()
                mock_recover.assert_called_once()

    def test_app_health_monitoring(self):
        """Test application health monitoring."""
        app = PiWardriveApp()

        # Mock health check
        with patch("piwardrive.main.check_app_health") as mock_health:
            mock_health.return_value = {
                "status": "healthy",
                "cpu_usage": 15.5,
                "memory_usage": 45.2,
            }

            health = app._check_health()
            assert health["status"] == "healthy"
            assert "cpu_usage" in health
            assert "memory_usage" in health


class TestApplicationIntegration:
    """Test application integration with other components."""

    def test_app_service_integration(self):
        """Test app integration with service layer."""
        app = PiWardriveApp()

        # Mock service integration
        with patch("piwardrive.main.start_service") as mock_service:
            app._start_services()
            mock_service.assert_called_once()

    def test_app_widget_integration(self):
        """Test app integration with widget system."""
        app = PiWardriveApp()

        # Mock widget integration
        with patch("piwardrive.main.initialize_widgets") as mock_widgets:
            app._initialize_widgets()
            mock_widgets.assert_called_once()

    def test_app_database_integration(self):
        """Test app integration with database."""
        app = PiWardriveApp()

        # Mock database integration
        with patch("piwardrive.main.initialize_database") as mock_db:
            app._initialize_database()
            mock_db.assert_called_once()

    def test_app_scheduler_integration(self):
        """Test app integration with scheduler."""
        app = PiWardriveApp()

        # Mock scheduler integration
        with patch("piwardrive.main.setup_scheduler") as mock_scheduler:
            app._setup_scheduler()
            mock_scheduler.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__])
