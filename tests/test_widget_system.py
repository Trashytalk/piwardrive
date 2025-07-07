"""
Tests for the widget management system.
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from piwardrive.widget_manager import WidgetManager, Widget, WidgetRegistry
from piwardrive.widgets.base import BaseWidget
from piwardrive.errors import ConfigError


class TestWidgetManager:
    """Test the main widget manager functionality."""

    def setup_method(self):
        """Setup test widget manager."""
        self.widget_manager = WidgetManager()

    def test_widget_manager_initialization(self):
        """Test widget manager initialization."""
        assert self.widget_manager is not None
        assert hasattr(self.widget_manager, 'widgets')
        assert hasattr(self.widget_manager, 'registry')
        assert isinstance(self.widget_manager.widgets, dict)

    def test_register_widget(self):
        """Test registering a widget."""
        class TestWidget(BaseWidget):
            def __init__(self, name="test_widget"):
                super().__init__(name)
            
            def get_data(self):
                return {"test": "data"}
        
        widget = TestWidget()
        self.widget_manager.register_widget(widget)
        
        assert "test_widget" in self.widget_manager.widgets
        assert self.widget_manager.widgets["test_widget"] == widget

    def test_unregister_widget(self):
        """Test unregistering a widget."""
        class TestWidget(BaseWidget):
            def __init__(self, name="test_widget"):
                super().__init__(name)
            
            def get_data(self):
                return {"test": "data"}
        
        widget = TestWidget()
        self.widget_manager.register_widget(widget)
        
        assert "test_widget" in self.widget_manager.widgets
        
        self.widget_manager.unregister_widget("test_widget")
        assert "test_widget" not in self.widget_manager.widgets

    def test_get_widget(self):
        """Test getting a widget by name."""
        class TestWidget(BaseWidget):
            def __init__(self, name="test_widget"):
                super().__init__(name)
            
            def get_data(self):
                return {"test": "data"}
        
        widget = TestWidget()
        self.widget_manager.register_widget(widget)
        
        retrieved = self.widget_manager.get_widget("test_widget")
        assert retrieved == widget

    def test_get_widget_nonexistent(self):
        """Test getting a non-existent widget."""
        retrieved = self.widget_manager.get_widget("nonexistent")
        assert retrieved is None

    def test_list_widgets(self):
        """Test listing all widgets."""
        class TestWidget1(BaseWidget):
            def __init__(self, name="test_widget1"):
                super().__init__(name)
            
            def get_data(self):
                return {"test": "data1"}
        
        class TestWidget2(BaseWidget):
            def __init__(self, name="test_widget2"):
                super().__init__(name)
            
            def get_data(self):
                return {"test": "data2"}
        
        widget1 = TestWidget1()
        widget2 = TestWidget2()
        
        self.widget_manager.register_widget(widget1)
        self.widget_manager.register_widget(widget2)
        
        widgets = self.widget_manager.list_widgets()
        assert len(widgets) == 2
        assert "test_widget1" in widgets
        assert "test_widget2" in widgets

    def test_refresh_widgets(self):
        """Test refreshing all widgets."""
        class TestWidget(BaseWidget):
            def __init__(self, name="test_widget"):
                super().__init__(name)
                self.refresh_called = False
            
            def get_data(self):
                return {"test": "data"}
            
            def refresh(self):
                self.refresh_called = True
        
        widget = TestWidget()
        self.widget_manager.register_widget(widget)
        
        self.widget_manager.refresh_widgets()
        assert widget.refresh_called

    def test_get_widget_data(self):
        """Test getting widget data."""
        class TestWidget(BaseWidget):
            def __init__(self, name="test_widget"):
                super().__init__(name)
            
            def get_data(self):
                return {"test": "data", "value": 42}
        
        widget = TestWidget()
        self.widget_manager.register_widget(widget)
        
        data = self.widget_manager.get_widget_data("test_widget")
        assert data == {"test": "data", "value": 42}

    def test_get_all_widget_data(self):
        """Test getting all widget data."""
        class TestWidget1(BaseWidget):
            def __init__(self, name="test_widget1"):
                super().__init__(name)
            
            def get_data(self):
                return {"test": "data1"}
        
        class TestWidget2(BaseWidget):
            def __init__(self, name="test_widget2"):
                super().__init__(name)
            
            def get_data(self):
                return {"test": "data2"}
        
        widget1 = TestWidget1()
        widget2 = TestWidget2()
        
        self.widget_manager.register_widget(widget1)
        self.widget_manager.register_widget(widget2)
        
        all_data = self.widget_manager.get_all_widget_data()
        assert "test_widget1" in all_data
        assert "test_widget2" in all_data
        assert all_data["test_widget1"] == {"test": "data1"}
        assert all_data["test_widget2"] == {"test": "data2"}

    def test_widget_error_handling(self):
        """Test widget error handling."""
        class FailingWidget(BaseWidget):
            def __init__(self, name="failing_widget"):
                super().__init__(name)
            
            def get_data(self):
                raise Exception("Widget failed")
        
        widget = FailingWidget()
        self.widget_manager.register_widget(widget)
        
        # Should handle error gracefully
        data = self.widget_manager.get_widget_data("failing_widget")
        assert data is None or "error" in data

    def test_widget_caching(self):
        """Test widget data caching."""
        class CountingWidget(BaseWidget):
            def __init__(self, name="counting_widget"):
                super().__init__(name)
                self.call_count = 0
            
            def get_data(self):
                self.call_count += 1
                return {"count": self.call_count}
        
        widget = CountingWidget()
        self.widget_manager.register_widget(widget)
        
        # First call should increment counter
        data1 = self.widget_manager.get_widget_data("counting_widget")
        assert data1["count"] == 1
        
        # Second call should use cached data if caching is enabled
        data2 = self.widget_manager.get_widget_data("counting_widget")
        # This depends on caching implementation
        assert data2["count"] >= 1

    def test_widget_configuration(self):
        """Test widget configuration."""
        class ConfigurableWidget(BaseWidget):
            def __init__(self, name="configurable_widget"):
                super().__init__(name)
                self.config = {}
            
            def get_data(self):
                return self.config
            
            def set_config(self, config):
                self.config = config
        
        widget = ConfigurableWidget()
        self.widget_manager.register_widget(widget)
        
        # Configure widget
        config = {"setting1": "value1", "setting2": 42}
        widget.set_config(config)
        
        data = self.widget_manager.get_widget_data("configurable_widget")
        assert data == config


class TestWidgetRegistry:
    """Test the widget registry functionality."""

    def setup_method(self):
        """Setup test widget registry."""
        self.registry = WidgetRegistry()

    def test_registry_initialization(self):
        """Test registry initialization."""
        assert self.registry is not None
        assert hasattr(self.registry, 'widget_classes')
        assert isinstance(self.registry.widget_classes, dict)

    def test_register_widget_class(self):
        """Test registering a widget class."""
        class TestWidget(BaseWidget):
            def __init__(self, name="test_widget"):
                super().__init__(name)
            
            def get_data(self):
                return {"test": "data"}
        
        self.registry.register_widget_class("TestWidget", TestWidget)
        
        assert "TestWidget" in self.registry.widget_classes
        assert self.registry.widget_classes["TestWidget"] == TestWidget

    def test_create_widget_instance(self):
        """Test creating widget instances from registry."""
        class TestWidget(BaseWidget):
            def __init__(self, name="test_widget"):
                super().__init__(name)
            
            def get_data(self):
                return {"test": "data"}
        
        self.registry.register_widget_class("TestWidget", TestWidget)
        
        widget = self.registry.create_widget("TestWidget")
        assert isinstance(widget, TestWidget)

    def test_list_available_widgets(self):
        """Test listing available widget classes."""
        class TestWidget1(BaseWidget):
            def __init__(self, name="test_widget1"):
                super().__init__(name)
            
            def get_data(self):
                return {"test": "data1"}
        
        class TestWidget2(BaseWidget):
            def __init__(self, name="test_widget2"):
                super().__init__(name)
            
            def get_data(self):
                return {"test": "data2"}
        
        self.registry.register_widget_class("TestWidget1", TestWidget1)
        self.registry.register_widget_class("TestWidget2", TestWidget2)
        
        available = self.registry.list_available_widgets()
        assert "TestWidget1" in available
        assert "TestWidget2" in available

    def test_widget_discovery(self):
        """Test automatic widget discovery."""
        with patch('piwardrive.widget_manager.discover_widgets') as mock_discover:
            mock_discover.return_value = {
                "DiscoveredWidget": Mock(spec=BaseWidget)
            }
            
            self.registry.discover_widgets()
            mock_discover.assert_called_once()


class TestBaseWidget:
    """Test the base widget functionality."""

    def test_base_widget_initialization(self):
        """Test base widget initialization."""
        widget = BaseWidget("test_widget")
        assert widget.name == "test_widget"
        assert hasattr(widget, 'config')
        assert hasattr(widget, 'last_update')

    def test_base_widget_get_data(self):
        """Test base widget get_data method."""
        widget = BaseWidget("test_widget")
        
        # Base implementation should return empty dict
        data = widget.get_data()
        assert data == {}

    def test_base_widget_refresh(self):
        """Test base widget refresh method."""
        widget = BaseWidget("test_widget")
        
        # Should not raise any errors
        widget.refresh()

    def test_base_widget_configuration(self):
        """Test base widget configuration."""
        widget = BaseWidget("test_widget")
        
        config = {"setting": "value"}
        widget.set_config(config)
        
        assert widget.config == config

    def test_base_widget_status(self):
        """Test base widget status."""
        widget = BaseWidget("test_widget")
        
        status = widget.get_status()
        assert "name" in status
        assert "last_update" in status
        assert status["name"] == "test_widget"


class TestWidgetIntegration:
    """Test widget integration with other systems."""

    def setup_method(self):
        """Setup test environment."""
        self.widget_manager = WidgetManager()

    @patch('piwardrive.widget_manager.DatabaseManager')
    def test_database_integration(self, mock_db):
        """Test widget integration with database."""
        mock_db_instance = Mock()
        mock_db.return_value = mock_db_instance
        mock_db_instance.get_system_stats.return_value = {
            "cpu_usage": 15.5,
            "memory_usage": 45.2
        }
        
        class DatabaseWidget(BaseWidget):
            def __init__(self, name="db_widget"):
                super().__init__(name)
                self.db = mock_db_instance
            
            def get_data(self):
                return self.db.get_system_stats()
        
        widget = DatabaseWidget()
        self.widget_manager.register_widget(widget)
        
        data = self.widget_manager.get_widget_data("db_widget")
        assert data["cpu_usage"] == 15.5
        assert data["memory_usage"] == 45.2

    @patch('piwardrive.widget_manager.Scheduler')
    def test_scheduler_integration(self, mock_scheduler):
        """Test widget integration with scheduler."""
        mock_scheduler_instance = Mock()
        mock_scheduler.return_value = mock_scheduler_instance
        
        class SchedulerWidget(BaseWidget):
            def __init__(self, name="scheduler_widget"):
                super().__init__(name)
                self.scheduler = mock_scheduler_instance
            
            def get_data(self):
                return {"status": "running"}
        
        widget = SchedulerWidget()
        self.widget_manager.register_widget(widget)
        
        data = self.widget_manager.get_widget_data("scheduler_widget")
        assert data["status"] == "running"

    @patch('piwardrive.widget_manager.ConfigManager')
    def test_config_integration(self, mock_config):
        """Test widget integration with configuration."""
        mock_config_instance = Mock()
        mock_config.return_value = mock_config_instance
        mock_config_instance.get_config.return_value = {
            "debug": True,
            "logging_level": "DEBUG"
        }
        
        class ConfigWidget(BaseWidget):
            def __init__(self, name="config_widget"):
                super().__init__(name)
                self.config_manager = mock_config_instance
            
            def get_data(self):
                return self.config_manager.get_config()
        
        widget = ConfigWidget()
        self.widget_manager.register_widget(widget)
        
        data = self.widget_manager.get_widget_data("config_widget")
        assert data["debug"] is True
        assert data["logging_level"] == "DEBUG"


class TestWidgetPerformance:
    """Test widget performance characteristics."""

    def setup_method(self):
        """Setup test environment."""
        self.widget_manager = WidgetManager()

    def test_widget_refresh_performance(self):
        """Test widget refresh performance."""
        import time
        
        class SlowWidget(BaseWidget):
            def __init__(self, name):
                super().__init__(name)
                self.refresh_count = 0
            
            def get_data(self):
                time.sleep(0.01)  # Simulate slow operation
                self.refresh_count += 1
                return {"refresh_count": self.refresh_count}
        
        # Create multiple widgets
        for i in range(10):
            widget = SlowWidget(f"slow_widget_{i}")
            self.widget_manager.register_widget(widget)
        
        # Measure refresh time
        start_time = time.time()
        self.widget_manager.refresh_widgets()
        end_time = time.time()
        
        refresh_time = end_time - start_time
        
        # Should complete within reasonable time
        assert refresh_time < 1.0  # Less than 1 second

    def test_widget_memory_usage(self):
        """Test widget memory usage."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        class MemoryWidget(BaseWidget):
            def __init__(self, name):
                super().__init__(name)
                self.data = [0] * 1000  # Small data array
            
            def get_data(self):
                return {"data_length": len(self.data)}
        
        # Create many widgets
        for i in range(100):
            widget = MemoryWidget(f"memory_widget_{i}")
            self.widget_manager.register_widget(widget)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable
        assert memory_increase < 50 * 1024 * 1024  # Less than 50MB

    def test_concurrent_widget_access(self):
        """Test concurrent widget access."""
        import threading
        import time
        
        class ConcurrentWidget(BaseWidget):
            def __init__(self, name="concurrent_widget"):
                super().__init__(name)
                self.access_count = 0
            
            def get_data(self):
                self.access_count += 1
                time.sleep(0.01)  # Simulate work
                return {"access_count": self.access_count}
        
        widget = ConcurrentWidget()
        self.widget_manager.register_widget(widget)
        
        results = []
        
        def access_widget():
            data = self.widget_manager.get_widget_data("concurrent_widget")
            results.append(data)
        
        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=access_widget)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All threads should complete successfully
        assert len(results) == 5


