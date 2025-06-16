import os
import sys
import importlib
from types import ModuleType
from typing import Any

os.environ.setdefault("KIVY_NO_ARGS", "1")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def load_screen(monkeypatch: Any):
    mods = {
        "kivy.app": ModuleType("kivy.app"),
        "kivy.clock": ModuleType("kivy.clock"),
        "kivy.metrics": ModuleType("kivy.metrics"),
        "kivy.uix.label": ModuleType("kivy.uix.label"),
        "kivy.uix.screenmanager": ModuleType("kivy.uix.screenmanager"),
        "kivy.animation": ModuleType("kivy.animation"),
        "kivy_garden.mapview": ModuleType("kivy_garden.mapview"),
        "kivymd.uix.dialog": ModuleType("kivymd.uix.dialog"),
        "kivymd.uix.menu": ModuleType("kivymd.uix.menu"),
        "kivymd.uix.snackbar": ModuleType("kivymd.uix.snackbar"),
        "kivymd.uix.textfield": ModuleType("kivymd.uix.textfield"),
        "kivymd.uix.progressbar": ModuleType("kivymd.uix.progressbar"),
        "kivymd.uix.boxlayout": ModuleType("kivymd.uix.boxlayout"),
        "kivymd.uix.label": ModuleType("kivymd.uix.label"),
        "aiohttp": ModuleType("aiohttp"),
        "gps": ModuleType("gps"),
        "requests": ModuleType("requests"),
        "utils": ModuleType("utils"),
        "persistence": ModuleType("persistence"),
    }
    setattr(mods["aiohttp"], "ClientSession", object)
    setattr(mods["kivy.app"], "App", type("App", (), {"get_running_app": staticmethod(lambda: None)}))
    setattr(
        mods["kivy.clock"],
        "Clock",
        type("Clock", (), {"create_trigger": staticmethod(lambda *a, **k: lambda *a2, **k2: None)}),
    )
    setattr(mods["kivy.clock"], "mainthread", lambda f: f)
    setattr(mods["kivy.metrics"], "dp", lambda x: x)
    setattr(mods["kivy.uix.label"], "Label", object)
    setattr(mods["kivy.uix.screenmanager"], "Screen", object)
    setattr(mods["kivy.animation"], "Animation", object)
    for name in ["MapMarker", "MapMarkerPopup", "MBTilesMapSource", "LineMapLayer"]:
        setattr(mods["kivy_garden.mapview"], name, object)
    setattr(mods["kivymd.uix.dialog"], "MDDialog", object)
    setattr(mods["kivymd.uix.menu"], "MDDropdownMenu", object)
    setattr(mods["kivymd.uix.snackbar"], "Snackbar", object)
    setattr(mods["kivymd.uix.textfield"], "MDTextField", object)
    setattr(mods["kivymd.uix.progressbar"], "MDProgressBar", object)
    setattr(mods["kivymd.uix.boxlayout"], "MDBoxLayout", object)
    setattr(mods["kivymd.uix.label"], "MDLabel", object)
    setattr(mods["utils"], "haversine_distance", lambda *a, **k: 0.0)
    setattr(mods["utils"], "polygon_area", lambda *a, **k: 0.0)
    setattr(mods["utils"], "load_kml", lambda *a, **k: [])
    setattr(mods["utils"], "point_in_polygon", lambda p, poly: (
        poly[0][0] <= p[0] <= poly[2][0] and poly[0][1] <= p[1] <= poly[2][1]
    ))
    setattr(mods["utils"], "report_error", lambda msg: None)
    setattr(mods["persistence"], "save_app_state", lambda *a, **k: None)
    for n, m in mods.items():
        monkeypatch.setitem(sys.modules, n, m)
    if "screens.map_screen" in sys.modules:
        monkeypatch.delitem(sys.modules, "screens.map_screen")
    return importlib.import_module("screens.map_screen").MapScreen


def make_screen(MapScreen: Any) -> Any:
    screen = object.__new__(MapScreen)
    screen.geofences = []
    return screen


def test_geofence_enter_exit(monkeypatch: Any) -> None:
    class DummySnackbar:
        def __init__(self, *a: Any, **k: Any) -> None:
            pass

        def open(self) -> None:
            pass

    MapScreen = load_screen(monkeypatch)
    monkeypatch.setattr(sys.modules["screens.map_screen"], "Snackbar", DummySnackbar, raising=False)
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

def test_add_geofence_string_callbacks(monkeypatch: Any) -> None:
    calls: list[str] = []

    class DummySnackbar:
        def __init__(self, text: str) -> None:
            calls.append(text)

        def open(self) -> None:
            calls.append("open")

    MapScreen = load_screen(monkeypatch)
    monkeypatch.setattr(sys.modules["screens.map_screen"], "Snackbar", DummySnackbar, raising=False)
    screen = make_screen(MapScreen)

    polygon = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)]
    screen.add_geofence("zone", polygon, on_enter="enter {name}", on_exit="exit {name}")
    assert len(screen.geofences) == 1

    screen.geofences[0]["on_enter"]("zone")
    screen.geofences[0]["on_exit"]("zone")
    assert calls == ["enter zone", "open", "exit zone", "open"]
