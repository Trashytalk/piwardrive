import asyncio
import importlib
from unittest.mock import AsyncMock


def test_main_starts_uvicorn(monkeypatch):
    server_mock = AsyncMock()
    monkeypatch.setattr("uvicorn.Config", lambda *a, **k: object())
    monkeypatch.setattr("uvicorn.Server", lambda cfg: server_mock)
    module = importlib.import_module("piwardrive.aggregation_service")
    asyncio.run(module.main())
    server_mock.serve.assert_awaited()
