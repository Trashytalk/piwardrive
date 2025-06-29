"""Entry point for :mod:`piwardrive.main` when running from the repo."""

from __future__ import annotations

import os
import sys

SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from piwardrive.main import PiWardriveApp  # noqa: E402


__all__ = ["PiWardriveApp"]

