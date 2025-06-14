from __future__ import annotations

"""Common service interfaces for PiWardrive components."""

from typing import Any, Protocol

import json
import subprocess

import diagnostics
import utils


class MapService(Protocol):
    """Abstract operations required by :class:`screens.map_screen.MapScreen`."""

    def get_current_position(self) -> tuple[float, float] | None:
        """Return current ``(lat, lon)`` or ``None`` if unavailable."""

    def fetch_access_points(self) -> list[dict[str, Any]]:
        """Return a list of access point dictionaries."""


class DefaultMapService:
    """Map service using ``gpspipe`` and the local Kismet API."""

    def get_current_position(self) -> tuple[float, float] | None:
        try:
            proc = subprocess.run(
                ["gpspipe", "-w", "-n", "1"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            line = proc.stdout.strip().splitlines()[0]
            data = json.loads(line)
            lat = data.get("lat")
            lon = data.get("lon")
            if lat is not None and lon is not None:
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
