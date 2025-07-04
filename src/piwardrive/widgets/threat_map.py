"""Widget rendering a mini threat map."""

import logging
from typing import Any

from piwardrive.simpleui import Card as MDCard
from piwardrive.simpleui import Label as MDLabel
from piwardrive.simpleui import dp

from .base import DashboardWidget


class ThreatMapWidget(DashboardWidget):
    """Render a small threat map image."""

    update_interval = 60.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.card = MDCard(orientation="vertical", padding=dp(8), radius=[8])
        self.label = MDLabel(text="Threat Map", halign="center")
        self.card.add_widget(self.label)
        self.add_widget(self.card)
        self.update()

    def update(self) -> None:
        try:
            # Real implementation would draw a map
            self.label.text = "Threat Map"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("ThreatMapWidget update failed: %s", exc)
