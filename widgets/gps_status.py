+5-3
"""Widget showing GPS fix quality."""

import logging
from typing import Any
from kivymd.uix.label import MDLabel

from .base import DashboardWidget
from utils import get_gps_fix_quality


class GPSStatusWidget(DashboardWidget):
    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.label = MDLabel(text="GPS: N/A")
        self.add_widget(self.label)
        self.update()

    def update(self) -> None:
        try:
            self.label.text = f"GPS: {get_gps_fix_quality()}"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("GPSStatusWidget update failed: %s", exc)
