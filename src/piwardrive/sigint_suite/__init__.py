"""SIGINT suite compatibility wrapper."""

from __future__ import annotations

import importlib
import os
import sys
from typing import Any, cast

# Import the actual implementation from piwardrive.integrations.sigint_suite
_impl = cast(Any, importlib.import_module("piwardrive.integrations.sigint_suite"))

# Reload paths to pick up environment changes (e.g. HOME) that may occur between
# imports during tests.
_paths_mod = importlib.reload(
    importlib.import_module("piwardrive.integrations.sigint_suite.paths")
)
_impl.paths = _paths_mod
sys.modules[__name__ + ".paths"] = _paths_mod

if hasattr(_impl, "plugins"):
    # Ensure the plugin loader uses the updated configuration directory
    _impl.plugins.CONFIG_DIR = _paths_mod.CONFIG_DIR

# Reload plugins each time the wrapper is imported so that tests manipulating the
# configuration directory get a fresh view.
if hasattr(_impl, "plugins"):
    _impl.plugins.clear_plugin_cache()
    _impl.plugins._load_plugins()

# Expose this compatibility wrapper under the original top-level package name so
# that modules inside ``sigint_suite`` using absolute imports (e.g.
# ``from sigint_suite.hooks import ...``) resolve to this package. This ensures
# a single module instance is used regardless of whether callers import
# ``sigint_suite`` or ``piwardrive.sigint_suite``.
sys.modules.setdefault("sigint_suite", sys.modules[__name__])

# Expose package submodules by extending __path__ to include the implementation
# package directory. This allows ``piwardrive.sigint_suite.<mod>`` imports to
# resolve to modules under ``piwardrive.integrations.sigint_suite``.
_pkg_dir = os.path.join(
    os.path.dirname(__file__), os.pardir, "integrations", "sigint_suite"
)
if os.path.isdir(_pkg_dir) and _pkg_dir not in __path__:
    __path__.append(_pkg_dir)

__all__ = list(getattr(_impl, "__all__", []))


def __getattr__(name: str) -> Any:
    return getattr(_impl, name)


import sys  # noqa: E402

_real = importlib.import_module("piwardrive.integrations.sigint_suite")
# Mirror the public attributes of the real package
globals().update(_real.__dict__)
sys.modules.setdefault(__name__, _real)
