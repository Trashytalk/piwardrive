"""Widget displaying battery status."""

import logging
from typing import Any

import psutil

from piwardrive.localization import _
from piwardrive.simpleui import Card as MDCard
from piwardrive.simpleui import Label as MDLabel
from piwardrive.simpleui import dp

from .base import DashboardWidget


class BatteryStatusWidget(DashboardWidget):
    """Show battery percentage and charging state.

    A label widget is created on initialization and the first reading is
    displayed immediately.
    """

    update_interval = 30.0

    def __init__(self, **kwargs: Any) -> None:
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
                self.label.text = f"{_('battery')}: {batt.percent:.0f}% {status}"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("BatteryStatusWidget update failed: %s", exc)
