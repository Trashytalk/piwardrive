"""Main application entry point for the PiWardrive GUI."""

import logging
import os
import subprocess
from dataclasses import asdict, fields
from typing import Any

from scheduler import PollScheduler
from config import load_config, save_config, Config
import diagnostics
import utils
from logconfig import setup_logging

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import (  # pylint: disable=no-name-in-module
    BooleanProperty,
    NumericProperty,
    StringProperty,
    ListProperty
)
from kivymd.app import MDApp

# Trim down HTTP debug logging

from screens.console_screen import ConsoleScreen  # type: ignore[import]
from screens.dashboard_screen import DashboardScreen  # type: ignore[import]
from screens.map_screen import MapScreen  # type: ignore[import]
from screens.settings_screen import SettingsScreen  # type: ignore[import]
from screens.split_screen import SplitScreen  # type: ignore[import]
from screens.stats_screen import StatsScreen  # type: ignore[import]

logging.getLogger("urllib3").setLevel(logging.WARNING)


class PiWardriveApp(MDApp):
    """Main application class handling screen setup and helpers."""

    map_poll_gps = NumericProperty(10)
    map_poll_aps = NumericProperty(60)
    map_show_gps = BooleanProperty(True)
    map_show_aps = BooleanProperty(True)
    map_show_bt = BooleanProperty(False)
    map_cluster_aps = BooleanProperty(False)
    map_fullscreen = BooleanProperty(False)
    map_use_offline = BooleanProperty(False)
    theme = StringProperty("Dark")
    kismet_logdir = StringProperty("/mnt/ssd/kismet_logs")
    bettercap_caplet = StringProperty("/usr/local/etc/bettercap/alfa.cap")
    dashboard_layout = ListProperty([])
    debug_mode = BooleanProperty(False)
    widget_disk_trend = BooleanProperty(True)
    widget_cpu_temp = BooleanProperty(True)
    widget_net_throughput = BooleanProperty(True)
    health_poll_interval = NumericProperty(10)
    log_rotate_interval = NumericProperty(3600)
    log_rotate_archives = NumericProperty(3)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        # load persisted configuration
        self.config_data: Config = load_config()
        for key, val in asdict(self.config_data).items():
            if hasattr(self, key):
                setattr(self, key, val)
        setup_logging(level=logging.DEBUG if self.debug_mode else logging.INFO)
        self.scheduler: PollScheduler = PollScheduler()
        self.health_monitor = diagnostics.HealthMonitor(
            self.scheduler, self.health_poll_interval
        )
        if os.getenv("PW_PROFILE"):
            diagnostics.start_profiling()
        self.theme_cls.theme_style = self.theme

    def build(self) -> Any:
        """Load and return the root widget tree from KV."""
        root = Builder.load_file("kv/main.kv")
        self.root = root
        return root

    def on_start(self) -> None:
        """Initialize screens and navigation on start."""
        # DEBUG: show which IDs were parsed from KV
        print("Root IDs:", self.root.ids.keys())
        try:
            sm = self.root.ids.sm
        except KeyError:
            raise RuntimeError(
                f"ID 'sm' not found; available IDs: {list(self.root.ids.keys())}"
            )

        nav_bar = self.root.ids.nav_bar

        # 1) Add all six screens first
        sm.add_widget(MapScreen(name="Map"))
        sm.add_widget(StatsScreen(name="Stats"))
        sm.add_widget(SplitScreen(name="Split"))
        sm.add_widget(ConsoleScreen(name="Console"))
        sm.add_widget(SettingsScreen(name="Settings"))
        sm.add_widget(DashboardScreen(name="Dashboard"))

        # 2) Now set the initial screen explicitly
        sm.current = "Map"

        # 3) Build your responsive nav buttons
        for name in ["Map", "Stats", "Split", "Console", "Settings", "Dashboard"]:
            btn = Factory.NavigationButton(
                text=name, on_release=lambda btn, s=name: self.switch_screen(s)
            )
            nav_bar.add_widget(btn)
        for path in ["/var/log/syslog"]:
            ev = f"rotate_{os.path.basename(path)}"
            self.scheduler.schedule(
                ev,
                lambda _dt, p=path: diagnostics.rotate_log(p, self.log_rotate_archives),
                self.log_rotate_interval,
            )

    def switch_screen(self, name: str) -> None:
        """Change the active screen."""
        self.root.ids.sm.current = name

    # 1) Service control with feedback
    def control_service(self, svc: str, action: str) -> None:
        """Run a systemctl command for a given service with retries."""
        try:
            success, _out, err = utils.run_service_cmd(
                svc, action, attempts=3, delay=1
            )
        except Exception as exc:  # pragma: no cover - subprocess failures
            utils.report_error(f"Failed to {action} {svc}: {exc}")
            return
        if not success:
            utils.report_error(
                f"Failed to {action} {svc}: {err or 'Unknown error'}"
            )

    def show_alert(self, title: str, text: str) -> None:
        """Display a simple alert dialog with the given title and text."""
        from kivymd.uix.dialog import MDDialog

        dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(0.8, None),
            buttons=[],
        )
        dialog.open()

    def on_stop(self) -> None:
        """Persist configuration values on application exit."""
        prof = diagnostics.stop_profiling()
        if prof:
            logging.info("Profiling summary:\n%s", prof)
        for f in fields(Config):
            key = f.name
            if hasattr(self, key):
                setattr(self.config_data, key, getattr(self, key))
        try:
            save_config(self.config_data)
        except OSError as exc:  # pragma: no cover - save failure is non-critical
            logging.exception("Failed to save config: %s", exc)


if __name__ == "__main__":
    PiWardriveApp().run()
