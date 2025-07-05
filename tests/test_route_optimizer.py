import math

from piwardrive import route_optimizer  # noqa: E402


def test_suggest_route_empty_returns_empty() -> None:
    assert route_optimizer.suggest_route([]) == []


def test_suggest_route_unvisited_cells() -> None:
    points = [
        (0.0, 0.0),
        (0.0, 0.001),
        (0.0, 0.002),
    ]
    route = route_optimizer.suggest_route(
        points, cell_size=0.001, steps=2, search_radius=1
    )
    visited = {
        (math.floor(lat / 0.001), math.floor(lon / 0.001)) for lat, lon in points
    }
    assert len(route) <= 2
    for lat, lon in route:
        cell = (math.floor(lat / 0.001), math.floor(lon / 0.001))
        assert cell not in visited
