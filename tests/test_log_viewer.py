"""Tests for the log viewer widget."""

import os
import sys
from types import ModuleType, SimpleNamespace


modules = {
    "kivy": ModuleType("kivy"),
    "kivy.app": ModuleType("kivy.app"),
    "kivy.clock": ModuleType("kivy.clock"),
    "kivy.properties": ModuleType("kivy.properties"),
    "kivy.uix.label": ModuleType("kivy.uix.label"),
    "kivy.uix.scrollview": ModuleType("kivy.uix.scrollview"),
    "kivy.uix.behaviors": ModuleType("kivy.uix.behaviors"),
    "kivymd.uix.boxlayout": ModuleType("kivymd.uix.boxlayout"),
    "kivymd.uix.menu": ModuleType("kivymd.uix.menu"),
}


class _Property:
    def __init__(self, default=None):
        self.default = default

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, obj, owner=None):
        if obj is None:
            return self
        return getattr(obj, self.name, self.default)

    def __set__(self, obj, value):
        setattr(obj, self.name, value)


class _Widget:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def add_widget(self, _child):
        pass

    def bind(self, **kwargs):
        for attr, cb in kwargs.items():
            cb(self, getattr(self, attr, None))


class _Label(_Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = ""
        self.text_size = (0, 0)
        self.texture_size = [0, 0]


class _ScrollView(_Widget):
    width = 0
    scroll_y = 0.0


class DummyMenu:
    def __init__(self, **kwargs):
        DummyMenu.kwargs = kwargs

    def open(self):
        DummyMenu.opened = True

    def dismiss(self):
        DummyMenu.dismissed = True


modules["kivy.app"].App = type(
    "App", (), {"get_running_app": staticmethod(lambda: None)}
)
modules["kivy.clock"].Clock = SimpleNamespace(schedule_interval=lambda *a, **k: None)
modules["kivy.properties"].NumericProperty = _Property
modules["kivy.properties"].StringProperty = _Property
modules["kivy.uix.label"].Label = _Label
modules["kivy.uix.scrollview"].ScrollView = _ScrollView
modules["kivy.uix.behaviors"].DragBehavior = type("DragBehavior", (), {})
modules["kivymd.uix.boxlayout"].MDBoxLayout = object
modules["kivymd.uix.menu"].MDDropdownMenu = DummyMenu
modules["kivy"].__path__ = []
modules["kivy"].app = modules["kivy.app"]
modules["kivy"].clock = modules["kivy.clock"]

for name, mod in modules.items():
    sys.modules[name] = mod

os.environ.setdefault("KIVY_NO_ARGS", "1")
os.environ.setdefault("KIVY_WINDOW", "mock")
aiohttp_mod = ModuleType("aiohttp")
aiohttp_mod.ClientSession = object
aiohttp_mod.ClientTimeout = lambda *a, **k: None
aiohttp_mod.ClientError = Exception
sys.modules["aiohttp"] = aiohttp_mod
from typing import Any

from piwardrive.widgets.log_viewer import LogViewer


def test_log_viewer_filter_regex(tmp_path: Any) -> None:
    log = tmp_path / "log.txt"
    log.write_text("INFO ok\nERROR bad\nDEBUG meh\n")
    lv = LogViewer(log_path=str(log), max_lines=10, filter_regex="ERROR")
    lv._refresh(0)
    assert lv.label.text.strip() == "ERROR bad"


def test_log_viewer_no_filter(tmp_path: Any) -> None:
    log = tmp_path / "log.txt"
    log.write_text("A\nB\n")
    lv = LogViewer(log_path=str(log), max_lines=10)
    lv._refresh(0)
    assert lv.label.text.strip() == "A\nB"


def test_log_viewer_path_menu(monkeypatch: Any) -> None:
    app = SimpleNamespace(log_paths=["/a", "/b"])
    monkeypatch.setattr(
        "piwardrive.widgets.log_viewer.App.get_running_app", lambda: app
    )
    lv = LogViewer()
    lv.show_path_menu(None)
    items = DummyMenu.kwargs["items"]
    assert items[0]["text"] == "a"
    items[1]["on_release"]()
    assert lv.log_path == "/b"
