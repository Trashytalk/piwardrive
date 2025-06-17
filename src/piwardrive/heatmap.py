"""Utilities for generating access point heatmaps."""

from __future__ import annotations

from typing import Iterable, Sequence, Tuple, List


Coord = Tuple[float, float]


def histogram(
    coords: Iterable[Coord], *, bins: int | Tuple[int, int] = 100,
    bounds: Sequence[float] | None = None,
) -> Tuple[List[List[int]], Tuple[float, float], Tuple[float, float]]:
    """Return a 2D histogram for latitude/longitude pairs.

    ``bins`` sets the grid resolution. If ``bounds`` is omitted the
    minimum/maximum coordinates are derived from ``coords``.
    """
    pts = [(float(lat), float(lon)) for lat, lon in coords]
    if isinstance(bins, int):
        bins_lat = bins_lon = bins
    else:
        bins_lat, bins_lon = bins

    if bounds is None:
        if not pts:
            empty = [[0 for _ in range(bins_lon)] for _ in range(bins_lat)]
            return empty, (0.0, 0.0), (0.0, 0.0)        lats = [p[0] for p in pts]
        lons = [p[1] for p in pts]
        min_lat = min(lats)
        max_lat = max(lats)
        min_lon = min(lons)
        max_lon = max(lons)
    else:
        min_lat, min_lon, max_lat, max_lon = map(float, bounds)

    hist = [[0 for _ in range(bins_lon)] for _ in range(bins_lat)]
    if max_lat == min_lat or max_lon == min_lon:
        return hist, (min_lat, max_lat), (min_lon, max_lon)

    for lat, lon in pts:
        if not (min_lat <= lat <= max_lat and min_lon <= lon <= max_lon):
            continue
        i = int((lat - min_lat) / (max_lat - min_lat) * bins_lat)
        j = int((lon - min_lon) / (max_lon - min_lon) * bins_lon)
        if i == bins_lat:
            i -= 1
        if j == bins_lon:
            j -= 1
        hist[i][j] += 1

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
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(path, dpi=100, bbox_inches="tight", pad_inches=0)
    plt.close()
