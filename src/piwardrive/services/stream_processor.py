from __future__ import annotations

"""Real-time detection processing service."""

import asyncio
import contextlib
import time
from typing import Any, Dict, Iterable, Mapping

from piwardrive.services import network_fingerprinting, security_analyzer


class StreamProcessor:
    """Process detection events and broadcast results."""

    def __init__(
        self,
        *,
        max_queue: int = 1000,
        listener_queue: int = 100,
        rate_limit: float = 20.0,
    ) -> None:
        self._queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue(maxsize=max_queue)
        self._listeners: set[asyncio.Queue[dict[str, Any]]] = set()
        self._listener_size = listener_queue
        self._rate_limit = rate_limit
        self._task: asyncio.Task[None] | None = None
        self._running = False
        self.stats: Dict[str, int] = {
            "wifi": 0,
            "bluetooth": 0,
            "cellular": 0,
            "alerts": 0,
        }

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        self._running = False
        if self._task is not None:
            self._task.cancel()
            with contextlib.suppress(Exception):
                await self._task
            self._task = None

    def register_listener(self) -> asyncio.Queue[dict[str, Any]]:
        q: asyncio.Queue[dict[str, Any]] = asyncio.Queue(maxsize=self._listener_size)
        self._listeners.add(q)
        if not self._running:
            asyncio.create_task(self.start())
        return q

    def unregister_listener(self, q: asyncio.Queue[dict[str, Any]]) -> None:
        self._listeners.discard(q)

    def _enqueue(self, source: str, records: Iterable[Mapping[str, Any]]) -> None:
        if not records:
            return
        try:
            self._queue.put_nowait({"source": source, "records": list(records)})
        except asyncio.QueueFull:
            # drop the oldest item if queue is full
            try:
                _ = self._queue.get_nowait()
                self._queue.task_done()
                self._queue.put_nowait({"source": source, "records": list(records)})
            except Exception:
                pass

    def publish_wifi(self, records: Iterable[Mapping[str, Any]]) -> None:
        self._enqueue("wifi", records)

    def publish_bluetooth(self, records: Iterable[Mapping[str, Any]]) -> None:
        self._enqueue("bluetooth", records)

    def publish_cellular(self, records: Iterable[Mapping[str, Any]]) -> None:
        self._enqueue("cellular", records)

    async def _process_wifi(self, records: list[dict[str, Any]]) -> None:
        await network_fingerprinting.fingerprint_wifi_records(records)
        await security_analyzer.analyze_wifi_records(records)

    async def _run(self) -> None:
        sleep = 1.0 / self._rate_limit if self._rate_limit > 0 else 0.0
        while self._running:
            event = await self._queue.get()
            source = event.get("source")
            records = event.get("records", [])
            if source == "wifi":
                await self._process_wifi(records)
            self.stats[source] = self.stats.get(source, 0) + len(records)
            payload = {
                "timestamp": time.time(),
                "source": source,
                "records": records,
                "stats": self.stats,
            }
            for q in list(self._listeners):
                try:
                    q.put_nowait(payload)
                except asyncio.QueueFull:
                    pass
            self._queue.task_done()
            if sleep:
                await asyncio.sleep(sleep)


stream_processor = StreamProcessor()
