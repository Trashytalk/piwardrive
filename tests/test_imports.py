import importlib
import os
import sys
from types import ModuleType
from pathlib import Path

import pytest


MODULES = [
    p.stem
    for p in Path(__file__).resolve().parents[1].glob("*.py")
    if p.stem not in {"setup"}
]


def _setup_dummy_modules(monkeypatch: pytest.MonkeyPatch) -> None:
    kivy_pkg = ModuleType("kivy")
    base = ModuleType("kivy.base")
    base.ExceptionHandler = object
    base.ExceptionManager = type(
        "ExceptionManager",
        (),
        {"PASS": "PASS", "add_handler": staticmethod(lambda *a, **k: None)},
    )
    factory = ModuleType("kivy.factory")
    factory.Factory = object
    lang = ModuleType("kivy.lang")
    lang.Builder = object
    props = ModuleType("kivy.properties")
    props.BooleanProperty = lambda *a, **k: None
    props.NumericProperty = lambda *a, **k: None
    props.StringProperty = lambda *a, **k: None
    props.ListProperty = lambda *a, **k: None
    app_mod = ModuleType("kivy.app")
    app_mod.App = type("App", (), {"get_running_app": staticmethod(lambda: None)})
    for name, mod in {
        "kivy.base": base,
        "kivy.factory": factory,
        "kivy.lang": lang,
        "kivy.properties": props,
        "kivy.app": app_mod,
    }.items():
        monkeypatch.setitem(sys.modules, name, mod)
        setattr(kivy_pkg, name.split(".")[1], mod)
    monkeypatch.setitem(sys.modules, "kivy", kivy_pkg)

    km_pkg = ModuleType("kivymd")
    km_app = ModuleType("kivymd.app")
    km_app.MDApp = type("MDApp", (), {})
    km_pkg.app = km_app
    monkeypatch.setitem(sys.modules, "kivymd.app", km_app)
    monkeypatch.setitem(sys.modules, "kivymd", km_pkg)

    fastapi_mod = ModuleType("fastapi")

    class _FastAPI:
        def get(self, *a, **k):
            def decorator(func):
                return func
            return decorator

        def websocket(self, *a, **k):
            def decorator(func):
                return func
            return decorator

    fastapi_mod.FastAPI = _FastAPI
    fastapi_mod.Depends = lambda *a, **k: None
    fastapi_mod.HTTPException = type("HTTPException", (Exception,), {})
    fastapi_mod.WebSocket = object
    fastapi_mod.WebSocketDisconnect = Exception
    security_mod = ModuleType("fastapi.security")
    security_mod.HTTPBasic = type("HTTPBasic", (), {"__init__": lambda self, **k: None})
    security_mod.HTTPBasicCredentials = type("HTTPBasicCredentials", (), {})
    fastapi_mod.security = security_mod
    monkeypatch.setitem(sys.modules, "fastapi", fastapi_mod)
    monkeypatch.setitem(sys.modules, "fastapi.security", security_mod)

    aiohttp_mod = ModuleType("aiohttp")
    aiohttp_mod.ClientSession = object  # type: ignore[attr-defined]
    aiohttp_mod.ClientTimeout = lambda *a, **k: None  # type: ignore[attr-defined]
    aiohttp_mod.ClientError = Exception  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "aiohttp", aiohttp_mod)



@pytest.mark.parametrize("module", MODULES)
def test_import_top_level_modules(module: str, monkeypatch: pytest.MonkeyPatch) -> None:
    _setup_dummy_modules(monkeypatch)
    importlib.import_module(module)
