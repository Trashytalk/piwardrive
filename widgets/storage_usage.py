"""Widget displaying SSD usage."""

from kivymd.uix.label import MDLabel

from .base import DashboardWidget
from utils import get_disk_usage


class StorageUsageWidget(DashboardWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = MDLabel(text="SSD: N/A")
        self.add_widget(self.label)
        self.update()

    def update(self):
        pct = get_disk_usage('/mnt/ssd')
        if pct is not None:
            self.label.text = f"SSD: {pct:.0f}%"
        else:
            self.label.text = "SSD: N/A"
