"""Widget showing GPS fix quality."""

import logging
from typing import Any

from piwardrive.localization import _
from piwardrive.ui import Card
from piwardrive.ui import Label
from piwardrive.ui import dp
from piwardrive.utils import get_gps_fix_quality

from .base import DashboardWidget


class GPSStatusWidget(DashboardWidget):
    """Show quality of the current GPS fix.

    A label widget is created on startup and the first update is requested
    immediately.
    """

    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.card = Card(orientation="vertical", padding=dp(8), radius=[8])
        self.label = Label(text=f"{_('gps')}: {_('not_available')}", halign="center")
        self.card.add_widget(self.label)
        self.add_widget(self.card)
        self.update()

    def update(self) -> None:
        """Refresh with the latest GPS fix quality."""
        try:
            self.label.text = f"{_('gps')}: {get_gps_fix_quality()}"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("GPSStatusWidget update failed: %s", exc)
