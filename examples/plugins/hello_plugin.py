"""Example dashboard plugin that displays a greeting."""

from datetime import datetime

from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from widgets.base import DashboardWidget


class HelloPluginWidget(DashboardWidget):
    """Simple example widget for plugin demonstration."""

    update_interval = 5.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.card = MDCard(orientation="vertical", padding=dp(8), radius=[8])
        self.label = MDLabel(text="Hello from plugin!", halign="center")
        self.card.add_widget(self.label)
        self.add_widget(self.card)
        self.update()

    def update(self):
        """Update the label with the current time."""
        self.label.text = datetime.now().strftime("Hello %H:%M:%S")
