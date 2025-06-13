"""Widget counting captured handshakes."""

from kivymd.uix.label import MDLabel

from .base import DashboardWidget
from utils import count_bettercap_handshakes


class HandshakeCounterWidget(DashboardWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = MDLabel(text="Handshakes: 0")
        self.add_widget(self.label)
        self.update()

    def update(self):
        self.label.text = f"Handshakes: {count_bettercap_handshakes()}"
