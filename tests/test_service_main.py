import asyncio
import importlib
import sys
from types import ModuleType
from unittest.mock import AsyncMock


def test_main_starts_uvicorn(monkeypatch):
    dummy_sync = ModuleType("sync")
    dummy_sync.upload_data = AsyncMock()
    sys.modules["sync"] = dummy_sync
    module = importlib.import_module("piwardrive.service")
    server_mock = AsyncMock()
    monkeypatch.setattr("uvicorn.Server", lambda cfg: server_mock)
    monkeypatch.setattr("uvicorn.Config", lambda *a, **k: object())
    asyncio.run(module.main())
    server_mock.serve.assert_awaited()
