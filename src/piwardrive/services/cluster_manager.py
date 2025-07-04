from __future__ import annotations

"""Cluster management utilities for distributed deployments."""

import asyncio
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Iterable, List, Optional

import aiohttp

logger = logging.getLogger(__name__)


@dataclass
class DeviceStatus:
    """Metadata about a registered device."""

    id: str
    address: str
    last_seen: datetime = field(default_factory=datetime.utcnow)
    capabilities: List[str] = field(default_factory=list)
    load: int = 0
    config_version: str | None = None
    health: dict[str, float] = field(default_factory=dict)


class ClusterManager:
    """Manage a fleet of scanning devices."""

    def __init__(self) -> None:
        self._devices: Dict[str, DeviceStatus] = {}

    # Device registration -------------------------------------------------
    def register_device(self, device: DeviceStatus) -> None:
        """Register ``device`` for coordination."""
        self._devices[device.id] = device
        logger.info("Registered device %s at %s", device.id, device.address)

    def unregister_device(self, device_id: str) -> None:
        """Remove ``device_id`` from the fleet."""
        if device_id in self._devices:
            self._devices.pop(device_id)
            logger.info("Unregistered device %s", device_id)

    def get_device(self, device_id: str) -> Optional[DeviceStatus]:
        """Return device metadata if known."""
        return self._devices.get(device_id)

    def list_devices(self) -> List[DeviceStatus]:
        """Return all registered devices."""
        return list(self._devices.values())

    # Device discovery ----------------------------------------------------
    async def discover_devices(self) -> List[DeviceStatus]:
        """Discover devices specified via the ``PW_DEVICES`` environment var."""
        env = os.getenv("PW_DEVICES")
        if not env:
            return []
        discovered: List[DeviceStatus] = []
        tasks = [
            self._probe_device(addr.strip()) for addr in env.split(",") if addr.strip()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for res in results:
            if isinstance(res, DeviceStatus):
                self.register_device(res)
                discovered.append(res)
        return discovered

    async def _probe_device(self, address: str) -> DeviceStatus | None:
        """Return :class:`DeviceStatus` for ``address`` if reachable."""
        try:
            timeout = aiohttp.ClientTimeout(total=2)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"http://{address}/api/info") as resp:
                    data = await resp.json()
            return DeviceStatus(
                id=str(data.get("id", address)),
                address=address,
                capabilities=list(data.get("capabilities", [])),
                config_version=data.get("config_version"),
            )
        except Exception as exc:  # pragma: no cover - network errors
            logger.debug("Failed to probe %s: %s", address, exc)
            return None

    # Load balancing ------------------------------------------------------
    def select_device_for_task(self) -> DeviceStatus | None:
        """Return the least loaded registered device."""
        if not self._devices:
            return None
        return min(self._devices.values(), key=lambda d: d.load)

    # Health monitoring ---------------------------------------------------
    async def update_device_health(self, device: DeviceStatus) -> None:
        """Poll ``device`` for health metrics."""
        try:
            timeout = aiohttp.ClientTimeout(total=5)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"http://{device.address}/api/health") as resp:
                    device.health = await resp.json()
            device.last_seen = datetime.utcnow()
        except Exception as exc:  # pragma: no cover - network errors
            logger.debug("Health request failed for %s: %s", device.id, exc)

    async def collect_health_metrics(self) -> Dict[str, dict[str, float]]:
        """Return latest health metrics for all devices."""
        tasks = [self.update_device_health(dev) for dev in self._devices.values()]
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        return {dev.id: dev.health for dev in self._devices.values()}


__all__ = ["DeviceStatus", "ClusterManager"]
