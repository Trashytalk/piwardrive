from __future__ import annotations

"""Simple FastAPI service for health records."""

from dataclasses import asdict

import asyncio
from fastapi import FastAPI

from persistence import load_recent_health

app = FastAPI()


@app.get("/status")
async def get_status(limit: int = 5) -> list[dict]:
    """Return ``limit`` most recent :class:`HealthRecord` entries."""
    records = await asyncio.to_thread(load_recent_health, limit)
    return [asdict(rec) for rec in records]


async def main() -> None:
    import uvicorn

    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
