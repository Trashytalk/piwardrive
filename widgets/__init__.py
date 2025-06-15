"""Custom widget package for PiWardrive.

Lazy loading wrapper for widget classes with plugin support.
"""

from importlib import import_module, util
from pathlib import Path
import sys
from typing import Any, Dict, Optional

from utils import format_error, report_error

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
}

_PLUGIN_CLASSES: Dict[str, type] = {}


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
]


def _load_plugins() -> None:
    """Load widget classes from ``~/.config/piwardrive/plugins``."""
    plugin_dir = Path.home() / ".config" / "piwardrive" / "plugins"
    if not plugin_dir.is_dir():
        return
    for path in plugin_dir.iterdir():
        module: Optional[object] = None
        load_path: Path | None = None
        if path.is_file() and path.suffix in {".py", ".so", ".pyd"}:
            mod_name = path.name.split(".")[0]
            load_path = path
        elif path.is_dir():
            mod_name = path.name
            if (path / "__init__.py").exists():
                load_path = path / "__init__.py"
            else:
                so_files = list(path.glob("*.so")) + list(path.glob("*.pyd"))
                if so_files:
                    load_path = so_files[0]
        if load_path is None:
            continue
        spec = util.spec_from_file_location(mod_name, load_path)
        if spec and spec.loader:
            try:
                module = util.module_from_spec(spec)
                sys.modules[spec.name] = module
                spec.loader.exec_module(module)
            except Exception as exc:  # pragma: no cover - import errors
                report_error(
                    format_error(
                        401,
                        f"Failed to load plugin {load_path.name}: {exc}",
                    )
                )
                continue
            for name, obj in vars(module).items():
                if (
                    isinstance(obj, type)
                    and issubclass(obj, DashboardWidget)
                    and obj is not DashboardWidget
                ):
                    _PLUGIN_CLASSES[name] = obj
                    __all__.append(name)


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
