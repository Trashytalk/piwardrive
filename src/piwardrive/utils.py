"""Shared utilities with optional core features."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING

import requests

from .error_reporting import format_error, report_error

__all__ = ["format_error", "report_error"]

HTTP_TIMEOUT = 5
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1

try:  # pragma: no cover - optional dependencies may be missing
    from .core.utils import *  # noqa: F401,F403
    from .core.utils import __all__ as _core_all

    for _name in _core_all:
        if _name not in __all__:
            __all__.append(_name)
except Exception:
    # core utils couldn't be imported; define minimal stubs so optional
    # features can be patched in tests without import errors.

    if not TYPE_CHECKING:
        # The following stubs match the names used by the builtin widgets. They
        # are replaced by monkeypatching in the unit tests when the real
        # implementations are unavailable.
        @dataclass
        class MetricsResult:
            aps: list
            clients: list
            handshake_count: int

        def get_gps_fix_quality(
            *_args: object, **_kwargs: object
        ) -> str:  # type: ignore[misc]
            return "Unknown"

        def service_status(
            *_args: object, **_kwargs: object
        ) -> bool:  # type: ignore[misc]
            return False

        def count_bettercap_handshakes(
            *_args: object, **_kwargs: object
        ) -> int:  # type: ignore[misc]
            return 0

        def get_disk_usage(
            *_args: object, **_kwargs: object
        ) -> float | None:  # type: ignore[misc]
            return None

        async def fetch_kismet_devices_async(  # type: ignore[misc]
            *_args: object,
            **_kwargs: object,
        ) -> tuple[list, list]:
            return [], []

        def run_async_task(
            *_args: object, **_kwargs: object
        ) -> None:  # type: ignore[misc]
            return None

        def get_avg_rssi(
            *_args: object, **_kwargs: object
        ) -> float | None:  # type: ignore[misc]
            return None

        __all__ += [
            "MetricsResult",
            "get_gps_fix_quality",
            "service_status",
            "count_bettercap_handshakes",
            "get_disk_usage",
            "fetch_kismet_devices_async",
            "run_async_task",
            "get_avg_rssi",
        ]


def robust_request(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    timeout: float = HTTP_TIMEOUT,
) -> requests.Response:
    """Return ``requests.request`` with retries and exponential backoff."""

    delay = RETRY_DELAY
    last_exc: Exception | None = None
    for attempt in range(RETRY_ATTEMPTS):
        try:
            return requests.request(method, url, headers=headers, timeout=timeout)
        except requests.RequestException as exc:
            last_exc = exc
            logging.warning("Request failed: %s", exc)
            if attempt < RETRY_ATTEMPTS - 1:
                time.sleep(delay)
                delay *= 2
    assert last_exc is not None
    raise last_exc


__all__.append("robust_request")
