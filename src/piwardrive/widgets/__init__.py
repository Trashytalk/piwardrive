"""Custom widget package for PiWardrive.

Lazy loading wrapper for widget classes with plugin support.
"""

import ast
import sys
import weakref
from importlib import import_module, machinery, util
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Optional

try:  # pragma: no cover - optional dependency
    from piwardrive.utils import format_error, report_error
except Exception:  # pragma: no cover - minimal fallbacks when deps missing

    def format_error(code: int, message: str) -> str:
        return message

    def report_error(message: str) -> None:
        print(message)


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
    "DetectionRateWidget": "detection_rate",
    "ThreatLevelWidget": "threat_level",
    "NetworkDensityWidget": "network_density",
    "DeviceClassificationWidget": "device_classification",
    "SuspiciousActivityWidget": "suspicious_activity",
    "AlertSummaryWidget": "alert_summary",
    "ThreatMapWidget": "threat_map",
    "SecurityScoreWidget": "security_score",
    "DatabaseHealthWidget": "database_health",
    "ScannerStatusWidget": "scanner_status",
    "SystemResourceWidget": "system_resource",
}

_PLUGIN_LOADERS: Dict[str, Callable[[], type]] = {}
_WIDGET_CACHE: "weakref.WeakValueDictionary[str, type]" = weakref.WeakValueDictionary()
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
    "DetectionRateWidget",
    "ThreatLevelWidget",
    "NetworkDensityWidget",
    "DeviceClassificationWidget",
    "SuspiciousActivityWidget",
    "AlertSummaryWidget",
    "ThreatMapWidget",
    "SecurityScoreWidget",
    "DatabaseHealthWidget",
    "ScannerStatusWidget",
    "SystemResourceWidget",
]


def iter_plugin_paths(plugin_dir: Path) -> Iterable[tuple[str, Path]]:
    """Yield module name and file path for every plugin candidate."""
    for path in plugin_dir.iterdir():
        load_path: Path | None = None
        mod_name = path.name
        if path.is_file():
            if path.suffix == ".py":
                mod_name = path.stem
                load_path = path
            else:
                for suf in machinery.EXTENSION_SUFFIXES:
                    if mod_name.endswith(suf):
                        mod_name = mod_name[: -len(suf)]
                        load_path = path
                        break
        elif path.is_dir():
            mod_name = path.name
            if (path / "__init__.py").exists():
                load_path = path / "__init__.py"
            else:
                for suf in machinery.EXTENSION_SUFFIXES:
                    so_files = list(path.glob(f"*{suf}"))
                    if so_files:
                        load_path = so_files[0]
                        break
        if load_path is not None:
            yield mod_name, load_path


def _extract_class_names(path: Path) -> list[str]:
    """Return names of ``DashboardWidget`` subclasses in ``path`` without executing."""
    try:
        source = path.read_text(encoding="utf-8")
    except Exception:
        return []
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError:
        return []
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "DashboardWidget":
                    names.append(node.name)
                elif isinstance(base, ast.Attribute) and base.attr == "DashboardWidget":
                    names.append(node.name)
    return names


def load_plugin(mod_name: str, path: Path, cls_name: str) -> Optional[type]:
    """Load ``cls_name`` from ``path`` returning the widget class."""
    spec = util.spec_from_file_location(mod_name, path)
    if not spec or not spec.loader:
        return None
    try:
        module = util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
    except Exception as exc:  # pragma: no cover - import errors
        report_error(format_error(401, f"Failed to load plugin {path.name}: {exc}"))
        return None
    obj = getattr(module, cls_name, None)
    if isinstance(obj, type) and issubclass(obj, DashboardWidget):
        return obj
    return None


def _load_plugins() -> None:
    """Load widget classes from ``~/.config/piwardrive/plugins``."""
    plugin_dir = Path.home() / ".config" / "piwardrive" / "plugins"
    global _PLUGIN_STAMP
    if not plugin_dir.is_dir():
        if _PLUGIN_STAMP is not None:
            _PLUGIN_STAMP = None
            _PLUGIN_LOADERS.clear()
            _WIDGET_CACHE.clear()
            __all__[:] = [n for n in __all__ if n in _MODULE_MAP]
        return

    stamp = plugin_dir.stat().st_mtime
    if _PLUGIN_STAMP == stamp and _PLUGIN_LOADERS:
        return
    if _PLUGIN_STAMP != stamp:
        _PLUGIN_LOADERS.clear()
        _WIDGET_CACHE.clear()
        __all__[:] = [n for n in __all__ if n in _MODULE_MAP]
    for mod_name, path in iter_plugin_paths(plugin_dir):
        if path.suffix == ".py":
            for cls_name in _extract_class_names(path):

                def _loader(m=mod_name, p=path, c=cls_name) -> type:
                    return load_plugin(m, p, c)  # type: ignore[return-value]

                _PLUGIN_LOADERS[cls_name] = _loader
                __all__.append(cls_name)
        else:
            # compiled modules must be imported to introspect
            cls = None
            spec = util.spec_from_file_location(mod_name, path)
            if spec and spec.loader:
                try:
                    module = util.module_from_spec(spec)
                    sys.modules[spec.name] = module
                    spec.loader.exec_module(module)
                    for name, obj in vars(module).items():
                        if (
                            isinstance(obj, type)
                            and issubclass(obj, DashboardWidget)
                            and obj is not DashboardWidget
                        ):
                            cls = obj
                            break
                except Exception as exc:  # pragma: no cover - import errors
                    report_error(
                        format_error(401, f"Failed to load plugin {path.name}: {exc}")
                    )
            if cls is not None:
                _PLUGIN_LOADERS[cls.__name__] = lambda c=cls: c
                __all__.append(cls.__name__)
    _PLUGIN_STAMP = plugin_dir.stat().st_mtime


def clear_plugin_cache() -> None:
    """Clear cached plugin data so plugins are rescanned on the next load."""
    global _PLUGIN_STAMP
    _PLUGIN_STAMP = None
    _PLUGIN_LOADERS.clear()
    _WIDGET_CACHE.clear()
    __all__[:] = [n for n in __all__ if n in _MODULE_MAP]


def list_plugins() -> list[str]:
    """Return names of discovered plugin widget classes."""
    _load_plugins()
    return list(_PLUGIN_LOADERS.keys())


_load_plugins()


def __getattr__(name: str) -> Any:
    if name in _WIDGET_CACHE:
        return _WIDGET_CACHE[name]
    if name in _PLUGIN_LOADERS:
        cls = _PLUGIN_LOADERS[name]()
        if cls is not None:
            _WIDGET_CACHE[name] = cls
            globals()[name] = cls
            return cls
    if name in _MODULE_MAP:
        module = import_module(f".{_MODULE_MAP[name]}", __name__)
        attr = getattr(module, name)
        _WIDGET_CACHE[name] = attr
        globals()[name] = attr
        return attr
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
