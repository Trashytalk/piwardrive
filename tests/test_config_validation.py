from pathlib import Path

import pytest
from pydantic import ValidationError

from piwardrive import config


def setup(tmp_path: Path) -> None:
    config.CONFIG_DIR = str(tmp_path)
    config.CONFIG_PATH = str(tmp_path / "config.json")


def test_invalid_env_value(monkeypatch, tmp_path: Path) -> None:
    setup(tmp_path)
    monkeypatch.setenv("PW_HEALTH_POLL_INTERVAL", "0")
    monkeypatch.setenv("PW_GPS_MOVEMENT_THRESHOLD", "-1")
    with pytest.raises(ValidationError):
        config.AppConfig.load()
