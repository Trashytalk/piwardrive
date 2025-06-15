import os
import sys
import importlib
from types import ModuleType
from typing import Any

os.environ.setdefault("KIVY_NO_ARGS", "1")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


def load_screen(monkeypatch: Any):
    modules = {
        "kivy.app": ModuleType("kivy.app"),
        "kivy.uix.floatlayout": ModuleType("kivy.uix.floatlayout"),
        "kivy.uix.screenmanager": ModuleType("kivy.uix.screenmanager"),
    }
    modules["kivy.app"].App = type("App", (), {"get_running_app": staticmethod(lambda: None)})

    class DummyLayout:
        def __init__(self) -> None:
            self.children: list[Any] = []
        def add_widget(self, w: Any) -> None:
            self.children.append(w)
    modules["kivy.uix.floatlayout"].FloatLayout = DummyLayout
    modules["kivy.uix.screenmanager"].Screen = object

    widgets_mod = ModuleType("widgets")
    class BaseWidget:
        def __init__(self) -> None:
            self.pos = (0, 0)
    for name in [
        "SignalStrengthWidget",
        "GPSStatusWidget",
        "HandshakeCounterWidget",
        "ServiceStatusWidget",
        "StorageUsageWidget",
        "HealthStatusWidget",
        "DiskUsageTrendWidget",
        "CPUTempGraphWidget",
        "NetworkThroughputWidget",
        "BatteryStatusWidget",
        "HealthAnalysisWidget",
    ]:
        setattr(widgets_mod, name, type(name, (BaseWidget,), {}))

    for n, m in {**modules, "widgets": widgets_mod}.items():
        monkeypatch.setitem(sys.modules, n, m)
    if "piwardrive.screens.dashboard_screen" in sys.modules:
        monkeypatch.delitem(sys.modules, "piwardrive.screens.dashboard_screen")
    DashboardScreen = importlib.import_module("piwardrive.screens.dashboard_screen").DashboardScreen
    return DashboardScreen, widgets_mod, modules["kivy.uix.floatlayout"].FloatLayout


class DummyScheduler:
    def __init__(self) -> None:
        self.registered: list[Any] = []
    def register_widget(self, w: Any) -> None:
        self.registered.append(w)
    def cancel_all(self) -> None:
        pass

class DummyApp:
    def __init__(self) -> None:
        self.scheduler = DummyScheduler()
        self.dashboard_layout: list[dict[str, Any]] | None = None


def make_screen(cls: Any, app: DummyApp, layout_cls: Any) -> Any:
    screen = object.__new__(cls)
    screen.layout = layout_cls()
    sys.modules["kivy.app"].App.get_running_app = staticmethod(lambda: app)
    return screen


def test_save_and_load_layout(monkeypatch: Any) -> None:
    DashboardScreen, widgets_mod, layout_cls = load_screen(monkeypatch)
    app = DummyApp()
    screen = make_screen(DashboardScreen, app, layout_cls)
    w1 = widgets_mod.SignalStrengthWidget(); w1.pos = (1, 2)
    w2 = widgets_mod.GPSStatusWidget(); w2.pos = (3, 4)
    screen.layout.children = [w1, w2]

    screen.save_layout()
    assert app.dashboard_layout == [
        {"cls": "SignalStrengthWidget", "pos": (1, 2)},
        {"cls": "GPSStatusWidget", "pos": (3, 4)},
    ]

    screen2 = make_screen(DashboardScreen, app, layout_cls)
    screen2.load_widgets()

    names = {child.__class__.__name__: child.pos for child in screen2.layout.children}
    assert names == {"SignalStrengthWidget": (1, 2), "GPSStatusWidget": (3, 4)}
    assert screen2.layout.children == app.scheduler.registered

