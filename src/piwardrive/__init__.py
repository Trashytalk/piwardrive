
"""PiWardrive package initializer."""

from importlib import import_module
import sys

# Expose ``sigint_suite`` as a top-level module for backwards compatibility
sigint_suite = import_module("piwardrive.integrations.sigint_suite")
sys.modules.setdefault("sigint_suite", sigint_suite)

# Provide top-level access to frequently imported modules
for _mod in (
    "persistence",
    "utils",
    "vehicle_sensors",
    "orientation_sensors",
    "config",
    "sync",
):
    module = import_module(f"piwardrive.{_mod}")
    sys.modules.setdefault(_mod, module)

__all__ = ["sigint_suite"]
