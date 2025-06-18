import asyncio
from dataclasses import asdict
from httpx import AsyncClient, ASGITransport
import importlib

from piwardrive.persistence import HealthRecord


def test_get_status_async(monkeypatch, add_dummy_module):
    add_dummy_module(
        "aiohttp",
        ClientSession=object,
        ClientTimeout=lambda *a, **k: None,
        ClientError=Exception,
    )
    service = importlib.import_module("service")
    records = [HealthRecord("t", 1.0, 2.0, 3.0, 4.0)]
    async def fake_load(limit=5):
        return records

    monkeypatch.setattr(service, "load_recent_health", fake_load)

    async def _call() -> None:
        transport = ASGITransport(app=service.app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            resp = await client.get("/status")
        assert resp.status_code == 200
        assert resp.json() == [asdict(r) for r in records]

    asyncio.run(_call())
