"""Widget showing device classification distribution."""

import logging
from typing import Any

from piwardrive.simpleui import Card as MDCard
from piwardrive.simpleui import Label as MDLabel
from piwardrive.simpleui import dp

from .base import DashboardWidget


class DeviceClassificationWidget(DashboardWidget):
    """Display basic device classification stats."""

    update_interval = 10.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.card = MDCard(orientation="vertical", padding=dp(8), radius=[8])
        self.label = MDLabel(text="Device Types: N/A", halign="center")
        self.card.add_widget(self.label)
        self.add_widget(self.card)
        self.update()

    def update(self) -> None:
        try:
            self.label.text = "Device Types: N/A"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("DeviceClassificationWidget update failed: %s", exc)
