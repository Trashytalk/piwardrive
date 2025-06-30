import asyncio
import sys
from types import ModuleType

import piwardrive.data_sink as ds


async def _run(coro):
    return await coro


def test_upload_to_s3(monkeypatch):
    calls = []
    monkeypatch.setattr(
        ds.cloud_export, "upload_to_s3", lambda *a, **k: calls.append(a)
    )
    asyncio.run(ds.upload_to_s3("f", "b", "k", "p"))
    assert calls == [("f", "b", "k", "p")]


def test_write_influxdb(monkeypatch):
    calls = []

    class Sess:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

        def post(self, url, params=None, data=None, headers=None):
            calls.append((url, params, data, headers))

            class Resp:
                async def __aenter__(self):
                    return self

                async def __aexit__(self, exc_type, exc, tb):
                    pass

                def raise_for_status(self):
                    pass

            return Resp()

    aiohttp = ModuleType("aiohttp")
    aiohttp.ClientSession = lambda: Sess()
    monkeypatch.setitem(sys.modules, "aiohttp", aiohttp)
    asyncio.run(ds.write_influxdb("http://x", "tok", "org", "bucket", ["r1"]))
    assert calls and calls[0][0].startswith("http://x")


def test_write_postgres(monkeypatch):
    rows = [{"a": 1}, {"a": 2}]

    class Conn:
        def __init__(self):
            self.calls = []

        async def executemany(self, q, vals):
            self.calls.append((q, vals))

        async def close(self):
            self.calls.append("close")

    conn = Conn()

    async def fake_connect(dsn):
        assert dsn == "dsn"
        return conn

    asyncpg = ModuleType("asyncpg")
    asyncpg.connect = fake_connect  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "asyncpg", asyncpg)
    asyncio.run(ds.write_postgres("dsn", "tbl", rows))
    assert conn.calls and conn.calls[0][0].startswith("INSERT INTO tbl")
