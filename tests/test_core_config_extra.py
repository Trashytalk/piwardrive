import os
from piwardrive.core import config
import pytest


def test_env_override(monkeypatch):
    monkeypatch.setenv("PW_THEME", "Red")
    cfg = config.AppConfig.load()
    assert cfg.theme == "Red"


def test_yaml_export_import(tmp_path):
    cfg = config.Config(**config.DEFAULTS)
    cfg.remote_sync_url = "http://localhost"
    path = tmp_path / "cfg.yaml"
    config.export_config(cfg, str(path))
    loaded = config.import_config(str(path))
    assert loaded.theme == cfg.theme


def test_export_invalid_extension(tmp_path):
    cfg = config.DEFAULT_CONFIG
    bad = tmp_path / "cfg.txt"
    with pytest.raises(ValueError):
        config.export_config(cfg, str(bad))
