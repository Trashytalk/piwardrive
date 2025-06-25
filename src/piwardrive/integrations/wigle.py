"""Helpers for interacting with the WiGLE API."""

from __future__ import annotations

import aiohttp
from typing import Any, Dict, List


async def fetch_wigle_networks(
    api_name: str,
    api_key: str,
    lat: float,
    lon: float,
    *,
    radius: float = 0.01,
) -> List[Dict[str, Any]]:
    """
    Retrieve nearby Wi-Fi networks from the WiGLE API based on geographic coordinates.
    
    Parameters:
        api_name (str): WiGLE API username.
        api_key (str): WiGLE API key.
        lat (float): Latitude of the center point.
        lon (float): Longitude of the center point.
        radius (float, optional): Search radius in degrees for the bounding box (default is 0.01).
    
    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing the BSSID, SSID, encryption type, latitude, and longitude of a detected Wi-Fi network.
    """

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
