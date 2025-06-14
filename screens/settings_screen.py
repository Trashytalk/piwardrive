## settings_screen.py


"""Settings screen for starting and stopping background services."""

import os
from dataclasses import fields

from kivy.app import App

from kivy.metrics import dp

from kivy.uix.screenmanager import Screen

from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.uix.button import MDRaisedButton

from kivymd.uix.label import MDLabel

from kivymd.uix.textfield import MDTextField

from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.snackbar import Snackbar
from utils import report_error, format_error
from config import Config, save_config


class SettingsScreen(Screen):
    """Placeholder for various application settings."""

    def on_enter(self):
        """Create service control buttons on first entry."""

        if getattr(self, "_initialized", False):

            return

        self._initialized = True

        layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10),
            size_hint=(1, 1),
        )

        for svc, label in [
            ("kismet.service", "Kismet"),
            ("bettercap.service", "BetterCAP"),
        ]:

            row = MDBoxLayout(spacing=dp(8), size_hint_y=None, height=dp(48))

            row.add_widget(MDLabel(text=label, size_hint_x=None, width=dp(80)))

            for action in ("start", "stop", "restart"):

                row.add_widget(
                    MDRaisedButton(
                        text=action.capitalize(),
                        on_release=lambda _btn, s=svc, a=action: App.get_running_app().control_service(
                            s, a
                        ),
                    )
                )

            layout.add_widget(row)

        app = App.get_running_app()

        # Config fields

        self.kismet_field = MDTextField(
            text=app.kismet_logdir, hint_text="Kismet log dir"
        )

        self.bcap_field = MDTextField(
            text=app.bettercap_caplet, hint_text="BetterCAP caplet"
        )

        self.gps_poll_field = MDTextField(
            text=str(app.map_poll_gps), hint_text="GPS poll rate (s)"
        )

        self.ap_poll_field = MDTextField(
            text=str(app.map_poll_aps), hint_text="AP poll rate (s)"
        )

        self.health_poll_field = MDTextField(
            text=str(app.health_poll_interval), hint_text="Health poll (s)"
        )

        self.log_rotate_field = MDTextField(
            text=str(app.log_rotate_interval), hint_text="Log rotate (s)"
        )

        self.log_archives_field = MDTextField(
            text=str(app.log_rotate_archives), hint_text="Log archives"
        )

        self.offline_path_field = MDTextField(
            text=app.offline_tile_path, hint_text="Offline tiles path"
        )

        layout.add_widget(self.kismet_field)

        layout.add_widget(self.bcap_field)

        layout.add_widget(self.gps_poll_field)
        layout.add_widget(self.ap_poll_field)
        layout.add_widget(self.health_poll_field)
        layout.add_widget(self.log_rotate_field)
        layout.add_widget(self.log_archives_field)
        layout.add_widget(self.offline_path_field)

        # Toggles

        theme_row = MDBoxLayout(spacing=dp(8), size_hint_y=None, height=dp(48))

        theme_row.add_widget(MDLabel(text="Dark Theme", size_hint_x=0.7))

        self.theme_switch = MDSwitch(active=app.theme == "Dark")

        theme_row.add_widget(self.theme_switch)

        layout.add_widget(theme_row)

        offline_row = MDBoxLayout(spacing=dp(8), size_hint_y=None, height=dp(48))

        offline_row.add_widget(MDLabel(text="Offline Tiles", size_hint_x=0.7))

        self.offline_switch = MDSwitch(active=app.map_use_offline)

        offline_row.add_widget(self.offline_switch)

        layout.add_widget(offline_row)

        show_gps_row = MDBoxLayout(spacing=dp(8), size_hint_y=None, height=dp(48))
        show_gps_row.add_widget(MDLabel(text="Show GPS", size_hint_x=0.7))
        self.show_gps_switch = MDSwitch(active=app.map_show_gps)
        show_gps_row.add_widget(self.show_gps_switch)
        layout.add_widget(show_gps_row)

        show_aps_row = MDBoxLayout(spacing=dp(8), size_hint_y=None, height=dp(48))
        show_aps_row.add_widget(MDLabel(text="Show APs", size_hint_x=0.7))
        self.show_aps_switch = MDSwitch(active=app.map_show_aps)
        show_aps_row.add_widget(self.show_aps_switch)
        layout.add_widget(show_aps_row)

        cluster_row = MDBoxLayout(spacing=dp(8), size_hint_y=None, height=dp(48))
        cluster_row.add_widget(MDLabel(text="Cluster APs", size_hint_x=0.7))
        self.cluster_switch = MDSwitch(active=app.map_cluster_aps)
        cluster_row.add_widget(self.cluster_switch)
        layout.add_widget(cluster_row)

        debug_row = MDBoxLayout(spacing=dp(8), size_hint_y=None, height=dp(48))
        debug_row.add_widget(MDLabel(text="Debug Mode", size_hint_x=0.7))
        self.debug_switch = MDSwitch(active=app.debug_mode)
        debug_row.add_widget(self.debug_switch)
        layout.add_widget(debug_row)

        battery_row = MDBoxLayout(spacing=dp(8), size_hint_y=None, height=dp(48))
        battery_row.add_widget(MDLabel(text="Battery Widget", size_hint_x=0.7))
        self.battery_switch = MDSwitch(active=app.widget_battery_status)
        battery_row.add_widget(self.battery_switch)
        layout.add_widget(battery_row)

        save_btn = MDRaisedButton(
            text="Save", on_release=lambda *_: self.save_settings()
        )

        layout.add_widget(save_btn)

        self.add_widget(layout)

    def save_settings(self):
        """Persist settings back to the app instance."""

        app = App.get_running_app()

        path = self.kismet_field.text
        if os.path.exists(path):
            app.kismet_logdir = path
        else:
            report_error(
                format_error(
                    201, f"Invalid Kismet log dir: {path}. Please provide an existing path."
                )
            )

        path = self.bcap_field.text
        if os.path.exists(path):
            app.bettercap_caplet = path
        else:
            report_error(
                format_error(
                    202,
                    f"Invalid BetterCAP caplet: {path}. Provide a valid file path.",
                )
            )

        try:
            value = int(self.gps_poll_field.text)
            if value > 0:
                app.map_poll_gps = value
            else:
                raise ValueError
        except ValueError:
            report_error(
                format_error(203, "GPS poll rate must be a positive integer. Enter a value greater than 0.")
            )

        try:
            value = int(self.ap_poll_field.text)
            if value > 0:
                app.map_poll_aps = value
            else:
                raise ValueError
        except ValueError:
            report_error(
                format_error(206, "AP poll rate must be a positive integer. Enter a value greater than 0.")
            )

        try:
            value = int(self.health_poll_field.text)
            if value > 0:
                app.health_poll_interval = value
            else:
                raise ValueError
        except ValueError:
            report_error(
                format_error(207, "Health poll must be a positive integer.")
            )

        try:
            value = int(self.log_rotate_field.text)
            if value > 0:
                app.log_rotate_interval = value
            else:
                raise ValueError
        except ValueError:
            report_error(
                format_error(208, "Log rotate interval must be positive.")
            )

        try:
            value = int(self.log_archives_field.text)
            if value > 0:
                app.log_rotate_archives = value
            else:
                raise ValueError
        except ValueError:
            report_error(
                format_error(209, "Log archives must be a positive integer.")
            )

        path = self.offline_path_field.text
        if os.path.exists(path):
            app.offline_tile_path = path
        else:
            report_error(
                format_error(
                    204,
                    f"Invalid offline tile path: {path}. Please provide an existing directory.",
                )
            )

        app.map_use_offline = self.offline_switch.active
        app.theme = "Dark" if self.theme_switch.active else "Light"
        app.theme_cls.theme_style = app.theme
        app.map_show_gps = self.show_gps_switch.active
        app.map_show_aps = self.show_aps_switch.active
        app.map_cluster_aps = self.cluster_switch.active
        app.debug_mode = self.debug_switch.active
        app.widget_battery_status = self.battery_switch.active

        for f in fields(Config):
            key = f.name
            if hasattr(app, key):
                setattr(app.config_data, key, getattr(app, key))
        try:
            save_config(app.config_data)
        except OSError as exc:  # pragma: no cover - save failure
            report_error(
                format_error(
                    205,
                    f"Failed to save config: {exc}. Check file permissions.",
                )
            )

        Snackbar(text="Settings saved", duration=1).open()
