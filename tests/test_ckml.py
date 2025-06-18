import os, sys
from piwardrive import ckml


def test_parse_coords_simple() -> None:
    coords = ckml.parse_coords("1,2 3,4")
    assert coords == [(2.0, 1.0), (4.0, 3.0)]


def test_parse_coords_with_altitude() -> None:
    coords = ckml.parse_coords("1,2,3 4,5,6")
    assert coords == [(2.0, 1.0), (5.0, 4.0)]


def test_parse_coords_negative() -> None:
    coords = ckml.parse_coords("-1,-2 -3,-4")
    assert coords == [(-2.0, -1.0), (-4.0, -3.0)]


def test_parse_coords_malformed_single_token() -> None:
    coords = ckml.parse_coords("foo")
    assert coords == [(0.0, 0.0)]


def test_parse_coords_mixed_valid_invalid() -> None:
    coords = ckml.parse_coords("1,2 foo 3,4")
    assert coords == [(2.0, 1.0), (0.0, 0.0), (4.0, 3.0)]
