## settings_screen.py

"""Settings screen for starting and stopping background services."""



from kivy.app import App
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel




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

         for svc, label in [␊
            ("kismet.service", "Kismet"),␊
            ("bettercap.service", "BetterCAP"),␊
        ]:␊
            row = MDBoxLayout(spacing=dp(8), size_hint_y=None, height=dp(48))
            row.add_widget(MDLabel(text=label, size_hint_x=None, width=dp(80)))
            for action in ("start", "stop", "restart"):
                row.add_widget(
                    MDRaisedButton(
                        text=action.capitalize(),
                        on_release=lambda _btn, s=svc, a=action: App.get_running_app().control_service(s, a),
                    )
                )
            layout.add_widget(row)

        app = App.get_running_app()

        # Config fields
        self.kismet_field = MDTextField(text=app.kismet_logdir, hint_text="Kismet log dir")
        self.bcap_field = MDTextField(text=app.bettercap_caplet, hint_text="BetterCAP caplet")
        layout.add_widget(self.kismet_field)
        layout.add_widget(self.bcap_field)

        # Toggles
        theme_row = MDBoxLayout(spacing=dp(8), size_hint_y=None, height=dp(48))
        theme_row.add_widget(MDLabel(text="Dark Theme", size_hint_x=.7))
        self.theme_switch = MDSwitch(active=app.theme == "Dark")
        theme_row.add_widget(self.theme_switch)
        layout.add_widget(theme_row)

        offline_row = MDBoxLayout(spacing=dp(8), size_hint_y=None, height=dp(48))
        offline_row.add_widget(MDLabel(text="Offline Tiles", size_hint_x=.7))
        self.offline_switch = MDSwitch(active=app.map_use_offline)
        offline_row.add_widget(self.offline_switch)
        layout.add_widget(offline_row)

        save_btn = MDRaisedButton(text="Save", on_release=lambda *_: self.save_settings())
        layout.add_widget(save_btn)

        self.add_widget(layout)

    def save_settings(self):
        """Persist settings back to the app instance."""
        app = App.get_running_app()
        app.kismet_logdir = self.kismet_field.text
        app.bettercap_caplet = self.bcap_field.text
        app.map_use_offline = self.offline_switch.active
        app.theme = "Dark" if self.theme_switch.active else "Light"
        app.theme_cls.theme_style = app.theme
        Snackbar(text="Settings saved", duration=1).open()
