"""Widget graphing network throughput."""
from typing import Any

from kivy.app import App
from kivy_garden.graph import Graph, LinePlot
from piwardrive.localization import _
import psutil

from .base import DashboardWidget


class NetworkThroughputWidget(DashboardWidget):
    """Graph of bytes received and sent per second."""

    def __init__(self, update_interval: int = 1, max_points: int = 60, **kwargs: Any) -> None:
        """Set up throughput graphs and schedule polling."""
        super().__init__(**kwargs)
        self.update_interval = update_interval
        self.max_points = max_points
        self.index: int = 0
        self.data_rx: list[tuple[int, float]] = []
        self.data_tx: list[tuple[int, float]] = []
        self.prev = psutil.net_io_counters()

        self.plot_rx: LinePlot = LinePlot(color=[0, 0, 1, 1], line_width=1.5)
        self.plot_tx: LinePlot = LinePlot(color=[1, 0, 0, 1], line_width=1.5)
        self.graph: Graph = Graph(
            xlabel=_("samples"),
            ylabel=_("kbps"),
            x_ticks_minor=5,
            x_grid=True,
            y_grid=True,
            ymin=0,
            ymax=100,
            xmin=0,
            xmax=self.max_points,
        )
        self.graph.add_plot(self.plot_rx)
        self.graph.add_plot(self.plot_tx)
        self.add_widget(self.graph)
        self._event_name: str = f"net_tp_{id(self)}"
        App.get_running_app().scheduler.schedule(
            self._event_name, lambda dt: self.update(), self.update_interval
        )
        self.update()

    def update(self) -> None:
        """Sample network counters and update the graph."""
        cur = psutil.net_io_counters()
        delta_rx = cur.bytes_recv - self.prev.bytes_recv
        delta_tx = cur.bytes_sent - self.prev.bytes_sent
        self.prev = cur
        rx_rate = delta_rx / self.update_interval / 1024
        tx_rate = delta_tx / self.update_interval / 1024

        self.index += 1
        self.data_rx.append((self.index, rx_rate))
        self.data_tx.append((self.index, tx_rate))
        if len(self.data_rx) > self.max_points:
            self.data_rx.pop(0)
            self.data_tx.pop(0)
        self.plot_rx.points = self.data_rx
        self.plot_tx.points = self.data_tx
        self.graph.xmax = max(self.index, self.max_points)
        ymax = max([p[1] for p in self.data_rx + self.data_tx] + [1])
        self.graph.ymax = max(1, ymax * 1.2)
