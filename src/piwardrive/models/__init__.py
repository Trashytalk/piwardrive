"""API request and response models used by route handlers."""

from .api_models import (
    AccessPoint,
    ErrorResponse,
    SystemStats,
    WiFiScanRequest,
    WiFiScanResponse,
)

__all__ = [
    "AccessPoint",
    "ErrorResponse",
    "SystemStats",
    "WiFiScanRequest",
    "WiFiScanResponse",
]
