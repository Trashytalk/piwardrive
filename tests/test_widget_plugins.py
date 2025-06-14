import os
import sys
import importlib
from pathlib import Path
from types import ModuleType

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Provide dummy kivy modules
mods = {
    "kivy.uix.behaviors": ModuleType("kivy.uix.behaviors"),
    "kivymd.uix.boxlayout": ModuleType("kivymd.uix.boxlayout"),
}
mods["kivy.uix.behaviors"].DragBehavior = type("DragBehavior", (), {})
mods["kivymd.uix.boxlayout"].MDBoxLayout = type("MDBoxLayout", (), {})
for n, m in mods.items():
    sys.modules[n] = m


def test_plugin_discovery(tmp_path, monkeypatch):
    plugin_dir = tmp_path / ".config" / "piwardrive" / "plugins"
    plugin_dir.mkdir(parents=True)
    plugin_file = plugin_dir / "my_widget.py"
    plugin_file.write_text(
        "from widgets.base import DashboardWidget\n"
        "class ExtraWidget(DashboardWidget):\n"
        "    pass\n"
    )

    monkeypatch.setenv("HOME", str(tmp_path))
    sys.modules.pop("widgets", None)
    widgets = importlib.import_module("widgets")
    assert hasattr(widgets, "ExtraWidget")
    assert "ExtraWidget" in widgets.__all__

