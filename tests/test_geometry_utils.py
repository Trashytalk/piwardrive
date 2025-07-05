import math

from piwardrive import utils
from piwardrive.core import utils as core_utils


def test_haversine_distance_zero():
    assert utils.haversine_distance((0.0, 0.0), (0.0, 0.0)) == 0.0


def test_haversine_distance_known():
    dist = utils.haversine_distance((0.0, 0.0), (0.0, 1.0))
    assert 111000 < dist < 112000


def test_polygon_area_triangle():
    triangle = [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0)]
    area = utils.polygon_area(triangle)
    # approximate area of right triangle with legs about 111km each -> ~6.17e9 m^2
    assert math.isclose(area, 0.5 * 111320**2, rel_tol=0.05)


def test_polygon_area_insufficient_points():
    assert utils.polygon_area([(0.0, 0.0), (1.0, 1.0)]) == 0.0


def test_parse_coord_text():
    coords = core_utils._parse_coord_text("1,2 3,4")
    assert coords == [(2.0, 1.0), (4.0, 3.0)]


def test_get_avg_rssi():
    aps = [{"signal_dbm": -50}, {"signal_dbm": -70}, {"signal_dbm": None}]
    avg = utils.get_avg_rssi(aps)
    assert math.isclose(avg, (-50 - 70) / 2)
