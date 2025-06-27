from __future__ import annotations

from typing import Sequence

def haversine_distance(p1: tuple[float, float], p2: tuple[float, float]) -> float: ...


def polygon_area(points: Sequence[tuple[float, float]]) -> float: ...


def point_in_polygon(
    point: tuple[float, float],
    polygon: Sequence[tuple[float, float]],
) -> bool: ...
