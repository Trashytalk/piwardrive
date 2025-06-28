"""Widget displaying analyzed health metrics with a plot."""

import logging
import tempfile
from typing import Any

from piwardrive.analysis import compute_health_stats, plot_cpu_temp
from piwardrive.localization import _
from piwardrive.persistence import load_recent_health
from piwardrive.simpleui import Card as MDCard
from piwardrive.simpleui import Image
from piwardrive.simpleui import Label as MDLabel
from piwardrive.simpleui import dp
from piwardrive.utils import run_async_task

from .base import DashboardWidget


class HealthAnalysisWidget(DashboardWidget):
    """Visualize averaged system metrics and a temperature plot."""

    update_interval = 30.0

    def __init__(self, max_records: int = 50, **kwargs: Any) -> None:
        """Prepare widgets and schedule periodic analysis updates."""
        super().__init__(**kwargs)
        self.max_records = max_records
        self.card = MDCard(orientation="vertical", padding=dp(8), radius=[8])
        self.label = MDLabel(
            text=f"{_('health_analysis')}: {_('not_available')}", halign="center"
        )
        self.image = Image(size_hint_y=None, height=dp(150))
        self.card.add_widget(self.label)
        self.card.add_widget(self.image)
        self.add_widget(self.card)
        self._tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        self._event = f"health_analysis_{id(self)}"
        self.update()

    def update(self) -> None:  # pragma: no cover - GUI update
        """Load recent metrics, compute stats and refresh the view."""

        def _apply(records: list) -> None:
            try:
                if not records:
                    self.label.text = f"{_('health_analysis')}: {_('not_available')}"
                    return
                stats = compute_health_stats(records)
                self.label.text = (
                    f"{_('temp')}:{stats['temp_avg']:.1f}°C "
                    f"{_('cpu')}:{stats['cpu_avg']:.0f}% "
                    f"{_('mem')}:{stats['mem_avg']:.0f}% "
                    f"{_('disk')}:{stats['disk_avg']:.0f}%"
                )
                plot_cpu_temp(records, self._tmp.name)
                self.image.source = self._tmp.name
                self.image.reload()
            except Exception as exc:
                logging.exception("HealthAnalysisWidget update failed: %s", exc)

        run_async_task(load_recent_health(self.max_records), _apply)
