"""Widget counting captured handshakes."""

import logging
from typing import Any
from kivymd.uix.label import MDLabel

from .base import DashboardWidget
from utils import count_bettercap_handshakes


class HandshakeCounterWidget(DashboardWidget):
    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.label = MDLabel(text="Handshakes: 0")
        self.add_widget(self.label)
        self.update()

    def update(self) -> None:
        try:
            self.label.text = f"Handshakes: {count_bettercap_handshakes()}"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("HandshakeCounterWidget update failed: %s", exc)
