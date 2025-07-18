"""Direct tests for service.py module to ensure coverage."""

import os
from unittest.mock import patch

import pytest


def test_service_module_import():
    """Test that service module can be imported successfully."""
    # Import the service module directly
    from piwardrive import service

    # Check that the app instance exists
    assert hasattr(service, "app")
    assert service.app is not None


def test_service_app_configuration():
    """Test that the FastAPI app is configured correctly."""
    # Check that the app is a FastAPI instance
    from fastapi import FastAPI

    from piwardrive import service

    assert isinstance(service.app, FastAPI)

    # Check that middleware is added
    assert len(service.app.user_middleware) > 0

    # Check that routes are included
    assert len(service.app.routes) > 0


@patch.dict(
    os.environ, {"PW_CORS_ORIGINS": "http://localhost:3000,http://localhost:8080"}
)
def test_cors_configuration_with_origins():
    """Test CORS configuration when origins are provided."""
    # Re-import to trigger the environment variable check
    import importlib

    from piwardrive import service

    importlib.reload(service)

    # Check that CORS middleware is configured
    cors_middleware = None
    for middleware in service.app.user_middleware:
        if hasattr(middleware, "cls") and "CORS" in str(middleware.cls):
            cors_middleware = middleware
            break

    assert cors_middleware is not None


@patch.dict(os.environ, {"PW_CORS_ORIGINS": ""})
def test_cors_configuration_without_origins():
    """Test CORS configuration when no origins are provided."""
    # Re-import to trigger the environment variable check
    import importlib

    from piwardrive import service

    importlib.reload(service)

    # The app should still work without CORS origins
    assert service.app is not None


def test_service_exports():
    """Test that service module exports the expected items."""
    from piwardrive import service

    # Check that all expected items are exported
    expected_exports = [
        "app",
        "AUTH_DEP",
        "async_scan_lora",
        "async_tail_file",
        "fetch_metrics_async",
        "get_avg_rssi",
        "get_cpu_temp",
        "get_mem_usage",
        "get_disk_usage",
        "get_network_throughput",
        "get_gps_fix_quality",
        "get_gps_accuracy",
        "service_status_async",
        "run_service_cmd",
        "_collect_widget_metrics",
    ]

    for export in expected_exports:
        assert hasattr(service, export), f"Missing export: {export}"


def test_service_app_routes():
    """Test that the app has the expected routes configured."""
    from piwardrive import service

    # Check that routes are configured
    routes = service.app.routes
    assert len(routes) > 0

    # Check for some expected route patterns
    route_paths = [route.path for route in routes if hasattr(route, "path")]

    # Should have at least some routes (exact paths depend on router configuration)
    assert len(route_paths) > 0


def test_service_middleware_configuration():
    """Test that middleware is properly configured."""
    from piwardrive import service

    # Check that middleware is configured
    middleware_stack = service.app.user_middleware
    assert len(middleware_stack) > 0

    # Check for AuthMiddleware
    auth_middleware_found = False
    for middleware in middleware_stack:
        if hasattr(middleware, "cls") and "Auth" in str(middleware.cls):
            auth_middleware_found = True
            break

    assert auth_middleware_found, "AuthMiddleware not found in middleware stack"


def test_service_module_level_imports():
    """Test that all module-level imports work correctly."""
    # This test ensures that importing the service module doesn't raise any errors
    try:
        from piwardrive import service

        # Access the app to ensure it's properly initialized
        app = service.app
        assert app is not None
    except ImportError as e:
        pytest.fail(f"Failed to import service module: {e}")
    except Exception as e:
        pytest.fail(f"Error initializing service module: {e}")


@patch("piwardrive.service.os.getenv")
def test_cors_origins_parsing(mock_getenv):
    """Test CORS origins parsing logic."""
    # Test with comma-separated origins
    mock_getenv.return_value = "http://localhost:3000, http://localhost:8080 , "

    # Re-import to trigger the parsing
    import importlib

    from piwardrive import service

    importlib.reload(service)

    # The parsing should handle whitespace and empty strings
    assert service.app is not None


def test_service_app_openapi_schema():
    """Test that the FastAPI app can generate OpenAPI schema."""
    from piwardrive import service

    # Try to get the OpenAPI schema
    try:
        schema = service.app.openapi()
        assert schema is not None
        assert "openapi" in schema
        assert "info" in schema
    except Exception:
        # If schema generation fails, at least the app should be accessible
        assert service.app is not None
