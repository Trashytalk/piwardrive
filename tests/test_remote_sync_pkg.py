import asyncio
import io
import json
import sys
from types import ModuleType

import pytest

# provide a minimal aiohttp stub before importing the module
aiohttp_mod = ModuleType("aiohttp")
aiohttp_mod.ClientSession = object  # type: ignore[attr-defined]
aiohttp_mod.ClientTimeout = lambda *a, **k: None  # type: ignore[attr-defined]
aiohttp_mod.ClientError = Exception  # type: ignore[attr-defined]
aiohttp_mod.FormData = lambda: type("FormData", (), {"add_field": lambda *a, **k: None})()  # type: ignore[attr-defined]
sys.modules.setdefault("aiohttp", aiohttp_mod)

import piwardrive.remote_sync as rs


class DummyResp:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    def raise_for_status(self):
        pass


class DummySession:
    def __init__(self, calls, should_fail=False):
        self.calls = calls
        self.should_fail = should_fail

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    def post(self, url, data=None):
        self.calls.append(url)
        if self.should_fail and len(self.calls) == 1:
            raise rs.aiohttp.ClientError("fail")
        return DummyResp()


def prepare(monkeypatch, calls, should_fail=False):
    monkeypatch.setattr(rs.os.path, "exists", lambda p: True)
    monkeypatch.setattr("builtins.open", lambda *_a, **_k: io.BytesIO(b"x"))
    monkeypatch.setattr(rs.aiohttp, "ClientTimeout", lambda *a, **k: None)
    monkeypatch.setattr(
        rs.aiohttp, "ClientSession", lambda *a, **k: DummySession(calls, should_fail)
    )


async def run_sync(monkeypatch, retries=2, should_fail=False):
    calls = []
    prepare(monkeypatch, calls, should_fail)
    sleeps = []

    async def fake_sleep(d):
        sleeps.append(d)

    monkeypatch.setattr(rs.asyncio, "sleep", fake_sleep)

    await rs.sync_database_to_server("db", "http://remote", retries=retries)
    return sleeps, calls


def test_sync_database_file_missing(tmp_path):
    missing = tmp_path / "missing.db"
    with pytest.raises(FileNotFoundError):
        asyncio.run(rs.sync_database_to_server(str(missing), "http://x"))


def test_sync_database_retry(monkeypatch):
    sleeps, calls = asyncio.run(run_sync(monkeypatch, should_fail=True))
    assert sleeps == [1.0]
    assert calls == ["http://remote", "http://remote"]


def test_sync_database_failure(monkeypatch):
    monkeypatch.setattr(rs.os.path, "exists", lambda p: True)
    monkeypatch.setattr("builtins.open", lambda *_a, **_k: io.BytesIO(b"x"))
    monkeypatch.setattr(rs.aiohttp, "ClientTimeout", lambda *a, **k: None)

    class FailSession(DummySession):
        def post(self, url, data=None):
            raise rs.aiohttp.ClientError("boom")

    monkeypatch.setattr(rs.aiohttp, "ClientSession", lambda *a, **_k: FailSession())

    async def fake_sleep(_):
        pass

    monkeypatch.setattr(rs.asyncio, "sleep", fake_sleep)

    with pytest.raises(rs.aiohttp.ClientError):
        asyncio.run(rs.sync_database_to_server("db", "http://remote", retries=1))


def _create_db(path: str) -> None:
    import sqlite3

    with sqlite3.connect(path) as db:
        db.execute(
            """CREATE TABLE health_records (
                timestamp TEXT PRIMARY KEY,
                cpu_temp REAL,
                cpu_percent REAL,
                memory_percent REAL,
                disk_percent REAL
            )"""
        )
        db.execute("INSERT INTO health_records VALUES ('t1', 1, 2, 3, 4)")
        db.execute("INSERT INTO health_records VALUES ('t2', 2, 3, 4, 5)")
        db.commit()


def test_sync_new_records(monkeypatch, tmp_path):
    db_path = tmp_path / "db.sqlite"
    _create_db(db_path)
    state_file = tmp_path / "state.json"

    calls = []

    async def fake_sync(path, url, *, timeout=30, retries=3, row_range=None):
        calls.append(row_range)

    monkeypatch.setattr(rs, "sync_database_to_server", fake_sync)

    count = asyncio.run(
        rs.sync_new_records(str(db_path), "http://x", state_file=str(state_file))
    )
    assert count == 2
    assert calls[-1] == (1, 2)
    with open(state_file) as fh:
        assert int(json.load(fh)) == 2

    import sqlite3

    with sqlite3.connect(db_path) as db:
        db.execute("INSERT INTO health_records VALUES ('t3', 3, 4, 5, 6)")
        db.commit()

    count = asyncio.run(
        rs.sync_new_records(str(db_path), "http://x", state_file=str(state_file))
    )
    assert count == 1
    assert calls[-1] == (3, 3)
    with open(state_file) as fh:
        assert int(json.load(fh)) == 3
