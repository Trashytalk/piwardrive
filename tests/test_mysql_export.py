import asyncio

import piwardrive.mysql_export as me
from piwardrive.persistence import HealthRecord


class DummyCursor:
    def __init__(self, log):
        self.log = log

    async def execute(self, sql, params=None):
        self.log.append(("execute", sql, params))

    async def executemany(self, sql, params):
        self.log.append(("executemany", sql, params))

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass


class DummyConn:
    def __init__(self):
        self.log = []

    def cursor(self):
        return DummyCursor(self.log)

    async def commit(self):
        self.log.append("commit")

    def close(self):
        self.log.append("close")

    async def wait_closed(self):
        self.log.append("wait_closed")


def test_init_schema(monkeypatch):
    conn = DummyConn()

    async def fake_connect(*a, **k):
        return conn

    monkeypatch.setattr(me.aiomysql, "connect", fake_connect)
    cfg = me.MySQLConfig()
    asyncio.run(me.export_data(cfg, [], []))
    # ensure table creation was attempted
    assert any("health_records" in q[1] for q in conn.log if isinstance(q, tuple))
    assert "commit" in conn.log


def test_insert_records(monkeypatch):
    conn = DummyConn()

    async def fake_connect(*a, **k):
        return conn

    monkeypatch.setattr(me.aiomysql, "connect", fake_connect)
    health = [HealthRecord("t", 1.0, 2.0, 3.0, 4.0)]
    wifi = [{"bssid": "aa", "ssid": "net", "lat": 1.0, "lon": 2.0, "timestamp": 3}]
    asyncio.run(me.export_data(me.MySQLConfig(), health, wifi))
    found = [q for q in conn.log if isinstance(q, tuple) and q[0] == "executemany"]
    assert any("health_records" in q[1] for q in found)
    assert any("wifi_observations" in q[1] for q in found)
