import os
import sys
import importlib
from types import ModuleType
from typing import Any

os.environ.setdefault("KIVY_NO_ARGS", "1")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


def load_screen(monkeypatch: Any):
    mods = {
        "kivy.app": ModuleType("kivy.app"),
        "kivy.clock": ModuleType("kivy.clock"),
        "kivy.metrics": ModuleType("kivy.metrics"),
        "kivy.uix.label": ModuleType("kivy.uix.label"),
        "kivy.uix.screenmanager": ModuleType("kivy.uix.screenmanager"),
        "kivy_garden.mapview": ModuleType("kivy_garden.mapview"),
        "kivymd.uix.dialog": ModuleType("kivymd.uix.dialog"),
        "kivymd.uix.menu": ModuleType("kivymd.uix.menu"),
        "kivymd.uix.snackbar": ModuleType("kivymd.uix.snackbar"),
        "kivymd.uix.textfield": ModuleType("kivymd.uix.textfield"),
        "aiohttp": ModuleType("aiohttp"),
    }
    mods["aiohttp"].ClientSession = object
    mods["kivy.app"].App = type("App", (), {"get_running_app": staticmethod(lambda: None)})
    mods["kivy.clock"].Clock = type("Clock", (), {"create_trigger": staticmethod(lambda *a, **k: lambda *a2, **k2: None)})
    mods["kivy.clock"].mainthread = lambda f: f
    mods["kivy.metrics"].dp = lambda x: x
    mods["kivy.uix.label"].Label = object
    mods["kivy.uix.screenmanager"].Screen = object
    for name in ["MapMarker", "MapMarkerPopup", "MBTilesMapSource", "LineMapLayer"]:
        setattr(mods["kivy_garden.mapview"], name, object)
    mods["kivymd.uix.dialog"].MDDialog = object
    mods["kivymd.uix.menu"].MDDropdownMenu = object
    mods["kivymd.uix.snackbar"].Snackbar = object
    mods["kivymd.uix.textfield"].MDTextField = object
    for n, m in mods.items():
        monkeypatch.setitem(sys.modules, n, m)
    if "piwardrive.screens.map_screen" in sys.modules:
        monkeypatch.delitem(sys.modules, "piwardrive.screens.map_screen")
    return importlib.import_module("piwardrive.screens.map_screen").MapScreen


def make_screen(MapScreen: Any) -> Any:
    screen = object.__new__(MapScreen)
    screen.geofences = []
    return screen


def test_geofence_enter_exit(monkeypatch: Any) -> None:
    MapScreen = load_screen(monkeypatch)
    screen = make_screen(MapScreen)
    polygon = [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)]
    events: list[str] = []
    screen.add_geofence(
        "zone",
        polygon,
        on_enter=lambda name: events.append(f"enter:{name}"),
        on_exit=lambda name: events.append(f"exit:{name}"),
    )

    screen._check_geofences(0.5, 0.5)
    assert events == ["enter:zone"]
    assert screen.geofences[0]["inside"] is True

    screen._check_geofences(1.5, 0.5)
    assert events == ["enter:zone", "exit:zone"]
    assert screen.geofences[0]["inside"] is False
