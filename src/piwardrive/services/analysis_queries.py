"""Database analysis query helpers."""

from __future__ import annotations

import hashlib
import threading
from typing import Any, Sequence

from cachetools import TTLCache

from piwardrive.cache import RedisCache
from piwardrive.database_service import db_service

_CACHE_TTL = 300
_CACHE_MAX_SIZE = 128

_local_cache: TTLCache[str, list[dict[str, Any]]] = TTLCache(
    maxsize=_CACHE_MAX_SIZE, ttl=_CACHE_TTL
)
_cache_lock = threading.Lock()
_remote_cache = RedisCache(prefix="analysis")


async def _cached_fetch(
    key: str, query: str, params: Sequence[Any] | None = None, ttl: int = _CACHE_TTL
) -> list[dict[str, Any]]:
    params = params or []
    digest = hashlib.sha256(repr((key, params)).encode()).hexdigest()
    cache_key = f"{key}:{digest}"
    with _cache_lock:
        _local_cache.expire()
        result = _local_cache.get(cache_key)
    if result is not None:
        return result
    result = await _remote_cache.get(cache_key)
    if result is not None:
        with _cache_lock:
            _local_cache[cache_key] = result
        return result
    result = await db_service.fetch(query, *params)
    with _cache_lock:
        _local_cache[cache_key] = result
    await _remote_cache.set(cache_key, result, ttl)
    return result


async def evil_twin_detection() -> list[dict[str, Any]]:
    """Detect potential evil twin access points with duplicate SSIDs.
    
    Returns:
        List of SSIDs with multiple BSSIDs that could indicate evil twins.
    """
    query = """
        SELECT
            ssid,
            COUNT(DISTINCT bssid) as bssid_count,
            GROUP_CONCAT(DISTINCT bssid) as bssids,
            GROUP_CONCAT(DISTINCT vendor_name) as vendors
        FROM wifi_detections
        WHERE ssid IS NOT NULL
          AND ssid != ''
        GROUP BY ssid
        HAVING COUNT(DISTINCT bssid) > 1
        ORDER BY bssid_count DESC
    """
    return await _cached_fetch("evil_twin", query)


async def signal_strength_analysis() -> list[dict[str, Any]]:
    """Analyze signal strength patterns across geographical locations.
    
    Returns:
        List of signal strength data grouped by location and BSSID.
    """
    query = """
        SELECT
            ROUND(latitude, 3) as lat,
            ROUND(longitude, 3) as lon,
            bssid,
            ssid,
            AVG(signal_strength_dbm) as avg_signal,
            COUNT(*) as detection_count,
            MIN(detection_timestamp) as first_seen,
            MAX(detection_timestamp) as last_seen
        FROM wifi_detections
        WHERE latitude IS NOT NULL
        GROUP BY ROUND(latitude, 3), ROUND(longitude, 3), bssid
        ORDER BY avg_signal DESC
    """
    return await _cached_fetch("signal_strength", query)


async def network_security_analysis() -> list[dict[str, Any]]:
    """Analyze network security configurations and encryption types.
    
    Returns:
        List of encryption type statistics with counts and percentages.
    """
    query = """
        SELECT
            encryption_type,
            COUNT(*) as network_count,
            COUNT(DISTINCT vendor_name) as vendor_count,
            AVG(signal_strength_dbm) as avg_signal,
            ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
        FROM wifi_detections
        GROUP BY encryption_type
        ORDER BY network_count DESC
    """
    return await _cached_fetch("network_security", query)


async def temporal_pattern_analysis() -> list[dict[str, Any]]:
    """Analyze WiFi detection patterns across time periods.
    
    Returns:
        List of detection statistics grouped by hour and day of week.
    """
    query = """
        SELECT
            strftime('%H', detection_timestamp) as hour,
            strftime('%w', detection_timestamp) as day_of_week,
            COUNT(*) as detection_count,
            COUNT(DISTINCT bssid) as unique_networks,
            AVG(signal_strength_dbm) as avg_signal
        FROM wifi_detections
        GROUP BY hour, day_of_week
        ORDER BY hour, day_of_week
    """
    return await _cached_fetch("temporal_pattern", query)


async def mobile_device_detection() -> list[dict[str, Any]]:
    """Detect potentially mobile devices based on location and speed patterns.
    
    Returns:
        List of devices with multiple locations or high speeds indicating mobility.
    """
    query = """
        SELECT
            bssid,
            ssid,
            vendor_name,
            COUNT(DISTINCT ROUND(latitude,
                3) || ',
                ' || ROUND(longitude,
                3)) as unique_locations,

            MAX(speed_kmh) as max_speed,
            AVG(signal_strength_dbm) as avg_signal,
            strftime('%s',
                MAX(detection_timestamp)) - strftime('%s',
                MIN(detection_timestamp)) as time_span_seconds
        FROM wifi_detections
        WHERE latitude IS NOT NULL
          AND longitude IS NOT NULL
        GROUP BY bssid
        HAVING unique_locations > 5
           OR max_speed > 10
        ORDER BY unique_locations DESC, max_speed DESC
    """
    return await _cached_fetch("mobile_device", query)


async def clear_cache() -> None:
    """Clear both local and remote analysis query caches."""
    with _cache_lock:
        _local_cache.clear()
    await _remote_cache.clear()


__all__ = [
    "evil_twin_detection",
    "signal_strength_analysis",
    "network_security_analysis",
    "temporal_pattern_analysis",
    "mobile_device_detection",
    "clear_cache",
]
