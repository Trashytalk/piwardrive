"""Deprecated module; maintained for backward compatibility."""

from __future__ import annotations

from .exceptions import ConfigurationError, DatabaseError, PiWardriveError, ServiceError


class ConfigError(ConfigurationError):
    """Alias of :class:`ConfigurationError`."""


class ExportError(ServiceError):
    """Raised when exporting data fails."""


class GeofenceError(ServiceError):
    """Raised for geofence load/save issues."""


# TODO: Stub for SecurityError
class SecurityError(Exception):
    pass


__all__ = [
    "PiWardriveError",
    "ConfigError",
    "ExportError",
    "GeofenceError",
    "DatabaseError",
    "ServiceError",
]
