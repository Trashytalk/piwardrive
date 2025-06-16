import os
import sys
import importlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_sigint_plugin_loaded(tmp_path, monkeypatch):
    plugin_dir = tmp_path / ".config" / "piwardrive" / "sigint_plugins"
    plugin_dir.mkdir(parents=True)
    plugin = plugin_dir / "example.py"
    plugin.write_text("def scan():\n    return [{'id': 1}]\n")

    monkeypatch.setenv("HOME", str(tmp_path))
    sys.modules.pop("sigint_suite", None)
    sys.modules.pop("sigint_suite.example", None)
    suite = importlib.import_module("sigint_suite")

    assert hasattr(suite, "example")
    assert suite.example.scan() == [{"id": 1}]


def test_sigint_plugin_error(tmp_path, monkeypatch):
    plugin_dir = tmp_path / ".config" / "piwardrive" / "sigint_plugins"
    plugin_dir.mkdir(parents=True)
    bad = plugin_dir / "bad.py"
    bad.write_text("raise Exception('boom')\n")

    monkeypatch.setenv("HOME", str(tmp_path))
    sys.modules.pop("sigint_suite", None)
    importlib.import_module("sigint_suite")

    assert not hasattr(sys.modules["sigint_suite"], "bad")


