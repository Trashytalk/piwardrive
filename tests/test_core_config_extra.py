from piwardrive.core import config
import pytest


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
