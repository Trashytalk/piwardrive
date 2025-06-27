"""Widget displaying number of LoRa scan results."""

import logging
from typing import Any

from piwardrive import lora_scanner
from piwardrive.localization import _
from piwardrive.simpleui import Card as MDCard
from piwardrive.simpleui import Label as MDLabel
from piwardrive.simpleui import dp

from .base import DashboardWidget


class LoRaScanWidget(DashboardWidget):
    """Display LoRa scan count."""

    update_interval = 30.0

    def __init__(self, **kwargs: Any) -> None:
        """Create label widget and show initial count."""
        super().__init__(**kwargs)
        self.card = MDCard(orientation="vertical", padding=dp(8), radius=[8])
        self.label = MDLabel(
            text=f"{_('lora_devices')}: 0", halign="center"
        )
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
