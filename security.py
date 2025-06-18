"""Entry point for security helpers with repo-based imports."""

from __future__ import annotations

import os
import sys

SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from piwardrive.security import *  # noqa: F401,F403
