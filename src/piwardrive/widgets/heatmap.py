"""Widget displaying an access point heatmap."""

from __future__ import annotations

import logging
import tempfile
from typing import Any

from piwardrive.heatmap import histogram, save_png
from piwardrive.localization import _
from piwardrive.persistence import load_ap_cache
from piwardrive.ui import Card
from piwardrive.ui import Image
from piwardrive.ui import Label
from piwardrive.ui import dp
from piwardrive.utils import run_async_task

from .base import DashboardWidget


class HeatmapWidget(DashboardWidget):
    """Render a simple heatmap of discovered access points."""

    update_interval = 60.0

    def __init__(self, bins: int = 40, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.bins = bins
        self.card = Card(orientation="vertical", padding=dp(8), radius=[8])
        self.label = Label(text=_("heatmap"), halign="center")
        self.image = Image(size_hint_y=None, height=dp(150))
        self.card.add_widget(self.label)
        self.card.add_widget(self.image)
        self.add_widget(self.card)
        self._tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        self._event = f"heatmap_{id(self)}"
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
                self.label.text = (
                    _("heatmap") + f" (cells {len(hist)}x{len(hist[0]) if hist else 0})"
                )
            except Exception as exc:
                logging.exception("HeatmapWidget update failed: %s", exc)

        run_async_task(load_ap_cache(), _apply)
