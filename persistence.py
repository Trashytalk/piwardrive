"""Entry point for persistence module.

This module provides convenient access to the real implementation under
``piwardrive.persistence`` when the package has not been installed.  The test
suite imports ``persistence`` directly from the repository root, so we ensure
that ``src`` is on ``sys.path`` before delegating to the package module."""

from __future__ import annotations

import os
import sys

SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from piwardrive.persistence import *  # noqa: F401,F403
from piwardrive import persistence as _p

_get_conn = _p._get_conn  # type: ignore[attr-defined]
flush_health_records = _p.flush_health_records  # type: ignore[attr-defined]
