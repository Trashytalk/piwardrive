"""Widget showing average Wi-Fi signal strength."""

import logging
from typing import Any
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from localization import _

from .base import DashboardWidget
from utils import fetch_kismet_devices_async, get_avg_rssi, run_async_task


class SignalStrengthWidget(DashboardWidget):
    """Display average RSSI from Kismet devices."""
    
    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.label = MDLabel(text=f"{_('rssi')}: {_('not_available')}")
        self.add_widget(self.label)
        self.update()

    def update(self) -> None:
        """Schedule an asynchronous RSSI refresh."""

        def _apply(result: tuple[list, list]) -> None:
            aps, _ = result
            avg = get_avg_rssi(aps)

            def _set(_dt: float) -> None:
                if avg is not None:
                    self.label.text = f"RSSI: {avg:.1f} dBm"
                else:
                    self.label.text = "RSSI: N/A"

            Clock.schedule_once(_set, 0)

        try:
            run_async_task(fetch_kismet_devices_async(), _apply)

        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("SignalStrengthWidget update failed: %s", exc)
