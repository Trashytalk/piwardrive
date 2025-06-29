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

    src = (
        Path(__file__).resolve().parents[1] / "examples" / "plugins" / "hello_plugin.py"
    )
    dest = plugin_dir / "hello_plugin.py"
    dest.write_text(src.read_text())

    monkeypatch.setenv("HOME", str(tmp_path))
    import sys

    sys.modules.pop("piwardrive.widgets", None)
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    widgets = importlib.import_module("piwardrive.widgets")
    assert "HelloPluginWidget" in widgets.list_plugins()


def test_clear_plugin_cache_loads_new(tmp_path, monkeypatch, add_dummy_module):
    _setup_kivy(add_dummy_module)
    plugin_dir = tmp_path / ".config" / "piwardrive" / "plugins"
    plugin_dir.mkdir(parents=True)

    monkeypatch.setenv("HOME", str(tmp_path))
    import sys

    sys.modules.pop("piwardrive.widgets", None)
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    widgets = importlib.import_module("piwardrive.widgets")

    plugin_file = plugin_dir / "tmp_plugin.py"
    plugin_file.write_text(
        "from piwardrive.widgets.base import DashboardWidget\n"
        "class TmpPluginWidget(DashboardWidget):\n"
        "    pass\n"
    )

    widgets.clear_plugin_cache()
    assert "TmpPluginWidget" in widgets.list_plugins()
