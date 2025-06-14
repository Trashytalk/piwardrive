from __future__ import annotations

"""Simple FastAPI service for health records."""

from dataclasses import asdict

from fastapi import FastAPI

from persistence import load_recent_health

app = FastAPI()


@app.get("/status")
def get_status(limit: int = 5) -> list[dict]:
    """Return ``limit`` most recent :class:`HealthRecord` entries."""
    records = load_recent_health(limit)
    return [asdict(rec) for rec in records]


def main() -> None:
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
