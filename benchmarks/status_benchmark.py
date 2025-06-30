"""Benchmark the REST status endpoint."""

import asyncio
import logging
import time

from httpx import ASGITransport, AsyncClient

from service import app


async def main(count: int = 100) -> None:
    """Send ``count`` requests to the status endpoint."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        start = time.perf_counter()
        tasks = [client.get("/status") for _ in range(count)]
        await asyncio.gather(*tasks)
        duration = time.perf_counter() - start
    logging.info(
        "%d requests in %.2fs (%.1f r/s)",
        count,
        duration,
        count / duration,
    )


if __name__ == "__main__":
    asyncio.run(main())
