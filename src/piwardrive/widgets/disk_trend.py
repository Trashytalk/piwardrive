"""Widget showing disk usage percentage over time."""

from typing import Any

from piwardrive.localization import _
from piwardrive.utils import get_disk_usage

from .base import DashboardWidget


class DiskUsageTrendWidget(DashboardWidget):
    """Plot SSD disk usage percentage over time.

    The graph widget is initialized during construction and periodic updates are
    scheduled automatically.
    """

    def __init__(
        self, update_interval: int = 5, max_points: int = 60, **kwargs: Any
    ) -> None:
        super().__init__(**kwargs)
        self.update_interval = update_interval
        self.max_points = max_points
        self.index: int = 0
        self.data: list[tuple[int, float]] = []
        self.update()

    def update(self) -> None:
        """Append the latest disk usage percentage to the plot."""
        pct = get_disk_usage("/mnt/ssd")
        if pct is None:
            return
        self.index += 1
        self.data.append((self.index, pct))
        if len(self.data) > self.max_points:
            self.data.pop(0)
