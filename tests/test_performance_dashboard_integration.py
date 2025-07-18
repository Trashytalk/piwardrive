"""Integration test for the performance dashboard."""

import os
import sys
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from piwardrive.service import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_performance_dashboard_stats(client):
    """Test the performance dashboard stats endpoint."""
    with (
        patch("piwardrive.api.performance_dashboard.DatabaseOptimizer") as mock_db_opt,
        patch("piwardrive.api.performance_dashboard.AsyncOptimizer") as mock_async_opt,
        patch("piwardrive.api.performance_dashboard.RealtimeOptimizer") as mock_rt_opt,
    ):

        # Mock the optimizers
        mock_db_opt.return_value.get_stats.return_value = {
            "total_queries": 1000,
            "avg_query_time": 0.05,
            "slow_queries": 10,
            "total_connections": 50,
        }

        mock_async_opt.return_value.get_stats.return_value = {
            "total_operations": 500,
            "avg_operation_time": 0.1,
            "failed_operations": 5,
            "queue_size": 10,
        }

        mock_rt_opt.return_value.get_stats.return_value = {
            "total_connections": 25,
            "avg_response_time": 0.02,
            "failed_connections": 2,
            "data_throughput": 1000,
        }

        # Test the stats endpoint
        response = client.get("/performance/stats")
        assert response.status_code == 200

        data = response.json()
        assert "database" in data
        assert "async" in data
        assert "realtime" in data

        # Verify database stats
        db_stats = data["database"]
        assert db_stats["total_queries"] == 1000
        assert db_stats["avg_query_time"] == 0.05

        # Verify async stats
        async_stats = data["async"]
        assert async_stats["total_operations"] == 500
        assert async_stats["avg_operation_time"] == 0.1

        # Verify realtime stats
        rt_stats = data["realtime"]
        assert rt_stats["total_connections"] == 25
        assert rt_stats["avg_response_time"] == 0.02


def test_performance_dashboard_alerts(client):
    """Test the performance dashboard alerts endpoint."""
    with (
        patch("piwardrive.api.performance_dashboard.DatabaseOptimizer") as mock_db_opt,
        patch("piwardrive.api.performance_dashboard.AsyncOptimizer") as mock_async_opt,
        patch("piwardrive.api.performance_dashboard.RealtimeOptimizer") as mock_rt_opt,
    ):

        # Mock the alerts
        mock_db_opt.return_value.get_alerts.return_value = [
            {
                "level": "warning",
                "message": "High query count detected",
                "timestamp": "2024-01-01T00:00:00Z",
            }
        ]

        mock_async_opt.return_value.get_alerts.return_value = [
            {
                "level": "critical",
                "message": "High failure rate",
                "timestamp": "2024-01-01T00:01:00Z",
            }
        ]

        mock_rt_opt.return_value.get_alerts.return_value = [
            {
                "level": "info",
                "message": "Connection limit reached",
                "timestamp": "2024-01-01T00:02:00Z",
            }
        ]

        # Test the alerts endpoint
        response = client.get("/performance/alerts")
        assert response.status_code == 200

        data = response.json()
        assert "alerts" in data
        alerts = data["alerts"]

        # Should have 3 alerts total
        assert len(alerts) == 3

        # Check alert levels
        levels = [alert["level"] for alert in alerts]
        assert "warning" in levels
        assert "critical" in levels
        assert "info" in levels


def test_performance_dashboard_recommendations(client):
    """Test the performance dashboard recommendations endpoint."""
    with (
        patch("piwardrive.api.performance_dashboard.DatabaseOptimizer") as mock_db_opt,
        patch("piwardrive.api.performance_dashboard.AsyncOptimizer") as mock_async_opt,
        patch("piwardrive.api.performance_dashboard.RealtimeOptimizer") as mock_rt_opt,
    ):

        # Mock the recommendations
        mock_db_opt.return_value.get_recommendations.return_value = [
            {"type": "index", "table": "users", "column": "email", "impact": "high"}
        ]

        mock_async_opt.return_value.get_recommendations.return_value = [
            {"type": "pool_size", "current": 10, "recommended": 20, "impact": "medium"}
        ]

        mock_rt_opt.return_value.get_recommendations.return_value = [
            {
                "type": "connection_limit",
                "current": 100,
                "recommended": 200,
                "impact": "low",
            }
        ]

        # Test the recommendations endpoint
        response = client.get("/performance/recommendations")
        assert response.status_code == 200

        data = response.json()
        assert "recommendations" in data
        recommendations = data["recommendations"]

        # Should have 3 recommendations total
        assert len(recommendations) == 3

        # Check recommendation types
        types = [rec["type"] for rec in recommendations]
        assert "index" in types
        assert "pool_size" in types
        assert "connection_limit" in types


def test_performance_dashboard_optimize(client):
    """Test the performance dashboard optimize endpoint."""
    with (
        patch("piwardrive.api.performance_dashboard.DatabaseOptimizer") as mock_db_opt,
        patch("piwardrive.api.performance_dashboard.AsyncOptimizer") as mock_async_opt,
        patch("piwardrive.api.performance_dashboard.RealtimeOptimizer") as mock_rt_opt,
    ):

        # Mock the optimization methods
        mock_db_opt.return_value.optimize.return_value = {
            "status": "success",
            "message": "Database optimized",
        }
        mock_async_opt.return_value.optimize.return_value = {
            "status": "success",
            "message": "Async optimized",
        }
        mock_rt_opt.return_value.optimize.return_value = {
            "status": "success",
            "message": "Realtime optimized",
        }

        # Test database optimization
        response = client.post("/performance/optimize", json={"component": "database"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "Database optimized" in data["message"]

        # Test async optimization
        response = client.post("/performance/optimize", json={"component": "async"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "Async optimized" in data["message"]

        # Test realtime optimization
        response = client.post("/performance/optimize", json={"component": "realtime"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "Realtime optimized" in data["message"]


if __name__ == "__main__":
    pytest.main([__file__])
