"""Shared utilities with optional core features."""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests  # type: ignore

from .error_reporting import App, format_error, report_error

__all__ = ["App", "format_error", "report_error"]

try:  # pragma: no cover - optional dependencies may be missing
    from .core.utils import *  # type: ignore  # noqa: F401,F403
    from .core.utils import __all__ as _core_all  # type: ignore

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
            "get_gps_fix_quality",
            "service_status",
            "count_bettercap_handshakes",
            "get_disk_usage",
            "fetch_kismet_devices_async",
            "run_async_task",
            "get_avg_rssi",
        ]


def robust_request(url: str) -> requests.Response:
    """Return ``requests.get(url)`` with simple retries."""

    def do_request() -> requests.Response:
        return requests.get(url, timeout=5)

    return retry_call(do_request, attempts=3, delay=1)  # noqa: F405


__all__.append("robust_request")
