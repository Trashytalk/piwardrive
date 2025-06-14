"""Widget displaying battery status."""

import logging
from typing import Any

from kivymd.uix.label import MDLabel
from .base import DashboardWidget
import psutil


class BatteryStatusWidget(DashboardWidget):
    """Show battery percentage and charging state."""

    update_interval = 30.0

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.label = MDLabel(text="Battery: N/A")
        self.add_widget(self.label)
        self.update()

    def update(self) -> None:
        try:
            batt = psutil.sensors_battery()
            if batt is None:
                self.label.text = "Battery: N/A"
            else:
                status = "Charging" if batt.power_plugged else "Discharging"
                self.label.text = f"Battery: {batt.percent:.0f}% {status}"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("BatteryStatusWidget update failed: %s", exc)
