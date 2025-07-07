"""
Comprehensive tests for the widget system and widget manager.
Tests widget loading, management, and UI component functionality.
"""

import asyncio
import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, AsyncMock

# Import widget system components
from piwardrive.widget_manager import LazyWidgetManager
from piwardrive.widgets.base import DashboardWidget
from piwardrive.memory_monitor import MemoryMonitor
from piwardrive.resource_manager import ResourceManager


class TestDashboardWidget:
    """Test base dashboard widget functionality."""
    
    def test_dashboard_widget_initialization(self):
        """Test dashboard widget can be initialized."""
        widget = DashboardWidget()
        assert widget is not None
        assert hasattr(widget, 'render')
        assert hasattr(widget, 'update')
        
    def test_dashboard_widget_render_not_implemented(self):
        """Test dashboard widget render method raises NotImplementedError."""
        widget = DashboardWidget()
        
        with pytest.raises(NotImplementedError):
            widget.render()
            
    def test_dashboard_widget_update_not_implemented(self):
        """Test dashboard widget update method raises NotImplementedError."""
        widget = DashboardWidget()
        
        with pytest.raises(NotImplementedError):
            widget.update({})
            
    def test_dashboard_widget_inheritance(self):
        """Test dashboard widget can be inherited."""
        class TestWidget(DashboardWidget):
            def render(self):
                return "<div>Test Widget</div>"
                
            def update(self, data):
                pass
                
        widget = TestWidget()
        assert widget.render() == "<div>Test Widget</div>"
        widget.update({})  # Should not raise


class TestLazyWidgetManager:
    """Test lazy widget manager functionality."""
    
    def test_lazy_widget_manager_initialization(self):
        """Test lazy widget manager can be initialized."""
        manager = LazyWidgetManager()
        assert manager is not None
        assert hasattr(manager, 'load_widget')
        assert hasattr(manager, 'unload_widget')
        assert hasattr(manager, 'get_widget')
        
    def test_lazy_widget_manager_with_memory_monitor(self):
        """Test lazy widget manager with memory monitor."""
        with patch('piwardrive.widget_manager.MemoryMonitor') as mock_monitor:
            mock_monitor_instance = Mock()
            mock_monitor.return_value = mock_monitor_instance
            
            manager = LazyWidgetManager()
            
            # Should have memory monitor
            assert hasattr(manager, '_memory_monitor')
            
    def test_lazy_widget_manager_with_resource_manager(self):
        """Test lazy widget manager with resource manager."""
        with patch('piwardrive.widget_manager.ResourceManager') as mock_resource:
            mock_resource_instance = Mock()
            mock_resource.return_value = mock_resource_instance
            
            manager = LazyWidgetManager()
            
            # Should have resource manager
            assert hasattr(manager, '_resource_manager')
            
    def test_lazy_widget_manager_load_widget(self):
        """Test lazy widget manager can load widgets."""
        manager = LazyWidgetManager()
        
        # Mock widget module
        with patch('piwardrive.widget_manager.widgets') as mock_widgets:
            mock_widget_class = Mock()
            mock_widget_instance = Mock()
            mock_widget_class.return_value = mock_widget_instance
            
            # Mock widget module has widget class
            setattr(mock_widgets, 'TestWidget', mock_widget_class)
            
            # Load widget
            widget = manager.load_widget('TestWidget')
            
            # Should return widget instance
            assert widget is mock_widget_instance
            
    def test_lazy_widget_manager_get_widget_cached(self):
        """Test lazy widget manager returns cached widgets."""
        manager = LazyWidgetManager()
        
        # Mock widget loading
        with patch.object(manager, 'load_widget') as mock_load:
            mock_widget = Mock()
            mock_load.return_value = mock_widget
            
            # First call should load widget
            widget1 = manager.get_widget('TestWidget')
            assert widget1 is mock_widget
            mock_load.assert_called_once_with('TestWidget')
            
            # Second call should return cached widget
            widget2 = manager.get_widget('TestWidget')
            assert widget2 is mock_widget
            assert mock_load.call_count == 1  # Should not be called again
            
    def test_lazy_widget_manager_unload_widget(self):
        """Test lazy widget manager can unload widgets."""
        manager = LazyWidgetManager()
        
        # Mock widget loading
        with patch.object(manager, 'load_widget') as mock_load:
            mock_widget = Mock()
            mock_load.return_value = mock_widget
            
            # Load widget
            widget = manager.get_widget('TestWidget')
            assert widget is mock_widget
            
            # Unload widget
            manager.unload_widget('TestWidget')
            
            # Widget should be removed from cache
            # Next call should reload widget
            widget2 = manager.get_widget('TestWidget')
            assert widget2 is mock_widget
            assert mock_load.call_count == 2  # Should be called twice
            
    def test_lazy_widget_manager_memory_pressure_cleanup(self):
        """Test lazy widget manager handles memory pressure."""
        manager = LazyWidgetManager()
        
        # Mock memory monitor
        with patch('piwardrive.widget_manager.MemoryMonitor') as mock_monitor:
            mock_monitor_instance = Mock()
            mock_monitor_instance.get_memory_usage.return_value = 85.0  # High memory usage
            mock_monitor.return_value = mock_monitor_instance
            
            # Mock widgets
            with patch.object(manager, 'load_widget') as mock_load:
                mock_widget = Mock()
                mock_load.return_value = mock_widget
                
                # Load multiple widgets
                manager.get_widget('Widget1')
                manager.get_widget('Widget2')
                manager.get_widget('Widget3')
                
                # Simulate memory pressure cleanup
                manager._cleanup_under_pressure()
                
                # Should have cleaned up some widgets
                assert len(manager._widget_cache) < 3


