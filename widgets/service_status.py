"""Widget showing whether services are running."""

from kivymd.uix.label import MDLabel

from .base import DashboardWidget
from utils import service_status


class ServiceStatusWidget(DashboardWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = MDLabel(text="Services: N/A")
        self.add_widget(self.label)
        self.update()

    def update(self):
        kis = service_status('kismet')
        btc = service_status('bettercap')
        self.label.text = f"Kismet: {'OK' if kis else 'DOWN'} | BetterCAP: {'OK' if btc else 'DOWN'}"
