"""PiWardrive package initializer."""

import logging as stdlib_logging
import sys
from importlib import import_module
from types import ModuleType

from .widget_manager import LazyWidgetManager

logger = stdlib_logging.getLogger(__name__)

sigint_suite: ModuleType | None

# Expose ``sigint_suite`` as a top-level module for backwards compatibility
try:  # pragma: no cover - optional dependency
    from . import sigint_suite as sigint_suite
except Exception:  # pragma: no cover - missing optional modules
    try:
        sigint_suite = import_module("piwardrive.integrations.sigint_suite")
    except Exception:
        sigint_suite = None
if sigint_suite is not None:
    sys.modules.setdefault("sigint_suite", sigint_suite)
    sys.modules.setdefault(__name__ + ".sigint_suite", sigint_suite)

# Provide top-level access to frequently imported modules
# Import commonly used modules and expose them at the package root so that
# ``import <module>`` works both when the package is installed and when it is
# used directly from the repository.  ``service`` depends on ``config`` and
# ``sync`` during import, therefore those modules must be loaded first.
for _mod in (
    "persistence",
    "utils",
    "vehicle_sensors",
    "orientation_sensors",
    "config",
    "sync",
    "service",
    "diagnostics",
    "exception_handler",
    "task_queue",
    "cpu_pool",
    "cache",
    "circuit_breaker",
    "performance",
    "visualization.advanced_viz",
    "data_processing.enhanced_processing",
    "hardware.enhanced_hardware",
    "ui.user_experience",
):
    try:  # pragma: no cover - optional imports may fail
        module = import_module(f"piwardrive.{_mod}")
        sys.modules.setdefault(_mod, module)
    except Exception as exc:
        logger.warning("Failed to import optional module '%s': %s", _mod, exc)

__all__ = ["sigint_suite", "LazyWidgetManager"]
