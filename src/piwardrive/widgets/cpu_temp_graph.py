"""Widget plotting CPU temperature over time."""

from typing import Any

from piwardrive.localization import _
from piwardrive.utils import get_cpu_temp

from .base import DashboardWidget


class CPUTempGraphWidget(DashboardWidget):
    """Display CPU temperature history using a line graph."""

    def __init__(self, update_interval: int = 5, max_points: int = 60, **kwargs: Any) -> None:
        """Initialize graph components and schedule updates."""
        super().__init__(**kwargs)
        self.update_interval = update_interval
        self.max_points = max_points
        self.index: int = 0
        self.data: list[tuple[int, float]] = []
        self._event_name: str = f"cpu_temp_{id(self)}"
        self.update()

    def update(self) -> None:
        """Append the latest temperature reading to the plot."""
        temp = get_cpu_temp()
        if temp is None:
            return
        self.index += 1
        self.data.append((self.index, temp))
        if len(self.data) > self.max_points:
            self.data.pop(0)
