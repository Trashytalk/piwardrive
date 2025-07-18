#!/usr/bin/env python3

"""
Comprehensive test suite for exceptions.py module.
Tests all custom exception classes and error handling functionality.
"""

import sys
from http import HTTPStatus
from pathlib import Path

import pytest

# Add source directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from piwardrive.exceptions import (
    ConfigurationError,
    DatabaseError,
    PiWardriveError,
    ServiceError,
)


class TestPiWardriveError:
    """Test the base PiWardriveError exception class."""

    def test_piwardrive_error_default_constructor(self):
        """Test PiWardriveError with default parameters."""
        message = "Test error message"
        error = PiWardriveError(message)

        assert str(error) == message
        assert error.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert isinstance(error, Exception)

    def test_piwardrive_error_custom_status_code(self):
        """Test PiWardriveError with custom status code."""
        message = "Custom error"
        status_code = HTTPStatus.BAD_REQUEST
        error = PiWardriveError(message, status_code=status_code)

        assert str(error) == message
        assert error.status_code == status_code

    def test_piwardrive_error_with_various_status_codes(self):
        """Test PiWardriveError with various HTTP status codes."""
        test_cases = [
            (HTTPStatus.NOT_FOUND, "Resource not found"),
            (HTTPStatus.UNAUTHORIZED, "Access denied"),
            (HTTPStatus.FORBIDDEN, "Permission denied"),
            (HTTPStatus.BAD_REQUEST, "Invalid request"),
            (HTTPStatus.CONFLICT, "Resource conflict"),
        ]

        for status_code, message in test_cases:
            error = PiWardriveError(message, status_code=status_code)
            assert error.status_code == status_code
            assert str(error) == message

    def test_piwardrive_error_inheritance(self):
        """Test that PiWardriveError properly inherits from Exception."""
        error = PiWardriveError("Test")
        assert isinstance(error, Exception)
        assert isinstance(error, PiWardriveError)

    def test_piwardrive_error_attributes(self):
        """Test that PiWardriveError has the expected attributes."""
        error = PiWardriveError("Test message", status_code=HTTPStatus.NOT_FOUND)

        # Check that the error has both message and status_code
        assert hasattr(error, "status_code")
        assert error.status_code == HTTPStatus.NOT_FOUND
        assert str(error) == "Test message"

    def test_piwardrive_error_keyword_only_status_code(self):
        """Test that status_code is a keyword-only argument."""
        # This should work
        error = PiWardriveError("message", status_code=HTTPStatus.NOT_FOUND)
        assert error.status_code == HTTPStatus.NOT_FOUND

        # This should also work (default status code)
        error = PiWardriveError("message")
        assert error.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


class TestConfigurationError:
    """Test the ConfigurationError exception class."""

    def test_configuration_error_basic(self):
        """Test basic ConfigurationError functionality."""
        message = "Invalid configuration"
        error = ConfigurationError(message)

        assert str(error) == message
        assert error.status_code == HTTPStatus.BAD_REQUEST
        assert isinstance(error, PiWardriveError)
        assert isinstance(error, ConfigurationError)

    def test_configuration_error_inheritance(self):
        """Test ConfigurationError inheritance chain."""
        error = ConfigurationError("Config error")

        assert isinstance(error, Exception)
        assert isinstance(error, PiWardriveError)
        assert isinstance(error, ConfigurationError)

    def test_configuration_error_status_code_fixed(self):
        """Test that ConfigurationError always has BAD_REQUEST status."""
        # ConfigurationError should always use BAD_REQUEST status
        error = ConfigurationError("Test config error")
        assert error.status_code == HTTPStatus.BAD_REQUEST

    def test_configuration_error_with_various_messages(self):
        """Test ConfigurationError with various error messages."""
        test_messages = [
            "Missing required configuration key",
            "Invalid configuration value for 'database_url'",
            "Configuration file not found",
            "YAML parsing error in config file",
            "Environment variable validation failed",
        ]

        for message in test_messages:
            error = ConfigurationError(message)
            assert str(error) == message
            assert error.status_code == HTTPStatus.BAD_REQUEST


class TestDatabaseError:
    """Test the DatabaseError exception class."""

    def test_database_error_default_constructor(self):
        """Test DatabaseError with default parameters."""
        message = "Database connection failed"
        error = DatabaseError(message)

        assert str(error) == message
        assert error.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert isinstance(error, PiWardriveError)
        assert isinstance(error, DatabaseError)

    def test_database_error_custom_status_code(self):
        """Test DatabaseError with custom status code."""
        message = "Database query failed"
        status_code = HTTPStatus.SERVICE_UNAVAILABLE
        error = DatabaseError(message, status_code=status_code)

        assert str(error) == message
        assert error.status_code == status_code

    def test_database_error_inheritance(self):
        """Test DatabaseError inheritance chain."""
        error = DatabaseError("DB error")

        assert isinstance(error, Exception)
        assert isinstance(error, PiWardriveError)
        assert isinstance(error, DatabaseError)

    def test_database_error_with_various_scenarios(self):
        """Test DatabaseError for various database scenarios."""
        test_cases = [
            ("Connection timeout", HTTPStatus.REQUEST_TIMEOUT),
            ("Table not found", HTTPStatus.NOT_FOUND),
            ("Constraint violation", HTTPStatus.CONFLICT),
            ("Database locked", HTTPStatus.LOCKED),
            ("Query syntax error", HTTPStatus.BAD_REQUEST),
        ]

        for message, status_code in test_cases:
            error = DatabaseError(message, status_code=status_code)
            assert str(error) == message
            assert error.status_code == status_code


