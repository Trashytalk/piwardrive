import importlib
from pathlib import Path


def _setup_env() -> None:
    import sys

    sys.modules.setdefault("widgets", importlib.import_module("piwardrive.widgets"))
    sys.modules["widgets.base"] = importlib.import_module("piwardrive.widgets.base")


def test_load_hello_plugin(tmp_path, monkeypatch):
    _setup_env()
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
    assert widgets.list_plugins() == []
