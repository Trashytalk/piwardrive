"""Widget displaying scanner status."""

import logging
from typing import Any

from piwardrive.simpleui import Card as MDCard
from piwardrive.simpleui import Label as MDLabel
from piwardrive.simpleui import dp

from .base import DashboardWidget


class ScannerStatusWidget(DashboardWidget):
    """Show whether the scanner device is running."""

    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.card = MDCard(orientation="vertical", padding=dp(8), radius=[8])
        self.label = MDLabel(text="Scanner: N/A", halign="center")
        self.card.add_widget(self.label)
        self.add_widget(self.card)
        self.update()

    def update(self) -> None:
        try:
            self.label.text = "Scanner: N/A"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("ScannerStatusWidget update failed: %s", exc)