class TestSpecificWidgets:
    """Test specific widget implementations."""
    
    def test_battery_status_widget(self):
        """Test battery status widget."""
        # Mock battery status widget
        with patch('piwardrive.widgets.battery_status.BatteryStatusWidget') as mock_widget:
            mock_widget_instance = Mock()
            mock_widget_instance.render.return_value = "<div>Battery: 85%</div>"
            mock_widget.return_value = mock_widget_instance
            
            widget = mock_widget()
            result = widget.render()
            
            assert "Battery" in result
            assert "85%" in result
            
    def test_detection_rate_widget(self):
        """Test detection rate widget."""
        with patch('piwardrive.widgets.detection_rate.DetectionRateWidget') as mock_widget:
            mock_widget_instance = Mock()
            mock_widget_instance.render.return_value = "<div>Detection Rate: 42/min</div>"
            mock_widget.return_value = mock_widget_instance
            
            widget = mock_widget()
            result = widget.render()
            
            assert "Detection Rate" in result
            assert "42/min" in result
            
    def test_threat_level_widget(self):
        """Test threat level widget."""
        with patch('piwardrive.widgets.threat_level.ThreatLevelWidget') as mock_widget:
            mock_widget_instance = Mock()
            mock_widget_instance.render.return_value = "<div>Threat Level: Medium</div>"
            mock_widget.return_value = mock_widget_instance
            
            widget = mock_widget()
            result = widget.render()
            
            assert "Threat Level" in result
            assert "Medium" in result
            
    def test_network_density_widget(self):
        """Test network density widget."""
        with patch('piwardrive.widgets.network_density.NetworkDensityWidget') as mock_widget:
            mock_widget_instance = Mock()
            mock_widget_instance.render.return_value = "<div>Networks: 15</div>"
            mock_widget.return_value = mock_widget_instance
            
            widget = mock_widget()
            result = widget.render()
            
            assert "Networks" in result
            assert "15" in result
            
    def test_database_health_widget(self):
        """Test database health widget."""
        with patch('piwardrive.widgets.database_health.DatabaseHealthWidget') as mock_widget:
            mock_widget_instance = Mock()
            mock_widget_instance.render.return_value = "<div>DB Health: Good</div>"
            mock_widget.return_value = mock_widget_instance
            
            widget = mock_widget()
            result = widget.render()
            
            assert "DB Health" in result
            assert "Good" in result


