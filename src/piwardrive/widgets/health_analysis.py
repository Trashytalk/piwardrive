"""Widget displaying analyzed health metrics with a plot."""
import logging
from typing import Any
import tempfile

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from ..localization import _

from .base import DashboardWidget
from ..persistence import load_recent_health
from ..utils import run_async_task
from ..analysis import compute_health_stats, plot_cpu_temp


class HealthAnalysisWidget(DashboardWidget):
    """Visualize averaged system metrics and a temperature plot."""

    update_interval = 30.0

    def __init__(self, max_records: int = 50, **kwargs: Any) -> None:
        """Prepare widgets and schedule periodic analysis updates."""
        super().__init__(**kwargs)
        self.max_records = max_records
        self.label = MDLabel(text=f"{_('health_analysis')}: {_('not_available')}")
        self.image = Image(size_hint_y=None, height=dp(150))
        self.add_widget(self.label)
        self.add_widget(self.image)
        self._tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        self._event = f"health_analysis_{id(self)}"
        App.get_running_app().scheduler.schedule(
            self._event, lambda dt: self.update(), self.update_interval
        )
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
