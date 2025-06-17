"""LoRa/IoT radio scanning integration."""

from __future__ import annotations

import logging
import subprocess
from dataclasses import dataclass
from typing import List, Sequence
import re

logger = logging.getLogger(__name__)


def scan_lora(interface: str = "lora0") -> List[str]:
    """Invoke an external LoRa scanning tool and return raw lines."""
    cmd = ["lora-scan", "--iface", interface]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return proc.stdout.splitlines()
    except Exception as exc:  # pragma: no cover - runtime errors
        logger.error("LoRa scan failed: %s", exc)
        return []


@dataclass
class LoRaPacket:
    """Parsed information about a LoRa packet."""

    timestamp: str | None
    freq: float | None
    rssi: float | None
    snr: float | None
    devaddr: str | None
    raw: str


def parse_packets(lines: Sequence[str]) -> List[LoRaPacket]:
    """Return :class:`LoRaPacket` objects parsed from ``lines``."""

    def _to_float(val: str | None) -> float | None:
        try:
            return float(val) if val is not None else None
        except ValueError:
            return None

    packets: List[LoRaPacket] = []
    for line in lines:
        fields = dict(re.findall(r"(\w+)=([\w.:-]+)", line))
        pkt = LoRaPacket(
            timestamp=fields.get("time"),
            freq=_to_float(fields.get("freq")),
            rssi=_to_float(fields.get("rssi")),
            snr=_to_float(fields.get("snr")),
            devaddr=fields.get("devaddr"),
            raw=line,
        )
        packets.append(pkt)
    return packets


def plot_signal_trend(packets: Sequence[LoRaPacket], path: str) -> None:
    """Plot RSSI trend from ``packets`` to ``path`` using matplotlib."""

    rssi = [p.rssi for p in packets if p.rssi is not None]
    if not rssi:
        with open(path, "wb") as fh:
            fh.write(b"")
        return

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:  # pragma: no cover - optional dependency
        with open(path, "wb") as fh:
            fh.write(b"")
        return

    plt.figure(figsize=(4, 2))
    plt.plot(rssi)
    plt.xlabel("packet")
    plt.ylabel("rssi")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
