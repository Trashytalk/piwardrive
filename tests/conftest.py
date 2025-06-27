"""Pytest fixtures used across the test suite."""

import os
import sys
from types import ModuleType

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))


@pytest.fixture
def add_dummy_module(monkeypatch):
    created = []

    def _add(name: str, **attrs):
        mod = ModuleType(name)
        for attr, val in attrs.items():
            setattr(mod, attr, val)
        monkeypatch.setitem(sys.modules, name, mod)
        created.append(name)
        return mod

    yield _add

    for name in created:
        monkeypatch.delitem(sys.modules, name, raising=False)


@pytest.fixture(autouse=True)
def _restore_modules(monkeypatch):
    """Ensure core modules are reloaded after each test."""
    yield
    import importlib
    for mod_name in ("persistence", "utils"):
        if mod_name in sys.modules:
            monkeypatch.delitem(sys.modules, mod_name, raising=False)
        importlib.import_module(mod_name)
