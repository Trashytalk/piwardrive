"""Widget displaying SSD usage."""

import logging
from typing import Any

from piwardrive.localization import _
from piwardrive.simpleui import Card as MDCard
from piwardrive.simpleui import Label as MDLabel
from piwardrive.simpleui import dp
from piwardrive.utils import get_disk_usage

from .base import DashboardWidget


class StorageUsageWidget(DashboardWidget):
    """Indicate SSD usage percentage.

    A label widget is created on initialization and an initial update is
    performed.
    """

    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.card = MDCard(orientation="vertical", padding=dp(8), radius=[8])
        self.label = MDLabel(text=f"{_('ssd')}: {_('not_available')}", halign="center")
        self.card.add_widget(self.label)
        self.add_widget(self.card)
        self.update()

    def update(self) -> None:
        """Refresh storage usage value."""
        try:
            pct = get_disk_usage("/mnt/ssd")
            if pct is not None:
                self.label.text = f"{_('ssd')}: {pct:.0f}%"
            else:
                self.label.text = f"{_('ssd')}: {_('not_available')}"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("StorageUsageWidget update failed: %s", exc)
