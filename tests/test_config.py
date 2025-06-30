"""Tests for the configuration module."""

import builtins
import json
import os
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from piwardrive import config  # noqa: E402


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
    assert data.disable_scanning == config.DEFAULT_CONFIG.disable_scanning
    assert data.map_auto_prefetch == config.DEFAULT_CONFIG.map_auto_prefetch
    assert data.ui_font_size == config.DEFAULT_CONFIG.ui_font_size
    assert data.map_cluster_capacity == config.DEFAULT_CONFIG.map_cluster_capacity
    assert data.route_prefetch_interval == config.DEFAULT_CONFIG.route_prefetch_interval
    assert (
        data.route_prefetch_lookahead == config.DEFAULT_CONFIG.route_prefetch_lookahead
    )


def test_save_and_load_roundtrip(tmp_path: Path) -> None:
    cfg_file = setup_temp_config(tmp_path)
    orig = config.load_config()
    orig.theme = "Light"
    orig.map_poll_gps = 5
    orig.map_poll_gps_max = 20
    orig.map_poll_bt = 30
    orig.map_show_bt = True
    orig.ui_font_size = 18
    orig.offline_tile_path = str(tmp_path / "off.mbtiles")
    orig.disable_scanning = True
    orig.map_auto_prefetch = True
    orig.map_cluster_capacity = 12
    orig.route_prefetch_interval = 123
    orig.route_prefetch_lookahead = 7
    config.save_config(orig)
    assert Path(cfg_file).is_file()
    loaded = config.load_config()
    assert loaded.theme == "Light"
    assert loaded.map_poll_gps == 5
    assert loaded.map_poll_gps_max == 20
    assert loaded.map_poll_bt == 30
    assert loaded.map_show_bt is True
    assert loaded.offline_tile_path == str(tmp_path / "off.mbtiles")
    assert loaded.disable_scanning is True
    assert loaded.map_auto_prefetch is True
    assert loaded.ui_font_size == 18
    assert loaded.map_cluster_capacity == 12
    assert loaded.route_prefetch_interval == 123
    assert loaded.route_prefetch_lookahead == 7


def test_save_config_dataclass_roundtrip(tmp_path: Path) -> None:
    cfg_file = setup_temp_config(tmp_path)
    cfg = config.Config(theme="Light", ui_font_size=20)
    config.save_config(cfg)
    assert Path(cfg_file).is_file()
    loaded = config.load_config()
    assert loaded.theme == "Light"
    assert loaded.ui_font_size == 20


def test_save_config_no_temp_files(tmp_path: Path) -> None:
    cfg_file = setup_temp_config(tmp_path)
    cfg = config.Config(theme="Temp")
    config.save_config(cfg)
    files = sorted(p.name for p in tmp_path.iterdir())
    assert files == [cfg_file.name]


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


def test_load_config_invalid_json_monkeypatch(monkeypatch: Any, tmp_path: Path) -> None:
    cfg_file = tmp_path / "config.json"
    cfg_file.write_text("{invalid}")
    monkeypatch.setattr(config, "CONFIG_PATH", str(cfg_file))
    import piwardrive.core.config as core

    monkeypatch.setattr(core, "CONFIG_PATH", str(cfg_file))
    data = config.load_config()
    assert asdict(data) == asdict(config.DEFAULT_CONFIG)


def test_save_config_validation_error(tmp_path: Path) -> None:
    setup_temp_config(tmp_path)
    cfg = config.Config(map_poll_gps=0)
    with pytest.raises(ValidationError):
        config.save_config(cfg)


def test_env_override_integer(monkeypatch: Any, tmp_path: Path) -> None:
    setup_temp_config(tmp_path)
    monkeypatch.setenv("PW_MAP_POLL_GPS", "42")
    monkeypatch.setenv("PW_MAP_POLL_GPS_MAX", "50")
    monkeypatch.setenv("PW_MAP_POLL_BT", "30")
    monkeypatch.setenv("PW_UI_FONT_SIZE", "22")
    monkeypatch.setenv("PW_MAP_CLUSTER_CAPACITY", "15")
    monkeypatch.setenv("PW_GPS_MOVEMENT_THRESHOLD", "2.5")
    cfg = config.AppConfig.load()
    assert cfg.map_poll_gps == 42
    assert cfg.map_poll_gps_max == 50
    assert cfg.map_poll_bt == 30
    assert cfg.ui_font_size == 22
    assert cfg.map_cluster_capacity == 15
    assert cfg.gps_movement_threshold == 2.5


def test_env_override_boolean(monkeypatch: Any, tmp_path: Path) -> None:
    setup_temp_config(tmp_path)
    monkeypatch.setenv("PW_MAP_SHOW_GPS", "false")
    monkeypatch.setenv("PW_MAP_SHOW_BT", "true")
    monkeypatch.setenv("PW_MAP_AUTO_PREFETCH", "1")
    cfg = config.AppConfig.load()
    assert cfg.map_show_gps is False
    assert cfg.map_show_bt is True
    assert cfg.map_auto_prefetch is True


def test_env_override_health_poll(monkeypatch: Any, tmp_path: Path) -> None:
    setup_temp_config(tmp_path)
    monkeypatch.setenv("PW_HEALTH_POLL_INTERVAL", "5")
    cfg = config.AppConfig.load()
    assert cfg.health_poll_interval == 5


