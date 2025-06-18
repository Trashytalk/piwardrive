import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from piwardrive import heatmap


def test_histogram_counts():
    points = [
        (0.1, 0.1),
        (0.9, 0.9),
        (0.8, 0.8),
    ]
    hist, lat_range, lon_range = heatmap.histogram(points, bins=2, bounds=(0, 0, 1, 1))
    assert lat_range == (0.0, 1.0)
    assert lon_range == (0.0, 1.0)
    assert hist[0][0] == 1
    assert hist[1][1] == 2


def test_histogram_points():
    hist = [[0, 1], [2, 0]]
    pts = heatmap.histogram_points(hist, (0.0, 1.0), (0.0, 1.0))
    assert len(pts) == 2
    values = {(round(lat,1), round(lon,1), cnt) for lat, lon, cnt in pts}
    assert (0.75, 0.25, 2) in values or (0.25, 0.75, 1) in values


def test_density_map_expands_counts():
    pts = [(0.5, 0.5)]
    dens, lat_r, lon_r = heatmap.density_map(pts, bins=3, bounds=(0, 0, 1, 1), radius=1)
    assert len(dens) == 3
    assert len(dens[0]) == 3
    total = sum(sum(r) for r in dens)
    # One point should influence multiple cells
    assert total > 1


def test_coverage_map_binary():
    pts = [(0.5, 0.5)]
    cov, _, _ = heatmap.coverage_map(pts, bins=3, bounds=(0, 0, 1, 1), radius=1)
    flat = [c for row in cov for c in row]
    assert all(v in (0, 1) for v in flat)
    assert sum(flat) > 1
