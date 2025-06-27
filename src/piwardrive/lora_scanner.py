"""LoRa/IoT radio scanning integration."""

from __future__ import annotations

import asyncio
import logging
import re
import subprocess  # nosec B404
from dataclasses import dataclass
from typing import List, Sequence

profile = globals().get("profile", lambda f: f)  # type: ignore[no-redef]


PACKET_RE = re.compile(r"(\w+)=([\w.:-]+)")

logger = logging.getLogger(__name__)


def scan_lora(interface: str = "lora0") -> List[str]:
    """Invoke an external LoRa scanning tool and return raw lines."""
    cmd = ["lora-scan", "--iface", interface]
    try:
        proc = subprocess.run(  # nosec B603
            cmd, capture_output=True, text=True, check=True
        )
        return proc.stdout.splitlines()
    except Exception as exc:  # pragma: no cover - runtime errors
        logger.error("LoRa scan failed: %s", exc)
        return []


async def async_scan_lora(interface: str = "lora0") -> List[str]:
    """Asynchronously invoke the LoRa scanning tool and return raw lines."""
    cmd = ["lora-scan", "--iface", interface]
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
        stdout, _ = await proc.communicate()
        return stdout.decode().splitlines()
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


@profile
def parse_packets(
    lines: Sequence[str], packet_re: re.Pattern[str] = PACKET_RE
) -> List[LoRaPacket]:
    """Return :class:`LoRaPacket` objects parsed from ``lines``."""

    def _to_float(val: str | None) -> float | None:
        try:
            return float(val) if val is not None else None
        except ValueError:
            return None

    packets: List[LoRaPacket] = []
    findall = packet_re.findall
    for line in lines:
        fields = dict(findall(line))
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


@profile
def parse_packets_pandas(lines: Sequence[str]) -> List[LoRaPacket]:
    """Parse packets using pandas for better throughput on large inputs."""
    if not lines:
        return []

    import pandas as pd  # local import to avoid optional dependency

    def _to_float(val: str | None) -> float | None:
        try:
            return float(val) if val is not None else None
        except ValueError:
            return None

    df = pd.DataFrame([dict(PACKET_RE.findall(line)) for line in lines])
    packets: List[LoRaPacket] = []
    for raw, row in zip(lines, df.to_dict(orient="records")):
        packets.append(
            LoRaPacket(
                timestamp=row.get("time"),
                freq=_to_float(row.get("freq")),
                rssi=_to_float(row.get("rssi")),
                snr=_to_float(row.get("snr")),
                devaddr=row.get("devaddr"),
                raw=raw,
            )
        )
    return packets


async def async_parse_packets(lines: Sequence[str]) -> List[LoRaPacket]:
    """Asynchronously parse packets from ``lines``."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, parse_packets, lines)


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


def main() -> None:  # pragma: no cover - CLI helper
    """Run a LoRa scan and print results."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Scan LoRa devices")
    parser.add_argument("--iface", default="lora0", help="LoRa interface")
    parser.add_argument("--json", action="store_true", help="print as JSON")
    args = parser.parse_args()

    lines = scan_lora(args.iface)
    if args.json:
        packets = [p.__dict__ for p in parse_packets(lines)]
        print(json.dumps(packets, indent=2))
    else:
        for line in lines:
            print(line)


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
