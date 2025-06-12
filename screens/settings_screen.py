## settings_screen.py





# screens/settings_screen.py
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.app import App
from kivy.metrics import dp


class SettingsScreen(Screen):
    def on_enter(self):
        """Build the service control buttons when the screen is shown."""
        if self.children:
            # Avoid creating the layout multiple times
            return

        container = MDBoxLayout(orientation="vertical",
                                padding=dp(20),
                                spacing=dp(20))

        container.add_widget(self._service_row("kismet.service", "Kismet"))
        container.add_widget(self._service_row("bettercap.service", "BetterCAP"))

        self.add_widget(container)

    def _service_row(self, service_name, display_name):
        """Return a row of Start/Stop/Restart buttons for a service."""
        row = MDBoxLayout(orientation="horizontal",
                          spacing=dp(10),
                          size_hint_y=None,
                          height=dp(40))

        row.add_widget(MDLabel(text=display_name, size_hint_x=None, width=dp(90)))

        for action in ("start", "stop", "restart"):
            btn = MDRaisedButton(
                text=action.capitalize(),
                on_release=lambda _btn, act=action, svc=service_name:
                    App.get_running_app().control_service(svc, act)
            )
            row.add_widget(btn)

        return row
