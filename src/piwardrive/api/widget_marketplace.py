from __future__ import annotations

"""Simple widget marketplace API."""

import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter

from piwardrive import service

router = APIRouter(prefix="/widget-marketplace", tags=["widget-marketplace"])

MARKET_PATH = Path(__file__).resolve().parents[2] / "widgets" / "marketplace.json"


def _load_market() -> dict[str, Any]:
    try:
        with open(MARKET_PATH, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return {"widgets": []}


@router.get("")
async def list_market(_auth: Any = service.AUTH_DEP) -> dict[str, Any]:
    """Return available marketplace entries."""
    return _load_market()


@router.post("/install")
async def install_widget(
    data: dict[str, Any], _auth: Any = service.AUTH_DEP
) -> dict[str, Any]:
    """Pretend to install a widget and return success."""
    name = data.get("name", "")
    # Real installation would fetch and place plugin files
    return {"installed": bool(name)}


__all__ = ["router"]
