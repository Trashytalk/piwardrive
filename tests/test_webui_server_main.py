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
