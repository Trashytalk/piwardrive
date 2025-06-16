"""Widget displaying an access point heatmap."""

from __future__ import annotations

import logging
import tempfile
from typing import Any

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.image import Image
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from .base import DashboardWidget
from heatmap import histogram, save_png
from persistence import load_ap_cache
from utils import run_async_task
from localization import _


class HeatmapWidget(DashboardWidget):
    """Render a simple heatmap of discovered access points."""

    update_interval = 60.0

    def __init__(self, bins: int = 40, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bins = bins
        self.card = MDCard(orientation="vertical", padding=dp(8), radius=[8])
        self.label = MDLabel(text=_("heatmap"), halign="center")
        self.image = Image(size_hint_y=None, height=dp(150))
        self.card.add_widget(self.label)
        self.card.add_widget(self.image)
        self.add_widget(self.card)
        self._tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        self._event = f"heatmap_{id(self)}"
        App.get_running_app().scheduler.schedule(
            self._event, lambda dt: self.update(), self.update_interval
        )
        self.update()

    def update(self) -> None:  # pragma: no cover - GUI updates
        """Load AP coordinates and refresh the heatmap."""

        def _apply(records: list[dict[str, Any]]) -> None:
            try:
                points = [
                    (r["lat"], r["lon"])
                    for r in records
                    if r.get("lat") is not None and r.get("lon") is not None
                ]
                hist, lat_r, lon_r = histogram(points, bins=self.bins)
                save_png(hist, self._tmp.name)
                self.image.source = self._tmp.name
                self.image.reload()
                self.label.text = _("heatmap") + f" (cells {len(hist)}x{len(hist[0]) if hist else 0})"
            except Exception as exc:
                logging.exception("HeatmapWidget update failed: %s", exc)

        run_async_task(load_ap_cache(), _apply)
