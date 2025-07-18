"""Custom exception hierarchy for PiWardrive."""

from __future__ import annotations

from http import HTTPStatus


class PiWardriveError(Exception):
    """Base class for all PiWardrive errors."""

    def __init__(
        self, message: str, *, status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    ) -> None:
        """Initialize PiWardrive base error.

        Args:
            message: Error message.
            status_code: HTTP status code for the error.
        """
        super().__init__(message)
        self.status_code = status_code


class ConfigurationError(PiWardriveError):
    """Raised when configuration validation or loading fails."""

    def __init__(self, message: str) -> None:
        """Initialize configuration error.

        Args:
            message: Error message.
        """
        super().__init__(message, status_code=HTTPStatus.BAD_REQUEST)


class DatabaseError(PiWardriveError):
    """Raised when a database operation fails."""

    def __init__(
        self, message: str, *, status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    ) -> None:
        """Initialize database error.

        Args:
            message: Error message.
            status_code: HTTP status code for the error.
        """
        super().__init__(message, status_code=status_code)


class ServiceError(PiWardriveError):
    """Raised for unexpected service layer errors."""

    def __init__(
        self, message: str, *, status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    ) -> None:
        """Initialize service error.

        Args:
            message: Error message.
            status_code: HTTP status code for the error.
        """
        super().__init__(message, status_code=status_code)


__all__ = [
    "PiWardriveError",
    "ConfigurationError",
    "DatabaseError",
    "ServiceError",
]
