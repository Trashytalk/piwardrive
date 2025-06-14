"""Widget showing disk usage percentage over time."""

from typing import Any

from kivy.app import App
from kivy_garden.graph import Graph, LinePlot

from .base import DashboardWidget
from utils import get_disk_usage


class DiskUsageTrendWidget(DashboardWidget):
    """Plot SSD disk usage percentage over time."""

    def __init__(self, update_interval: int = 5, max_points: int = 60, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.update_interval = update_interval
        self.max_points = max_points
        self.index: int = 0
        self.data: list[tuple[int, float]] = []
        self.plot = LinePlot(color=[0, 1, 0, 1], line_width=1.5)
        self.graph = Graph(
            xlabel="Samples",
            ylabel="%",
            x_ticks_minor=5,
            x_grid=True,
            y_grid=True,
            ymin=0,
            ymax=100,
            xmin=0,
            xmax=self.max_points,
        )
        self.graph.add_plot(self.plot)
        self.add_widget(self.graph)
        self._event_name: str = f"disk_trend_{id(self)}"
        App.get_running_app().scheduler.schedule(
            self._event_name, lambda dt: self.update(), self.update_interval
        )
        self.update()

    def update(self) -> None:
        pct = get_disk_usage("/mnt/ssd")
        if pct is None:
            return
        self.index += 1
        self.data.append((self.index, pct))
        if len(self.data) > self.max_points:
            self.data.pop(0)
        self.plot.points = self.data
        self.graph.xmax = max(self.index, self.max_points)
