"""Stub for :mod:`piwardrive.exception_handler` when running from the repo."""

from __future__ import annotations

import os
import sys
import importlib

SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

mod = importlib.import_module("piwardrive.exception_handler")

if hasattr(mod, "__all__"):
    names = list(mod.__all__)
else:
    names = [n for n in dir(mod) if not n.startswith("_")]

for name in names:
    globals()[name] = getattr(mod, name)

__all__ = names
