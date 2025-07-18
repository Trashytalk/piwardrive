import importlib
import sys
from pathlib import Path
from types import ModuleType

import pytest

MODULES = [
    p.stem
    for p in Path(__file__).resolve().parents[1].glob("*.py")
    if p.stem not in {"setup"}
]


# TODO: Stub for _setup_dummy_modules
def _setup_dummy_modules(*args, **kwargs):
    pass


@pytest.mark.parametrize("module", MODULES)
def test_import_top_level_modules(module: str, monkeypatch: pytest.MonkeyPatch) -> None:
    _setup_dummy_modules(monkeypatch)
    importlib.import_module(module)
