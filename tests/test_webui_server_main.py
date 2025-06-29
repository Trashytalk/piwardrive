import importlib
import sys
from types import ModuleType
from unittest.mock import Mock


def test_main_runs_uvicorn(monkeypatch):
    dummy_sync = ModuleType("sync")
    dummy_sync.upload_data = lambda: None
    sys.modules["sync"] = dummy_sync
    module = importlib.import_module("piwardrive.web.webui_server")
    run_mock = Mock()
    monkeypatch.setattr("uvicorn.run", run_mock)
    monkeypatch.setattr(module, "create_app", lambda: object())
    module.main()
    run_mock.assert_called()


def test_main_env_port(monkeypatch):
    dummy_sync = ModuleType("sync")
    dummy_sync.upload_data = lambda: None
    sys.modules["sync"] = dummy_sync
    module = importlib.import_module("piwardrive.web.webui_server")
    run_mock = Mock()
    monkeypatch.setattr("uvicorn.run", run_mock)
    app_obj = object()
    monkeypatch.setattr(module, "create_app", lambda: app_obj)
    monkeypatch.setenv("PW_WEBUI_PORT", "1234")
    module.main()
    run_mock.assert_called_with(app_obj, host="127.0.0.1", port=1234)
