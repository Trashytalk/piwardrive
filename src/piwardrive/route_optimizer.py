"""Route optimization helpers."""

from __future__ import annotations

import math
from typing import Iterable, Tuple, List

Coord = Tuple[float, float]


def suggest_route(
    points: Iterable[Coord],
    *,
    cell_size: float = 0.001,
    steps: int = 5,
    search_radius: int = 5,
) -> List[Coord]:
    """Return waypoints that maximize coverage based on ``points``.

    Parameters
    ----------
    points:
        Sequence of ``(lat, lon)`` coordinates in chronological order.
    cell_size:
        Grid resolution in degrees used to mark visited areas.
    steps:
        Number of waypoints to return.
    search_radius:
        How far to search for new cells around the current location, in grid
        cells.
    """
    pts = [(float(lat), float(lon)) for lat, lon in points]
    if not pts:
        return []

    def to_cell(lat: float, lon: float) -> tuple[int, int]:
        return math.floor(lat / cell_size), math.floor(lon / cell_size)

    visited = {to_cell(lat, lon) for lat, lon in pts}
    cur_cell = to_cell(*pts[-1])

    route: List[Coord] = []
    for _ in range(steps):
        best: tuple[int, int] | None = None
        best_dist: int | None = None
        for dx in range(-search_radius, search_radius + 1):
            for dy in range(-search_radius, search_radius + 1):
                cell = (cur_cell[0] + dx, cur_cell[1] + dy)
                if cell in visited:
                    continue
                dist = dx * dx + dy * dy
                if best_dist is None or dist < best_dist:
                    best = cell
                    best_dist = dist
        if best is None:
            break
        visited.add(best)
        cur_cell = best
        lat = (best[0] + 0.5) * cell_size
        lon = (best[1] + 0.5) * cell_size
        route.append((lat, lon))
    return route


__all__ = ["suggest_route"]
