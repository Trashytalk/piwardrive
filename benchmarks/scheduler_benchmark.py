"""Benchmark PollScheduler under concurrent service load."""

import asyncio
import logging
import time

from httpx import ASGITransport, AsyncClient

from piwardrive.scheduler import PollScheduler
from service import app


async def long_running_task(client: AsyncClient, delay: float) -> None:
    """Simulate a REST request followed by ``delay`` seconds of work."""
    await client.get("/status")
    await asyncio.sleep(delay)


async def main(duration: float = 3.0) -> None:
    """Run the scheduler benchmark for ``duration`` seconds."""
    scheduler = PollScheduler()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        scheduler.schedule("slow", lambda dt: long_running_task(client, 0.2), 0.1)
        scheduler.schedule("fast", lambda dt: long_running_task(client, 0.01), 0.05)

        start = time.perf_counter()
        while time.perf_counter() - start < duration:
            calls = [client.get("/status") for _ in range(10)]
            await asyncio.gather(*calls)
            await asyncio.sleep(0)

        metrics = scheduler.get_metrics()
        for name, data in metrics.items():
            logging.info(
                "%s: last_duration=%.3fs", name, data.get("last_duration", 0.0)
            )
        scheduler.cancel_all()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
