import json
import os
import sys
from pathlib import Path
from dataclasses import asdict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config


def setup_temp_config(tmp_path):
    config_path = tmp_path / "config.json"
    config.CONFIG_DIR = str(tmp_path)
    config.CONFIG_PATH = str(config_path)
    return config_path


def test_load_config_defaults_when_missing(tmp_path):
    setup_temp_config(tmp_path)
    data = config.load_config()
    assert data.theme == config.DEFAULT_CONFIG.theme
    assert data.map_poll_gps == config.DEFAULT_CONFIG.map_poll_gps
    assert data.offline_tile_path == config.DEFAULT_CONFIG.offline_tile_path


def test_save_and_load_roundtrip(tmp_path):
    cfg_file = setup_temp_config(tmp_path)
    orig = config.load_config()
    orig.theme = "Light"
    orig.map_poll_gps = 5
    orig.offline_tile_path = "/tmp/off.mbtiles"
    config.save_config(asdict(orig))
    assert Path(cfg_file).is_file()
    loaded = config.load_config()
    assert loaded.theme == "Light"
    assert loaded.map_poll_gps == 5
    assert loaded.offline_tile_path == "/tmp/off.mbtiles"

def test_load_config_bad_json(tmp_path):
    cfg_file = setup_temp_config(tmp_path)
    cfg_file.write_text("not json")
    data = config.load_config()
    assert asdict(data) == asdict(config.DEFAULT_CONFIG)


def test_env_override_integer(monkeypatch, tmp_path):
    setup_temp_config(tmp_path)
    monkeypatch.setenv("PW_MAP_POLL_GPS", "42")
    cfg = config.AppConfig.load()
    assert cfg.map_poll_gps == 42


def test_env_override_boolean(monkeypatch, tmp_path):
    setup_temp_config(tmp_path)
    monkeypatch.setenv("PW_MAP_SHOW_GPS", "false")
    cfg = config.AppConfig.load()
    assert cfg.map_show_gps is False
