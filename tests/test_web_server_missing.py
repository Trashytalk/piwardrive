import importlib
import sys
from types import ModuleType

import pytest


def test_create_app_missing_dist(tmp_path, monkeypatch):
    pytest.importorskip("fastapi")
    sys.modules.setdefault("uvicorn", ModuleType("uvicorn"))
    web_server = importlib.import_module("piwardrive.web_server")

    dist = tmp_path / "dist"

    orig_join = web_server.os.path.join

    def fake_join(*parts: str) -> str:
        path = orig_join(*parts)
        if path.endswith(orig_join("webui", "dist")):
            return str(dist)
        return path

    monkeypatch.setattr(web_server.os.path, "join", fake_join)
    monkeypatch.setattr(web_server.os.path, "isdir", lambda p: False)

    with pytest.raises(RuntimeError):
        web_server.create_app()
