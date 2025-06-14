"""Tests for the configuration module."""

import json
import os
import json
import os
import sys
from pathlib import Path
from dataclasses import asdict
from typing import Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config


def setup_temp_config(tmp_path: Path) -> Path:
    config_path = tmp_path / "config.json"
    config.CONFIG_DIR = str(tmp_path)
    config.CONFIG_PATH = str(config_path)
    config.PROFILES_DIR = str(tmp_path / "profiles")
    config.ACTIVE_PROFILE_FILE = str(tmp_path / "active_profile")
    return config_path


def test_load_config_defaults_when_missing(tmp_path: Path) -> None:
    setup_temp_config(tmp_path)
    data = config.load_config()
    assert data.theme == config.DEFAULT_CONFIG.theme
    assert data.map_poll_gps == config.DEFAULT_CONFIG.map_poll_gps
    assert data.map_poll_gps_max == config.DEFAULT_CONFIG.map_poll_gps_max
    assert data.map_poll_bt == config.DEFAULT_CONFIG.map_poll_bt
    assert data.map_show_bt == config.DEFAULT_CONFIG.map_show_bt
    assert data.offline_tile_path == config.DEFAULT_CONFIG.offline_tile_path


def test_save_and_load_roundtrip(tmp_path: Path) -> None:
    cfg_file = setup_temp_config(tmp_path)
    orig = config.load_config()
    orig.theme = "Light"
    orig.map_poll_gps = 5
    orig.map_poll_gps_max = 20
    orig.map_poll_bt = 30
    orig.map_show_bt = True
    orig.offline_tile_path = "/tmp/off.mbtiles"
    config.save_config(orig)
    assert Path(cfg_file).is_file()
    loaded = config.load_config()
    assert loaded.theme == "Light"
    assert loaded.map_poll_gps == 5
    assert loaded.map_poll_gps_max == 20
    assert loaded.map_poll_bt == 30
    assert loaded.map_show_bt is True
    assert loaded.offline_tile_path == "/tmp/off.mbtiles"

def test_save_config_dataclass_roundtrip(tmp_path: Path) -> None:
    cfg_file = setup_temp_config(tmp_path)
    cfg = config.Config(theme="Light")
    config.save_config(cfg)
    assert Path(cfg_file).is_file()
    loaded = config.load_config()
    assert loaded.theme == "Light"
    

def test_load_config_bad_json(tmp_path: Path) -> None:
    cfg_file = setup_temp_config(tmp_path)
    cfg_file.write_text("not json")
    data = config.load_config()
    assert asdict(data) == asdict(config.DEFAULT_CONFIG)


def test_load_config_schema_violation(tmp_path: Path) -> None:
    cfg_file = setup_temp_config(tmp_path)
    cfg_file.write_text(json.dumps({"map_poll_gps": "oops"}))
    data = config.load_config()
    assert asdict(data) == asdict(config.DEFAULT_CONFIG)
    

def test_env_override_integer(monkeypatch: Any, tmp_path: Path) -> None:
    setup_temp_config(tmp_path)
    monkeypatch.setenv("PW_MAP_POLL_GPS", "42")
    monkeypatch.setenv("PW_MAP_POLL_GPS_MAX", "50")
    monkeypatch.setenv("PW_MAP_POLL_BT", "30")
    cfg = config.AppConfig.load()
    assert cfg.map_poll_gps == 42
    assert cfg.map_poll_gps_max == 50
    assert cfg.map_poll_bt == 30


def test_env_override_boolean(monkeypatch: Any, tmp_path: Path) -> None:
    setup_temp_config(tmp_path)
    monkeypatch.setenv("PW_MAP_SHOW_GPS", "false")
    monkeypatch.setenv("PW_MAP_SHOW_BT", "true")
    cfg = config.AppConfig.load()
    assert cfg.map_show_gps is False
    assert cfg.map_show_bt is True


def test_env_override_health_poll(monkeypatch: Any, tmp_path: Path) -> None:
    setup_temp_config(tmp_path)
    monkeypatch.setenv("PW_HEALTH_POLL_INTERVAL", "5")
    cfg = config.AppConfig.load()
    assert cfg.health_poll_interval == 5


def test_env_override_battery_widget(monkeypatch: Any, tmp_path: Path) -> None:
    setup_temp_config(tmp_path)
    monkeypatch.setenv("PW_WIDGET_BATTERY_STATUS", "true")
    cfg = config.AppConfig.load()
    assert cfg.widget_battery_status is True


def test_export_import_json(tmp_path: Path) -> None:
    cfg_file = tmp_path / "out.json"
    cfg = config.Config(theme="Green", map_poll_gps=7)
    config.export_config(cfg, str(cfg_file))
    assert cfg_file.is_file()
    loaded = config.import_config(str(cfg_file))
    assert loaded.theme == "Green"
    assert loaded.map_poll_gps == 7


def test_export_import_yaml(tmp_path: Path) -> None:
    cfg_file = tmp_path / "out.yaml"
    cfg = config.Config(theme="Red", map_poll_aps=30)
    config.export_config(cfg, str(cfg_file))
    assert cfg_file.is_file()
    loaded = config.import_config(str(cfg_file))
    assert loaded.theme == "Red"
    assert loaded.map_poll_aps == 30

def test_profile_roundtrip(tmp_path: Path) -> None:
    setup_temp_config(tmp_path)
    cfg = config.Config(theme="Alt")
    config.save_config(cfg, profile="alt")
    path = Path(config.PROFILES_DIR) / "alt.json"
    assert path.is_file()
    config.set_active_profile("alt")
    loaded = config.load_config()
    assert loaded.theme == "Alt"
    assert "alt" in config.list_profiles()


def test_import_export_profile(tmp_path: Path) -> None:
    setup_temp_config(tmp_path)
    src = tmp_path / "src.json"
    src.write_text('{"theme": "Imp"}')
    name = config.import_profile(str(src))
    assert name == "src"
    exported = tmp_path / "exp.json"
    config.export_profile(name, str(exported))
    assert exported.is_file()

