"""Thread-safe client for ``gpsd`` with helpers for common queries."""

import logging
import os
import threading
from typing import Any, cast

gpsd: Any
try:
    import gpsd as _gpsd

    gpsd = _gpsd
except Exception as exc:  # pragma: no cover - optional dependency
    gpsd = None
    logging.getLogger(__name__).error("gpsd library not available: %s", exc)


class GPSDClient:
    """Persistent connection to ``gpsd`` providing basic helpers."""

    def __init__(self, host: str | None = None, port: int | None = None) -> None:
        self.host = host or os.getenv("PW_GPSD_HOST", "127.0.0.1")
        self.port = port or int(os.getenv("PW_GPSD_PORT", 2947))
        self._lock = threading.Lock()
        self._connected = False

    def _connect(self) -> None:
        if gpsd is None:
            return
        try:
            gpsd.connect(host=self.host, port=self.port)
            self._connected = True
        except Exception as exc:  # pragma: no cover - connection errors
            logging.getLogger(__name__).error("GPSD connect failed: %s", exc)
            self._connected = False

    def _ensure_connection(self) -> None:
        if not self._connected:
            self._connect()

    def _get_packet(self) -> Any | None:
        with self._lock:
            self._ensure_connection()
            if not self._connected or gpsd is None:
                return None
            try:
                return gpsd.get_current()
            except Exception as exc:  # pragma: no cover - runtime errors
                logging.getLogger(__name__).error("GPSD read failed: %s", exc)
                self._connected = False
                return None

    def get_position(self) -> tuple[float, float] | None:
        """Return the current latitude and longitude if available."""
        pkt = self._get_packet()
        if not pkt:
            return None
        try:
            if hasattr(pkt, "position"):
                return cast(tuple[float, float], pkt.position())
            lat = getattr(pkt, "lat", None)
            lon = getattr(pkt, "lon", None)
            if lat is not None and lon is not None:
                return float(lat), float(lon)
        except Exception:
            pass
        return None

    def get_accuracy(self) -> float | None:
        """Return horizontal accuracy in meters when available."""
        pkt = self._get_packet()
        if not pkt:
            return None
        try:
            acc, _ = pkt.position_precision()
            return float(acc)
        except Exception:
            return None

    def get_fix_quality(self) -> str:
        """Return a textual description of the current fix quality."""
        pkt = self._get_packet()
        if not pkt:
            return "Unknown"
        mode_map = {1: "No Fix", 2: "2D", 3: "3D", 4: "DGPS"}
        try:
            return mode_map.get(pkt.mode, str(pkt.mode))
        except Exception:
            return "Unknown"


client = GPSDClient()
