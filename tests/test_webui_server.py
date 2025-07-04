import os
import sys
from types import ModuleType, SimpleNamespace

import pytest
from fastapi.testclient import TestClient

aiosqlite_mod = ModuleType("aiosqlite")
aiosqlite_mod.Connection = object  # type: ignore[attr-defined]
sys.modules.setdefault("aiosqlite", aiosqlite_mod)
rc_mod = ModuleType("requests_cache")
rc_mod.CachedSession = lambda *a, **k: None  # type: ignore[attr-defined]
sys.modules.setdefault("requests_cache", rc_mod)

from piwardrive import security, service, webui_server


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


def test_webui_authentication(tmp_path, monkeypatch):
    """API routes mounted by the web UI enforce HTTP basic auth."""
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "index.html").write_text("hello")
    monkeypatch.setenv("PW_WEBUI_DIST", str(dist))

    pw_hash = security.hash_password("pw")
    monkeypatch.setenv("PW_API_PASSWORD_HASH", pw_hash)
    monkeypatch.setenv("PW_API_USER", "u")

    stub_widgets = SimpleNamespace(__all__=["W"])
    monkeypatch.setattr(service.importlib, "import_module", lambda n: stub_widgets)
    monkeypatch.setattr(
        "piwardrive.service.importlib.import_module", lambda n: stub_widgets
    )
    monkeypatch.setattr(service, "load_recent_health", lambda limit=5: [])
    monkeypatch.setattr(webui_server, "api_app", service.app)

    app = webui_server.create_app()
    client = TestClient(app)

    resp = client.get("/api/widgets")
    assert resp.status_code == 401

    resp = client.get("/api/widgets", auth=("u", "wrong"))
    assert resp.status_code == 401

    resp = client.get("/api/widgets", auth=("u", "pw"))
    assert resp.status_code == 200
    assert resp.json() == {"widgets": ["W"]}


def test_create_app_missing_dist(tmp_path, monkeypatch):
    """create_app raises if the build directory doesn't exist."""
    dist = tmp_path / "dist"
    monkeypatch.setenv("PW_WEBUI_DIST", str(dist))
    monkeypatch.setattr(webui_server, "api_app", service.app)

    with pytest.raises(RuntimeError):
        webui_server.create_app()
