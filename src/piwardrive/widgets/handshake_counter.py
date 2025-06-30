"""Widget counting captured handshakes."""

import logging
from typing import Any

from piwardrive.localization import _
from piwardrive.ui import Card
from piwardrive.ui import Label
from piwardrive.ui import dp
from piwardrive.utils import count_bettercap_handshakes

from .base import DashboardWidget


class HandshakeCounterWidget(DashboardWidget):
    """Track the number of WPA handshakes captured.

    A label widget is created during initialization and the first count is
    performed immediately.
    """

    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.card = Card(orientation="vertical", padding=dp(8), radius=[8])
        self.label = Label(text=f"{_('handshakes')}: 0", halign="center")
        self.card.add_widget(self.label)
        self.add_widget(self.card)
        self.update()

    def update(self) -> None:
        """Refresh handshake count from BetterCAP logs."""
        try:
            self.label.text = f"{_('handshakes')}: {count_bettercap_handshakes()}"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("HandshakeCounterWidget update failed: %s", exc)