def test_env_override_route_prefetch(monkeypatch: Any, tmp_path: Path) -> None:
    setup_temp_config(tmp_path)
    monkeypatch.setenv("PW_ROUTE_PREFETCH_INTERVAL", "120")
    monkeypatch.setenv("PW_ROUTE_PREFETCH_LOOKAHEAD", "4")
    cfg = config.AppConfig.load()
    assert cfg.route_prefetch_interval == 120
    assert cfg.route_prefetch_lookahead == 4


def test_env_override_battery_widget(monkeypatch: Any, tmp_path: Path) -> None:
    setup_temp_config(tmp_path)
    monkeypatch.setenv("PW_WIDGET_BATTERY_STATUS", "true")
    cfg = config.AppConfig.load()
    assert cfg.widget_battery_status is True


def test_list_env_overrides() -> None:
    mapping = config.list_env_overrides()
    assert mapping["PW_UI_FONT_SIZE"] == "ui_font_size"


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
    cfg = config.Config(theme="Green")
    config.save_config(cfg, profile="alt")
    path = Path(config.PROFILES_DIR) / "alt.json"
    assert path.is_file()
    config.set_active_profile("alt")
    loaded = config.load_config()
    assert loaded.theme == "Green"
    assert "alt" in config.list_profiles()


def test_import_export_profile(tmp_path: Path) -> None:
    setup_temp_config(tmp_path)
    src = tmp_path / "src.json"
    src.write_text('{"theme": "Light"}')
    name = config.import_profile(str(src))
    assert name == "src"
    exported = tmp_path / "exp.json"
    config.export_profile(name, str(exported))
    assert exported.is_file()


def test_import_export_delete_profile(tmp_path: Path) -> None:
    setup_temp_config(tmp_path)
    src = tmp_path / "profile.json"
    src.write_text('{"theme": "Dark"}')
    name = config.import_profile(str(src))
    path = Path(config.PROFILES_DIR) / f"{name}.json"
    assert path.is_file()
    exported = tmp_path / "export.json"
    config.export_profile(name, str(exported))
    assert exported.is_file()
    config.delete_profile(name)
    assert not path.exists()


def test_import_profile_custom_name(tmp_path: Path) -> None:
    """import_profile stores data under the provided name."""
    setup_temp_config(tmp_path)
    src = tmp_path / "profile.json"
    src.write_text('{"theme": "Dark"}')
    import piwardrive.core.config as core

    # keep core config in sync with the wrapper for this test
    core.CONFIG_DIR = config.CONFIG_DIR
    core.CONFIG_PATH = config.CONFIG_PATH
    core.PROFILES_DIR = config.PROFILES_DIR
    core.ACTIVE_PROFILE_FILE = config.ACTIVE_PROFILE_FILE

    name = config.import_profile(str(src), name="custom")
    assert name == "custom"
    stored = Path(config.PROFILES_DIR) / "custom.json"
    assert stored.is_file()
    data = json.loads(stored.read_text())
    assert data["theme"] == "Dark"


def test_export_profile_content(tmp_path: Path) -> None:
    """export_profile writes the profile data verbatim."""
    setup_temp_config(tmp_path)
    import piwardrive.core.config as core

    # keep core config in sync with the wrapper for this test
    core.CONFIG_DIR = config.CONFIG_DIR
    core.CONFIG_PATH = config.CONFIG_PATH
    core.PROFILES_DIR = config.PROFILES_DIR
    core.ACTIVE_PROFILE_FILE = config.ACTIVE_PROFILE_FILE

    cfg = config.Config(theme="Green")
    config.save_config(cfg, profile="p1")
    dest = tmp_path / "out.json"
    config.export_profile("p1", str(dest))
    assert dest.is_file()
    exported = json.loads(dest.read_text())
    assert exported["theme"] == "Green"


def test_import_config_missing_yaml(tmp_path: Path, monkeypatch) -> None:
    """import_config raises ConfigError if PyYAML is missing."""
    file = tmp_path / "cfg.yaml"
    file.write_text("theme: Light\nremote_sync_url: http://localhost")

    orig_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "yaml":
            raise ModuleNotFoundError
        return orig_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    monkeypatch.setitem(sys.modules, "yaml", None)
    with pytest.raises(config.ConfigError, match="PyYAML required"):
        config.import_config(str(file))


def test_export_config_missing_yaml(tmp_path: Path, monkeypatch) -> None:
    """export_config raises ConfigError if PyYAML is missing."""
    cfg = config.Config(theme="Dark")
    dest = tmp_path / "out.yaml"

    orig_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "yaml":
            raise ModuleNotFoundError
        return orig_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    monkeypatch.setitem(sys.modules, "yaml", None)
    with pytest.raises(config.ConfigError, match="PyYAML required"):
        config.export_config(cfg, str(dest))


def test_save_load_webhooks(tmp_path: Path) -> None:
    cfg_file = setup_temp_config(tmp_path)
    cfg = config.load_config()
    cfg.notification_webhooks = ["http://x"]
    config.save_config(cfg)
    assert Path(cfg_file).is_file()
    loaded = config.load_config()
    assert loaded.notification_webhooks == ["http://x"]
