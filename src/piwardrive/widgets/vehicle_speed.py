"""Widget showing vehicle speed via OBD-II."""

import logging
from typing import Any

from piwardrive import vehicle_sensors
from piwardrive.localization import _
from piwardrive.simpleui import Card as MDCard
from piwardrive.simpleui import Label as MDLabel
from piwardrive.simpleui import dp

from .base import DashboardWidget


class VehicleSpeedWidget(DashboardWidget):
    """Display vehicle speed in km/h.

    A label widget is created on initialization and the first reading is
    displayed immediately.
    """

    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.card = MDCard(orientation="vertical", padding=dp(8), radius=[8])
        self.label = MDLabel(
            text=f"{_('vehicle_speed')}: {_('not_available')}", halign="center"
        )
        self.card.add_widget(self.label)
        self.add_widget(self.card)
        self.update()

    def update(self) -> None:
        """Poll OBD speed and update the label."""
        try:
            speed = vehicle_sensors.read_speed_obd()
            if speed is None:
                self.label.text = f"{_('vehicle_speed')}: {_('not_available')}"
            else:
                self.label.text = f"{_('vehicle_speed')}: {speed:.1f} km/h"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("VehicleSpeedWidget update failed: %s", exc)
