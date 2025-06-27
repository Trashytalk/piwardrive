import importlib
import os
from pathlib import Path

import pytest
from test_imports import _setup_dummy_modules

PKG_ROOT = Path(__file__).resolve().parents[1] / "src" / "piwardrive"
MODULES = [
    "piwardrive." + str(p.with_suffix("").relative_to(PKG_ROOT)).replace(os.sep, ".")
    for p in PKG_ROOT.rglob("*.py")
    if p.name != "__init__.py"
]

@pytest.mark.parametrize("module", MODULES)
def test_import_package_modules(module: str, monkeypatch: pytest.MonkeyPatch) -> None:
    _setup_dummy_modules(monkeypatch)
    importlib.import_module(module)
