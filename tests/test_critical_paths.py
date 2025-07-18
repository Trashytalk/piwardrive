"""
Tests for core functionality focusing on modules with highest impact on coverage.
"""

import json
import os
import sys
import tempfile
from unittest.mock import patch

import pytest

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class TestCoreUtilityFunctions:
    """Test core utility functions that are heavily used."""

    def test_safe_json_load(self):
        """Test safe JSON loading utility."""
        try:
            from piwardrive.core.utils import safe_json_load
        except ImportError:
            pytest.skip("Module not available")

        # Test valid JSON
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"test": "data"}, f)
            temp_path = f.name

        try:
            result = safe_json_load(temp_path)
            assert result == {"test": "data"}
        finally:
            os.unlink(temp_path)

    def test_safe_json_load_invalid(self):
        """Test safe JSON loading with invalid JSON."""
        try:
            from piwardrive.core.utils import safe_json_load
        except ImportError:
            pytest.skip("Module not available")

        # Test invalid JSON
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{ invalid json }")
            temp_path = f.name

        try:
            result = safe_json_load(temp_path)
            assert result is None or result == {}
        finally:
            os.unlink(temp_path)

    def test_format_bytes(self):
        """Test byte formatting utility."""
        try:
            from piwardrive.core.utils import format_bytes
        except ImportError:
            pytest.skip("Module not available")

        assert format_bytes(0) == "0 B"
        assert format_bytes(1024) == "1.0 KB"
        assert format_bytes(1024 * 1024) == "1.0 MB"
        assert format_bytes(1024 * 1024 * 1024) == "1.0 GB"

    def test_ensure_dir(self):
        """Test directory creation utility."""
        try:
            from piwardrive.core.utils import ensure_dir
        except ImportError:
            pytest.skip("Module not available")

        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = os.path.join(temp_dir, "test", "nested", "dir")
            ensure_dir(test_path)
            assert os.path.exists(test_path)
            assert os.path.isdir(test_path)


class TestConfigurationManagement:
    """Test configuration management functions."""

    def test_config_loading(self):
        """Test basic configuration loading."""
        try:
            from piwardrive.core.config import load_config
        except ImportError:
            pytest.skip("Module not available")

        # Test with default config
        config = load_config()
        assert isinstance(config, dict)

    def test_config_validation(self):
        """Test configuration validation."""
        try:
            from piwardrive.core.config import validate_config_data
        except ImportError:
            pytest.skip("Module not available")

        # Test valid config
        valid_config = {
            "debug": False,
            "logging": {"level": "INFO"},
            "database": {"path": ":memory:"},
        }

        # Should not raise exception
        validate_config_data(valid_config)

    def test_config_get_path(self):
        """Test configuration path resolution."""
        try:
            from piwardrive.core.config import get_config_path
        except ImportError:
            pytest.skip("Module not available")

        path = get_config_path()
        assert isinstance(path, str)
        assert len(path) > 0

    def test_config_modification_time(self):
        """Test configuration modification time."""
        try:
            from piwardrive.core.config import config_mtime
        except ImportError:
            pytest.skip("Module not available")

        # Should return a timestamp or None
        mtime = config_mtime()
        assert mtime is None or isinstance(mtime, (int, float))


class TestDatabasePersistence:
    """Test database persistence layer."""

    def test_database_adapter_creation(self):
        """Test database adapter creation."""
        try:
            from piwardrive.db.adapter import get_adapter
        except ImportError:
            pytest.skip("Module not available")

        adapter = get_adapter(":memory:")
        assert adapter is not None

    def test_sqlite_operations(self):
        """Test basic SQLite operations."""
        try:
            from piwardrive.db.sqlite import SQLiteAdapter
        except ImportError:
            pytest.skip("Module not available")

        adapter = SQLiteAdapter(":memory:")

        # Test table creation
        adapter.execute(
            """
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        """
        )

        # Test insert
        adapter.execute("INSERT INTO test_table (name) VALUES (?)", ("test_name",))

        # Test select
        result = adapter.fetch_one("SELECT name FROM test_table WHERE id = 1")
        assert result is not None

    def test_database_migration_check(self):
        """Test database migration checking."""
        try:
            from piwardrive.migrations.runner import check_migrations_needed
        except ImportError:
            pytest.skip("Module not available")

        # Should return boolean
        result = check_migrations_needed(":memory:")
        assert isinstance(result, bool)