class TestServiceError:
    """Test the ServiceError exception class."""

    def test_service_error_default_constructor(self):
        """Test ServiceError with default parameters."""
        message = "Service operation failed"
        error = ServiceError(message)

        assert str(error) == message
        assert error.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert isinstance(error, PiWardriveError)
        assert isinstance(error, ServiceError)

    def test_service_error_custom_status_code(self):
        """Test ServiceError with custom status code."""
        message = "Service unavailable"
        status_code = HTTPStatus.SERVICE_UNAVAILABLE
        error = ServiceError(message, status_code=status_code)

        assert str(error) == message
        assert error.status_code == status_code

    def test_service_error_inheritance(self):
        """Test ServiceError inheritance chain."""
        error = ServiceError("Service error")

        assert isinstance(error, Exception)
        assert isinstance(error, PiWardriveError)
        assert isinstance(error, ServiceError)

    def test_service_error_with_various_scenarios(self):
        """Test ServiceError for various service scenarios."""
        test_cases = [
            ("External API timeout", HTTPStatus.REQUEST_TIMEOUT),
            ("Rate limit exceeded", HTTPStatus.TOO_MANY_REQUESTS),
            ("Service authentication failed", HTTPStatus.UNAUTHORIZED),
            ("Service configuration invalid", HTTPStatus.BAD_REQUEST),
            ("Service dependency unavailable", HTTPStatus.SERVICE_UNAVAILABLE),
        ]

        for message, status_code in test_cases:
            error = ServiceError(message, status_code=status_code)
            assert str(error) == message
            assert error.status_code == status_code


class TestExceptionHierarchy:
    """Test the overall exception hierarchy and relationships."""

    def test_all_exceptions_inherit_from_piwardrive_error(self):
        """Test that all custom exceptions inherit from PiWardriveError."""
        exceptions = [
            ConfigurationError("test"),
            DatabaseError("test"),
            ServiceError("test"),
        ]

        for exception in exceptions:
            assert isinstance(exception, PiWardriveError)
            assert isinstance(exception, Exception)

    def test_exception_hierarchy_consistency(self):
        """Test that exception hierarchy is consistent."""
        # All exceptions should have status_code attribute
        exceptions = [
            PiWardriveError("test"),
            ConfigurationError("test"),
            DatabaseError("test"),
            ServiceError("test"),
        ]

        for exception in exceptions:
            assert hasattr(exception, "status_code")
            assert isinstance(exception.status_code, HTTPStatus)

    def test_exception_str_representation(self):
        """Test string representation of all exceptions."""
        test_message = "Test error message"
        exceptions = [
            PiWardriveError(test_message),
            ConfigurationError(test_message),
            DatabaseError(test_message),
            ServiceError(test_message),
        ]

        for exception in exceptions:
            assert str(exception) == test_message

    def test_exception_module_exports(self):
        """Test that __all__ exports are correct."""
        from piwardrive import exceptions

        expected_exports = [
            "PiWardriveError",
            "ConfigurationError",
            "DatabaseError",
            "ServiceError",
        ]

        assert hasattr(exceptions, "__all__")
        assert set(exceptions.__all__) == set(expected_exports)

        # Verify all exported items are accessible
        for export_name in expected_exports:
            assert hasattr(exceptions, export_name)


class TestExceptionErrorScenarios:
    """Test exceptions in realistic error scenarios."""

    def test_configuration_loading_error_scenario(self):
        """Test ConfigurationError in configuration loading scenario."""
        try:
            # Simulate configuration loading failure
            raise ConfigurationError("Failed to load config file: /path/to/config.yaml")
        except ConfigurationError as e:
            assert e.status_code == HTTPStatus.BAD_REQUEST
            assert "config.yaml" in str(e)

    def test_database_connection_error_scenario(self):
        """Test DatabaseError in database connection scenario."""
        try:
            # Simulate database connection failure
            raise DatabaseError(
                "Connection to database failed",
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            )
        except DatabaseError as e:
            assert e.status_code == HTTPStatus.SERVICE_UNAVAILABLE
            assert "Connection to database failed" in str(e)

    def test_service_api_error_scenario(self):
        """Test ServiceError in API service scenario."""
        try:
            # Simulate external service failure
            raise ServiceError(
                "External API rate limit exceeded",
                status_code=HTTPStatus.TOO_MANY_REQUESTS,
            )
        except ServiceError as e:
            assert e.status_code == HTTPStatus.TOO_MANY_REQUESTS
            assert "rate limit" in str(e)

    def test_nested_exception_handling(self):
        """Test handling of nested exceptions."""
        try:
            try:
                raise DatabaseError("Primary DB failure")
            except DatabaseError:
                raise ServiceError(
                    "Service failed due to database issue",
                    status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                )
        except ServiceError as e:
            assert e.status_code == HTTPStatus.SERVICE_UNAVAILABLE
            assert "Service failed" in str(e)


if __name__ == "__main__":
    pytest.main([__file__])
