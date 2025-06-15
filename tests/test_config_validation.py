import os
import sys
from pathlib import Path
import pytest
from pydantic import ValidationError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from piwardrive import config


def setup(tmp_path: Path) -> None:
    config.CONFIG_DIR = str(tmp_path)
    config.CONFIG_PATH = str(tmp_path / "config.json")


def test_invalid_env_value(monkeypatch, tmp_path: Path) -> None:
    setup(tmp_path)
    monkeypatch.setenv("PW_MAP_POLL_GPS", "0")
    with pytest.raises(ValidationError):
        config.AppConfig.load()


def test_invalid_theme(monkeypatch, tmp_path: Path) -> None:
    setup(tmp_path)
    monkeypatch.setenv("PW_THEME", "Blue")
    with pytest.raises(ValidationError):
        config.AppConfig.load()
