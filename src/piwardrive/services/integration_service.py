"""Helpers for interacting with external services.

This module provides utilities for integrating with external APIs and services,
including rate-limited HTTP clients, authentication handling, and data
synchronization capabilities for third-party integrations.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any, Iterable, Mapping

import httpx

from piwardrive.logging.filters import RateLimiter

logger = logging.getLogger(__name__)


class APIClient:
    """HTTP client with token auth and simple rate limiting."""

    def __init__(
        self, token: str | None = None, *, max_rate: int = 60, window: int = 60
    ) -> None:
        """Initialize the API client.
        
        Args:
            token: Optional authentication token.
            max_rate: Maximum requests per window (default 60).
            window: Rate limiting window in seconds (default 60).
        """
        self.token = token
        self.rate_limiter = RateLimiter(max_rate, window)

    async def request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        """Make an HTTP request with rate limiting and authentication.
        
        Args:
            method: HTTP method (GET, POST, etc.).
            url: Request URL.
            **kwargs: Additional arguments passed to httpx.
            
        Returns:
            HTTP response object.
            
        Raises:
            RuntimeError: If rate limit is exceeded.
        """
        if not self.rate_limiter.should_allow(url):
            raise RuntimeError("rate limit exceeded")
        headers = kwargs.pop("headers", {})
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        async with httpx.AsyncClient() as client:
            resp = await client.request(method, url, headers=headers, **kwargs)
            resp.raise_for_status()
            return resp


async def fetch_stix_taxii(
    url: str, collection: str, client: APIClient
) -> list[Mapping[str, Any]]:
    """Fetch STIX indicators from a TAXII collection."""
    endpoint = f"{url.rstrip('/')}/collections/{collection}/objects"
    resp = await client.request("GET", endpoint)
    _data = resp.json()
    objects = _data.get("objects", []) if isinstance(_data, Mapping) else []
    return [obj for obj in objects if isinstance(obj, Mapping)]


async def send_to_elasticsearch(
    url: str, index: str, records: Iterable[Mapping[str, Any]], client: APIClient
) -> None:
    """Send ``records`` to an Elasticsearch index."""
    bulk_lines = []
    for rec in records:
        bulk_lines.append(json.dumps({"index": {"_index": index}}))
        bulk_lines.append(json.dumps(rec))
    payload = "\n".join(bulk_lines) + "\n"
    await client.request(
        "POST",
        f"{url.rstrip('/')}/_bulk",
        content=payload,
        headers={"Content-Type": "application/x-ndjson"},
    )


async def push_metrics_to_grafana(
    url: str, metrics: Mapping[str, Any], client: APIClient
) -> None:
    """Send metrics to Grafana via HTTP."""
    await client.request("POST", url, json=dict(metrics))


async def broadcast_webhooks(urls: Iterable[str], payload: Mapping[str, Any]) -> None:
    """POST ``payload`` to each webhook ``url``."""
    async with httpx.AsyncClient() as http:
        for url in urls:
            try:
                await http.post(url, json=payload)
            except Exception as exc:  # pragma: no cover - network errors
                logger.warning("webhook %s failed: %s", url, exc)


class IntegrationMonitor:
    """Store last success state for integrations."""

    def __init__(self) -> None:
        """Initialize the integration monitor with empty status tracking."""
        self.status: dict[str, dict[str, Any]] = {}

    def update(self, name: str, ok: bool, message: str | None = None) -> None:
        """Update the status of an integration.
        
        Args:
            name: Name of the integration.
            ok: Whether the integration is working correctly.
            message: Optional status message.
        """
        self.status[name] = {
            "ok": ok,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def get_status(self) -> dict[str, dict[str, Any]]:
        """Get current status of all tracked integrations.
        
        Returns:
            Dictionary mapping integration names to their status information.
        """
        return self.status


__all__ = [
    "APIClient",
    "fetch_stix_taxii",
    "send_to_elasticsearch",
    "push_metrics_to_grafana",
    "broadcast_webhooks",
    "IntegrationMonitor",
]
