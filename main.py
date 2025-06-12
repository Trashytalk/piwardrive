"""Main application entry point for the PiWardrive GUI."""

import logging
import subprocess

from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import (  # pylint: disable=no-name-in-module
    BooleanProperty, NumericProperty)
from kivymd.app import MDApp

# Trim down HTTP debug logging
logging.getLogger('urllib3').setLevel(logging.WARNING)

from screens.console_screen import ConsoleScreen
from screens.dashboard_screen import DashboardScreen
from screens.map_screen import MapScreen
from screens.settings_screen import SettingsScreen
from screens.split_screen import SplitScreen
from screens.stats_screen import StatsScreen


class PiWardriveApp(MDApp):
    """Main application class handling screen setup and helpers."""
    map_poll_gps     = NumericProperty(10)
    map_poll_aps     = NumericProperty(60)
    map_show_gps     = BooleanProperty(True)
    map_show_aps     = BooleanProperty(True)
    map_show_bt      = BooleanProperty(False)
    map_cluster_aps  = BooleanProperty(False)
    map_fullscreen   = BooleanProperty(False)
    map_use_offline  = BooleanProperty(False)

    def build(self):
        """Load and return the root widget tree from KV."""
        root = Builder.load_file('kv/main.kv')
        self.root = root
        return root

    def on_start(self):
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
        sm.add_widget(MapScreen(name='Map'))
        sm.add_widget(StatsScreen(name='Stats'))
        sm.add_widget(SplitScreen(name='Split'))
        sm.add_widget(ConsoleScreen(name='Console'))
        sm.add_widget(SettingsScreen(name='Settings'))
        sm.add_widget(DashboardScreen(name='Dashboard'))

        # 2) Now set the initial screen explicitly
        sm.current = 'Map'

        # 3) Build your responsive nav buttons
        for name in ['Map','Stats','Split','Console','Settings','Dashboard']:
            btn = Factory.NavigationButton(
                text=name,
                on_release=lambda btn, s=name: self.switch_screen(s)
            )
            nav_bar.add_widget(btn)

    def switch_screen(self, name):
        """Change the active screen."""
        self.root.ids.sm.current = name


    # 1) Service control with feedback
    def control_service(self, svc, action):
        """Run a systemctl command for a given service."""
        cmd = ['sudo', 'systemctl', action, svc]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            self.show_alert(
                f"Failed to {action} {svc}", res.stderr or "Unknown error"
            )

    def show_alert(self, title, text):
        """Display a simple alert dialog with the given title and text."""
        from kivymd.uix.dialog import MDDialog

        dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(0.8, None),
            buttons=[],
        )
        dialog.open()

    def toggle_theme(self):
        """Toggle between the light and dark theme."""
        self.theme_cls.theme_style = (
            'Light' if self.theme_cls.theme_style == 'Dark' else 'Dark'
        )


if __name__ == '__main__':
    PiWardriveApp().run()
