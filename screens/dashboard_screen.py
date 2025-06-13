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
    DiskUsageTrendWidget,
    CPUTempGraphWidget,
    NetworkThroughputWidget,
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
