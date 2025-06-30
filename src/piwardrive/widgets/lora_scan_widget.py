"""Widget displaying number of LoRa scan results."""

import logging
from typing import Any

from piwardrive import lora_scanner
from piwardrive.localization import _
from piwardrive.ui import Card
from piwardrive.ui import Label
from piwardrive.ui import dp

from .base import DashboardWidget


class LoRaScanWidget(DashboardWidget):
    """Display LoRa scan count.

    A label widget is created on initialization and populated with the initial
    scan count.
    """

    update_interval = 30.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.card = Card(orientation="vertical", padding=dp(8), radius=[8])
        self.label = Label(text=f"{_('lora_devices')}: 0", halign="center")
        self.card.add_widget(self.label)
        self.add_widget(self.card)
        self.update()

    def update(self) -> None:
        """Run a LoRa scan and update the label."""
        try:
            lines = lora_scanner.scan_lora()
            self.label.text = f"{_('lora_devices')}: {len(lines)}"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("LoRaScanWidget update failed: %s", exc)
