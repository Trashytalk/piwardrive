import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config


def setup_tmp(tmp_path: Path) -> Path:
    config.CONFIG_DIR = str(tmp_path)
    config.CONFIG_PATH = str(tmp_path / "config.json")
    config.PROFILES_DIR = str(tmp_path / "profiles")
    config.ACTIVE_PROFILE_FILE = str(tmp_path / "active_profile")
    return Path(config.CONFIG_PATH)


def test_config_mtime_updates(tmp_path: Path) -> None:
    path = setup_tmp(tmp_path)
    cfg = config.Config(theme="Dark")
    config.save_config(cfg)
    first = config.config_mtime()
    cfg.theme = "Green"
    config.save_config(cfg)
    second = config.config_mtime()
    assert first is not None and second is not None
    assert second >= first
