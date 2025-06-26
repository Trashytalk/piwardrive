from types import ModuleType
from unittest import mock
from typing import Any
import importlib
import sys


def load_handler(monkeypatch: Any) -> ModuleType:
    base = ModuleType('kivy.base')

    class DummyManager:
        PASS = 'PASS'
        handlers: list[Any] = []

        @classmethod
        def add_handler(cls, h: Any) -> None:
            cls.handlers.append(h)

    class DummyHandler:
        pass

    base.ExceptionManager = DummyManager
    base.ExceptionHandler = DummyHandler
    monkeypatch.setitem(sys.modules, 'kivy.base', base)

    for mod_name in ('exception_handler', 'piwardrive.exception_handler'):
        if mod_name in sys.modules:
            monkeypatch.delitem(sys.modules, mod_name, raising=False)

    return importlib.import_module('exception_handler')


def test_install_adds_handler(monkeypatch):
    handler_mod = load_handler(monkeypatch)
    manager = handler_mod.ExceptionManager
    manager.handlers = []
    handler_mod.install()
    assert any(isinstance(h, handler_mod.LogExceptionHandler) for h in manager.handlers)
    handler = manager.handlers[-1]
    with mock.patch('logging.exception') as log_exc:
        handler.handle_exception(RuntimeError('boom'))
        log_exc.assert_called()


def test_install_only_once(monkeypatch):
    handler_mod = load_handler(monkeypatch)
    manager = handler_mod.ExceptionManager
    manager.handlers = []
    handler_mod.install()
    handler_mod.install()
    count = sum(
        isinstance(h, handler_mod.LogExceptionHandler) for h in manager.handlers
    )
    assert count == 1
