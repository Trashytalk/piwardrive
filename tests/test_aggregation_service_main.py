"""Tests for the aggregation service main entrypoint."""

import asyncio
import importlib
from unittest.mock import AsyncMock


def test_main_starts_uvicorn(monkeypatch):
    module = importlib.import_module("piwardrive.aggregation_service")
    monkeypatch.setattr(module, "_get_conn", AsyncMock())
    server_mock = AsyncMock()
    monkeypatch.setattr("uvicorn.Server", lambda cfg: server_mock)
    monkeypatch.setattr("uvicorn.Config", lambda *a, **k: object())
    asyncio.run(module.main())
    server_mock.serve.assert_awaited()
