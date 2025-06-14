from unittest import mock
from types import SimpleNamespace, ModuleType
from typing import Any, cast
import os
import sys
import pytest

pytest.skip("GUI tests skipped in headless CI", allow_module_level=True)

os.environ.setdefault("KIVY_NO_ARGS", "1")
os.environ.setdefault("KIVY_WINDOW", "mock")

# Provide dummy mapview module to avoid heavy imports
dummy_mapview = ModuleType("kivy_garden.mapview")
dummy_mapview.MapMarker = object  # type: ignore[attr-defined]
dummy_mapview.MapMarkerPopup = object  # type: ignore[attr-defined]
dummy_mapview.MBTilesMapSource = object  # type: ignore[attr-defined]
dummy_mapview.LineMapLayer = object  # type: ignore[attr-defined]
sys.modules.setdefault("kivy_garden.mapview", dummy_mapview)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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

    def __init__(self) -> None:
        self.scheduler = DummyScheduler()


def test_on_enter_and_on_leave(monkeypatch: Any) -> None:
    app = DummyApp()
    monkeypatch.setattr(App, "get_running_app", lambda: app)
    screen = cast(Any, MapScreen())
    screen.ids = {"mapview": mock.Mock()}

    screen.on_enter()
    assert "map_gps" in app.scheduler.events
    assert "map_aps" in app.scheduler.events

    screen.on_leave()
    assert app.scheduler.events == {}
    assert screen._gps_event is None
    assert screen._aps_event is None
