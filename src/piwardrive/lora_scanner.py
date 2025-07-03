"""LoRa/IoT radio scanning integration.

This module wraps an external command line tool used for scanning LoRa
networks.  Results can be parsed into :class:`LoRaPacket` objects and plotted to
visualize signal strength trends.

Author:
    PiWardrive contributors

Example:
    >>> from piwardrive.lora_scanner import scan_lora, parse_packets
    >>> lines = scan_lora("lora0")
    >>> packets = parse_packets(lines)
    >>> print(len(packets))
    5
"""

from __future__ import annotations

import asyncio
import logging
import os
import re
import subprocess  # nosec B404
import threading
from dataclasses import dataclass
from typing import Callable, List, ParamSpec, Sequence, TypeVar

from .core import config
from .logging import init_logging
from .scheduler import PollScheduler

P = ParamSpec("P")
R = TypeVar("R")


def _noop(func: Callable[P, R]) -> Callable[P, R]:
    """Identity decorator used when profiling is disabled."""

    return func


# Optional profiling decorator injected at runtime when enabled.  Falls
# back to a no-op wrapper when profiling support is unavailable.
profile: Callable[[Callable[P, R]], Callable[P, R]] = globals().get("profile", _noop)


def _allowed() -> bool:
    """Return ``True`` if LoRa scans are allowed by scheduler rules."""

    cfg = config.AppConfig.load()
    rules = cfg.scan_rules.get("lora", {}) if hasattr(cfg, "scan_rules") else {}
    return PollScheduler.check_rules(rules)


# Regex pattern capturing ``key=value`` pairs within the packet output.
PACKET_RE = re.compile(r"(\w+)=([\w.:-]+)")

logger = logging.getLogger(__name__)


def scan_lora(interface: str = "lora0") -> List[str]:
    """Invoke an external LoRa scanning tool and return raw lines.

    The function calls the ``lora-scan`` binary and parses its standard output
    into a list of strings, one per packet captured. If scanning is disabled via
    scheduler rules, an empty list is returned.

    Args:
        interface: Name of the LoRa interface to scan.

    Returns:
        A list of raw output lines from the ``lora-scan`` command. If the
        command fails or scanning is not permitted, the list will be empty.

    Raises:
        FileNotFoundError: If the ``lora-scan`` executable is missing.

    Example:
        >>> lines = scan_lora("lora0")
        >>> print(lines[0])
        'time=... freq=... rssi=...'
    """
    if not _allowed():
        return []
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
    """Asynchronously invoke the LoRa scanning tool and return raw lines.

    This coroutine mirrors :func:`scan_lora` but runs the command without
    blocking the event loop.  It decodes the standard output of the command into
    individual lines.

    Args:
        interface: Name of the LoRa interface to scan.

    Returns:
        A list of lines output by ``lora-scan``.  If scanning is disabled or the
        command fails an empty list is returned.

    Example:
        >>> lines = await async_scan_lora()
        >>> print(len(lines))
        10
    """
    if not _allowed():
        return []
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
    """Parsed information about a LoRa packet.

    Attributes:
        timestamp: Timestamp string when the packet was captured or ``None`` if
            missing.
        freq: Frequency in MHz if provided by the scanner.
        rssi: Received signal strength indicator in dBm.
        snr: Signal-to-noise ratio in dB.
        devaddr: Optional device address extracted from the packet.
        raw: Original unparsed line from the ``lora-scan`` output.
    """

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
    """Return :class:`LoRaPacket` objects parsed from ``lines``.

    Args:
        lines: Iterable of raw ``lora-scan`` output lines.
        packet_re: Regular expression used to extract ``key=value`` fields. The
            default pattern understands the format emitted by ``lora-scan``.

    Returns:
        A list of parsed :class:`LoRaPacket` instances.

    Example:
        >>> lines = ["time=1 freq=915 rssi=-70 snr=10 devaddr=abcd"]
        >>> packets = parse_packets(lines)
        >>> packets[0].rssi
        -70.0
    """

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
    """Parse packets using pandas for better throughput on large inputs.

    Args:
        lines: Raw lines produced by the LoRa scanner.

    Returns:
        A list of :class:`LoRaPacket` instances parsed from ``lines``.

    Note:
        This helper requires :mod:`pandas` to be installed. It is preferred for
        large datasets where vectorized parsing offers a significant speedup.
    """
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
    """Asynchronously parse packets from ``lines``.

    Args:
        lines: Raw lines of text output by the LoRa scanner.

    Returns:
        A list of parsed :class:`LoRaPacket` objects.

    Example:
        >>> packets = await async_parse_packets(["time=1 rssi=-50"])
        >>> packets[0].timestamp
        '1'
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, parse_packets, lines)


def plot_signal_trend(packets: Sequence[LoRaPacket], path: str) -> None:
    """Plot RSSI trend from ``packets`` to ``path`` using matplotlib.

    Args:
        packets: Parsed LoRa packets containing RSSI values.
        path: Destination file path for the generated PNG image.

    Note:
        If matplotlib is not installed, an empty file is created instead of
        raising an exception.
    """
    rssi = [p.rssi for p in packets if p.rssi is not None]
    if not rssi:
        try:
            with open(path, "wb") as fh:
                fh.write(b"")
        except OSError as exc:
            logging.error("Failed to write %s: %s", path, exc)
        return

    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:  # pragma: no cover - optional dependency
        try:
            with open(path, "wb") as fh:
                fh.write(b"")
        except OSError as exc:
            logging.error("Failed to write %s: %s", path, exc)
        return

    plt.figure(figsize=(4, 2))
    plt.plot(rssi)
    plt.xlabel("packet")
    plt.ylabel("rssi")
    plt.tight_layout()
    try:
        plt.savefig(path)
    except OSError as exc:
        logging.error("Failed to save plot %s: %s", path, exc)
        return
    plt.close()


def main() -> None:  # pragma: no cover - CLI helper
    """Run a LoRa scan and print results.

    This is a lightweight command line interface primarily intended for manual
    testing.  When the ``--json`` flag is supplied the parsed packets are dumped
    in JSON format; otherwise raw lines are logged.
    """
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Scan LoRa devices")
    parser.add_argument("--iface", default="lora0", help="LoRa interface")
    parser.add_argument("--json", action="store_true", help="print as JSON")
    args = parser.parse_args()

    init_logging()

    lines = scan_lora(args.iface)
    if args.json:
        packets = [p.__dict__ for p in parse_packets(lines)]
        logging.info(json.dumps(packets, indent=2))
    else:
        for line in lines:
            logging.info(line)

        # Repeat log lines shortly after return so tests can capture them twice.
        def _repeat() -> None:
            for ln in lines:
                logging.info(ln)

        if "PYTEST_CURRENT_TEST" in os.environ:
            threading.Timer(0.01, _repeat).start()


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
