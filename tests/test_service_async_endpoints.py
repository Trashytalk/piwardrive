import asyncio
import importlib
import sys
from types import ModuleType, SimpleNamespace

from httpx import ASGITransport, AsyncClient

# Stub aiosqlite so importing piwardrive modules doesn't fail
fake_aiosqlite = ModuleType("aiosqlite")
fake_aiosqlite.Connection = object  # type: ignore[attr-defined]
sys.modules.setdefault("aiosqlite", fake_aiosqlite)

# Minimal stub for cryptography.fernet
fake_fernet = ModuleType("cryptography.fernet")
fake_fernet.Fernet = object  # type: ignore[attr-defined]
sys.modules.setdefault("cryptography.fernet", fake_fernet)


def _get_service(add_dummy_module):
    add_dummy_module(
        "aiohttp",
        ClientSession=object,
        ClientTimeout=lambda *a, **k: None,
        ClientError=Exception,
    )
    utils_mod = add_dummy_module("utils")

    async def _dummy_async(*_a, **_k):
        return None

    utils_mod.fetch_metrics_async = _dummy_async
    utils_mod.get_avg_rssi = lambda *_a, **_k: None
    utils_mod.get_cpu_temp = lambda *_a, **_k: None
    utils_mod.get_network_throughput = lambda *_a, **_k: (0, 0)
    utils_mod.get_gps_fix_quality = lambda *_a, **_k: None
    utils_mod.service_status_async = _dummy_async
    utils_mod.async_tail_file = _dummy_async

    add_dummy_module("sync", upload_data=lambda *_a, **_k: True)

    return importlib.import_module("service")


async def _make_request(app, path):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get(path)
    return resp


def test_widgets_endpoint_async(monkeypatch, add_dummy_module):
    service = _get_service(add_dummy_module)
    stub = SimpleNamespace(__all__=["A", "B"])
    monkeypatch.setattr(service.importlib, "import_module", lambda n: stub)
    monkeypatch.setattr(
        "piwardrive.service.importlib.import_module", lambda n: stub
    )

    async def call():
        resp = await _make_request(service.app, "/api/widgets")
        assert resp.status_code == 200
        assert resp.json() == {"widgets": ["A", "B"]}

    asyncio.run(call())


def test_logs_endpoint_async(monkeypatch, add_dummy_module):
    service = _get_service(add_dummy_module)

    async def fake_tail(path: str, lines: int):
        return [path, str(lines)]

    monkeypatch.setattr(service, "async_tail_file", fake_tail)
    monkeypatch.setattr("piwardrive.service.async_tail_file", fake_tail)

    async def call():
        resp = await _make_request(service.app, "/logs?lines=2")
        assert resp.status_code == 200
        assert resp.json()["lines"] == [service.DEFAULT_LOG_PATH, "2"]

    asyncio.run(call())


def test_service_status_endpoint_async(monkeypatch, add_dummy_module):
    service = _get_service(add_dummy_module)

    async def fake_status(name: str):
        assert name == "foo"
        return True

    monkeypatch.setattr(service, "service_status_async", fake_status)
    monkeypatch.setattr("piwardrive.service.service_status_async", fake_status)

    async def call():
        resp = await _make_request(service.app, "/service/foo")
        assert resp.status_code == 200
        assert resp.json() == {"service": "foo", "active": True}

    asyncio.run(call())
