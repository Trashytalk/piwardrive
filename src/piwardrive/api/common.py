from __future__ import annotations

from http import HTTPStatus

from fastapi import Body, Depends
from fastapi.security import OAuth2PasswordBearer

try:
    import utils as _utils
except Exception:  # pragma: no cover - fall back to real module
    from piwardrive import utils as _utils

try:
    import lora_scanner as _lora_scanner
except Exception:  # pragma: no cover - fall back to real module
    from piwardrive import lora_scanner as _lora_scanner

__all__ = [
    "fetch_metrics_async",
    "get_avg_rssi",
    "get_cpu_temp",
    "get_mem_usage",
    "get_disk_usage",
    "get_network_throughput",
    "get_gps_fix_quality",
    "get_gps_accuracy",
    "async_scan_lora",
    "service_status_async",
    "run_service_cmd",
    "async_tail_file",
    "oauth2_scheme",
    "SECURITY_DEP",
    "BODY",
    "error_json",
]


def error_json(code: int, message: str | None = None) -> dict[str, str]:
    if message is None:
        try:
            message = HTTPStatus(code).phrase
        except Exception:
            message = str(code)
    return {"code": str(int(code)), "message": message}


async def _default_fetch_metrics_async(*_a: Any, **_k: Any) -> "MetricsResult":
    return _utils.MetricsResult([], [], 0)  # type: ignore[attr-defined]


fetch_metrics_async: Callable[..., Awaitable["MetricsResult"]] = getattr(
    _utils, "fetch_metrics_async", _default_fetch_metrics_async
)
get_avg_rssi = getattr(_utils, "get_avg_rssi", lambda *_a, **_k: None)
get_cpu_temp = getattr(_utils, "get_cpu_temp", lambda *_a, **_k: None)
get_mem_usage = getattr(_utils, "get_mem_usage", lambda *_a, **_k: None)
get_disk_usage = getattr(_utils, "get_disk_usage", lambda *_a, **_k: None)
get_network_throughput = getattr(
    _utils,
    "get_network_throughput",
    lambda *_a, **_k: (0, 0),
)
get_gps_fix_quality = getattr(_utils, "get_gps_fix_quality", lambda *_a, **_k: None)
get_gps_accuracy = getattr(_utils, "get_gps_accuracy", lambda *_a, **_k: None)


async def _default_async_scan_lora(*_a: Any, **_k: Any) -> list[str]:
    return []


async_scan_lora: Callable[[str], Awaitable[list[str]]] = getattr(
    _lora_scanner, "async_scan_lora", _default_async_scan_lora
)


async def _default_service_status_async(*_a: Any, **_k: Any) -> bool:
    return False


service_status_async: Callable[[str], Awaitable[bool]] = getattr(
    _utils, "service_status_async", _default_service_status_async
)
run_service_cmd: Callable[[str, str], tuple[bool, str, str] | None] = getattr(
    _utils, "run_service_cmd", lambda *_a, **_k: None
)


async def _default_async_tail_file(*_a: Any, **_k: Any) -> list[str]:
    return []


async_tail_file: Callable[[str, int], Awaitable[list[str]]] = getattr(
    _utils, "async_tail_file", _default_async_tail_file
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
SECURITY_DEP = Depends(oauth2_scheme)
BODY = Body(...)
