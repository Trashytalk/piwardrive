import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import heatmap


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
