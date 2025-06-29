import importlib
import sys
from types import ModuleType


def test_widget_plugin_cache(tmp_path, monkeypatch):
    plugin_dir = tmp_path / ".config" / "piwardrive" / "plugins"
    plugin_dir.mkdir(parents=True)
    plugin_file = plugin_dir / "plug1.py"
    plugin_file.write_text(
        "from piwardrive.widgets.base import DashboardWidget\n"
        "class W1(DashboardWidget):\n"
        "    pass\n"
    )

    monkeypatch.setenv("HOME", str(tmp_path))
    mods = {
        "kivy.uix.behaviors": ModuleType("kivy.uix.behaviors"),
        "kivymd.uix.boxlayout": ModuleType("kivymd.uix.boxlayout"),
    }
    mods["kivy.uix.behaviors"].DragBehavior = type("DragBehavior", (), {})
    mods["kivymd.uix.boxlayout"].MDBoxLayout = type("MDBoxLayout", (), {})
    for n, m in mods.items():
        sys.modules[n] = m
    sys.modules.pop("piwardrive.widgets", None)
    widgets = importlib.import_module("piwardrive.widgets")

    call_count = 0
    orig_spec = importlib.util.spec_from_file_location

    def wrapped(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        return orig_spec(*args, **kwargs)

    monkeypatch.setattr(importlib.util, "spec_from_file_location", wrapped)
    widgets._load_plugins()
    assert call_count == 0

    widgets.clear_plugin_cache()
    plugin_file2 = plugin_dir / "plug2.py"
    plugin_file2.write_text(
        "from piwardrive.widgets.base import DashboardWidget\n"
        "class W2(DashboardWidget):\n"
        "    pass\n"
    )
    widgets._load_plugins()
    assert call_count > 0
    assert hasattr(widgets, "W2")
