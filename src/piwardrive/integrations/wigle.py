"""Helpers for interacting with the WiGLE API."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, Dict, List

from piwardrive.core.utils import WIGLE_CACHE_SECONDS, async_ttl_cache

try:  # pragma: no cover - optional dependency
    import aiohttp
    if not hasattr(aiohttp, "BasicAuth"):
        raise ImportError("incomplete aiohttp")
except Exception:  # pragma: no cover - aiohttp not installed or incomplete
    aiohttp = SimpleNamespace(
        BasicAuth=lambda *_a, **_k: None,
        ClientTimeout=lambda *_a, **_k: None,
        ClientSession=None,
    )


@async_ttl_cache(lambda: WIGLE_CACHE_SECONDS)
async def fetch_wigle_networks(
    api_name: str,
    api_key: str,
    lat: float,
    lon: float,
    *,
    radius: float = 0.01,
) -> List[Dict[str, Any]]:
    """Return Wi-Fi networks around ``lat``/``lon`` via the WiGLE API."""
    auth = aiohttp.BasicAuth(api_name, api_key)
    params = {
        "latrange1": lat - radius,
        "latrange2": lat + radius,
        "longrange1": lon - radius,
        "longrange2": lon + radius,
        "resultsPerPage": 100,
    }
    url = "https://api.wigle.net/api/v2/network/search"
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, params=params, auth=auth) as resp:
            resp.raise_for_status()
            data = await resp.json()
    nets = []
    for rec in data.get("results", []):
        lat_val = rec.get("trilat")
        lon_val = rec.get("trilong")
        if lat_val is None or lon_val is None:
            continue
        nets.append(
            {
                "bssid": rec.get("netid"),
                "ssid": rec.get("ssid"),
                "encryption": rec.get("encryption"),
                "lat": lat_val,
                "lon": lon_val,
            }
        )
    return nets


__all__ = ["fetch_wigle_networks", "aiohttp"]
