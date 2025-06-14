"""Custom widget package for PiWardrive.

Lazy loading wrapper for widget classes with plugin support.
"""

from importlib import import_module, util
from pathlib import Path
import sys
from typing import Any, Dict

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
    for path in plugin_dir.glob("*.py"):
        spec = util.spec_from_file_location(f"_plugin_{path.stem}", path)
        if spec and spec.loader:
            module = util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
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
