"""Shared utilities with optional core features."""
from __future__ import annotations

from .error_reporting import App, format_error, report_error

__all__ = ["App", "format_error", "report_error"]

try:  # pragma: no cover - optional dependencies may be missing
    from .core.utils import *  # type: ignore  # noqa: F401,F403
    from .core.utils import __all__ as _core_all  # type: ignore
    for _name in _core_all:
        if _name not in __all__:
            __all__.append(_name)
except Exception:
    # core utils couldn't be imported; keep basic functionality
    pass
