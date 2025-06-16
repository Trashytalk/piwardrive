import asyncio
import math
import os
from typing import Callable
import aiohttp
from kivymd.toast import toast


def deg2num(lat: float, lon: float, zoom: int) -> tuple[int, int]:
    """Convert latitude and longitude to XYZ tile coordinates."""
    lat_rad = math.radians(lat)
    n = 2 ** zoom
    x = int((lon + 180.0) / 360.0 * n)
    y = int((1.0 - math.log(math.tan(lat_rad) + 1 / math.cos(lat_rad)) / math.pi) / 2.0 * n)
    return x, y


async def download_tile_async(session: aiohttp.ClientSession, url: str, local: str) -> None:
    """Fetch a single tile from ``url`` into ``local`` asynchronously."""
    async with session.get(url) as resp:
        resp.raise_for_status()
        data = await resp.read()
    os.makedirs(os.path.dirname(local), exist_ok=True)
    with open(local, "wb") as fh:
        fh.write(data)


def prefetch_tiles(
    bounds,
    zoom: int = 16,
    folder: str = "/mnt/ssd/tiles",
    *,
    concurrency: int | None = None,
    progress_cb: Callable[[int, int], None] | None = None,
) -> None:
    """Download PNG tiles covering ``bounds`` to ``folder``."""
    try:
        min_lat, min_lon, max_lat, max_lon = bounds
        zoom = int(zoom)
        x1, y1 = deg2num(max_lat, min_lon, zoom)
        x2, y2 = deg2num(min_lat, max_lon, zoom)
        x_min, x_max = sorted((x1, x2))
        y_min, y_max = sorted((y1, y2))
        base_url = "https://tile.openstreetmap.org"
        tasks = []
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                url = f"{base_url}/{zoom}/{x}/{y}.png"
                local = os.path.join(folder, str(zoom), str(x), f"{y}.png")
                tasks.append((url, local))
        total = len(tasks)
        completed = 0

        async def _run() -> None:
            sem = asyncio.Semaphore(concurrency or os.cpu_count() or 4)
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async def _task(url: str, local: str) -> None:
                    nonlocal completed
                    async with sem:
                        if not os.path.exists(local):
                            await download_tile_async(session, url, local)
                    completed += 1
                    if progress_cb:
                        progress_cb(completed, total)
                await asyncio.gather(*[asyncio.create_task(_task(u, l)) for u, l in tasks])

        fut = asyncio.run(_run())
        return fut
    except Exception as exc:  # pragma: no cover - network errors
        toast(f"Prefetch error: {exc}")
