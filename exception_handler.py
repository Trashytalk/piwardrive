"""Stub for :mod:`piwardrive.exception_handler` when running from the repo."""
from __future__ import annotations
import os, sys
SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)
from piwardrive import exception_handler as _p  # noqa: E402
from piwardrive.exception_handler import *  # noqa: F401,F403,E402
