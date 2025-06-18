from unittest import mock
from types import SimpleNamespace, ModuleType
from typing import Any, cast
import os
import sys
import pytest

sys.modules.setdefault('psutil', mock.Mock())

modules = {
    "kivy": ModuleType("kivy"),
    "kivy.app": ModuleType("kivy.app"),
    "kivy.clock": ModuleType("kivy.clock"),
    "kivy.metrics": ModuleType("kivy.metrics"),
    "kivy.uix.label": ModuleType("kivy.uix.label"),
    "kivy.uix.screenmanager": ModuleType("kivy.uix.screenmanager"),
    "kivy.animation": ModuleType("kivy.animation"),
    "kivymd.uix.dialog": ModuleType("kivymd.uix.dialog"),
    "kivymd.uix.menu": ModuleType("kivymd.uix.menu"),
    "kivymd.uix.snackbar": ModuleType("kivymd.uix.snackbar"),
    "kivymd.uix.textfield": ModuleType("kivymd.uix.textfield"),
    "kivymd.uix.progressbar": ModuleType("kivymd.uix.progressbar"),
    "kivymd.uix.boxlayout": ModuleType("kivymd.uix.boxlayout"),
    "kivymd.uix.label": ModuleType("kivymd.uix.label"),
    "gps": ModuleType("gps"),
}
modules["kivy.animation"].Animation = object

aiohttp_mod = ModuleType("aiohttp")
aiohttp_mod.ClientSession = object
aiohttp_mod.ClientTimeout = lambda *a, **k: None
aiohttp_mod.ClientError = Exception
sys.modules["aiohttp"] = aiohttp_mod

modules["kivy.app"].App = type(
    "App", (), {"get_running_app": staticmethod(lambda: None)}
)
modules["kivy.clock"].Clock = SimpleNamespace(
    create_trigger=lambda *a, **k: lambda *a2, **k2: None
)
modules["kivy.clock"].mainthread = lambda f: f
modules["kivy.metrics"].dp = lambda x: x
modules["kivy.uix.label"].Label = object
modules["kivy.uix.screenmanager"].Screen = object
modules["kivymd.uix.dialog"].MDDialog = object
modules["kivymd.uix.menu"].MDDropdownMenu = object
modules["kivymd.uix.snackbar"].Snackbar = object
modules["kivymd.uix.textfield"].MDTextField = object
modules["kivymd.uix.progressbar"].MDProgressBar = object
modules["kivymd.uix.boxlayout"].MDBoxLayout = object
modules["kivymd.uix.label"].MDLabel = object
modules["kivy"].__path__ = []
modules["kivy"].app = modules["kivy.app"]
modules["kivy"].clock = modules["kivy.clock"]

for name, mod in modules.items():
    sys.modules[name] = mod

os.environ.setdefault("KIVY_NO_ARGS", "1")
os.environ.setdefault("KIVY_WINDOW", "mock")

# Provide dummy mapview module to avoid heavy imports
dummy_mapview = ModuleType("kivy_garden.mapview")
dummy_mapview.MapMarker = object  # type: ignore[attr-defined]
dummy_mapview.MapMarkerPopup = object  # type: ignore[attr-defined]
dummy_mapview.MBTilesMapSource = object  # type: ignore[attr-defined]
dummy_mapview.LineMapLayer = object  # type: ignore[attr-defined]
sys.modules["kivy_garden.mapview"] = dummy_mapview


if "piwardrive.screens.map_screen" in sys.modules:
    del sys.modules["piwardrive.screens.map_screen"]
from piwardrive.screens.map_screen import MapScreen  # noqa: E402
from kivy.app import App


class DummyScheduler:
    def __init__(self) -> None:
        self.events: dict[str, tuple[Any, int]] = {}

    def schedule(self, name: str, callback: Any, interval: int) -> None:
        self.events[name] = (callback, interval)

    def cancel(self, name: str) -> None:
        self.events.pop(name, None)


class DummyApp:
    map_use_offline = False
    offline_tile_path = ""
    map_poll_gps = 1
    map_poll_aps = 2
    map_poll_bt = 3
    disable_scanning = False
    map_cluster_capacity = 8
    map_auto_prefetch = False
    map_follow_gps = True

    def __init__(self) -> None:
        self.scheduler = DummyScheduler()


def test_on_enter_and_on_leave(monkeypatch: Any) -> None:
    app = DummyApp()
    monkeypatch.setattr(App, "get_running_app", staticmethod(lambda: app))
    screen = cast(Any, MapScreen())
    ids = SimpleNamespace(mapview=mock.Mock())
    ids.get = lambda k, d=None: getattr(ids, k, d)  # type: ignore[attr-defined]
    screen.ids = ids

    screen.on_enter()
    assert "map_gps" in app.scheduler.events
    assert "map_aps" in app.scheduler.events

    screen.on_leave()
    assert app.scheduler.events == {}
    assert screen._gps_event is None
    assert screen._aps_event is None


def test_auto_prefetch(monkeypatch: Any) -> None:
    app = DummyApp()
    app.map_use_offline = True
    app.map_auto_prefetch = True
    app.offline_tile_path = "/tiles/offline.mbtiles"
    monkeypatch.setattr(App, "get_running_app", staticmethod(lambda: app))
    mv = SimpleNamespace(
        center_on=lambda *a, **k: None,
        zoom=16,
        remove_layer=lambda *a, **k: None,
        add_layer=lambda *a, **k: None,
    )
    screen = cast(Any, MapScreen())
    screen.ids = SimpleNamespace(mapview=mv)
    called = {}

    def fake_prefetch(bounds, zoom=16, folder="/mnt/ssd/tiles", **_):
        called["bounds"] = bounds
        called["zoom"] = zoom
        called["folder"] = folder

    monkeypatch.setattr(screen, "prefetch_tiles", fake_prefetch)
    screen._update_map(1.0, 2.0)
    assert called["folder"].endswith("/tiles")
    assert called["zoom"] == 16
    
    
def test_update_orientation(monkeypatch: Any) -> None:
    app = DummyApp()
    monkeypatch.setattr(App, "get_running_app", staticmethod(lambda: app))
    screen = cast(Any, MapScreen())
    mv = mock.Mock()
    ids2 = SimpleNamespace(mapview=mv)
    ids2.get = lambda k, d=None: getattr(ids2, k, d)  # type: ignore[attr-defined]
    screen.ids = ids2

    screen.update_orientation("left-up")
    assert mv.rotation == -270.0
    screen.update_orientation(None, {"x": 1}, {"z": 2})
    assert hasattr(screen, "sensor_accel")
    assert hasattr(screen, "sensor_gyro")

