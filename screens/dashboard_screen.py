from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen

from widgets import (
    SignalStrengthWidget,
    GPSStatusWidget,
    HandshakeCounterWidget,
    ServiceStatusWidget,
    StorageUsageWidget,
)


class DashboardScreen(Screen):
    """Drag-and-drop dashboard for custom widgets."""

    def on_enter(self):
        if getattr(self, '_init', False):
            return
        self._init = True
        self.layout = FloatLayout()
        self.add_widget(self.layout)
        self.load_widgets()

    def load_widgets(self):
        app = App.get_running_app()
        for info in app.dashboard_layout:
            cls_name = info.get('cls')
            pos = info.get('pos', (0, 0))
            try:
                cls = globals()[cls_name]
            except KeyError:
                continue
            widget = cls(size_hint=(None, None), size=(120, 60), pos=pos)
            self.layout.add_widget(widget)

    def on_leave(self):
        self.save_layout()

    def save_layout(self):
        app = App.get_running_app()
        layout = []
        for child in self.layout.children:
            layout.append({'cls': child.__class__.__name__, 'pos': child.pos})
        app.dashboard_layout = layout
