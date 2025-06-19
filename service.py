"""Entry point for :mod:`piwardrive.service` when running from the repo.

This stub mirrors the real module located under ``src/piwardrive`` but ensures
that tests can monkeypatch attributes on ``service`` and have those patches take
effect within ``piwardrive.service``.  When the package isn't installed, the
``src`` directory is added to ``sys.path`` so imports succeed."""

from __future__ import annotations

import os
import sys

SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from piwardrive import service as _p
from piwardrive import orientation_sensors

# Re-export everything from the real module
from piwardrive.service import *  # noqa: F401,F403

def _proxy(name: str):
    def wrapper(*args: any, **kwargs: any):
        return globals()[name](*args, **kwargs)

    return wrapper

# Replace selected callables in the real module with proxies that defer to this
# module's attributes.  This allows tests to patch ``service.load_recent_health``
# without also patching ``piwardrive.service.load_recent_health``.
_p.load_recent_health = _proxy("load_recent_health")  # type: ignore[attr-defined]
