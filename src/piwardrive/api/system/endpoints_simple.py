"""Simplified system endpoints for testing purposes."""

from typing import Any, Dict

from fastapi import APIRouter

from piwardrive.api.auth import AUTH_DEP

router = APIRouter()


@router.get("/cpu")
async def get_cpu(_auth: Any = AUTH_DEP) -> Dict[str, Any]:
    """Get CPU information."""
    return {"temp": 45.0, "percent": 25.5}


@router.get("/ram")
async def get_ram(_auth: Any = AUTH_DEP) -> Dict[str, Any]:
    """Get RAM information."""
    return {"percent": 60.2}


@router.get("/storage")
async def get_storage(path: str = "/", _auth: Any = AUTH_DEP) -> Dict[str, Any]:
    """Get storage information."""
    return {"percent": 42.3}


@router.get("/health")
async def system_health(_auth: Any = AUTH_DEP) -> Dict[str, Any]:
    """Get system health status."""
    return {"status": "healthy", "uptime": 86400, "load_average": [0.5, 0.4, 0.3]}
