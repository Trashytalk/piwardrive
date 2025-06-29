import importlib
import os
import sys
from types import ModuleType

from fastapi.testclient import TestClient

# Provide dummy modules for optional dependencies
aiosqlite_mod = ModuleType("aiosqlite")
aiosqlite_mod.Connection = object  # type: ignore[attr-defined]
sys.modules.setdefault("aiosqlite", aiosqlite_mod)
rc_mod = ModuleType("requests_cache")
rc_mod.CachedSession = lambda *a, **k: None  # type: ignore[attr-defined]
sys.modules.setdefault("requests_cache", rc_mod)
# Service expects a "sync" module at import time
sync_mod = ModuleType("sync")
sync_mod.upload_data = lambda *a, **k: None
sys.modules.setdefault("sync", sync_mod)


def test_web_server_serves_static_and_api(tmp_path, monkeypatch):
    service = importlib.import_module("service")
    web_server = importlib.import_module("piwardrive.web_server")

    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("hello")

    orig_join = web_server.os.path.join

    def fake_join(*parts: str) -> str:
        path = orig_join(*parts)
        if path.endswith(orig_join("webui", "dist")):
            return str(dist)
        return path

    monkeypatch.setattr(web_server.os.path, "join", fake_join)

    orig_isdir = web_server.os.path.isdir

    def fake_isdir(path: str) -> bool:
        if path == str(dist):
            return True
        return orig_isdir(path)

    monkeypatch.setattr(web_server.os.path, "isdir", fake_isdir)

    monkeypatch.setattr(service, "load_recent_health", lambda limit=5: [])
    monkeypatch.setattr(web_server, "api_app", service.app)

    app = web_server.create_app()
    client = TestClient(app)

    resp = client.get("/")
    assert resp.status_code == 200
    assert "hello" in resp.text

    resp = client.get("/api/status")
    assert resp.status_code == 200
    assert resp.json() == []
