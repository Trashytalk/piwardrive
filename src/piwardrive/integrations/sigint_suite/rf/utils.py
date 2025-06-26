"""RF helper functions for basic frequency conversions."""

from __future__ import annotations

import re

__all__ = [
    "hz_to_khz",
    "hz_to_mhz",
    "hz_to_ghz",
    "khz_to_hz",
    "mhz_to_hz",
    "ghz_to_hz",
    "parse_frequency",
]


def hz_to_khz(freq: float) -> float:
    """Return ``freq`` expressed in kHz."""
    return freq / 1_000.0


def hz_to_mhz(freq: float) -> float:
    """Return ``freq`` expressed in MHz."""
    return freq / 1_000_000.0


def hz_to_ghz(freq: float) -> float:
    """Return ``freq`` expressed in GHz."""
    return freq / 1_000_000_000.0


def khz_to_hz(freq: float) -> float:
    """Return ``freq`` expressed in Hz from kHz."""
    return freq * 1_000.0


def mhz_to_hz(freq: float) -> float:
    """Return ``freq`` expressed in Hz from MHz."""
    return freq * 1_000_000.0


def ghz_to_hz(freq: float) -> float:
    """Return ``freq`` expressed in Hz from GHz."""
    return freq * 1_000_000_000.0


_UNIT_MAP = {
    "hz": 1.0,
    "khz": 1_000.0,
    "mhz": 1_000_000.0,
    "ghz": 1_000_000_000.0,
}


def parse_frequency(value: str | float) -> float:
    """Return frequency in Hz parsed from ``value``.

    Strings may include units like ``kHz``, ``MHz`` or ``GHz`` (case-insensitive).
    Numbers are assumed to already be in Hz.
    """

    if isinstance(value, (int, float)):
        return float(value)

    match = re.match(r"\s*(\d+(?:\.\d+)?)([kKmMgG]?Hz)?\s*", value)
    if not match:
        raise ValueError(f"invalid frequency: {value!r}")

    number = float(match.group(1))
    unit = (match.group(2) or "Hz").lower()
    scale = _UNIT_MAP.get(unit, 1.0)
    return number * scale
