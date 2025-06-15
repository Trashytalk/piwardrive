"""Widget displaying battery status."""

import logging
from typing import Any

from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from .base import DashboardWidget
from localization import _
import psutil


class BatteryStatusWidget(DashboardWidget):
    """Show battery percentage and charging state."""

    update_interval = 30.0

    def __init__(self, **kwargs: Any) -> None:
        """Create label widget and display initial reading."""
        super().__init__(**kwargs)
        self.card = MDCard(orientation="vertical", padding=dp(8), radius=[8])
        self.label = MDLabel(
            text=f"{_('battery')}: {_('not_available')}", halign="center"
        )
        self.card.add_widget(self.label)
        self.add_widget(self.card)
        self.update()

    def update(self) -> None:
        """Poll the battery state and update the label."""
        try:
            batt = psutil.sensors_battery()
            if batt is None:
                self.label.text = f"{_('battery')}: {_('not_available')}"
            else:
                status = _("charging") if batt.power_plugged else _("discharging")
                self.label.text = (
                    f"{_('battery')}: {batt.percent:.0f}% {status}"
                )
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("BatteryStatusWidget update failed: %s", exc)