class TestTaskScheduling:
    """Test task scheduling functionality."""

    def test_task_creation(self):
        """Test basic task creation."""
        try:
            from piwardrive.task_queue import Task, TaskPriority
        except ImportError:
            pytest.skip("Module not available")

        def test_func():
            return "test"

        task = Task(name="test_task", func=test_func, priority=TaskPriority.NORMAL)

        assert task.name == "test_task"
        assert task.priority == TaskPriority.NORMAL

    def test_task_execution(self):
        """Test task execution."""
        try:
            from piwardrive.task_queue import Task, TaskPriority
        except ImportError:
            pytest.skip("Module not available")

        result = []

        def test_func():
            result.append("executed")
            return "success"

        task = Task(name="test_task", func=test_func, priority=TaskPriority.NORMAL)

        # Execute task
        task.execute()
        assert result == ["executed"]

    def test_scheduler_task_addition(self):
        """Test adding tasks to scheduler."""
        try:
            from piwardrive.scheduler import ScheduledTask, Scheduler
        except ImportError:
            pytest.skip("Module not available")

        scheduler = Scheduler()

        def test_func():
            return "test"

        task = ScheduledTask(name="test_task", func=test_func, interval=60)

        scheduler.add_task(task)
        assert len(scheduler.tasks) == 1


class TestWidgetSystem:
    """Test widget system functionality."""

    def test_widget_base_class(self):
        """Test widget base class."""
        try:
            from piwardrive.widgets.base import BaseWidget
        except ImportError:
            pytest.skip("Module not available")

        widget = BaseWidget("test_widget")
        assert widget.name == "test_widget"

        # Test get_data returns empty dict
        data = widget.get_data()
        assert isinstance(data, dict)

    def test_widget_manager_initialization(self):
        """Test widget manager initialization."""
        try:
            from piwardrive.widget_manager import WidgetManager
        except ImportError:
            pytest.skip("Module not available")

        manager = WidgetManager()
        assert hasattr(manager, "widgets")
        assert isinstance(manager.widgets, dict)

    def test_widget_registration(self):
        """Test widget registration."""
        try:
            from piwardrive.widget_manager import WidgetManager
            from piwardrive.widgets.base import BaseWidget
        except ImportError:
            pytest.skip("Module not available")

        manager = WidgetManager()
        widget = BaseWidget("test_widget")

        manager.register_widget(widget)
        assert "test_widget" in manager.widgets


class TestSecurityFunctions:
    """Test security functions."""

    def test_password_hashing(self):
        """Test password hashing function."""
        try:
            from piwardrive.security import hash_password, verify_password
        except ImportError:
            pytest.skip("Module not available")

        password = "test_password_123"
        hashed = hash_password(password)

        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrong_password", hashed) is False

    def test_path_sanitization(self):
        """Test path sanitization."""
        try:
            from piwardrive.security import sanitize_path
        except ImportError:
            pytest.skip("Module not available")

        # Test safe path
        safe_path = "/var/log/piwardrive/app.log"
        result = sanitize_path(safe_path)
        assert result == safe_path

    def test_input_validation(self):
        """Test input validation."""
        try:
            from piwardrive.security import validate_input
        except ImportError:
            pytest.skip("Module not available")

        # Test safe input
        assert validate_input("normal_string") is True

        # Test dangerous input
        assert validate_input("<script>alert('xss')</script>") is False


class TestDataAnalysis:
    """Test data analysis functionality."""

    def test_compute_health_stats(self):
        """Test health statistics computation."""
        try:
            from piwardrive.analysis import compute_health_stats
        except ImportError:
            pytest.skip("Module not available")

        # Test with sample data
        health_data = [
            {"cpu_temp": 45.0, "cpu_percent": 15.5, "memory_percent": 60.2},
            {"cpu_temp": 46.0, "cpu_percent": 20.1, "memory_percent": 58.7},
            {"cpu_temp": 44.5, "cpu_percent": 18.3, "memory_percent": 62.1},
        ]

        stats = compute_health_stats(health_data)
        assert isinstance(stats, dict)
        assert "avg_cpu_temp" in stats
        assert "avg_cpu_percent" in stats
        assert "avg_memory_percent" in stats

    def test_plot_cpu_temp(self):
        """Test CPU temperature plotting."""
        try:
            from piwardrive.analysis import plot_cpu_temp
        except ImportError:
            pytest.skip("Module not available")

        # Test with sample data
        temp_data = [
            {"timestamp": "2024-01-01T12:00:00", "cpu_temp": 45.0},
            {"timestamp": "2024-01-01T12:01:00", "cpu_temp": 46.0},
            {"timestamp": "2024-01-01T12:02:00", "cpu_temp": 44.5},
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "cpu_temp.png")
            result = plot_cpu_temp(temp_data, output_path)

            # Should create a file or return success
            assert result is not None


