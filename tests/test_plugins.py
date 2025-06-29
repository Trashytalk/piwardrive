import importlib
from pathlib import Path


def _setup_kivy(add_dummy_module):
    add_dummy_module(
        "requests",
        get=lambda *a, **k: None,
        Session=object,
        RequestException=Exception,
    )
    add_dummy_module("kivy.metrics", dp=lambda x: x)
    add_dummy_module("kivy.uix.behaviors", DragBehavior=type("DragBehavior", (), {}))
    add_dummy_module("kivymd.uix.boxlayout", MDBoxLayout=type("MDBoxLayout", (), {}))
    add_dummy_module(
        "kivymd.uix.card",
        MDCard=type(
            "MDCard",
            (),
            {"__init__": lambda self, **kw: None, "add_widget": lambda self, w: None},
        ),
    )
    add_dummy_module(
        "kivymd.uix.label",
        MDLabel=type("MDLabel", (), {"__init__": lambda self, **kw: None, "text": ""}),
    )
    import importlib
    import sys

    sys.modules.setdefault("widgets", importlib.import_module("piwardrive.widgets"))
    sys.modules["widgets.base"] = importlib.import_module("piwardrive.widgets.base")


def test_load_hello_plugin(tmp_path, monkeypatch, add_dummy_module):
    _setup_kivy(add_dummy_module)
    plugin_dir = tmp_path / ".config" / "piwardrive" / "plugins"
    plugin_dir.mkdir(parents=True)

    dest = plugin_dir / "hello_plugin.py"
    dest.write_text(
        """from datetime import datetime
from piwardrive.simpleui import Card as MDCard, Label as MDLabel, dp
from widgets.base import DashboardWidget


class HelloPluginWidget(DashboardWidget):
    update_interval = 5.0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.card = MDCard(orientation='vertical', padding=dp(8), radius=[8])
        self.label = MDLabel(text='Hello from plugin!', halign='center')
        self.card.add_widget(self.label)
        self.add_widget(self.card)
        self.update()

    def update(self):
        self.label.text = datetime.now().strftime('Hello %H:%M:%S')
"""
    )

    monkeypatch.setenv("HOME", str(tmp_path))
    import sys

    sys.modules.pop("piwardrive.widgets", None)
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    widgets = importlib.import_module("piwardrive.widgets")
    assert "HelloPluginWidget" in widgets.list_plugins()  # nosec B101
