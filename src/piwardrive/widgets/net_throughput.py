"""Widget graphing network throughput."""

from typing import Any

import psutil

from piwardrive.localization import _

from .base import DashboardWidget


class NetworkThroughputWidget(DashboardWidget):
    """Graph of bytes received and sent per second."""

    def __init__(
        self, update_interval: int = 1, max_points: int = 60, **kwargs: Any
    ) -> None:
        """Set up throughput graphs and schedule polling."""
        super().__init__(**kwargs)
        if update_interval <= 0:
            raise ValueError(_("update_interval must be positive"))
        self.update_interval = update_interval
        self.max_points = max_points
        self.index: int = 0
        self.data_rx: list[tuple[int, float]] = []
        self.data_tx: list[tuple[int, float]] = []
        self.prev = psutil.net_io_counters()

        self.plot_rx: list[tuple[int, float]] = []
        self.plot_tx: list[tuple[int, float]] = []
        self._event_name: str = f"net_tp_{id(self)}"
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
