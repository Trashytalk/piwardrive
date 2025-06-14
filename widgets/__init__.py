"""Custom widget package for PiWardrive."""

"""Lazy loading wrapper for widget classes."""

from importlib import import_module

_MODULE_MAP = {
    "LogViewer": "log_viewer",
    "SignalStrengthWidget": "signal_strength",
    "GPSStatusWidget": "gps_status",
    "HandshakeCounterWidget": "handshake_counter",
    "ServiceStatusWidget": "service_status",
    "StorageUsageWidget": "storage_usage",
    "DiskUsageTrendWidget": "disk_trend",
    "CPUTempGraphWidget": "cpu_temp_graph",
    "NetworkThroughputWidget": "net_throughput",
}


def __getattr__(name):
    if name in _MODULE_MAP:
        module = import_module(f".{_MODULE_MAP[name]}", __name__)
        attr = getattr(module, name)
        globals()[name] = attr
        return attr
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "LogViewer",
    "SignalStrengthWidget",
    "GPSStatusWidget",
    "HandshakeCounterWidget",
    "ServiceStatusWidget",
    "StorageUsageWidget",
    "DiskUsageTrendWidget",
    "CPUTempGraphWidget",
    "NetworkThroughputWidget",
]
