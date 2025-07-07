"""Utilities for generating access point heatmaps."""

from __future__ import annotations

from typing import Iterable, List, Sequence, Tuple

import numpy as np
from scipy.ndimage import convolve


def _get_bins(bins: int | Tuple[int, int]) -> Tuple[int, int]:
    """Return latitude/longitude bin counts.

    ``bins`` may be specified as a single integer or a ``(lat, lon)`` tuple. All
    values must be strictly positive, otherwise a ``ValueError`` is raised.
    """
    if isinstance(bins, int):
        if bins <= 0:
            raise ValueError("bin count must be positive")
        return (bins, bins)

    lat_bins, lon_bins = bins
    if lat_bins <= 0 or lon_bins <= 0:
        raise ValueError("bin count must be positive")
    return lat_bins, lon_bins


def _derive_bounds(pts: list[Coord]) -> Tuple[float, float, float, float]:
    lats = [p[0] for p in pts]
    lons = [p[1] for p in pts]
    return min(lats), min(lons), max(lats), max(lons)


def _fill_histogram(
    pts: Iterable[Coord],
    bins_lat: int,
    bins_lon: int,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
) -> list[list[int]]:
    hist = [[0 for _ in range(bins_lon)] for _ in range(bins_lat)]
    if max_lat == min_lat or max_lon == min_lon:
        return hist

    lat_span = max_lat - min_lat
    lon_span = max_lon - min_lon
    for lat, lon in pts:
        if not (min_lat <= lat <= max_lat and min_lon <= lon <= max_lon):
            continue
        i = int((lat - min_lat) / lat_span * bins_lat)
        j = int((lon - min_lon) / lon_span * bins_lon)
        i = min(i, bins_lat - 1)
        j = min(j, bins_lon - 1)
        hist[i][j] += 1
    return hist


Coord = Tuple[float, float]


def histogram(
    coords: Iterable[Coord],
    *,
    bins: int | Tuple[int, int] = 100,
    bounds: Sequence[float] | None = None,
) -> Tuple[List[List[int]], Tuple[float, float], Tuple[float, float]]:
    """Return a 2D histogram for latitude/longitude pairs.

    ``bins`` sets the grid resolution. If ``bounds`` is omitted the
    minimum/maximum coordinates are derived from ``coords``.
    """
    pts = [(float(lat), float(lon)) for lat, lon in coords]
    bins_lat, bins_lon = _get_bins(bins)

    if bounds is None:
        if not pts:
            empty = [[0 for _ in range(bins_lon)] for _ in range(bins_lat)]
            return empty, (0.0, 0.0), (0.0, 0.0)
        min_lat, min_lon, max_lat, max_lon = _derive_bounds(pts)
    else:
        min_lat, min_lon, max_lat, max_lon = map(float, bounds)

    hist = _fill_histogram(pts, bins_lat, bins_lon, min_lat, max_lat, min_lon, max_lon)
    return hist, (min_lat, max_lat), (min_lon, max_lon)


def histogram_points(
    hist: Sequence[Sequence[int]],
    lat_range: Sequence[float],
    lon_range: Sequence[float],
) -> List[Tuple[float, float, int]]:
    """Return center coordinates and counts for each populated cell."""
    min_lat, max_lat = map(float, lat_range)
    min_lon, max_lon = map(float, lon_range)
    bins_lat = len(hist)
    bins_lon = len(hist[0]) if hist else 0
    if bins_lat == 0 or bins_lon == 0:
        return []
    lat_step = (max_lat - min_lat) / bins_lat
    lon_step = (max_lon - min_lon) / bins_lon
    points: List[Tuple[float, float, int]] = []
    for i, row in enumerate(hist):
        for j, count in enumerate(row):
            if count <= 0:
                continue
            lat = min_lat + (i + 0.5) * lat_step
            lon = min_lon + (j + 0.5) * lon_step
            points.append((lat, lon, int(count)))
    return points


def save_png(hist: Sequence[Sequence[int]], path: str) -> None:
    """Render ``hist`` to ``path`` using matplotlib if available."""
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:  # pragma: no cover - optional dependency
        with open(path, "wb") as fh:
            fh.write(b"")
        return

    plt.figure(figsize=(3, 3))
    plt.imshow(hist, cmap="hot", origin="lower")
    plt.axis("o")
    plt.tight_layout()
    plt.savefig(path, dpi=100, bbox_inches="tight", pad_inches=0)
    plt.close()


def _spread_density(hist: Sequence[Sequence[int]], radius: int) -> List[List[int]]:
    """Spread the counts from ``hist`` to neighbouring cells using convolution."""
    arr = np.asarray(hist, dtype=int)
    if arr.size == 0:
        return arr.tolist()

    kernel_size = 2 * radius + 1
    kernel = np.ones((kernel_size, kernel_size), dtype=int)
    density = convolve(arr, kernel, mode="constant", cval=0)
    return density.tolist()
    bins_lat = len(hist)
    bins_lon = len(hist[0]) if hist else 0
    density = [[0 for _ in range(bins_lon)] for _ in range(bins_lat)]
    if radius <= 0:
        raise ValueError("radius must be positive")
    for i, row in enumerate(hist):
        for j, count in enumerate(row):
            if count <= 0:
                continue
            for di in range(-radius, radius + 1):
                for dj in range(-radius, radius + 1):
                    ii = i + di
                    jj = j + dj
                    if 0 <= ii < bins_lat and 0 <= jj < bins_lon:
                        density[ii][jj] += count
    return density


def density_map(
    coords: Iterable[Coord],
    *,
    bins: int | Tuple[int, int] = 100,
    bounds: Sequence[float] | None = None,
    radius: int = 1,
) -> Tuple[List[List[int]], Tuple[float, float], Tuple[float, float]]:
    """Return a density map expanding counts to neighbouring cells."""
    hist, lat_range, lon_range = histogram(coords, bins=bins, bounds=bounds)
    if not hist or not hist[0]:
        return hist, lat_range, lon_range
    density = _spread_density(hist, radius)
    return density, lat_range, lon_range


def coverage_map(
    coords: Iterable[Coord],
    *,
    bins: int | Tuple[int, int] = 100,
    bounds: Sequence[float] | None = None,
    radius: int = 1,
) -> Tuple[List[List[int]], Tuple[float, float], Tuple[float, float]]:
    """Return a binary coverage map from ``coords`` using ``radius`` cells."""
    dens, lat_range, lon_range = density_map(
        coords, bins=bins, bounds=bounds, radius=radius
    )
    coverage = [[1 if c > 0 else 0 for c in row] for row in dens]
    return coverage, lat_range, lon_range
