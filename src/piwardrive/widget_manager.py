from __future__ import annotations

"""Lazy widget loading with memory aware cleanup."""

import asyncio
import os
import sys
import weakref
from pathlib import Path
from typing import Dict, Optional

from . import widgets
from .memory_monitor import MemoryMonitor
from .resource_manager import ResourceManager
from .widgets.base import DashboardWidget


class LazyWidgetManager:
    """Load widget plugins on demand and release them under memory pressure."""

    def __init__(
        self,
        resource_manager: ResourceManager,
        *,
        memory_monitor: Optional[MemoryMonitor] = None,
        unload_threshold_mb: float = 200.0,
    ) -> None:
        self._rm = resource_manager
        self._monitor = memory_monitor or MemoryMonitor(history=1)
        self._threshold_mb = unload_threshold_mb
        self._instances: "weakref.WeakValueDictionary[str, DashboardWidget]" = (
            weakref.WeakValueDictionary()
        )
        self._locks: Dict[str, asyncio.Lock] = {}
        self._plugin_cache: Dict[str, tuple[str, Path]] = {}
        self._cache_stamp: float | None = None

    # ------------------------------------------------------------------
    # Public API
    async def get_widget(self, name: str) -> DashboardWidget:
        """Return a widget instance loading the plugin if necessary."""
        if name in self._instances:
            obj = self._instances[name]
            if obj is not None:
                return obj
        lock = self._locks.setdefault(name, asyncio.Lock())
        async with lock:
            if name in self._instances:
                obj = self._instances[name]
                if obj is not None:
                    return obj
            cls = self._load_widget_class(name)
            widget = cls()
            self._instances[name] = widget
            if hasattr(widget, "deactivate"):
                self._rm.register(widget, widget.deactivate)
            self._maybe_unload()
            return widget

    def release_widget(self, name: str) -> None:
        """Manually remove a widget instance."""
        widget = self._instances.pop(name, None)
        if widget and hasattr(widget, "deactivate"):
            try:
                widget.deactivate()  # type: ignore[call-arg]
            except Exception:
                pass

    def loaded(self) -> list[str]:
        """Return names of currently loaded widget instances."""
        return [n for n, w in self._instances.items() if w is not None]

    # ------------------------------------------------------------------
    # Internal helpers
    def _plugin_dir(self) -> Path:
        env = os.getenv("PIWARDIVE_PLUGIN_DIR")
        return Path(env) if env else Path.home() / ".config" / "piwardrive" / "plugins"

    def _discover_plugins(self) -> None:
        plugin_dir = self._plugin_dir()
        if not plugin_dir.is_dir():
            self._plugin_cache.clear()
            self._cache_stamp = None
            return
        stamp = plugin_dir.stat().st_mtime
        if self._cache_stamp == stamp:
            return
        info: Dict[str, tuple[str, Path]] = {}
        for mod_name, path in widgets.iter_plugin_paths(plugin_dir):
            if path.suffix == ".py":
                for cls in widgets._extract_class_names(path):
                    info[cls] = (mod_name, path)
            else:
                spec = util.spec_from_file_location(mod_name, path)
                if spec and spec.loader:
                    try:
                        module = util.module_from_spec(spec)
                        sys.modules[spec.name] = module
                        spec.loader.exec_module(module)
                        for cname, obj in vars(module).items():
                            if (
                                isinstance(obj, type)
                                and issubclass(obj, DashboardWidget)
                                and obj is not DashboardWidget
                            ):
                                info[cname] = (mod_name, path)
                    except Exception:
                        continue
        self._plugin_cache = info
        self._cache_stamp = stamp

    def _load_widget_class(self, name: str) -> type[DashboardWidget]:
        self._discover_plugins()
        if name in self._plugin_cache:
            mod_name, path = self._plugin_cache[name]
            cls = widgets.load_plugin(mod_name, path, name)
            if cls is None:
                raise ImportError(f"unable to load plugin {name}")
            return cls  # type: ignore[return-value]
        return getattr(widgets, name)

    def _maybe_unload(self) -> None:
        rss = self._monitor.sample()
        if rss <= self._threshold_mb:
            return
        # drop the oldest entry
        for name in list(self._instances.keys()):
            widget = self._instances.pop(name, None)
            if widget and hasattr(widget, "deactivate"):
                try:
                    widget.deactivate()  # type: ignore[call-arg]
                except Exception:
                    pass
            break


__all__ = ["LazyWidgetManager"]
