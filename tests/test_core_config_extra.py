import builtins
import sys

import pytest

from piwardrive.core import config


def test_env_override(monkeypatch):
    monkeypatch.setenv("PW_HEALTH_POLL_INTERVAL", "5")
    cfg = config.AppConfig.load()
    assert cfg.health_poll_interval == 5


@pytest.mark.parametrize("ext", [".json", ".yaml"])
def test_export_import_roundtrip(tmp_path, ext):
    cfg = config.Config(**config.DEFAULTS)
    cfg.remote_sync_url = "http://localhost"
    path = tmp_path / f"cfg{ext}"
    config.export_config(cfg, str(path))
    loaded = config.import_config(str(path))
    assert loaded.remote_sync_url == cfg.remote_sync_url


def test_export_invalid_extension(tmp_path):
    cfg = config.DEFAULT_CONFIG
    bad = tmp_path / "cfg.txt"
    with pytest.raises(config.ConfigError):
        config.export_config(cfg, str(bad))


def test_yaml_export_import(tmp_path):
    cfg = config.Config(**config.DEFAULTS)
    cfg.remote_sync_url = "http://localhost"
    path = tmp_path / "cfg.yaml"
    config.export_config(cfg, str(path))
    loaded = config.import_config(str(path))
    assert loaded.remote_sync_url == cfg.remote_sync_url




def test_apply_env_overrides_remote_sync_url(monkeypatch):
    base = {"remote_sync_url": "http://old"}
    monkeypatch.setenv("PW_REMOTE_SYNC_URL", "http://example.com")
    result = config._apply_env_overrides(base)
    assert result["remote_sync_url"] == "http://example.com"


def test_apply_env_overrides_mysql(monkeypatch):
    base = {"mysql_host": "localhost"}
    monkeypatch.setenv("PW_MYSQL_HOST", "db.example.com")
    result = config._apply_env_overrides(base)
    assert result["mysql_host"] == "db.example.com"


@pytest.mark.parametrize(
    "raw,default,expected",
    [
        ("true", False, True),
        ("0", True, False),
        ("10", 5, 10),
        ("bad", 5, 5),
        ("3.2", 1.0, 3.2),
        ("oops", 1.0, 1.0),
        ("[1, 2]", [0], [1, 2]),
        ("oops", [0], [0]),
    ],
)
def test_parse_env_value(raw, default, expected):
    assert config._parse_env_value(raw, default) == expected


def test_list_profiles(tmp_path, monkeypatch):
    profiles = tmp_path / "profiles"
    profiles.mkdir()
    (profiles / "one.json").write_text("{}")
    (profiles / "two.json").write_text("{}")
    (profiles / "ignore.txt").write_text("")
    monkeypatch.setattr(config, "PROFILES_DIR", str(profiles))
    found = config.list_profiles()
    assert set(found) == {"one", "two"}


def test_switch_profile(tmp_path, monkeypatch):
    cfg_dir = tmp_path
    monkeypatch.setattr(config, "CONFIG_DIR", str(cfg_dir))
    monkeypatch.setattr(config, "ACTIVE_PROFILE_FILE", str(cfg_dir / "active_profile"))
    profiles = cfg_dir / "profiles"
    monkeypatch.setattr(config, "PROFILES_DIR", str(profiles))
    profiles.mkdir()
    cfg = config.Config(mysql_host="db")
    config.save_config(cfg, profile="p1")
    loaded = config.switch_profile("p1")
    assert loaded.mysql_host == "db"
    assert (cfg_dir / "active_profile").read_text() == "p1"


def test_import_config_missing_yaml(tmp_path, monkeypatch):
    """import_config raises ConfigError if PyYAML is missing."""
    file = tmp_path / "cfg.yaml"
    file.write_text("mysql_host: db\nremote_sync_url: http://localhost")

    orig_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "yaml":
            raise ModuleNotFoundError
        return orig_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    monkeypatch.setitem(sys.modules, "yaml", None)
    with pytest.raises(config.ConfigError, match="PyYAML required"):
        config.import_config(str(file))


def test_export_config_missing_yaml(tmp_path, monkeypatch):
    """export_config raises ConfigError if PyYAML is missing."""
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
    with pytest.raises(config.ConfigError, match="PyYAML required"):
        config.export_config(cfg, str(dest))


def test_env_override_webhooks(monkeypatch):
    monkeypatch.setenv("PW_NOTIFICATION_WEBHOOKS", '["http://h"]')
    cfg = config.AppConfig.load()
    assert cfg.notification_webhooks == ["http://h"]
