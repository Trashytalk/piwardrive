class PiWardriveError(Exception):
    """Base class for PiWardrive domain errors."""


class ConfigError(PiWardriveError):
    """Raised when configuration validation fails."""


class ExportError(PiWardriveError):
    """Raised when exporting data fails."""


class GeofenceError(PiWardriveError):
    """Raised for geofence load/save issues."""
