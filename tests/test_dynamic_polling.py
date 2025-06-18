import os
import sys
import time
from types import ModuleType, SimpleNamespace

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

modules["kivy.app"].App = type(
    "App", (), {"get_running_app": staticmethod(lambda: None)}
)
modules["kivy.clock"].Clock = SimpleNamespace(
    create_trigger=lambda *a, **k: (lambda *a2, **k2: None),
    schedule_once=lambda cb, dt=0: cb(dt),
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

dummy_mapview = ModuleType("kivy_garden.mapview")
dummy_mapview.MapMarker = object
dummy_mapview.MapMarkerPopup = object
dummy_mapview.MBTilesMapSource = object
dummy_mapview.LineMapLayer = object
sys.modules["kivy_garden.mapview"] = dummy_mapview


if "piwardrive.screens.map_screen" in sys.modules:
    del sys.modules["piwardrive.screens.map_screen"]
from piwardrive.screens.map_screen import MapScreen  # noqa: E402
from kivy.app import App


class DummyScheduler:
    def __init__(self) -> None:
        self.events: dict[str, tuple[object, int]] = {}

    def schedule(self, name: str, callback: object, interval: int) -> None:
        self.events[name] = (callback, interval)


class DummyApp:
    map_poll_gps = 5
    map_poll_gps_max = 20
    gps_movement_threshold = 1.0
    map_follow_gps = True

    def __init__(self) -> None:
        self.scheduler = DummyScheduler()


@pytest.mark.parametrize(
    "moves,expected",
    [
        ([(0.0, 0.0), (0.0, 0.00005), (0.001, 0.00005)], [20, 20, 5]),
    ],
)
def test_dynamic_polling(monkeypatch, moves, expected):
    app = DummyApp()
    monkeypatch.setattr(App, "get_running_app", staticmethod(lambda: app))

    screen = MapScreen()

    times = iter([0.0, 10.0, 20.0])
    monkeypatch.setattr(time, "time", lambda: next(times))
    screen._gps_event = "gps"

    for pos, exp in zip(moves, expected):
        app.scheduler.events.clear()
        screen._adjust_gps_interval(*pos)
        assert screen._gps_interval == exp
        assert app.scheduler.events.get("gps", (None, exp))[1] == exp
