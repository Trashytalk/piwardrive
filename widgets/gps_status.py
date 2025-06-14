"""Widget showing GPS fix quality."""

import logging
from typing import Any
from kivymd.uix.label import MDLabel
from localization import _

from .base import DashboardWidget
from utils import get_gps_fix_quality


class GPSStatusWidget(DashboardWidget):
    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.label = MDLabel(text=f"{_('gps')}: {_('not_available')}")
        self.add_widget(self.label)
        self.update()

    def update(self) -> None:
        try:
            self.label.text = f"{_('gps')}: {get_gps_fix_quality()}"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("GPSStatusWidget update failed: %s", exc)
