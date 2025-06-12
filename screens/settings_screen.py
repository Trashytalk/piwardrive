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
                        on_release=lambda _btn, s=svc, a=action: App.get_running_app().control_service(s, a),
                    )
                )
            layout.add_widget(row)

        self.add_widget(layout)
