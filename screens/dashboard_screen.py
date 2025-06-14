"""Drag-and-drop dashboard screen with metrics widgets."""
import logging
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen


from widgets import (
    SignalStrengthWidget,
    GPSStatusWidget,
    HandshakeCounterWidget,
    ServiceStatusWidget,
    StorageUsageWidget,
    HealthStatusWidget,
    DiskUsageTrendWidget,
    CPUTempGraphWidget,
    NetworkThroughputWidget,
    BatteryStatusWidget,
)


class DashboardScreen(Screen):
    """Drag-and-drop dashboard for custom widgets."""

    def on_enter(self):
        if not getattr(self, '_init', False):
            self._init = True
            self.layout = FloatLayout()
            self.add_widget(self.layout)
            self.load_widgets()
        self._register_widgets()

    def _register_widgets(self):
        app = App.get_running_app()
        for child in self.layout.children:
            try:
                app.scheduler.register_widget(child)
            except Exception as exc:  # pragma: no cover - registration failure
                logging.exception("Failed to register widget %s: %s", child, exc)

    def on_leave(self):
        App.get_running_app().scheduler.cancel_all()
        self.save_layout()


    def save_layout(self):
        app = App.get_running_app()
        layout = []
        for child in self.layout.children:
            layout.append({'cls': child.__class__.__name__, 'pos': child.pos})
        app.dashboard_layout = layout

    def load_widgets(self):
        """Instantiate dashboard widgets from config or defaults."""
        app = App.get_running_app()
        cls_map = {
            'SignalStrengthWidget': SignalStrengthWidget,
            'GPSStatusWidget': GPSStatusWidget,
            'HandshakeCounterWidget': HandshakeCounterWidget,
            'ServiceStatusWidget': ServiceStatusWidget,
            'StorageUsageWidget': StorageUsageWidget,
            'HealthStatusWidget': HealthStatusWidget,
            'DiskUsageTrendWidget': DiskUsageTrendWidget,
            'CPUTempGraphWidget': CPUTempGraphWidget,
            'NetworkThroughputWidget': NetworkThroughputWidget,
            'BatteryStatusWidget': BatteryStatusWidget,
        }

        widgets: list[object] = []
        if app.dashboard_layout:
            for info in app.dashboard_layout:
                cls = cls_map.get(info.get('cls'))
                if not cls:
                    continue
                widget = cls()
                if pos := info.get('pos'):
                    widget.pos = pos
                widgets.append(widget)
        else:
            widgets = self._create_default_widgets(app)

        for widget in widgets:
            self.layout.add_widget(widget)
            try:
                app.scheduler.register_widget(widget)
            except Exception as exc:  # pragma: no cover - registration failure
                logging.exception('Failed to register widget %s: %s', widget, exc)

    def _create_default_widgets(self, app) -> list:
        """Return default widgets based on ``app`` settings."""
        classes = [
            SignalStrengthWidget,
            GPSStatusWidget,
            HandshakeCounterWidget,
            ServiceStatusWidget,
            StorageUsageWidget,
            HealthStatusWidget,
        ]
        if getattr(app, 'widget_disk_trend', False):
            classes.append(DiskUsageTrendWidget)
        if getattr(app, 'widget_cpu_temp', False):
            classes.append(CPUTempGraphWidget)
        if getattr(app, 'widget_net_throughput', False):
            classes.append(NetworkThroughputWidget)
        if getattr(app, 'widget_battery_status', False):
            classes.append(BatteryStatusWidget)
        return [cls() for cls in classes]
