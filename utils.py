"""Entry point for utils module.

This small shim ensures the ``src`` package can be imported when running the
code from the repository without installation.  It mirrors the real
``piwardrive.utils`` module so that tests importing ``utils`` behave the same as
if the package were installed."""

from __future__ import annotations

import os
import sys
from importlib import import_module

SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

module = import_module("piwardrive.utils")
sys.modules[__name__] = module
