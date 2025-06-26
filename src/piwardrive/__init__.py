
"""PiWardrive package initializer."""

from importlib import import_module
import sys

# Expose ``sigint_suite`` as a top-level module for backwards compatibility
try:  # pragma: no cover - optional dependency
    sigint_suite = import_module("piwardrive.integrations.sigint_suite")
    sys.modules.setdefault("sigint_suite", sigint_suite)
    # Ensure ``piwardrive.sigint_suite`` can be imported as a submodule
    # for backward compatibility with external callers and tests.
    sys.modules.setdefault("piwardrive.sigint_suite", sigint_suite)
except Exception:  # pragma: no cover - missing optional modules
    sigint_suite = None

# Provide top-level access to frequently imported modules
for _mod in (
    "persistence",
    "utils",
    "vehicle_sensors",
    "orientation_sensors",
    "config",
    "sync",
    "diagnostics",
    "exception_handler",
):
    try:  # pragma: no cover - optional imports may fail
        module = import_module(f"piwardrive.{_mod}")
        sys.modules.setdefault(_mod, module)
    except Exception:
        pass

__all__ = ["sigint_suite"]
