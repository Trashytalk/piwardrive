import asyncio
import importlib
from dataclasses import asdict

from httpx import ASGITransport, AsyncClient

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
    pw_hash = service.security.hash_password("pw")
    monkeypatch.setenv("PW_API_PASSWORD_HASH", pw_hash)

    async def _call() -> None:
        transport = ASGITransport(app=service.app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            token_resp = await client.post(
                "/token",
                data={"username": "admin", "password": "pw"},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            assert token_resp.status_code == 200
            token = token_resp.json()["access_token"]
            resp = await client.get(
                "/status",
                headers={"Authorization": f"Bearer {token}"},
            )
        assert resp.status_code == 200
        assert resp.json() == [asdict(r) for r in records]

    asyncio.run(_call())
