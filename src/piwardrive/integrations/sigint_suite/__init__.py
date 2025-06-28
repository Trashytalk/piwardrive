"""Common initialization for sigint_suite."""

import logging
import os
from typing import Any

from . import plugins as _plugins

_DEBUG_FLAG = "SIGINT_DEBUG"


def _setup_logging() -> None:
    """Configure basic logging based on ``SIGINT_DEBUG``."""
    level = logging.DEBUG if os.getenv(_DEBUG_FLAG) else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


_setup_logging()

__all__ = ["plugins"] + _plugins.__all__


def __getattr__(name: str) -> Any:
    if name in _plugins._PLUGIN_MODULES:
        mod = _plugins._PLUGIN_MODULES[name]
        globals()[name] = mod
        return mod
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
