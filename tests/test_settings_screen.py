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
        self.map_poll_gps_max = 30
        self.map_poll_aps = 60
        self.map_poll_bt = 60
        self.map_show_gps = True
        self.map_show_aps = True
        self.map_show_bt = False
        self.map_cluster_aps = False
        self.map_cluster_capacity = 8
        self.debug_mode = False
        self.offline_tile_path = "/valid/tiles"
        self.map_use_offline = False
        self.health_poll_interval = 10
        self.log_rotate_interval = 3600
        self.log_rotate_archives = 3
        self.widget_battery_status = False
        self.ui_font_size = 16
        self.theme = "Dark"
        self.theme_cls = SimpleNamespace(theme_style="Dark")
        self.config_data = config.Config()


def make_screen(module: ModuleType, app: DummyApp) -> Any:
    screen = module.SettingsScreen()
    screen.kismet_field = SimpleNamespace(text=app.kismet_logdir)
    screen.bcap_field = SimpleNamespace(text=app.bettercap_caplet)
    screen.gps_poll_field = SimpleNamespace(text=str(app.map_poll_gps))
    screen.gps_poll_max_field = SimpleNamespace(text=str(app.map_poll_gps_max))
    screen.ap_poll_field = SimpleNamespace(text=str(app.map_poll_aps))
    screen.bt_poll_field = SimpleNamespace(text=str(app.map_poll_bt))
    screen.health_poll_field = SimpleNamespace(text=str(app.health_poll_interval))
    screen.log_rotate_field = SimpleNamespace(text=str(app.log_rotate_interval))
    screen.log_archives_field = SimpleNamespace(text=str(app.log_rotate_archives))
    screen.offline_path_field = SimpleNamespace(text=app.offline_tile_path)
    screen.offline_switch = SimpleNamespace(active=app.map_use_offline)
    screen.show_gps_switch = SimpleNamespace(active=app.map_show_gps)
    screen.show_aps_switch = SimpleNamespace(active=app.map_show_aps)
    screen.show_bt_switch = SimpleNamespace(active=app.map_show_bt)
    screen.cluster_switch = SimpleNamespace(active=app.map_cluster_aps)
    screen.cluster_capacity_field = SimpleNamespace(
        text=str(app.map_cluster_capacity)
    )
    screen.debug_switch = SimpleNamespace(active=app.debug_mode)
    screen.battery_switch = SimpleNamespace(active=app.widget_battery_status)
    screen.font_size_field = SimpleNamespace(text=str(app.ui_font_size))
    screen.theme_switch = SimpleNamespace(active=app.theme == "Dark")
    screen.theme_cls = SimpleNamespace(theme_style=app.theme)
    return screen


def test_save_settings_invalid_gps(monkeypatch: Any) -> None:
    module = load_screen(monkeypatch)
    app = DummyApp()
    monkeypatch.setattr(module.App, "get_running_app", lambda: app)
    screen = make_screen(module, app)
    screen.gps_poll_field.text = "-1"
    screen.gps_poll_max_field.text = "-5"
    errors = []
    monkeypatch.setattr(module, "report_error", lambda msg: errors.append(msg))
    monkeypatch.setattr(module.os.path, "exists", lambda p: True)
    screen.save_settings()
    assert errors and "GPS poll" in errors[0]
    assert app.map_poll_gps == 10
    assert app.map_poll_gps_max == 30


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


def test_save_settings_updates_multiple_fields(monkeypatch: Any) -> None:
    module = load_screen(monkeypatch)
    app = DummyApp()
    monkeypatch.setattr(module.App, "get_running_app", lambda: app)
    screen = make_screen(module, app)

    screen.ap_poll_field.text = "30"
    screen.bt_poll_field.text = "25"
    screen.health_poll_field.text = "15"
    screen.log_rotate_field.text = "1200"
    screen.log_archives_field.text = "5"
    screen.font_size_field.text = "18"
    screen.cluster_capacity_field.text = "12"
    screen.show_gps_switch.active = False
    screen.show_aps_switch.active = False
    screen.show_bt_switch.active = True
    screen.cluster_switch.active = True
    screen.debug_switch.active = True
    screen.battery_switch.active = True

    monkeypatch.setattr(module.os.path, "exists", lambda p: True)
    saved = {}

    def fake_save(cfg: config.Config) -> None:
        saved.update(cfg.__dict__)

    monkeypatch.setattr(module, "save_config", fake_save)

    screen.save_settings()

    assert app.map_poll_aps == 30
    assert app.map_poll_bt == 25
    assert app.health_poll_interval == 15
    assert app.log_rotate_interval == 1200
    assert app.log_rotate_archives == 5
    assert app.ui_font_size == 18
    assert app.map_show_gps is False
    assert app.map_show_aps is False
    assert app.map_show_bt is True
    assert app.map_cluster_aps is True
    assert app.map_cluster_capacity == 12
    assert app.debug_mode is True
    assert app.widget_battery_status is True
    assert saved
    assert saved.get("map_cluster_capacity") == 12


@pytest.mark.asyncio
async def test_export_logs_button(monkeypatch: Any) -> None:
    module = load_screen(monkeypatch)
    app = DummyApp()
    called = {}
    async def fake_export() -> str:
        called['ok'] = True
        return '/tmp/logs.txt'
    app.export_logs = fake_export
    monkeypatch.setattr(module.App, 'get_running_app', lambda: app)
    outputs = {}
    class DummySnackbar:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            outputs['text'] = kwargs.get('text') or (args[0] if args else '')
        def open(self) -> None:
            outputs['opened'] = True
    monkeypatch.setattr(module, 'Snackbar', DummySnackbar)
    screen = make_screen(module, app)
    await screen._export_logs()
    assert called.get('ok') is True
    assert outputs.get('opened') is True
