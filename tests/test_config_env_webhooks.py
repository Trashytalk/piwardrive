from pathlib import Path

import pytest


def setup_tmp(tmp_path: Path) -> None:
    from piwardrive import config

    config.CONFIG_DIR = str(tmp_path)
    config.CONFIG_PATH = str(tmp_path / "config.json")
    config.PROFILES_DIR = str(tmp_path / "profiles")
    config.ACTIVE_PROFILE_FILE = str(tmp_path / "active_profile")
    Path(config.CONFIG_DIR).mkdir(parents=True, exist_ok=True)
    Path(config.CONFIG_PATH).write_text("{}")


def test_env_override_list(monkeypatch, tmp_path: Path) -> None:
    pytest.importorskip("pydantic")
    setup_tmp(tmp_path)
    monkeypatch.setenv("PW_NOTIFICATION_WEBHOOKS", '["http://a","http://b"]')
    from piwardrive import config

    cfg = config.AppConfig.load()
    assert cfg.notification_webhooks == ["http://a", "http://b"]  # nosec B101
