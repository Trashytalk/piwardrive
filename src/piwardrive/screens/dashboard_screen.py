"""Drag-and-drop dashboard screen with metrics widgets."""

import logging
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
import asyncio
from piwardrive.core.persistence import (
    save_dashboard_settings,
    load_dashboard_settings,
    DashboardSettings,
)


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
    HealthAnalysisWidget,
)


class DashboardScreen(Screen):
    """Drag-and-drop dashboard for custom widgets."""

    def on_enter(self):
        """Instantiate widgets on first entry and register them."""
        if not getattr(self, "_init", False):
            self._init = True
            self.layout = FloatLayout()
            self.add_widget(self.layout)
            self.load_widgets()
        self._register_widgets()

    def _register_widgets(self):
        """Register each dashboard widget with the scheduler."""
        app = App.get_running_app()
        for child in self.layout.children:
            try:
                app.scheduler.register_widget(child)
            except Exception as exc:  # pragma: no cover - registration failure
                logging.exception("Failed to register widget %s: %s", child, exc)

    def on_leave(self):
        """Save layout and cancel scheduled widget updates."""
        App.get_running_app().scheduler.cancel_all()
        self.save_layout()

    def save_layout(self):
        """Persist current widget positions to the application object."""
        app = App.get_running_app()
        layout = []
        for child in self.layout.children:
            layout.append({"cls": child.__class__.__name__, "pos": child.pos})
        app.dashboard_layout = layout
        try:
            asyncio.run(
                save_dashboard_settings(DashboardSettings(layout=layout, widgets=[]))
            )
        except Exception as exc:  # pragma: no cover - persistence failures
            logging.exception("Failed to save dashboard settings: %s", exc)

    def load_widgets(self):
        """Instantiate dashboard widgets from config or defaults."""
        app = App.get_running_app()
        cls_map = {
            "SignalStrengthWidget": SignalStrengthWidget,
            "GPSStatusWidget": GPSStatusWidget,
            "HandshakeCounterWidget": HandshakeCounterWidget,
            "ServiceStatusWidget": ServiceStatusWidget,
            "StorageUsageWidget": StorageUsageWidget,
            "HealthStatusWidget": HealthStatusWidget,
            "DiskUsageTrendWidget": DiskUsageTrendWidget,
            "CPUTempGraphWidget": CPUTempGraphWidget,
            "NetworkThroughputWidget": NetworkThroughputWidget,
            "BatteryStatusWidget": BatteryStatusWidget,
        }

        widgets: list[object] = []
        settings = None
        try:
            settings = asyncio.run(load_dashboard_settings())
        except Exception as exc:  # pragma: no cover - load failure
            logging.exception("Failed to load dashboard settings: %s", exc)

        layout_data = (
            settings.layout if settings and settings.layout else app.dashboard_layout
        )
        if layout_data:

            cls_map = {
                "SignalStrengthWidget": SignalStrengthWidget,
                "GPSStatusWidget": GPSStatusWidget,
                "HandshakeCounterWidget": HandshakeCounterWidget,
                "ServiceStatusWidget": ServiceStatusWidget,
                "StorageUsageWidget": StorageUsageWidget,
                "HealthStatusWidget": HealthStatusWidget,
                "DiskUsageTrendWidget": DiskUsageTrendWidget,
                "CPUTempGraphWidget": CPUTempGraphWidget,
                "NetworkThroughputWidget": NetworkThroughputWidget,
                "BatteryStatusWidget": BatteryStatusWidget,
                "HealthAnalysisWidget": HealthAnalysisWidget,
            }

            for info in layout_data:
                cls = cls_map.get(info.get("cls"))
                if not cls:
                    continue
                widget = cls()
                if pos := info.get("pos"):
                    widget.pos = pos
                widgets.append(widget)
            app.dashboard_layout = layout_data
        else:
            widgets = [
                SignalStrengthWidget(),
                GPSStatusWidget(),
                HandshakeCounterWidget(),
                ServiceStatusWidget(),
                StorageUsageWidget(),
                HealthStatusWidget(),
            ]
            if getattr(app, "widget_disk_trend", False):
                widgets.append(DiskUsageTrendWidget())
            if getattr(app, "widget_cpu_temp", False):
                widgets.append(CPUTempGraphWidget())
            if getattr(app, "widget_net_throughput", False):
                widgets.append(NetworkThroughputWidget())
            if getattr(app, "widget_battery_status", False):
                widgets.append(BatteryStatusWidget())
            if getattr(app, "widget_health_analysis", False):
                widgets.append(HealthAnalysisWidget())

        for widget in widgets:
            self.layout.add_widget(widget)
            try:
                app.scheduler.register_widget(widget)
            except Exception as exc:  # pragma: no cover - registration failure
                logging.exception("Failed to register widget %s: %s", widget, exc)

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
        if getattr(app, "widget_disk_trend", False):
            classes.append(DiskUsageTrendWidget)
        if getattr(app, "widget_cpu_temp", False):
            classes.append(CPUTempGraphWidget)
        if getattr(app, "widget_net_throughput", False):
            classes.append(NetworkThroughputWidget)
        if getattr(app, "widget_battery_status", False):
            classes.append(BatteryStatusWidget)
        return [cls() for cls in classes]
