"""Widget showing whether services are running."""

import logging
from typing import Any
from kivymd.uix.label import MDLabel

from .base import DashboardWidget
from utils import service_status


class ServiceStatusWidget(DashboardWidget):
    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.label = MDLabel(text="Services: N/A")
        self.add_widget(self.label)
        self.update()

    def update(self) -> None:
        try:
            kis = service_status('kismet')
            btc = service_status('bettercap')
            self.label.text = (
                f"Kismet: {'OK' if kis else 'DOWN'} | BetterCAP: {'OK' if btc else 'DOWN'}"
            )
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("ServiceStatusWidget update failed: %s", exc)
