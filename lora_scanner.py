"""LoRa/IoT radio scanning integration."""

from __future__ import annotations

import logging
import subprocess
from typing import List

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
