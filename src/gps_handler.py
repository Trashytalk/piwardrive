"""High level GPS helper using ``python-gps``.

This module wraps the :mod:`gps` package to obtain the current GPS fix from
``gpsd``.  It provides convenience methods mirroring
:mod:`piwardrive.gpsd_client` but uses the official ``python-gps`` bindings.

Functions automatically reconnect on failure and gracefully handle timeouts so
callers do not block indefinitely when no GPS data is available.
"""

from __future__ import annotations

import logging
import os
from typing import Any

try:  # pragma: no cover - optional dependency may be missing
    from gps import WATCH_ENABLE, WATCH_NEWSTYLE, gps
except Exception as exc:  # pragma: no cover - missing dependency
    gps = None
    WATCH_ENABLE = WATCH_NEWSTYLE = 0  # type: ignore[assignment]
    logging.getLogger(__name__).error("python-gps not available: %s", exc)

logger = logging.getLogger(__name__)


class GPSHandler:
    """Simple wrapper around :mod:`gps` providing timeout handling."""

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        *,
        timeout: float = 1.0,
    ) -> None:
        """Initialize GPS handler.
        
        Args:
            host: GPS daemon host (default: 127.0.0.1)
            port: GPS daemon port (default: 2947)
            timeout: Connection timeout in seconds
        """
        self.host = host or os.getenv("PW_GPSD_HOST", "127.0.0.1")
        self.port = port or int(os.getenv("PW_GPSD_PORT", 2947))
        self.timeout = timeout
        self._session: Any | None = None
        self._connected = False

    # Internal helpers -------------------------------------------------
    def _connect(self) -> None:
        if gps is None:
            return
        try:
            self._session = gps(host=self.host, port=self.port)
            self._session.stream(WATCH_ENABLE | WATCH_NEWSTYLE)
            self._connected = True
        except Exception as exc:  # pragma: no cover - connection errors
            logger.error("GPS connect failed: %s", exc)
            self._connected = False
            self._session = None

    def _ensure_connection(self) -> None:
        if not self._connected:
            self._connect()

    def _get_report(self, timeout: float | None = None) -> Any | None:
        """Return the latest TPV report or ``None`` on timeout/error."""
        self._ensure_connection()
        if not self._connected or self._session is None:
            return None
        to = self.timeout if timeout is None else timeout
        try:
            if not self._session.waiting(to):
                logger.warning("GPS timeout after %.1fs", to)
                return None
            return self._session.next()
        except StopIteration:  # pragma: no cover - no data available
            logger.warning("GPS timed out")
            return None
        except Exception as exc:  # pragma: no cover - runtime errors
            logger.error("GPS read failed: %s", exc)
            self._connected = False
            self._session = None
            return None

    # Public API -------------------------------------------------------
    def get_position(self, timeout: float | None = None) -> tuple[float, float] | None:
        """Get current GPS position as (latitude, longitude).
        
        Args:
            timeout: Read timeout in seconds
            
        Returns:
            Tuple of (lat, lon) or None if unavailable
        """
        report = self._get_report(timeout)
        if not report or getattr(report, "class", None) != "TPV":
            return None
        lat = getattr(report, "lat", None)
        lon = getattr(report, "lon", None)
        if lat is None or lon is None:
            return None
        try:
            return float(lat), float(lon)
        except Exception:
            return None

    def get_accuracy(self, timeout: float | None = None) -> float | None:
        """Get current GPS accuracy in meters.
        
        Args:
            timeout: Read timeout in seconds
            
        Returns:
            Accuracy in meters or None if unavailable
        """
        report = self._get_report(timeout)
        if not report or getattr(report, "class", None) != "TPV":
            return None
        epx = getattr(report, "epx", None)
        epy = getattr(report, "epy", None)
        if epx is None or epy is None:
            return None
        try:
            return float(max(epx, epy))
        except Exception:
            return None

    def get_fix_quality(self, timeout: float | None = None) -> str:
        """Get current GPS fix quality.
        
        Args:
            timeout: Read timeout in seconds
            
        Returns:
            Fix quality string (No Fix, 2D, 3D, DGPS, etc.)
        """
        report = self._get_report(timeout)
        if not report or getattr(report, "class", None) != "TPV":
            return "Unknown"
        mode_map = {1: "No Fix", 2: "2D", 3: "3D", 4: "DGPS"}
        try:
            mode = getattr(report, "mode", None)
            if isinstance(mode, int):
                return mode_map.get(mode, str(mode))
        except Exception:
            pass
        return "Unknown"

    def close(self) -> None:
        """Close the GPS connection and clean up resources."""
        session = self._session
        self._session = None
        self._connected = False
        if session is not None:
            try:
                session.close()
            except Exception:  # pragma: no cover - close errors
                pass


handler = GPSHandler()

__all__ = ["GPSHandler", "handler"]
