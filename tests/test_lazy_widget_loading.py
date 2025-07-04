import importlib
import sys


def test_lazy_loading(tmp_path, monkeypatch):
    plugin_dir = tmp_path / ".config" / "piwardrive" / "plugins"
    plugin_dir.mkdir(parents=True)
    plugin_file = plugin_dir / "lazy.py"
    plugin_file.write_text(
        "from piwardrive.widgets.base import DashboardWidget\n"
        "loaded = True\n"
        "class Lazy(DashboardWidget):\n"
        "    pass\n"
    )

    monkeypatch.setenv("HOME", str(tmp_path))
    sys.modules.pop("piwardrive.widgets", None)
    widgets = importlib.import_module("piwardrive.widgets")
    assert "lazy" not in sys.modules
    assert "Lazy" in widgets.__all__
    _ = widgets.Lazy
    assert "lazy" in sys.modules
