"""Predictive map tile prefetching based on recent GPS points."""

from __future__ import annotations

import logging
import os
from typing import Any

from kivy.app import App

from scheduler import PollScheduler


logger = logging.getLogger(__name__)


class RoutePrefetcher:
    """Schedule tile downloads along the predicted route."""

    def __init__(
        self,
        scheduler: PollScheduler,
        map_screen: Any,
        *,
        interval: int = 3600,
        lookahead: int = 5,
        delta: float = 0.01,
    ) -> None:
        self._map_screen = map_screen
        self._lookahead = lookahead
        self._delta = delta
        scheduler.schedule(
            "route_prefetch", lambda _dt: self._run(), interval
        )

    # --------------------------------------------------------------
    def _predict_points(self) -> list[tuple[float, float]]:
        track = getattr(self._map_screen, "track_points", [])
        if len(track) < 2:
            return []
        lat1, lon1 = track[-2]
        lat2, lon2 = track[-1]
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        pts: list[tuple[float, float]] = []
        lat = lat2
        lon = lon2
        for _ in range(self._lookahead):
            lat += dlat
            lon += dlon
            pts.append((lat, lon))
        return pts

    def _run(self) -> None:
        try:
            points: list[tuple[float, float]] = list(
                getattr(self._map_screen, "track_points", [])
            )[-self._lookahead :]
            points += self._predict_points()
            if not points:
                return
            lats = [p[0] for p in points]
            lons = [p[1] for p in points]
            bbox = (
                min(lats) - self._delta,
                min(lons) - self._delta,
                max(lats) + self._delta,
                max(lons) + self._delta,
            )
            mv = getattr(self._map_screen.ids, "mapview", None)
            zoom = getattr(mv, "zoom", 16)
            app = App.get_running_app()
            folder = os.path.dirname(
                getattr(app, "offline_tile_path", "")
            ) or "/mnt/ssd/tiles"
            self._map_screen.prefetch_tiles(bbox, zoom=zoom, folder=folder)
        except Exception as exc:  # pragma: no cover - unexpected errors
            logger.exception("RoutePrefetcher failed: %s", exc)
