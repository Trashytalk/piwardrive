"""Plugin loader for sigint_suite.

Python modules placed in ``~/.config/piwardrive/sigint_plugins`` are imported
and exposed through :mod:`sigint_suite` on demand. Each plugin should provide a
``scan()`` function returning structured results such as ``WifiNetwork`` or
``BluetoothDevice`` records.
"""

from __future__ import annotations

import logging
import sys
from importlib import util
from pathlib import Path
from types import ModuleType
from typing import Dict

from .paths import CONFIG_DIR

logger = logging.getLogger(__name__)

_PLUGIN_MODULES: Dict[str, ModuleType] = {}
_PLUGIN_STAMP: float | None = None

__all__: list[str] = []


def _load_plugins() -> None:
    """Load plugin modules from ``~/.config/piwardrive/sigint_plugins``."""
    plugin_dir = Path(CONFIG_DIR) / "sigint_plugins"
    if not plugin_dir.is_dir():
        return
    global _PLUGIN_STAMP
    stamp = plugin_dir.stat().st_mtime
    if _PLUGIN_STAMP == stamp and _PLUGIN_MODULES:
        return
    if _PLUGIN_STAMP != stamp:
        _PLUGIN_MODULES.clear()
        __all__.clear()
    for path in plugin_dir.iterdir():
        module: ModuleType | None = None
        load_path: Path | None = None
        if path.is_file() and path.suffix == ".py":
            mod_name = path.stem
            load_path = path
        elif path.is_dir() and (path / "__init__.py").exists():
            mod_name = path.name
            load_path = path / "__init__.py"
        else:
            continue
        spec = util.spec_from_file_location(mod_name, load_path)
        if spec and spec.loader:
            try:
                module = util.module_from_spec(spec)
                sys.modules[f"sigint_suite.{mod_name}"] = module
                spec.loader.exec_module(module)
            except Exception as exc:  # pragma: no cover - import errors
                logger.exception("Failed to load plugin %s: %s", load_path.name, exc)
                continue
            _PLUGIN_MODULES[mod_name] = module
            __all__.append(mod_name)
    _PLUGIN_STAMP = stamp


def clear_plugin_cache() -> None:
    """Clear cached plugin data so plugins are rescanned on the next load."""
    global _PLUGIN_STAMP
    _PLUGIN_STAMP = None
    _PLUGIN_MODULES.clear()
    __all__.clear()


_load_plugins()
