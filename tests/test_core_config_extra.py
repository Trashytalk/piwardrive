import builtins
import sys
import pytest

from piwardrive.core import config


def test_env_override(monkeypatch):
    monkeypatch.setenv("PW_THEME", "Red")
    cfg = config.AppConfig.load()
    assert cfg.theme == "Red"


@pytest.mark.parametrize("ext", [".json", ".yaml"])
def test_export_import_roundtrip(tmp_path, ext):
    cfg = config.Config(**config.DEFAULTS)
    cfg.remote_sync_url = "http://localhost"
    path = tmp_path / f"cfg{ext}"
    config.export_config(cfg, str(path))
    loaded = config.import_config(str(path))
    assert loaded.theme == cfg.theme
    assert loaded.remote_sync_url == cfg.remote_sync_url


def test_export_invalid_extension(tmp_path):
    cfg = config.DEFAULT_CONFIG
    bad = tmp_path / "cfg.txt"
    with pytest.raises(ValueError):
        config.export_config(cfg, str(bad))


def test_import_config_missing_yaml(tmp_path, monkeypatch):
    """import_config raises RuntimeError if PyYAML is missing."""
    file = tmp_path / "cfg.yaml"
    file.write_text("theme: Dark\nremote_sync_url: http://localhost")

    orig_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "yaml":
            raise ModuleNotFoundError
        return orig_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    monkeypatch.setitem(sys.modules, "yaml", None)
    with pytest.raises(RuntimeError, match="PyYAML required"):
        config.import_config(str(file))


def test_export_config_missing_yaml(tmp_path, monkeypatch):
    """export_config raises RuntimeError if PyYAML is missing."""
    cfg = config.Config(**config.DEFAULTS)
    cfg.remote_sync_url = "http://localhost"
    dest = tmp_path / "out.yaml"

    orig_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "yaml":
            raise ModuleNotFoundError
        return orig_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    monkeypatch.setitem(sys.modules, "yaml", None)
    with pytest.raises(RuntimeError, match="PyYAML required"):
        config.export_config(cfg, str(dest))
