"""Compatibility wrapper for :mod:`piwardrive.service`."""

from importlib import import_module

try:  # pragma: no cover - optional dependency loading
    _service = import_module("piwardrive.service")
except Exception:  # pragma: no cover - allow import without extras
    _service = None

if _service is not None:
    globals().update(_service.__dict__)