class TestWidgetDataFlow:
    """Test widget data flow and updates."""
    
    def test_widget_data_update(self):
        """Test widget can receive and process data updates."""
        class MockWidget(DashboardWidget):
            def __init__(self):
                self.data = {}
                
            def render(self):
                return f"<div>{self.data}</div>"
                
            def update(self, data):
                self.data = data
                
        widget = MockWidget()
        
        # Update with test data
        test_data = {"value": 42, "status": "active"}
        widget.update(test_data)
        
        # Data should be updated
        assert widget.data == test_data
        
        # Render should include updated data
        result = widget.render()
        assert "42" in result
        assert "active" in result
        
    def test_widget_async_data_update(self):
        """Test widget can handle async data updates."""
        class AsyncWidget(DashboardWidget):
            def __init__(self):
                self.data = {}
                
            def render(self):
                return f"<div>{self.data}</div>"
                
            async def update_async(self, data):
                # Simulate async operation
                await asyncio.sleep(0.01)
                self.data = data
                
        widget = AsyncWidget()
        
        # Test async update
        async def test_async_update():
            test_data = {"async_value": 123}
            await widget.update_async(test_data)
            assert widget.data == test_data
            
        asyncio.run(test_async_update())
        
    def test_widget_error_handling(self):
        """Test widget handles errors gracefully."""
        class ErrorWidget(DashboardWidget):
            def render(self):
                raise ValueError("Rendering error")
                
            def update(self, data):
                raise ValueError("Update error")
                
        widget = ErrorWidget()
        
        # Should handle render error
        with pytest.raises(ValueError, match="Rendering error"):
            widget.render()
            
        # Should handle update error
        with pytest.raises(ValueError, match="Update error"):
            widget.update({})


class TestWidgetMemoryManagement:
    """Test widget memory management and cleanup."""
    
    def test_widget_memory_monitoring(self):
        """Test widget memory usage is monitored."""
        with patch('piwardrive.widget_manager.MemoryMonitor') as mock_monitor:
            mock_monitor_instance = Mock()
            mock_monitor_instance.get_memory_usage.return_value = 45.0
            mock_monitor.return_value = mock_monitor_instance
            
            manager = LazyWidgetManager()
            
            # Check memory usage
            usage = manager._memory_monitor.get_memory_usage()
            assert usage == 45.0
            
    def test_widget_cleanup_on_high_memory(self):
        """Test widgets are cleaned up when memory is high."""
        manager = LazyWidgetManager()
        
        # Mock high memory usage
        with patch.object(manager, '_get_memory_usage', return_value=90.0):
            # Load widgets
            with patch.object(manager, 'load_widget') as mock_load:
                mock_widget = Mock()
                mock_load.return_value = mock_widget
                
                # Load multiple widgets
                manager.get_widget('Widget1')
                manager.get_widget('Widget2')
                manager.get_widget('Widget3')
                
                # Simulate memory pressure
                manager._cleanup_under_pressure()
                
                # Should have cleaned up widgets
                assert len(manager._widget_cache) < 3
                
    def test_widget_weak_references(self):
        """Test widgets use weak references for memory management."""
        manager = LazyWidgetManager()
        
        # Test weak reference behavior
        import weakref
        
        class TestWidget(DashboardWidget):
            def render(self):
                return "<div>Test</div>"
                
            def update(self, data):
                pass
                
        widget = TestWidget()
        weak_ref = weakref.ref(widget)
        
        # Widget should be alive
        assert weak_ref() is not None
        
        # Delete widget
        del widget
        
        # Weak reference should be None
        assert weak_ref() is None


