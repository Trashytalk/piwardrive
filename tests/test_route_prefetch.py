import os
import sys
from types import SimpleNamespace

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import route_prefetch  # noqa: E402


class DummyScheduler:
    def __init__(self) -> None:
        self.scheduled: list[tuple[str, int]] = []

    def schedule(self, name: str, cb: any, interval: int) -> None:
        self.scheduled.append((name, interval))
        cb(0)

    def cancel(self, name: str) -> None:  # pragma: no cover - not used
        pass


class DummyMap:
    def __init__(self) -> None:
        self.track_points = [(0.0, 0.0), (0.1, 0.1)]
        self.ids = SimpleNamespace(mapview=SimpleNamespace(zoom=16))
        self.called = False

    def prefetch_tiles(self, bbox, zoom=16, folder="/mnt/ssd/tiles") -> None:
        self.called = True
        self.bbox = bbox
        self.zoom = zoom
        self.folder = folder


def test_route_prefetcher_runs(monkeypatch):
    sched = DummyScheduler()
    m = DummyMap()
    monkeypatch.setattr(
        route_prefetch.App,
        "get_running_app",
        lambda: SimpleNamespace(offline_tile_path="/tiles/off.mbtiles"),
    )
    route_prefetch.RoutePrefetcher(sched, m, interval=1, lookahead=1)
    assert ("route_prefetch", 1) in sched.scheduled
    assert m.called
    assert m.zoom == 16
    assert m.folder.endswith("tiles")


def test_route_prefetcher_no_points(monkeypatch):
    sched = DummyScheduler()
    m = DummyMap()
    m.track_points = []
    monkeypatch.setattr(
        route_prefetch.App,
        "get_running_app",
        lambda: SimpleNamespace(offline_tile_path="/tiles/off.mbtiles"),
    )
    route_prefetch.RoutePrefetcher(sched, m, interval=1, lookahead=1)
    # callback executed but nothing prefetched
    assert ("route_prefetch", 1) in sched.scheduled
    assert not m.called
