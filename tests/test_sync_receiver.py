import importlib.util
import sys
from pathlib import Path

from fastapi.testclient import TestClient


def _load_receiver(tmp_path, monkeypatch):
    def fake_expand(p):
        return str(tmp_path)

    monkeypatch.setattr("os.path.expanduser", fake_expand)
    spec = importlib.util.spec_from_file_location("sync_receiver", Path("sync_receiver.py"))
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    sys.modules["sync_receiver"] = module
    return module


def test_rejects_traversal(tmp_path, monkeypatch):
    receiver = _load_receiver(tmp_path, monkeypatch)
    client = TestClient(receiver.app)
    resp = client.post("/", files={"file": ("../x", b"data")})
    assert resp.status_code == 400


def test_rejects_nested_traversal(tmp_path, monkeypatch):
    receiver = _load_receiver(tmp_path, monkeypatch)
    client = TestClient(receiver.app)
    resp = client.post("/", files={"file": ("../../etc/passwd", b"data")})
    assert resp.status_code == 400
