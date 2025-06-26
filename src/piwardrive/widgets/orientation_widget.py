"""Widget displaying device orientation."""

import logging
from typing import Any

from piwardrive.simpleui import dp, Label as MDLabel, Card as MDCard
from piwardrive.localization import _

from .base import DashboardWidget
from piwardrive import orientation_sensors


class OrientationWidget(DashboardWidget):
    """Show the current device orientation."""

    update_interval = 5.0

    def __init__(self, **kwargs: Any) -> None:
        """Create label widget and display initial reading."""
        super().__init__(**kwargs)
        self.card = MDCard(orientation="vertical", padding=dp(8), radius=[8])
        self.label = MDLabel(
            text=f"{_('orientation')}: {_('not_available')}", halign="center"
        )
        self.card.add_widget(self.label)
        self.add_widget(self.card)
        self.update()

    def update(self) -> None:
        """Poll sensors and refresh the label."""
        try:
            orient = orientation_sensors.get_orientation_dbus()
            if orient:
                angle = orientation_sensors.orientation_to_angle(orient)
                suffix = f" ({angle:.0f}\N{DEGREE SIGN})" if angle is not None else ""
                self.label.text = f"{_('orientation')}: {orient}{suffix}"
                return
            data = orientation_sensors.read_mpu6050()
            if data and 'accelerometer' in data:
                acc = data['accelerometer']
                self.label.text = (
                    f"accel: x={acc.get('x', 0):.1f} "
                    f"y={acc.get('y', 0):.1f} z={acc.get('z', 0):.1f}"
                )
            else:
                self.label.text = f"{_('orientation')}: {_('not_available')}"
        except Exception as exc:  # pragma: no cover - UI update
            logging.exception("OrientationWidget update failed: %s", exc)
