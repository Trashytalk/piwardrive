import importlib
import os
import sys
from types import SimpleNamespace, ModuleType
from typing import Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config


def load_screen(monkeypatch: Any) -> ModuleType:
    modules: dict[str, Any] = {
        "kivy.app": ModuleType("kivy.app"),
        "kivy.metrics": ModuleType("kivy.metrics"),
        "kivy.uix.screenmanager": ModuleType("kivy.uix.screenmanager"),
        "kivymd.uix.boxlayout": ModuleType("kivymd.uix.boxlayout"),
        "kivymd.uix.button": ModuleType("kivymd.uix.button"),
        "kivymd.uix.label": ModuleType("kivymd.uix.label"),
        "kivymd.uix.textfield": ModuleType("kivymd.uix.textfield"),
        "kivymd.uix.selectioncontrol": ModuleType("kivymd.uix.selectioncontrol"),
        "kivymd.uix.snackbar": ModuleType("kivymd.uix.snackbar"),
    }
    modules["kivy.app"].App = type(
        "App", (), {"get_running_app": staticmethod(lambda: None)}
    )
    modules["kivy.metrics"].dp = lambda x: x
    modules["kivy.uix.screenmanager"].Screen = object
    modules["kivymd.uix.boxlayout"].MDBoxLayout = object
    modules["kivymd.uix.button"].MDRaisedButton = object
    modules["kivymd.uix.label"].MDLabel = object
    modules["kivymd.uix.textfield"].MDTextField = object
    modules["kivymd.uix.selectioncontrol"].MDSwitch = object

    class DummySnackbar:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        def open(self) -> None:
            pass

    modules["kivymd.uix.snackbar"].Snackbar = DummySnackbar

    for name, mod in modules.items():
        monkeypatch.setitem(sys.modules, name, mod)

    if "screens.settings_screen" in sys.modules:
        monkeypatch.delitem(sys.modules, "screens.settings_screen", raising=False)
    return importlib.import_module("screens.settings_screen")


class DummyApp:
    def __init__(self) -> None:
        self.kismet_logdir = "/valid/kismet"
        self.bettercap_caplet = "/valid/caplet"
        self.map_poll_gps = 10
        self.offline_tile_path = "/valid/tiles"
        self.map_use_offline = False
        self.theme = "Dark"
        self.theme_cls = SimpleNamespace(theme_style="Dark")
        self.config_data = config.Config()


def make_screen(module: ModuleType, app: DummyApp) -> Any:
    screen = module.SettingsScreen()
    screen.kismet_field = SimpleNamespace(text=app.kismet_logdir)
    screen.bcap_field = SimpleNamespace(text=app.bettercap_caplet)
    screen.gps_poll_field = SimpleNamespace(text=str(app.map_poll_gps))
    screen.offline_path_field = SimpleNamespace(text=app.offline_tile_path)
    screen.offline_switch = SimpleNamespace(active=app.map_use_offline)
    screen.theme_switch = SimpleNamespace(active=app.theme == "Dark")
    screen.theme_cls = SimpleNamespace(theme_style=app.theme)
    return screen


def test_save_settings_invalid_gps(monkeypatch: Any) -> None:
    module = load_screen(monkeypatch)
    app = DummyApp()
    monkeypatch.setattr(module.App, "get_running_app", lambda: app)
    screen = make_screen(module, app)
    screen.gps_poll_field.text = "-1"
    errors = []
    monkeypatch.setattr(module, "report_error", lambda msg: errors.append(msg))
    monkeypatch.setattr(module.os.path, "exists", lambda p: True)
    screen.save_settings()
    assert errors and "GPS poll" in errors[0]
    assert app.map_poll_gps == 10


import pytest


@pytest.mark.parametrize(
    "field, attr",
    [
        ("kismet_field", "kismet_logdir"),
        ("bcap_field", "bettercap_caplet"),
        ("offline_path_field", "offline_tile_path"),
    ],
)
def test_save_settings_invalid_paths(monkeypatch: Any, field: str, attr: str) -> None:
    module = load_screen(monkeypatch)
    app = DummyApp()
    monkeypatch.setattr(module.App, "get_running_app", lambda: app)
    screen = make_screen(module, app)
    getattr(screen, field).text = "/invalid"
    errors = []
    monkeypatch.setattr(module, "report_error", lambda msg: errors.append(msg))

    def fake_exists(path: str) -> bool:
        return not path.startswith("/invalid")

    monkeypatch.setattr(module.os.path, "exists", fake_exists)
    screen.save_settings()
    assert errors
    assert getattr(app, attr) != "/invalid"
