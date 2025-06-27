"""Vehicle sensor integrations for OBD‑II data."""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

try:
    import obd  # pragma: no cover - optional
except Exception:  # pragma: no cover - library not available
    obd = None


def read_speed_obd(port: Optional[str] = None) -> float | None:
    """Return vehicle speed in km/h using an OBD-II adapter."""
    if obd is None:
        return None
    try:
        conn = obd.OBD(port)
        rsp = conn.query(obd.commands.SPEED)
        return float(rsp.value.to("km/h")) if rsp.value is not None else None
    except Exception as exc:  # pragma: no cover - runtime errors
        logger.error("OBD speed read failed: %s", exc)
        return None


def read_rpm_obd(port: Optional[str] = None) -> float | None:
    """Return engine RPM using an OBD-II adapter."""
    if obd is None:
        return None
    try:
        conn = obd.OBD(port)
        rsp = conn.query(obd.commands.RPM)
        return float(rsp.value.to("rpm")) if rsp.value is not None else None
    except Exception as exc:  # pragma: no cover - runtime errors
        logger.error("OBD RPM read failed: %s", exc)
        return None


def read_engine_load_obd(port: Optional[str] = None) -> float | None:
    """Return calculated engine load percentage via an OBD-II adapter."""
    if obd is None:
        return None
    try:
        conn = obd.OBD(port)
        rsp = conn.query(obd.commands.ENGINE_LOAD)
        return float(rsp.value.to("percent")) if rsp.value is not None else None
    except Exception as exc:  # pragma: no cover - runtime errors
        logger.error("OBD engine load read failed: %s", exc)
        return None
