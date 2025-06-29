import importlib
import os
import sys
from pathlib import Path
from types import ModuleType

import pytest

MODULES = [
    p.stem
    for p in Path(__file__).resolve().parents[1].glob("*.py")
    if p.stem not in {"setup"}
]


def _setup_dummy_modules(monkeypatch: pytest.MonkeyPatch) -> None:
    root = Path(__file__).resolve().parents[1]
    monkeypatch.syspath_prepend(str(root))
    km_pkg = ModuleType("kivymd")
    km_app = ModuleType("kivymd.app")
    km_app.MDApp = type("MDApp", (), {})
    km_pkg.app = km_app
    monkeypatch.setitem(sys.modules, "kivymd.app", km_app)
    monkeypatch.setitem(sys.modules, "kivymd", km_pkg)

    fastapi_mod = ModuleType("fastapi")
    fastapi_mod.__path__ = []  # type: ignore[attr-defined]

    class _FastAPI:
        def get(self, *a, **k):
            def decorator(func):
                return func

            return decorator

        def post(self, *a, **k):
            def decorator(func):
                return func

            return decorator

        def put(self, *a, **k):
            def decorator(func):
                return func

            return decorator

        def delete(self, *a, **k):
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
    fastapi_mod.UploadFile = object
    fastapi_mod.Body = lambda *a, **k: None
    fastapi_mod.Request = object
    fastapi_static = ModuleType("fastapi.staticfiles")
    fastapi_static.StaticFiles = object
    responses_mod = ModuleType("fastapi.responses")
    responses_mod.StreamingResponse = object
    responses_mod.Response = object
    security_mod = ModuleType("fastapi.security")
    security_mod.HTTPBasic = type("HTTPBasic", (), {"__init__": lambda self, **k: None})
    security_mod.HTTPBasicCredentials = type("HTTPBasicCredentials", (), {})
    fastapi_mod.security = security_mod
    monkeypatch.setitem(sys.modules, "fastapi", fastapi_mod)
    monkeypatch.setitem(sys.modules, "fastapi.security", security_mod)
    monkeypatch.setitem(sys.modules, "fastapi.responses", responses_mod)
    monkeypatch.setitem(sys.modules, "fastapi.staticfiles", fastapi_static)

    aiohttp_mod = ModuleType("aiohttp")
    aiohttp_mod.ClientSession = object  # type: ignore[attr-defined]
    aiohttp_mod.ClientTimeout = lambda *a, **k: None  # type: ignore[attr-defined]
    aiohttp_mod.ClientError = Exception  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "aiohttp", aiohttp_mod)

    # Optional dependencies for top-level modules
    watchdog_pkg = ModuleType("watchdog")
    watchdog_pkg.__path__ = []  # type: ignore[attr-defined]
    watchdog_events = ModuleType("watchdog.events")
    watchdog_events.FileSystemEventHandler = object
    watchdog_observers = ModuleType("watchdog.observers")
    watchdog_observers.Observer = type(
        "Observer",
        (),
        {"schedule": lambda *a, **k: None, "start": lambda *a, **k: None},
    )
    watchdog_pkg.events = watchdog_events
    watchdog_pkg.observers = watchdog_observers
    monkeypatch.setitem(sys.modules, "watchdog", watchdog_pkg)
    monkeypatch.setitem(sys.modules, "watchdog.events", watchdog_events)
    monkeypatch.setitem(sys.modules, "watchdog.observers", watchdog_observers)

    aiosqlite_mod = ModuleType("aiosqlite")
    aiosqlite_mod.Connection = object  # type: ignore[attr-defined]
    aiosqlite_mod.Row = object  # type: ignore[attr-defined]
    aiosqlite_mod.connect = lambda *a, **k: None
    monkeypatch.setitem(sys.modules, "aiosqlite", aiosqlite_mod)

    requests_mod = ModuleType("requests")
    requests_mod.get = lambda *a, **k: None
    requests_mod.Session = object
    requests_mod.RequestException = Exception
    monkeypatch.setitem(sys.modules, "requests", requests_mod)
    rc_mod = ModuleType("requests_cache")
    rc_mod.CachedSession = lambda *a, **k: object()
    monkeypatch.setitem(sys.modules, "requests_cache", rc_mod)

    pyd_mod = ModuleType("pydantic")
    pyd_mod.BaseModel = object
    pyd_mod.Field = lambda *a, **k: None
    pyd_mod.ValidationError = type("ValidationError", (Exception,), {})
    pyd_mod.field_validator = lambda *a, **k: (lambda f: f)
    pyd_mod.ConfigDict = dict
    monkeypatch.setitem(sys.modules, "pydantic", pyd_mod)

    np_mod = ModuleType("numpy")
    np_mod.ndarray = object
    np_mod.asarray = lambda *a, **k: []
    np_mod.sqrt = lambda x: x
    np_mod.average = lambda *a, **k: 0
    monkeypatch.setitem(sys.modules, "numpy", np_mod)

    pd_mod = ModuleType("pandas")
    pd_mod.DataFrame = object
    monkeypatch.setitem(sys.modules, "pandas", pd_mod)

    skl_mod = ModuleType("sklearn")
    cluster_mod = ModuleType("sklearn.cluster")
    cluster_mod.DBSCAN = lambda *a, **k: object()
    skl_mod.cluster = cluster_mod
    monkeypatch.setitem(sys.modules, "sklearn", skl_mod)
    monkeypatch.setitem(sys.modules, "sklearn.cluster", cluster_mod)

    sci_mod = ModuleType("scipy")
    signal_mod = ModuleType("scipy.signal")
    signal_mod.lfilter_zi = lambda *a, **k: 0
    signal_mod.lfilter = lambda *a, **k: ([], None)
    sci_mod.signal = signal_mod
    monkeypatch.setitem(sys.modules, "scipy", sci_mod)
    monkeypatch.setitem(sys.modules, "scipy.signal", signal_mod)

    psutil_mod = ModuleType("psutil")
    psutil_mod.sensors_battery = lambda *a, **k: None
    psutil_mod.net_io_counters = lambda *a, **k: None
    psutil_mod.virtual_memory = lambda: type("vm", (), {"percent": 0})
    psutil_mod.disk_usage = lambda p: type("du", (), {"percent": 0})
    monkeypatch.setitem(sys.modules, "psutil", psutil_mod)

    crypt_mod = ModuleType("cryptography.fernet")
    crypt_mod.Fernet = object
    monkeypatch.setitem(sys.modules, "cryptography.fernet", crypt_mod)

    uvicorn_mod = ModuleType("uvicorn")
    uvicorn_mod.run = lambda *a, **k: None
    monkeypatch.setitem(sys.modules, "uvicorn", uvicorn_mod)

    sys.modules.pop("main", None)

    monkeypatch.setitem(sys.modules, "orjson", ModuleType("orjson"))
    monkeypatch.setitem(sys.modules, "ujson", ModuleType("ujson"))

    # Ensure test helpers do not shadow real modules
    sys.modules.pop("persistence", None)


@pytest.mark.parametrize("module", MODULES)
def test_import_top_level_modules(module: str, monkeypatch: pytest.MonkeyPatch) -> None:
    _setup_dummy_modules(monkeypatch)
    importlib.import_module(module)
