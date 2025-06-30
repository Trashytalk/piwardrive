"""Predictive map tile prefetching based on recent GPS points."""

from __future__ import annotations

import logging
import math
import os
from typing import Any


class App:  # type: ignore[misc]
    """Placeholder application interface."""

    @staticmethod
    def get_running_app() -> None:
        """Return ``None`` when no GUI is active."""
        return None


from piwardrive.scheduler import PollScheduler
from piwardrive.utils import haversine_distance

logger = logging.getLogger(__name__)


def _bearing(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Return initial bearing in degrees from ``p1`` to ``p2``."""
    lat1, lon1 = map(math.radians, p1)
    lat2, lon2 = map(math.radians, p2)
    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(
        dlon
    )
    return (math.degrees(math.atan2(x, y)) + 360) % 360


def _destination(
    origin: tuple[float, float], bearing: float, distance: float
) -> tuple[float, float]:
    """Return destination point from ``origin`` after ``distance`` meters."""
    r = 6371000.0
    ang = distance / r
    lat1 = math.radians(origin[0])
    lon1 = math.radians(origin[1])
    br = math.radians(bearing)
    lat2 = math.asin(
        math.sin(lat1) * math.cos(ang) + math.cos(lat1) * math.sin(ang) * math.cos(br)
    )
    lon2 = lon1 + math.atan2(
        math.sin(br) * math.sin(ang) * math.cos(lat1),
        math.cos(ang) - math.sin(lat1) * math.sin(lat2),
    )
    return math.degrees(lat2), ((math.degrees(lon2) + 540) % 360) - 180


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
        offline_tile_path: str | None = None,
    ) -> None:
        self._map_screen = map_screen
        self._lookahead = lookahead
        self._delta = delta
        self._offline_tile_path = offline_tile_path
        scheduler.schedule("route_prefetch", lambda _dt: self._run(), interval)

    # --------------------------------------------------------------
    def _predict_points(self) -> list[tuple[float, float]]:
        track = getattr(self._map_screen, "track_points", [])
        if len(track) < 2:
            return []
        p1 = track[-2]
        p2 = track[-1]
        heading = _bearing(p1, p2)
        step = haversine_distance(p1, p2)
        if step == 0.0:
            return []
        pts: list[tuple[float, float]] = []
        lat, lon = p2
        for _ in range(self._lookahead):
            lat, lon = _destination((lat, lon), heading, step)
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
            folder = (
                os.path.dirname(getattr(app, "offline_tile_path", ""))
                or "/mnt/ssd/tiles"
            )
            self._map_screen.prefetch_tiles(bbox, zoom=zoom, folder=folder)
        except Exception as exc:  # pragma: no cover - unexpected errors
            logger.exception("RoutePrefetcher failed: %s", exc)