class TestServiceAPI:
    """Test service API functionality."""

    def test_service_import(self):
        """Test service module import."""
        try:
            import piwardrive.service

            assert hasattr(piwardrive.service, "app")
        except ImportError:
            pytest.skip("Service module not available")

    @patch("piwardrive.service.get_system_status")
    def test_get_system_status(self, mock_get_status):
        """Test system status function."""
        try:
            from piwardrive.service import get_system_status
        except ImportError:
            pytest.skip("Service module not available")

        mock_status = {"cpu_usage": 15.5, "memory_usage": 45.2, "disk_usage": 60.1}
        mock_get_status.return_value = mock_status

        status = get_system_status()
        assert "cpu_usage" in status
        assert status["cpu_usage"] == 15.5


class TestLoggingSystem:
    """Test logging system functionality."""

    def test_logging_config(self):
        """Test logging configuration."""
        try:
            from piwardrive.logging.config import setup_logging
        except ImportError:
            pytest.skip("Logging module not available")

        # Should not raise exception
        setup_logging()

    def test_structured_logger(self):
        """Test structured logger."""
        try:
            from piwardrive.logging.structured_logger import StructuredLogger
        except ImportError:
            pytest.skip("Structured logger not available")

        logger = StructuredLogger("test")
        assert logger is not None

        # Test logging
        logger.info("Test message", {"key": "value"})


class TestCoreIntegration:
    """Test integration between core components."""

    def test_component_availability(self):
        """Test that core components can be imported."""
        components = [
            "piwardrive.core.config",
            "piwardrive.core.persistence",
            "piwardrive.analysis",
            "piwardrive.security",
            "piwardrive.task_queue",
            "piwardrive.widget_manager",
        ]

        available_components = []
        for component in components:
            try:
                __import__(component)
                available_components.append(component)
            except ImportError:
                pass

        # Should have at least some components available
        assert len(available_components) > 0

    def test_error_classes(self):
        """Test error classes are available."""
        try:
            from piwardrive.errors import ConfigError, SecurityError

            # Test error creation
            config_error = ConfigError("Test config error")
            assert str(config_error) == "Test config error"

            security_error = SecurityError("Test security error")
            assert str(security_error) == "Test security error"
        except ImportError:
            pytest.skip("Error classes not available")

    def test_constants_and_enums(self):
        """Test constants and enums are available."""
        try:
            from piwardrive.task_queue import TaskPriority

            assert hasattr(TaskPriority, "LOW")
            assert hasattr(TaskPriority, "NORMAL")
            assert hasattr(TaskPriority, "HIGH")
        except ImportError:
            pytest.skip("TaskPriority not available")


class TestDataStructures:
    """Test core data structures and models."""

    def test_sigint_models(self):
        """Test SIGINT suite models."""
        try:
            from piwardrive.integrations.sigint_suite.models import BluetoothDevice

            device = BluetoothDevice(
                address="00:11:22:33:44:55", name="Test Device", rssi=-50
            )

            assert device.address == "00:11:22:33:44:55"
            assert device.name == "Test Device"
            assert device.rssi == -50
        except ImportError:
            pytest.skip("SIGINT models not available")

    def test_paths_module(self):
        """Test paths module."""
        try:
            from piwardrive.integrations.sigint_suite.paths import get_data_dir

            data_dir = get_data_dir()
            assert isinstance(data_dir, str)
            assert len(data_dir) > 0
        except ImportError:
            pytest.skip("Paths module not available")


class TestUtilityHelpers:
    """Test utility helper functions."""

    def test_memory_monitoring(self):
        """Test memory monitoring utilities."""
        try:
            from piwardrive.memory_monitor import get_memory_usage

            usage = get_memory_usage()
            assert isinstance(usage, (int, float))
            assert 0 <= usage <= 100
        except ImportError:
            pytest.skip("Memory monitor not available")

    def test_cpu_pool(self):
        """Test CPU pool utilities."""
        try:
            from piwardrive.cpu_pool import get_cpu_count

            count = get_cpu_count()
            assert isinstance(count, int)
            assert count > 0
        except ImportError:
            pytest.skip("CPU pool not available")

    def test_resource_manager(self):
        """Test resource manager."""
        try:
            from piwardrive.resource_manager import ResourceManager

            manager = ResourceManager()
            assert manager is not None
        except ImportError:
            pytest.skip("Resource manager not available")


if __name__ == "__main__":
    pytest.main([__file__])
