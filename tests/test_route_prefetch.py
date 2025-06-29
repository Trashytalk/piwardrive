import sys
from types import SimpleNamespace

# lightweight scheduler and utils modules for import
def _haversine(a, b):
    import math

    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dphi = lat2 - lat1
    dl = lon2 - lon1
    aa = (
        math.sin(dphi / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dl / 2) ** 2
    )
    return 6371000 * 2 * math.atan2(math.sqrt(aa), math.sqrt(1 - aa))


sys.modules["utils"] = SimpleNamespace(haversine_distance=_haversine)
from piwardrive import route_prefetch  # noqa: E402


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


def test_predict_points(monkeypatch):
    sched = DummyScheduler()
    m = DummyMap()
    monkeypatch.setattr(
        route_prefetch.App,
        "get_running_app",
        lambda: SimpleNamespace(offline_tile_path="/tiles/off.mbtiles"),
    )
    rp = route_prefetch.RoutePrefetcher(sched, m, interval=1, lookahead=1)
    pts = rp._predict_points()
    assert pts
    lat, lon = pts[0]
    assert lat == pytest.approx(0.2, rel=1e-3)
    assert lon == pytest.approx(0.2, rel=1e-3)
