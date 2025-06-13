"""Widget showing GPS fix quality."""

from kivymd.uix.label import MDLabel

from .base import DashboardWidget
from utils import get_gps_fix_quality


class GPSStatusWidget(DashboardWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = MDLabel(text="GPS: N/A")
        self.add_widget(self.label)
        self.update()

    def update(self):
        self.label.text = f"GPS: {get_gps_fix_quality()}"
