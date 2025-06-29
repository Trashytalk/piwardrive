"""Vehicle sensor integrations for OBD‑II data."""

from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger(__name__)

try:
    import obd  # pragma: no cover - optional
except Exception:  # pragma: no cover - library not available
    obd = None


_OBD_CONN: "obd.OBD | None" = None


def _get_conn(port: Optional[str] = None) -> "obd.OBD | None":
    """Return a cached OBD connection or attempt to create one."""
    global _OBD_CONN

    if obd is None:
        return None

    if _OBD_CONN is None or not getattr(_OBD_CONN, "is_connected", lambda: True)():
        try:
            _OBD_CONN = obd.OBD(port)
        except Exception as exc:  # pragma: no cover - runtime errors
            logger.error("Failed to connect to OBD: %s", exc)
            _OBD_CONN = None
    return (
        _OBD_CONN
        if _OBD_CONN and getattr(_OBD_CONN, "is_connected", lambda: True)()
        else None
    )


def close_obd() -> None:
    """Close the cached OBD connection if open."""
    global _OBD_CONN

    if _OBD_CONN is not None:
        try:
            _OBD_CONN.close()
        except Exception as exc:  # pragma: no cover - runtime errors
            logger.error("OBD close failed: %s", exc)
        _OBD_CONN = None


def read_speed_obd(port: Optional[str] = None) -> float | None:
    """Return vehicle speed in km/h using an OBD-II adapter."""
    conn = _get_conn(port)
    if conn is None:
        return None
    try:
        rsp = conn.query(obd.commands.SPEED)
        return float(rsp.value.to("km/h")) if rsp.value is not None else None
    except Exception as exc:  # pragma: no cover - runtime errors
        logger.error("OBD speed read failed: %s", exc)
        return None


def read_rpm_obd(port: Optional[str] = None) -> float | None:
    """Return engine RPM using an OBD-II adapter."""
    conn = _get_conn(port)
    if conn is None:
        return None
    try:
        rsp = conn.query(obd.commands.RPM)
        return float(rsp.value.to("rpm")) if rsp.value is not None else None
    except Exception as exc:  # pragma: no cover - runtime errors
        logger.error("OBD RPM read failed: %s", exc)
        return None


def read_engine_load_obd(port: Optional[str] = None) -> float | None:
    """Return calculated engine load percentage via an OBD-II adapter."""
    conn = _get_conn(port)
    if conn is None:
        return None
    try:
        rsp = conn.query(obd.commands.ENGINE_LOAD)
        return float(rsp.value.to("percent")) if rsp.value is not None else None
    except Exception as exc:  # pragma: no cover - runtime errors
        logger.error("OBD engine load read failed: %s", exc)
        return None
