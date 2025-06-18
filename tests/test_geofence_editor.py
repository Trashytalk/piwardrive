import os
import sys
from types import ModuleType
from typing import Any

# Stub out heavy Kivy dependencies
modules = {
    "kivy.app": ModuleType("kivy.app"),
    "kivy.uix.screenmanager": ModuleType("kivy.uix.screenmanager"),
    "kivy.uix.boxlayout": ModuleType("kivy.uix.boxlayout"),
    "kivy.metrics": ModuleType("kivy.metrics"),
    "kivymd.uix.button": ModuleType("kivymd.uix.button"),
    "kivy_garden.mapview": ModuleType("kivy_garden.mapview"),
    "pydantic": ModuleType("pydantic"),
}
modules["kivy.app"].App = type("App", (), {"get_running_app": staticmethod(lambda: None)})
modules["kivy.uix.screenmanager"].Screen = type("Screen", (), {"add_widget": lambda self, *a, **k: None})
modules["kivy.metrics"].dp = lambda x: x
class DummyButton:
    def __init__(self, *a: Any, **k: Any) -> None:
        pass

modules["kivymd.uix.button"].MDFlatButton = DummyButton

class DummyMapView:
    def __init__(self, *a: Any, **k: Any) -> None:
        self._layers = []

    def bind(self, **kwargs: Any) -> None:
        pass

    def add_layer(self, layer: Any) -> None:
        self._layers.append(layer)

    def remove_layer(self, layer: Any) -> None:
        if layer in self._layers:
            self._layers.remove(layer)

modules["kivy_garden.mapview"].MapView = DummyMapView
modules["kivy_garden.mapview"].LineMapLayer = object
class DummyBoxLayout:
    def __init__(self, *a: Any, **k: Any) -> None:
        pass

    def add_widget(self, *a: Any, **k: Any) -> None:
        pass

modules["kivy.uix.boxlayout"].BoxLayout = DummyBoxLayout
modules["pydantic"].BaseModel = object
modules["pydantic"].Field = lambda *a, **k: None
modules["pydantic"].ValidationError = Exception
modules["pydantic"].field_validator = lambda *a, **k: (lambda f: f)
for n, m in modules.items():
    sys.modules[n] = m


from piwardrive.screens.geofence_editor import GeofenceEditor  # noqa: E402


def test_editor_editing(tmp_path: Any) -> None:
    GeofenceEditor.GEOFENCE_FILE = str(tmp_path / "geofences.json")
    editor = GeofenceEditor()
    editor.polygons = [{"name": "zone", "points": [(0.0, 0.0), (1.0, 0.0)]}]
    editor.save_polygons()

    assert editor.rename_polygon("zone", "area") is True
    assert editor.polygons[0]["name"] == "area"

    assert editor.update_polygon("area", [(0, 0), (1, 0), (1, 1)]) is True
    assert editor.polygons[0]["points"] == [(0, 0), (1, 0), (1, 1)]

    assert editor.configure_alerts("area", "enter", "exit") is True
    assert editor.polygons[0]["enter_message"] == "enter"
    assert editor.polygons[0]["exit_message"] == "exit"

    assert editor.remove_polygon("area") is True
    assert editor.polygons == []
