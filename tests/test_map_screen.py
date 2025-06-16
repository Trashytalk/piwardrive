from unittest import mock
from types import SimpleNamespace, ModuleType
from typing import Any, cast
import os
import sys
import pytest

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

modules["kivy.app"].App = type("App", (), {"get_running_app": staticmethod(lambda: None)})
modules["kivy.clock"].Clock = SimpleNamespace(create_trigger=lambda *a, **k: lambda *a2, **k2: None)
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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if "screens.map_screen" in sys.modules:
    del sys.modules["screens.map_screen"]
from screens.map_screen import MapScreen  # noqa: E402
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


    def __init__(self) -> None:
        self.scheduler = DummyScheduler()


def test_on_enter_and_on_leave(monkeypatch: Any) -> None:
    app = DummyApp()
    monkeypatch.setattr(App, "get_running_app", staticmethod(lambda: app))
    screen = cast(Any, MapScreen())
    screen.ids = SimpleNamespace(mapview=mock.Mock())

    screen.on_enter()
    assert "map_gps" in app.scheduler.events
    assert "map_aps" in app.scheduler.events

    screen.on_leave()
    assert app.scheduler.events == {}
    assert screen._gps_event is None
    assert screen._aps_event is None
