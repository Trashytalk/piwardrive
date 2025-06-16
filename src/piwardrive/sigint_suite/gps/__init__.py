"""GPS helpers for SIGINT suite."""

from typing import Optional, Tuple

from gpsd_client import client as gps_client


def get_position() -> Optional[Tuple[float, float]]:
    """Return the current GPS position as ``(lat, lon)`` or ``None``."""
    try:
        return gps_client.get_position()
    except Exception:
        return None


__all__ = ["get_position"]
