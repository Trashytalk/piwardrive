"""Widget displaying SSD usage."""

import logging
from kivymd.uix.label import MDLabel

from .base import DashboardWidget
from utils import get_disk_usage


class StorageUsageWidget(DashboardWidget):
    update_interval = 5.0
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = MDLabel(text="SSD: N/A")
        self.add_widget(self.label)
        self.update()

    def update(self):
        try:
            pct = get_disk_usage('/mnt/ssd')
            if pct is not None:
                self.label.text = f"SSD: {pct:.0f}%"
            else:
                self.label.text = "SSD: N/A"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("StorageUsageWidget update failed: %s", exc)
