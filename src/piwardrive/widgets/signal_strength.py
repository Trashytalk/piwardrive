"""Widget showing average Wi-Fi signal strength."""

import logging
from typing import Any

from piwardrive.localization import _
from piwardrive.ui import Card
from piwardrive.ui import Label
from piwardrive.ui import dp
from piwardrive.utils import fetch_kismet_devices_async, get_avg_rssi, run_async_task

from .base import DashboardWidget


class SignalStrengthWidget(DashboardWidget):
    """Display average RSSI from Kismet devices.

    The label widget is initialized when the widget is created and the first
    RSSI poll is queued immediately.
    """

    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.card = Card(orientation="vertical", padding=dp(8), radius=[8])
        self.label = Label(text=f"{_('rssi')}: {_('not_available')}", halign="center")
        self.card.add_widget(self.label)
        self.add_widget(self.card)
        self.update()

    def update(self) -> None:
        """Schedule an asynchronous RSSI refresh."""

        def _apply(result: tuple[list, list]) -> None:
            aps, _ = result
            avg = get_avg_rssi(aps)

            if avg is not None:
                self.label.text = f"RSSI: {avg:.1f} dBm"
            else:
                self.label.text = "RSSI: N/A"

        try:
            run_async_task(fetch_kismet_devices_async(), _apply)

        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("SignalStrengthWidget update failed: %s", exc)
