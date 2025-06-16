import sys
from types import ModuleType
import pytest


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
