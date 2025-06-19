import os
import sys
from types import ModuleType, SimpleNamespace

import pytest
from fastapi.testclient import TestClient

aiosqlite_mod = ModuleType("aiosqlite")
aiosqlite_mod.Connection = object
sys.modules.setdefault("aiosqlite", aiosqlite_mod)
rc_mod = ModuleType("requests_cache")
rc_mod.CachedSession = lambda *a, **k: None
sys.modules.setdefault("requests_cache", rc_mod)

from piwardrive import webui_server
from piwardrive import service


def test_webui_serves_static_and_api(tmp_path, monkeypatch):
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("hello")
    monkeypatch.setenv("PW_WEBUI_DIST", str(dist))

    monkeypatch.setattr(service, "load_recent_health", lambda limit=5: [])
    monkeypatch.setattr(webui_server, "api_app", service.app)

    app = webui_server.create_app()
    client = TestClient(app)

    resp = client.get("/")
    assert resp.status_code == 200
    assert "hello" in resp.text

    resp = client.get("/api/status")
    assert resp.status_code == 200
    assert resp.json() == []
