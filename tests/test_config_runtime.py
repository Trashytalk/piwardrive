from pathlib import Path

from piwardrive import config


def setup_tmp(tmp_path: Path) -> Path:
    config.CONFIG_DIR = str(tmp_path)
    config.CONFIG_PATH = str(tmp_path / "config.json")
    config.PROFILES_DIR = str(tmp_path / "profiles")
    config.ACTIVE_PROFILE_FILE = str(tmp_path / "active_profile")
    return Path(config.CONFIG_PATH)


def test_config_mtime_updates(tmp_path: Path) -> None:
    setup_tmp(tmp_path)
    cfg = config.Config(theme="Dark")
    config.save_config(cfg)
    first = config.config_mtime()
    cfg.theme = "Green"
    config.save_config(cfg)
    second = config.config_mtime()
    assert first is not None and second is not None  # nosec B101
    assert second >= first  # nosec B101


def test_config_mtime_returns_timestamp(tmp_path: Path) -> None:
    path = setup_tmp(tmp_path)
    path.write_text("{}")
    expected = path.stat().st_mtime
    actual = config.config_mtime()
    assert actual is not None  # nosec B101
    assert abs(actual - expected) < 1e-3  # nosec B101


def test_config_mtime_missing(tmp_path: Path) -> None:
    """config_mtime returns None when the file does not exist."""
    setup_tmp(tmp_path)
    assert config.config_mtime() is None
