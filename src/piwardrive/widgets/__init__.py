"""Custom widget package for PiWardrive.

Lazy loading wrapper for widget classes with plugin support.
"""

from importlib import import_module, util
from pathlib import Path
import sys
from typing import Any, Dict, Iterable, Optional

try:  # pragma: no cover - optional dependency
    from piwardrive.utils import format_error, report_error
except Exception:  # pragma: no cover - minimal fallbacks when deps missing
    def format_error(_code: int, msg: str) -> str:
        return msg

    def report_error(msg: str) -> None:
        print(msg)

from .base import DashboardWidget

_MODULE_MAP: Dict[str, str] = {
    "LogViewer": "log_viewer",
    "SignalStrengthWidget": "signal_strength",
    "GPSStatusWidget": "gps_status",
    "HandshakeCounterWidget": "handshake_counter",
    "ServiceStatusWidget": "service_status",
    "StorageUsageWidget": "storage_usage",
    "DiskUsageTrendWidget": "disk_trend",
    "CPUTempGraphWidget": "cpu_temp_graph",
    "NetworkThroughputWidget": "net_throughput",
    "HealthStatusWidget": "health_status",
    "BatteryStatusWidget": "battery_status",
    "HealthAnalysisWidget": "health_analysis",
    "HeatmapWidget": "heatmap",
    "DBStatsWidget": "db_stats",
    "OrientationWidget": "orientation_widget",
    "VehicleSpeedWidget": "vehicle_speed",
    "LoRaScanWidget": "lora_scan_widget",
}

_PLUGIN_CLASSES: Dict[str, type] = {}
_PLUGIN_STAMP: float | None = None


__all__: list[str] = [
    "LogViewer",
    "SignalStrengthWidget",
    "GPSStatusWidget",
    "HandshakeCounterWidget",
    "ServiceStatusWidget",
    "StorageUsageWidget",
    "DiskUsageTrendWidget",
    "CPUTempGraphWidget",
    "NetworkThroughputWidget",
    "HealthStatusWidget",
    "BatteryStatusWidget",
    "HealthAnalysisWidget",
    "HeatmapWidget",
    "DBStatsWidget",
    "OrientationWidget",
    "VehicleSpeedWidget",
    "LoRaScanWidget",
]


def iter_plugin_paths(plugin_dir: Path) -> Iterable[tuple[str, Path]]:
    """Yield module name and file path for every plugin candidate."""
    for path in plugin_dir.iterdir():
        mod_name = path.stem if path.is_file() else path.name
        load_path: Path | None = None
        if path.is_file() and path.suffix in {".py", ".so", ".pyd"}:
            load_path = path
        elif path.is_dir():
            if (path / "__init__.py").exists():
                load_path = path / "__init__.py"
            else:
                so_files = list(path.glob("*.so")) + list(path.glob("*.pyd"))
                if so_files:
                    load_path = so_files[0]
        if load_path is not None:
            yield mod_name, load_path


def load_plugin(mod_name: str, path: Path) -> Optional[type]:
    """Load plugin module ``mod_name`` from ``path`` and return widget class."""
    spec = util.spec_from_file_location(mod_name, path)
    if not spec or not spec.loader:
        return None
    try:
        module = util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    except Exception as exc:  # pragma: no cover - import errors
        report_error(
            format_error(401, f"Failed to load plugin {path.name}: {exc}")
        )
        return None
    for name, obj in vars(module).items():
        if (
            isinstance(obj, type)
            and issubclass(obj, DashboardWidget)
            and obj is not DashboardWidget
        ):
            return obj
    return None


def _load_plugins() -> None:
    """Load widget classes from ``~/.config/piwardrive/plugins``."""
    plugin_dir = Path.home() / ".config" / "piwardrive" / "plugins"
    if not plugin_dir.is_dir():
        return
    global _PLUGIN_STAMP
    stamp = plugin_dir.stat().st_mtime
    if _PLUGIN_STAMP == stamp and _PLUGIN_CLASSES:
        return
    if _PLUGIN_STAMP != stamp:
        _PLUGIN_CLASSES.clear()
        __all__[:] = [n for n in __all__ if n in _MODULE_MAP]
    for mod_name, path in iter_plugin_paths(plugin_dir):
        cls = load_plugin(mod_name, path)
        if cls is not None:
            _PLUGIN_CLASSES[cls.__name__] = cls
            __all__.append(cls.__name__)
    _PLUGIN_STAMP = plugin_dir.stat().st_mtime


def clear_plugin_cache() -> None:
    """Clear cached plugin data so plugins are rescanned on the next load."""
    global _PLUGIN_STAMP
    _PLUGIN_STAMP = None
    _PLUGIN_CLASSES.clear()
    __all__[:] = [n for n in __all__ if n in _MODULE_MAP]


def list_plugins() -> list[str]:
    """Return names of discovered plugin widget classes."""
    _load_plugins()
    return list(_PLUGIN_CLASSES.keys())


_load_plugins()


def __getattr__(name: str) -> Any:
    if name in _PLUGIN_CLASSES:
        globals()[name] = _PLUGIN_CLASSES[name]
        return _PLUGIN_CLASSES[name]
    if name in _MODULE_MAP:
        module = import_module(f".{_MODULE_MAP[name]}", __name__)
        attr = getattr(module, name)
        globals()[name] = attr
        return attr
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
