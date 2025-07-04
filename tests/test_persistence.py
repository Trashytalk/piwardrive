import asyncio
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from piwardrive import config, persistence


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


def test_save_and_load_dashboard_settings(tmp_path: Path) -> None:
    setup_tmp(tmp_path)
    settings = persistence.DashboardSettings(
        layout=[{"cls": "TestWidget", "pos": [1, 2]}],
        widgets=["TestWidget"],
    )
    asyncio.run(persistence.save_dashboard_settings(settings))
    loaded = asyncio.run(persistence.load_dashboard_settings())
    assert loaded.layout == settings.layout
    assert loaded.widgets == settings.widgets


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


def test_purge_old_health(tmp_path: Path) -> None:
    setup_tmp(tmp_path)
    now = datetime.now()
    old_time = (now - timedelta(days=5)).isoformat()
    new_time = now.isoformat()
    old_rec = persistence.HealthRecord(old_time, 1.0, 1.0, 1.0, 1.0)
    new_rec = persistence.HealthRecord(new_time, 2.0, 2.0, 2.0, 2.0)
    asyncio.run(persistence.save_health_record(old_rec))
    asyncio.run(persistence.save_health_record(new_rec))
    asyncio.run(persistence.purge_old_health(2))
    rows = asyncio.run(persistence.load_recent_health(10))
    assert len(rows) == 1
    assert rows[0].timestamp == new_time


def test_vacuum(tmp_path: Path) -> None:
    setup_tmp(tmp_path)
    old_time = (datetime.now() - timedelta(days=1)).isoformat()
    rec = persistence.HealthRecord(old_time, 1.0, 1.0, 1.0, 1.0)
    asyncio.run(persistence.save_health_record(rec))
    asyncio.run(persistence.purge_old_health(0))
    asyncio.run(persistence.vacuum())
    rows = asyncio.run(persistence.load_recent_health(10))
    assert rows == []


def test_conn_closed_on_loop_switch(tmp_path: Path) -> None:
    setup_tmp(tmp_path)
    loop1 = asyncio.new_event_loop()
    conn1 = loop1.run_until_complete(persistence._acquire_conn())
    loop1.run_until_complete(conn1.execute("SELECT 1"))
    loop1.run_until_complete(persistence._release_conn(conn1))
    loop1.run_until_complete(loop1.shutdown_asyncgens())
    loop1.close()

    loop2 = asyncio.new_event_loop()
    conn2 = loop2.run_until_complete(persistence._acquire_conn())
    loop2.run_until_complete(conn2.execute("SELECT 1"))
    loop2.run_until_complete(persistence._release_conn(conn2))
    loop2.run_until_complete(loop2.shutdown_asyncgens())
    loop2.close()

    assert conn2 is not conn1
    assert conn1._connection is None


def test_schema_version(tmp_path: Path) -> None:
    setup_tmp(tmp_path)
    asyncio.run(persistence.migrate())
    conn = asyncio.run(persistence._acquire_conn())
    cur = asyncio.run(conn.execute("SELECT version FROM schema_version"))
    row = asyncio.run(cur.fetchone())
    asyncio.run(persistence._release_conn(conn))
    assert row["version"] == persistence.LATEST_VERSION
