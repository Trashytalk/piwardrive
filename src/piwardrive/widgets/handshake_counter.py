"""Widget counting captured handshakes."""

import logging
from typing import Any
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from piwardrive.localization import _

from .base import DashboardWidget
from piwardrive.utils import count_bettercap_handshakes


class HandshakeCounterWidget(DashboardWidget):
    """Track the number of WPA handshakes captured."""

    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        """Initialize label widget and trigger first count."""
        super().__init__(**kwargs)
        self.card = MDCard(orientation="vertical", padding=dp(8), radius=[8])
        self.label = MDLabel(text=f"{_('handshakes')}: 0", halign="center")
        self.card.add_widget(self.label)
        self.add_widget(self.card)
        self.update()

    def update(self) -> None:
        """Refresh handshake count from BetterCAP logs."""
        try:
            self.label.text = f"{_('handshakes')}: {count_bettercap_handshakes()}"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("HandshakeCounterWidget update failed: %s", exc)
