"""Widget plotting CPU temperature over time."""

from typing import Any

from kivy.app import App
from kivy_garden.graph import Graph, LinePlot
from ..localization import _

from .base import DashboardWidget
from ..utils import get_cpu_temp


class CPUTempGraphWidget(DashboardWidget):
    """Display CPU temperature history using a line graph."""

    def __init__(self, update_interval: int = 5, max_points: int = 60, **kwargs: Any) -> None:
        """Initialize graph components and schedule updates."""
        super().__init__(**kwargs)
        self.update_interval = update_interval
        self.max_points = max_points
        self.index: int = 0
        self.data: list[tuple[int, float]] = []
        self.plot = LinePlot(color=[1, 0, 0, 1], line_width=1.5)
        self.graph = Graph(
            xlabel=_("samples"),
            ylabel="°C",
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
        self._event_name: str = f"cpu_temp_{id(self)}"
        App.get_running_app().scheduler.schedule(
            self._event_name, lambda dt: self.update(), self.update_interval
        )
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
        self.plot.points = self.data
        self.graph.xmax = max(self.index, self.max_points)
