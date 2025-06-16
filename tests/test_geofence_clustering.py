import os
import sys
from types import ModuleType, SimpleNamespace
from typing import Any

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

# Provide lightweight stubs for external dependencies
modules["persistence"] = ModuleType("persistence")
modules["persistence"].save_app_state = lambda *a, **k: None
modules["sigint_suite.models"] = ModuleType("sigint_suite.models")
modules["sigint_suite.models"].BluetoothDevice = object
modules["psutil"] = ModuleType("psutil")
modules["psutil"].net_io_counters = lambda *a, **k: SimpleNamespace()

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
_dummy_mapview = ModuleType("kivy_garden.mapview")
_dummy_mapview.MapMarker = object  # type: ignore[attr-defined]
_dummy_mapview.MapMarkerPopup = object  # type: ignore[attr-defined]
_dummy_mapview.MBTilesMapSource = object  # type: ignore[attr-defined]
_dummy_mapview.LineMapLayer = object  # type: ignore[attr-defined]
sys.modules["kivy_garden.mapview"] = _dummy_mapview

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if "screens.map_screen" in sys.modules:
    del sys.modules["screens.map_screen"]
from screens.map_screen import MapScreen  # noqa: E402


def make_screen() -> MapScreen:
    screen = MapScreen()
    return screen


def test_add_geofence_registers_polygon() -> None:
    screen = make_screen()
    poly = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0)]
    screen.add_geofence("home", poly)
    assert len(screen.geofences) == 1
    gf = screen.geofences[0]
    assert gf["name"] == "home"
    assert gf["polygon"] == poly
    assert gf["inside"] is False


def test_check_geofences_triggers_callbacks() -> None:
    screen = make_screen()
    square = [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)]
    events: list[str] = []

    def on_enter(name: str) -> None:
        events.append(f"enter:{name}")

    def on_exit(name: str) -> None:
        events.append(f"exit:{name}")

    screen.add_geofence("zone", square, on_enter=on_enter, on_exit=on_exit)

    screen._check_geofences(0.5, 0.5)
    assert events == ["enter:zone"]
    assert screen.geofences[0]["inside"] is True

    screen._check_geofences(0.5, 0.5)
    assert events == ["enter:zone"]  # still inside, no new event

    screen._check_geofences(1.5, 0.5)
    assert events == ["enter:zone", "exit:zone"]
    assert screen.geofences[0]["inside"] is False


def test_update_clusters_on_zoom_merges_markers(monkeypatch: Any) -> None:
    screen = make_screen()
    m1 = SimpleNamespace(lat=0.0, lon=0.0)
    m2 = SimpleNamespace(lat=0.01, lon=0.01)
    m3 = SimpleNamespace(lat=50.0, lon=50.0)
    screen.ap_markers = [m1, m2, m3]

    called = []
    monkeypatch.setattr(screen, "spiderfy_markers", lambda: called.append(True))
    screen.update_clusters_on_zoom(None, zoom=1)

    assert called
    assert pytest.approx(m1.lat, rel=1e-6) == 0.005
    assert pytest.approx(m1.lon, rel=1e-6) == 0.005
    assert m1.lat == m2.lat and m1.lon == m2.lon
    assert m3.lat == 50.0 and m3.lon == 50.0


def test_update_clusters_on_zoom_handles_adjacent_cells(monkeypatch: Any) -> None:
    screen = make_screen()
    screen._cluster_capacity = 4
    m1 = SimpleNamespace(lat=0.044, lon=0.0)
    m2 = SimpleNamespace(lat=0.09, lon=0.0)
    screen.ap_markers = [m1, m2]

    monkeypatch.setattr(screen, "spiderfy_markers", lambda: None)
    screen.update_clusters_on_zoom(None, zoom=10)

    assert pytest.approx(m1.lat, rel=1e-6) == pytest.approx(m2.lat, rel=1e-6)
    assert pytest.approx(m1.lon, rel=1e-6) == pytest.approx(m2.lon, rel=1e-6)


def test_spiderfy_markers_spreads_overlaps() -> None:
    screen = make_screen()
    m1 = SimpleNamespace(lat=1.0, lon=2.0)
    m2 = SimpleNamespace(lat=1.0, lon=2.0)
    m3 = SimpleNamespace(lat=1.0, lon=2.0)
    screen.ap_markers = [m1, m2, m3]

    screen.spiderfy_markers()
    coords = {(round(m.lat, 7), round(m.lon, 7)) for m in screen.ap_markers}
    assert len(coords) == 3

