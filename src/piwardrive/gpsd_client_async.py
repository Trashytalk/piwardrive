"""Asynchronous client for ``gpsd`` using a persistent connection."""

from __future__ import annotations

import asyncio
import json
import logging
import os
from typing import Any


class AsyncGPSDClient:
    """Minimal async interface to a running ``gpsd`` daemon."""

    def __init__(self, host: str | None = None, port: int | None = None) -> None:
        self.host = host or os.getenv("PW_GPSD_HOST", "127.0.0.1")
        self.port = port or int(os.getenv("PW_GPSD_PORT", 2947))
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None
        self._lock = asyncio.Lock()
        self._connected = False

    async def __aenter__(self) -> "AsyncGPSDClient":
        await self._ensure_connection()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def _connect(self) -> None:
        try:
            self._reader, self._writer = await asyncio.open_connection(
                self.host, self.port
            )
            await self._reader.readline()  # VERSION greeting
            assert self._writer is not None
            self._writer.write(b'?WATCH={"enable":true,"json":true}\n')
            await self._writer.drain()
            # Discard the device list and initial TPV if sent
            await self._reader.readline()
            await self._reader.readline()
            self._connected = True
        except Exception as exc:  # pragma: no cover - connection errors
            logging.getLogger(__name__).error("GPSD connect failed: %s", exc)
            self._connected = False

    async def _ensure_connection(self) -> None:
        if not self._connected:
            await self._connect()

    async def close(self) -> None:
        """Close the GPSD connection if open."""
        writer = self._writer
        self._writer = None
        self._reader = None
        self._connected = False
        if writer is not None:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception as exc:  # pragma: no cover - close errors
                logging.getLogger(__name__).error("GPSD close failed: %s", exc)

    async def _poll(self) -> dict[str, Any] | None:
        async with self._lock:
            await self._ensure_connection()
            if not self._connected or self._writer is None or self._reader is None:
                return None
            try:
                self._writer.write(b"?POLL;\n")
                await self._writer.drain()
                line = await self._reader.readline()
                data = json.loads(line.decode())
                if data.get("class") != "POLL":
                    return None
                tpv_list = data.get("tpv") or []
                if tpv_list:
                    return tpv_list[-1]
                return None
            except Exception as exc:  # pragma: no cover - runtime errors
                logging.getLogger(__name__).error("GPSD poll failed: %s", exc)
                self._connected = False
                return None

    async def get_position_async(self) -> tuple[float, float] | None:
        tpv = await self._poll()
        if not tpv:
            return None
        lat = tpv.get("lat")
        lon = tpv.get("lon")
        if lat is None or lon is None:
            return None
        return float(lat), float(lon)

    async def get_accuracy_async(self) -> float | None:
        tpv = await self._poll()
        if not tpv:
            return None
        epx = tpv.get("epx")
        epy = tpv.get("epy")
        if epx is None or epy is None:
            return None
        return float(max(epx, epy))

    async def get_fix_quality_async(self) -> str:
        tpv = await self._poll()
        if not tpv:
            return "Unknown"
        mode = tpv.get("mode")
        mode_map = {1: "No Fix", 2: "2D", 3: "3D", 4: "DGPS"}
        if isinstance(mode, int):
            return mode_map.get(mode, str(mode))
        return str(mode)


async_client = AsyncGPSDClient()
