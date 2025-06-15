import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from piwardrive import config
from piwardrive import persistence
import asyncio


def setup_tmp(tmp_path: Path) -> None:
    config.CONFIG_DIR = str(tmp_path)


def test_save_and_load_health_record(tmp_path: Path) -> None:
    setup_tmp(tmp_path)
    rec = persistence.HealthRecord(
        timestamp="t",
        cpu_temp=1.0,
        cpu_percent=2.0,
        memory_percent=3.0,
        disk_percent=4.0,
    )
    asyncio.run(persistence.save_health_record(rec))
    rows = asyncio.run(persistence.load_recent_health(1))
    assert rows and rows[0].cpu_temp == 1.0


def test_save_and_load_app_state(tmp_path: Path) -> None:
    setup_tmp(tmp_path)
    state = persistence.AppState(last_screen="Stats", last_start="now")
    asyncio.run(persistence.save_app_state(state))
    loaded = asyncio.run(persistence.load_app_state())
    assert loaded.last_screen == "Stats"
