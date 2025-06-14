"""Widget showing average Wi-Fi signal strength."""

import logging
from typing import Any
from kivymd.uix.label import MDLabel

from .base import DashboardWidget
import asyncio
from utils import fetch_kismet_devices_async, get_avg_rssi


class SignalStrengthWidget(DashboardWidget):
    """Display average RSSI from Kismet devices."""
    
    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.label = MDLabel(text="RSSI: N/A")
        self.add_widget(self.label)
        self.update()

    def update(self) -> None:
        try:
            aps, _ = asyncio.run(fetch_kismet_devices_async())
            avg = get_avg_rssi(aps)
            if avg is not None:
                self.label.text = f"RSSI: {avg:.1f} dBm"
            else:
                self.label.text = "RSSI: N/A"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("SignalStrengthWidget update failed: %s", exc)
