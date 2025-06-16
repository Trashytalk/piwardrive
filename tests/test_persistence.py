import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config
import persistence
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
    state = persistence.AppState(last_screen="Stats", last_start="now", first_run=False)
    asyncio.run(persistence.save_app_state(state))
    loaded = asyncio.run(persistence.load_app_state())
    assert loaded.last_screen == "Stats"
    assert loaded.first_run is False


def test_custom_db_path(tmp_path: Path, monkeypatch: Any) -> None:
    setup_tmp(tmp_path)
    custom = tmp_path / "db" / "custom.db"
    monkeypatch.setenv("PW_DB_PATH", str(custom))
    rec = persistence.HealthRecord(
        timestamp="c",
        cpu_temp=2.0,
        cpu_percent=2.5,
        memory_percent=3.5,
        disk_percent=4.5,
    )
    asyncio.run(persistence.save_health_record(rec))
    assert custom.is_file()
    rows = asyncio.run(persistence.load_recent_health(1))
    assert rows and rows[0].cpu_temp == 2.0


def test_conn_closed_on_loop_switch(tmp_path: Path) -> None:
    setup_tmp(tmp_path)
    loop1 = asyncio.new_event_loop()
    conn1 = loop1.run_until_complete(persistence._get_conn())
    loop1.run_until_complete(conn1.execute("SELECT 1"))
    loop1.run_until_complete(loop1.shutdown_asyncgens())
    loop1.close()

    loop2 = asyncio.new_event_loop()
    conn2 = loop2.run_until_complete(persistence._get_conn())
    loop2.run_until_complete(conn2.execute("SELECT 1"))
    loop2.run_until_complete(loop2.shutdown_asyncgens())
    loop2.close()

    assert conn2 is not conn1
    assert conn1._connection is None


