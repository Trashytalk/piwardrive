"""Simple screen hosting a console log view."""

from kivy.uix.screenmanager import Screen

from widgets import LogViewer


class ConsoleScreen(Screen):
    """Display real-time logs from Kismet or other services."""

    def __init__(self, **kwargs) -> None:
        """Create the screen and a fallback log viewer."""
        super().__init__(**kwargs)
        # ``kv`` defines the layout when available. Tests may instantiate this
        # class directly, so create a log widget if ``ids`` is empty.
        if not getattr(self, "ids", {}):
            self.log_widget = LogViewer()
            self.add_widget(self.log_widget)

    def on_kv_post(self, _base_widget) -> None:  # pragma: no cover - GUI hook
        """Store the ``LogViewer`` created via ``kv`` rules."""
        if "console_log" in self.ids:
            self.log_widget = self.ids.console_log