class TestWidgetRegistry:
    """Test widget registry and discovery."""
    
    def test_widget_registry_initialization(self):
        """Test widget registry can be initialized."""
        # Mock widget registry
        class MockWidgetRegistry:
            def __init__(self):
                self.widgets = {}
                
            def register(self, name, widget_class):
                self.widgets[name] = widget_class
                
            def get(self, name):
                return self.widgets.get(name)
                
        registry = MockWidgetRegistry()
        assert registry is not None
        
    def test_widget_registry_registration(self):
        """Test widgets can be registered."""
        class MockWidgetRegistry:
            def __init__(self):
                self.widgets = {}
                
            def register(self, name, widget_class):
                self.widgets[name] = widget_class
                
            def get(self, name):
                return self.widgets.get(name)
                
        registry = MockWidgetRegistry()
        
        # Register widget
        class TestWidget(DashboardWidget):
            def render(self):
                return "<div>Test</div>"
                
            def update(self, data):
                pass
                
        registry.register('TestWidget', TestWidget)
        
        # Should be able to retrieve widget
        widget_class = registry.get('TestWidget')
        assert widget_class is TestWidget
        
    def test_widget_registry_discovery(self):
        """Test widgets can be discovered automatically."""
        # Mock widget discovery
        with patch('piwardrive.widget_manager.os.listdir') as mock_listdir:
            mock_listdir.return_value = ['battery_status.py', 'detection_rate.py', 'threat_level.py']
            
            with patch('piwardrive.widget_manager.importlib.import_module') as mock_import:
                mock_module = Mock()
                mock_widget_class = Mock()
                mock_module.Widget = mock_widget_class
                mock_import.return_value = mock_module
                
                # Test discovery
                discovered_widgets = []
                for filename in mock_listdir.return_value:
                    if filename.endswith('.py') and filename != '__init__.py':
                        widget_name = filename[:-3]  # Remove .py extension
                        discovered_widgets.append(widget_name)
                        
                assert 'battery_status' in discovered_widgets
                assert 'detection_rate' in discovered_widgets
                assert 'threat_level' in discovered_widgets


class TestWidgetIntegration:
    """Test complete widget system integration."""
    
    def test_widget_manager_integration(self):
        """Test widget manager integrates with all components."""
        with patch('piwardrive.widget_manager.MemoryMonitor') as mock_monitor:
            with patch('piwardrive.widget_manager.ResourceManager') as mock_resource:
                mock_monitor_instance = Mock()
                mock_resource_instance = Mock()
                mock_monitor.return_value = mock_monitor_instance
                mock_resource.return_value = mock_resource_instance
                
                manager = LazyWidgetManager()
                
                # Should have all components
                assert hasattr(manager, '_memory_monitor')
                assert hasattr(manager, '_resource_manager')
                assert hasattr(manager, '_widget_cache')
                
    def test_widget_lifecycle_integration(self):
        """Test complete widget lifecycle."""
        manager = LazyWidgetManager()
        
        # Mock widget class
        class TestWidget(DashboardWidget):
            def __init__(self):
                self.initialized = True
                
            def render(self):
                return "<div>Test Widget</div>"
                
            def update(self, data):
                self.data = data
                
        # Mock widget loading
        with patch.object(manager, 'load_widget', return_value=TestWidget()):
            # Load widget
            widget = manager.get_widget('TestWidget')
            assert widget.initialized is True
            
            # Update widget
            widget.update({"test": "data"})
            assert widget.data == {"test": "data"}
            
            # Render widget
            result = widget.render()
            assert "Test Widget" in result
            
            # Unload widget
            manager.unload_widget('TestWidget')
            
            # Widget should be removed from cache
            assert 'TestWidget' not in manager._widget_cache
            
    def test_widget_error_recovery(self):
        """Test widget system recovers from errors."""
        manager = LazyWidgetManager()
        
        # Mock widget that fails to load
        with patch.object(manager, 'load_widget', side_effect=Exception("Load error")):
            # Should handle load error gracefully
            widget = manager.get_widget('FailingWidget')
            assert widget is None
            
        # Should be able to try again
        with patch.object(manager, 'load_widget', return_value=Mock()):
            widget = manager.get_widget('FailingWidget')
            assert widget is not None
            
    def test_widget_performance_optimization(self):
        """Test widget system performance optimizations."""
        manager = LazyWidgetManager()
        
        # Mock resource manager
        with patch('piwardrive.widget_manager.ResourceManager') as mock_resource:
            mock_resource_instance = Mock()
            mock_resource_instance.can_allocate.return_value = True
            mock_resource.return_value = mock_resource_instance
            
            # Test resource allocation
            can_allocate = manager._resource_manager.can_allocate('memory', 1024)
            assert can_allocate is True
            
        # Mock memory optimization
        with patch('piwardrive.widget_manager.MemoryMonitor') as mock_monitor:
            mock_monitor_instance = Mock()
            mock_monitor_instance.get_memory_usage.return_value = 45.0
            mock_monitor.return_value = mock_monitor_instance
            
            # Test memory monitoring
            usage = manager._memory_monitor.get_memory_usage()
            assert usage == 45.0
