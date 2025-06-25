"""Simple screen hosting a console log view."""

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.app import App
import requests

from widgets import LogViewer


class ConsoleScreen(Screen):
    """Display real-time logs from Kismet or other services."""

    command_output = StringProperty("")

    def __init__(self, **kwargs):
        """Instantiate the log viewer widget."""
        super().__init__(**kwargs)
        self.log_widget = LogViewer()
        self.add_widget(self.log_widget)
        self._http = requests.Session()

    def run_command(self, cmd: str) -> None:
        """Execute ``cmd`` via the backend ``/command`` endpoint."""
        cmd = cmd.strip()
        if not cmd:
            return
        app = App.get_running_app()
        url = getattr(app, "service_url", "http://localhost:8000")
        try:
            resp = self._http.post(f"{url}/command", json={"cmd": cmd}, timeout=5)
            if resp.ok:
                self.command_output = resp.json().get("output", "")
            else:
                self.command_output = resp.text
        except Exception as exc:  # pragma: no cover - network errors
            self.command_output = str(exc)
