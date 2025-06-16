"""Vehicle sensor integrations for speed data."""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

try:
    import obd  # pragma: no cover - optional
except Exception:  # pragma: no cover - library not available
    obd = None  # type: ignore


def read_speed_obd(port: Optional[str] = None) -> float | None:
    """Return vehicle speed in km/h using an OBD-II adapter."""
    if obd is None:
        return None
    try:
        conn = obd.OBD(port)  # type: ignore
        rsp = conn.query(obd.commands.SPEED)
        return float(rsp.value.to("km/h")) if rsp.value is not None else None
    except Exception as exc:  # pragma: no cover - runtime errors
        logger.error("OBD speed read failed: %s", exc)
        return None
