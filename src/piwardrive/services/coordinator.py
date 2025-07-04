from __future__ import annotations

"""Utilities for coordinating distributed scanning tasks."""

import asyncio
import logging
from typing import Dict, Iterable, List, Mapping

import aiohttp

from piwardrive.core import config

from .cluster_manager import ClusterManager, DeviceStatus

logger = logging.getLogger(__name__)


# Default global manager instance used by helper functions
cluster_manager = ClusterManager()


async def coordinate_scanning_tasks(
    tasks: Iterable[Mapping[str, object]],
    manager: ClusterManager = cluster_manager,
) -> Dict[str, List[Mapping[str, object]]]:
    """Distribute ``tasks`` across available devices using load balancing."""
    assignments: Dict[str, List[Mapping[str, object]]] = {}
    for task in tasks:
        device = manager.select_device_for_task()
        if device is None:
            logger.warning("No devices available for task %s", task)
            break
        await _dispatch_task(device, task)
        device.load += 1
        assignments.setdefault(device.id, []).append(task)
    return assignments


async def _dispatch_task(device: DeviceStatus, task: Mapping[str, object]) -> None:
    """Send ``task`` to ``device`` via HTTP."""
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            await session.post(f"http://{device.address}/api/scan", json=task)
    except Exception as exc:  # pragma: no cover - network errors
        logger.error("Failed to dispatch task to %s: %s", device.id, exc)


def aggregate_distributed_results(
    results: Iterable[Iterable[Mapping[str, object]]],
) -> List[Mapping[str, object]]:
    """Combine scan results from multiple devices into a single list."""
    merged: List[Mapping[str, object]] = []
    for chunk in results:
        merged.extend(list(chunk))
    return merged


async def manage_device_fleet(
    manager: ClusterManager = cluster_manager,
) -> ClusterManager:
    """Discover devices and refresh their health status."""
    await manager.discover_devices()
    await manager.collect_health_metrics()
    return manager


async def synchronize_configurations(
    manager: ClusterManager = cluster_manager,
) -> None:
    """Ensure all devices share the same configuration."""
    cfg = config.AppConfig.load().to_dict()
    tasks = []
    for dev in manager.list_devices():
        if dev.config_version == cfg.get("config_version"):
            continue
        tasks.append(_push_config(dev, cfg))
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)


async def _push_config(device: DeviceStatus, cfg: Mapping[str, object]) -> None:
    try:
        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            await session.post(f"http://{device.address}/api/config", json=cfg)
        device.config_version = str(cfg.get("config_version"))
    except Exception as exc:  # pragma: no cover - network errors
        logger.error("Failed to sync config to %s: %s", device.id, exc)


__all__ = [
    "cluster_manager",
    "coordinate_scanning_tasks",
    "aggregate_distributed_results",
    "manage_device_fleet",
    "synchronize_configurations",
]
