import asyncio
import importlib
import sys
from types import ModuleType
from typing import Any
from unittest import mock


def load_handler(monkeypatch: Any) -> ModuleType:
    for mod_name in ("exception_handler", "piwardrive.exception_handler"):
        if mod_name in sys.modules:
            monkeypatch.delitem(sys.modules, mod_name, raising=False)
    return importlib.import_module("exception_handler")


class DummyLoop:
    def __init__(self) -> None:
        self.handler = None

    def set_exception_handler(self, handler) -> None:  # type: ignore[override]
        self.handler = handler


def test_install_sets_hooks(monkeypatch: Any) -> None:
    handler_mod = load_handler(monkeypatch)
    dummy_loop = DummyLoop()
    monkeypatch.setattr(asyncio, "get_running_loop", lambda: dummy_loop)

    def sentinel(*_a: Any, **_k: Any) -> None:
        pass

    monkeypatch.setattr(sys, "excepthook", sentinel)

    handler_mod.install()

    assert sys.excepthook is not sentinel  # nosec B101
    assert callable(sys.excepthook)  # nosec B101
    assert dummy_loop.handler is not None  # nosec B101
    with mock.patch("logging.exception") as log_exc:
        sys.excepthook(RuntimeError, RuntimeError("boom"), None)
        log_exc.assert_called()


def test_install_only_once(monkeypatch: Any) -> None:
    handler_mod = load_handler(monkeypatch)
    dummy_loop = DummyLoop()
    monkeypatch.setattr(asyncio, "get_running_loop", lambda: dummy_loop)

    def sentinel(*_a: Any, **_k: Any) -> None:
        pass

    monkeypatch.setattr(sys, "excepthook", sentinel)

    handler_mod.install()
    hook = sys.excepthook
    loop_handler = dummy_loop.handler
    handler_mod.install()

    assert sys.excepthook is hook  # nosec B101
    assert dummy_loop.handler is loop_handler  # nosec B101
