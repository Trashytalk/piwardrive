"""Widget showing average Wi-Fi signal strength."""

from kivymd.uix.label import MDLabel

from .base import DashboardWidget
from utils import fetch_kismet_devices, get_avg_rssi


class SignalStrengthWidget(DashboardWidget):
    """Display average RSSI from Kismet devices."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = MDLabel(text="RSSI: N/A")
        self.add_widget(self.label)
        self.update()

    def update(self):
        aps, _ = fetch_kismet_devices()
        avg = get_avg_rssi(aps)
        if avg is not None:
            self.label.text = f"RSSI: {avg:.1f} dBm"
        else:
            self.label.text = "RSSI: N/A"
