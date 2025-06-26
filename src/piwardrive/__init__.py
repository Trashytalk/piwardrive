
"""PiWardrive package initializer."""

from importlib import import_module
import sys

# Expose ``sigint_suite`` as a top-level module for backwards compatibility
_sigint_name = "piwardrive.integrations.sigint_suite"
if _sigint_name in sys.modules:
    sigint_suite = sys.modules[_sigint_name]
else:
    try:  # pragma: no cover - optional dependency
        sigint_suite = import_module(_sigint_name)
    except Exception:  # pragma: no cover - missing optional modules
        sigint_suite = None

if sigint_suite is not None:
    # Register the module under legacy import paths
    sys.modules.setdefault("sigint_suite", sigint_suite)
    sys.modules.setdefault(__name__ + ".sigint_suite", sigint_suite)

# Provide top-level access to frequently imported modules
for _mod in (
    "persistence",
    "utils",
    "vehicle_sensors",
    "orientation_sensors",
    "service",
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