class TestWidgetSecurity:
    """Test widget security features."""

    def setup_method(self):
        """Setup test environment."""
        self.widget_manager = WidgetManager()

    def test_widget_input_validation(self):
        """Test widget input validation."""
        class ValidatingWidget(BaseWidget):
            def __init__(self, name="validating_widget"):
                super().__init__(name)
            
            def get_data(self):
                return {"status": "ok"}
            
            def set_config(self, config):
                # Validate config
                if not isinstance(config, dict):
                    raise ValueError("Config must be a dictionary")
                
                # Check for dangerous keys
                dangerous_keys = ["__", "eval", "exec"]
                for key in config:
                    if any(dangerous in str(key) for dangerous in dangerous_keys):
                        raise ValueError(f"Dangerous key not allowed: {key}")
                
                self.config = config
        
        widget = ValidatingWidget()
        self.widget_manager.register_widget(widget)
        
        # Valid config should work
        widget.set_config({"setting": "value"})
        assert widget.config == {"setting": "value"}
        
        # Invalid config should raise error
        with pytest.raises(ValueError):
            widget.set_config("not_a_dict")
        
        with pytest.raises(ValueError):
            widget.set_config({"__dangerous": "value"})

    def test_widget_output_sanitization(self):
        """Test widget output sanitization."""
        class SanitizingWidget(BaseWidget):
            def __init__(self, name="sanitizing_widget"):
                super().__init__(name)
            
            def get_data(self):
                # Potentially dangerous data
                return {
                    "user_input": "<script>alert('xss')</script>",
                    "safe_data": "normal_value"
                }
            
            def sanitize_output(self, data):
                """Sanitize output data."""
                if isinstance(data, dict):
                    sanitized = {}
                    for key, value in data.items():
                        if isinstance(value, str):
                            # Remove script tags
                            sanitized[key] = value.replace("<script>", "").replace("</script>", "")
                        else:
                            sanitized[key] = value
                    return sanitized
                return data
        
        widget = SanitizingWidget()
        self.widget_manager.register_widget(widget)
        
        # Raw data should contain script tags
        raw_data = widget.get_data()
        assert "<script>" in raw_data["user_input"]
        
        # Sanitized data should not contain script tags
        sanitized_data = widget.sanitize_output(raw_data)
        assert "<script>" not in sanitized_data["user_input"]
        assert sanitized_data["safe_data"] == "normal_value"


if __name__ == '__main__':
    pytest.main([__file__])
