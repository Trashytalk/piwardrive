from __future__ import annotations

"""Common service interfaces for PiWardrive components."""

from typing import Any, Protocol

from .gpsd_client import client as gps_client

from . import diagnostics
from . import utils


class MapService(Protocol):
    """Abstract operations required by :class:`screens.map_screen.MapScreen`."""

    def get_current_position(self) -> tuple[float, float] | None:
        """Return current ``(lat, lon)`` or ``None`` if unavailable."""

    def fetch_access_points(self) -> list[dict[str, Any]]:
        """Return a list of access point dictionaries."""


class DefaultMapService:
    """Map service using ``gpsd`` and the local Kismet API."""

    def get_current_position(self) -> tuple[float, float] | None:
        try:
            pos = gps_client.get_position()
            if pos:
                lat, lon = pos
                return float(lat), float(lon)
        except Exception:
            return None
        return None

    def fetch_access_points(self) -> list[dict[str, Any]]:
        aps, _ = utils.fetch_kismet_devices()
        return list(aps)


class DataCollector(Protocol):
    """Interface for periodic metric collectors."""

    def collect(self) -> dict[str, Any]:
        """Return a metrics snapshot."""


class SelfTestCollector:
    """Wrapper around :func:`diagnostics.self_test`."""

    def collect(self) -> dict[str, Any]:
        return diagnostics.self_test()
