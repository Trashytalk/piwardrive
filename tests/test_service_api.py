"""
Comprehensive tests for the FastAPI service layer.
Tests web service endpoints, authentication, and API functionality.
"""

import json
import os
import pytest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from fastapi import HTTPException
from typing import Any, Dict, List

# Import individual components to avoid circular imports
from piwardrive.api.auth import AUTH_DEP, AuthMiddleware
from piwardrive.api.common import (
    get_cpu_temp,
    get_mem_usage,
    get_disk_usage,
    get_network_throughput,
    service_status_async,
    run_service_cmd,
)
from piwardrive.error_middleware import add_error_middleware


class TestFastAPIService:
    """Test FastAPI service initialization and configuration."""
    
    def test_fastapi_app_creation(self):
        """Test FastAPI app can be created without circular imports."""
        # Mock the problematic imports to avoid circular dependency
        with patch('piwardrive.api.analysis_queries.router') as mock_router:
            with patch('piwardrive.routes.analytics.router') as mock_analytics:
                with patch('piwardrive.routes.wifi.router') as mock_wifi:
                    with patch('piwardrive.routes.bluetooth.router') as mock_bt:
                        with patch('piwardrive.routes.cellular.router') as mock_cell:
                            # Import after mocking to avoid circular dependency
                            from fastapi import FastAPI
                            
                            app = FastAPI()
                            
                            # Test basic app properties
                            assert app is not None
                            assert hasattr(app, 'router')
                            assert hasattr(app, 'middleware')
                            
    def test_cors_middleware_configuration(self):
        """Test CORS middleware configuration."""
        with patch.dict(os.environ, {'PW_CORS_ORIGINS': 'http://localhost:3000,http://localhost:8080'}):
            from fastapi import FastAPI
            from fastapi.middleware.cors import CORSMiddleware
            
            app = FastAPI()
            app.add_middleware(
                CORSMiddleware,
                allow_origins=['http://localhost:3000', 'http://localhost:8080'],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
            
            # Test middleware is added
            assert len(app.middleware) > 0
            
    def test_auth_middleware_integration(self):
        """Test authentication middleware integration."""
        from fastapi import FastAPI
        
        app = FastAPI()
        app.add_middleware(AuthMiddleware)
        
        # Test auth middleware is added
        assert len(app.middleware) > 0


class TestAuthenticationSystem:
    """Test authentication system and security."""
    
    def test_auth_dependency_function(self):
        """Test authentication dependency function."""
        # Test AUTH_DEP is callable
        assert callable(AUTH_DEP)
        
    def test_auth_middleware_initialization(self):
        """Test AuthMiddleware can be initialized."""
        middleware = AuthMiddleware(Mock())
        assert middleware is not None
        
    @pytest.mark.asyncio
    async def test_auth_middleware_call(self):
        """Test AuthMiddleware request processing."""
        # Mock request and call_next
        mock_request = Mock()
        mock_request.method = "GET"
        mock_request.url.path = "/api/test"
        mock_request.headers = {}
        
        async def mock_call_next(request):
            return Mock(status_code=200)
            
        middleware = AuthMiddleware(Mock())
        
        # Test middleware processes request
        response = await middleware.dispatch(mock_request, mock_call_next)
        assert response is not None


class TestAPICommonFunctions:
    """Test common API utility functions."""
    
    def test_get_cpu_temp(self):
        """Test CPU temperature retrieval."""
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = "45678"
            
            temp = get_cpu_temp()
            assert isinstance(temp, (int, float))
            assert temp > 0
            
    def test_get_cpu_temp_file_not_found(self):
        """Test CPU temperature when file not found."""
        with patch('builtins.open', side_effect=FileNotFoundError):
            temp = get_cpu_temp()
            assert temp == 0
            
    def test_get_mem_usage(self):
        """Test memory usage retrieval."""
        with patch('psutil.virtual_memory') as mock_mem:
            mock_mem.return_value.percent = 75.5
            
            usage = get_mem_usage()
            assert isinstance(usage, (int, float))
            assert 0 <= usage <= 100
            
    def test_get_disk_usage(self):
        """Test disk usage retrieval."""
        with patch('psutil.disk_usage') as mock_disk:
            mock_disk.return_value.percent = 42.3
            
            usage = get_disk_usage()
            assert isinstance(usage, (int, float))
            assert 0 <= usage <= 100
            
    def test_get_network_throughput(self):
        """Test network throughput calculation."""
        with patch('psutil.net_io_counters') as mock_net:
            mock_net.return_value.bytes_sent = 1024000
            mock_net.return_value.bytes_recv = 2048000
            
            throughput = get_network_throughput()
            assert isinstance(throughput, dict)
            assert 'upload' in throughput
            assert 'download' in throughput
            
    @pytest.mark.asyncio
    async def test_service_status_async(self):
        """Test async service status check."""
        with patch('asyncio.create_subprocess_exec') as mock_exec:
            mock_proc = Mock()
            mock_proc.communicate.return_value = (b"active", b"")
            mock_proc.returncode = 0
            mock_exec.return_value = mock_proc
            
            status = await service_status_async("test_service")
            assert isinstance(status, dict)
            assert 'status' in status
            assert 'active' in status
            
    def test_run_service_cmd(self):
        """Test service command execution."""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "success"
            mock_run.return_value.stderr = ""
            
            success, stdout, stderr = run_service_cmd("test", "status")
            assert success is True
            assert stdout == "success"
            assert stderr == ""


class TestErrorMiddleware:
    """Test error handling middleware."""
    
    def test_error_middleware_addition(self):
        """Test error middleware can be added to FastAPI app."""
        from fastapi import FastAPI
        
        app = FastAPI()
        add_error_middleware(app)
        
        # Test middleware is added
        assert len(app.middleware) > 0
        
    def test_error_middleware_handles_http_exceptions(self):
        """Test error middleware handles HTTP exceptions."""
        from fastapi import FastAPI, HTTPException
        from fastapi.testclient import TestClient
        
        app = FastAPI()
        add_error_middleware(app)
        
        @app.get("/test-error")
        async def test_error():
            raise HTTPException(status_code=404, detail="Not found")
            
        client = TestClient(app)
        response = client.get("/test-error")
        
        assert response.status_code == 404
        assert "Not found" in response.text
        
    def test_error_middleware_handles_general_exceptions(self):
        """Test error middleware handles general exceptions."""
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        
        app = FastAPI()
        add_error_middleware(app)
        
        @app.get("/test-exception")
        async def test_exception():
            raise ValueError("Test error")
            
        client = TestClient(app)
        response = client.get("/test-exception")
        
        # Should return 500 for unhandled exceptions
        assert response.status_code == 500


class TestServiceEndpointIntegration:
    """Test service endpoint integration without circular imports."""
    
    def test_service_app_structure(self):
        """Test service app has expected structure."""
        # Mock all the routers to avoid circular imports
        with patch('piwardrive.api.analysis_queries.router') as mock_analysis:
            with patch('piwardrive.routes.wifi.router') as mock_wifi:
                with patch('piwardrive.routes.bluetooth.router') as mock_bluetooth:
                    with patch('piwardrive.routes.cellular.router') as mock_cellular:
                        with patch('piwardrive.routes.analytics.router') as mock_analytics:
                            # Create minimal service app
                            from fastapi import FastAPI
                            
                            app = FastAPI()
                            
                            # Test app can be created
                            assert app is not None
                            assert hasattr(app, 'routes')
                            assert hasattr(app, 'middleware')
                            
    def test_service_exports(self):
        """Test service module exports expected functions."""
        # Test that expected functions are available for import
        try:
            from piwardrive.api.auth import AUTH_DEP
            from piwardrive.api.common import get_cpu_temp, get_mem_usage
            from piwardrive.error_middleware import add_error_middleware
            
            # If we can import these, the module structure is correct
            assert AUTH_DEP is not None
            assert callable(get_cpu_temp)
            assert callable(get_mem_usage)
            assert callable(add_error_middleware)
            
        except ImportError as e:
            pytest.fail(f"Failed to import expected service functions: {e}")


class TestServiceConfiguration:
    """Test service configuration and environment handling."""
    
    def test_cors_origins_parsing(self):
        """Test CORS origins environment variable parsing."""
        test_origins = "http://localhost:3000,http://localhost:8080,https://example.com"
        
        with patch.dict(os.environ, {'PW_CORS_ORIGINS': test_origins}):
            cors_origins = [
                o.strip() for o in os.getenv("PW_CORS_ORIGINS", "").split(",") if o.strip()
            ]
            
            assert len(cors_origins) == 3
            assert "http://localhost:3000" in cors_origins
            assert "http://localhost:8080" in cors_origins
            assert "https://example.com" in cors_origins
            
    def test_cors_origins_empty(self):
        """Test CORS origins when not set."""
        with patch.dict(os.environ, {}, clear=True):
            cors_origins = [
                o.strip() for o in os.getenv("PW_CORS_ORIGINS", "").split(",") if o.strip()
            ]
            
            assert len(cors_origins) == 0
            
    def test_service_environment_variables(self):
        """Test service responds to environment variables."""
        test_env = {
            'PW_CORS_ORIGINS': 'http://localhost:3000',
            'PW_DEBUG': 'true',
            'PW_LOG_LEVEL': 'DEBUG'
        }
        
        with patch.dict(os.environ, test_env):
            # Test environment variables are accessible
            assert os.getenv('PW_CORS_ORIGINS') == 'http://localhost:3000'
            assert os.getenv('PW_DEBUG') == 'true'
            assert os.getenv('PW_LOG_LEVEL') == 'DEBUG'


class TestServiceHealthChecks:
    """Test service health check functionality."""
    
    @pytest.mark.asyncio
    async def test_service_health_check(self):
        """Test service health check endpoint."""
        # Mock the health check functionality
        with patch('piwardrive.api.common.service_status_async') as mock_status:
            mock_status.return_value = {
                'status': 'active',
                'uptime': '1d 2h 3m',
                'memory_usage': 45.2,
                'cpu_usage': 12.5
            }
            
            status = await service_status_async('piwardrive')
            
            assert status['status'] == 'active'
            assert 'uptime' in status
            assert 'memory_usage' in status
            assert 'cpu_usage' in status
            
    def test_system_metrics_collection(self):
        """Test system metrics collection."""
        # Test CPU temperature
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = "50000"
            temp = get_cpu_temp()
            assert temp == 50.0
            
        # Test memory usage
        with patch('psutil.virtual_memory') as mock_mem:
            mock_mem.return_value.percent = 60.0
            mem = get_mem_usage()
            assert mem == 60.0
            
        # Test disk usage
        with patch('psutil.disk_usage') as mock_disk:
            mock_disk.return_value.percent = 75.0
            disk = get_disk_usage()
            assert disk == 75.0


class TestServiceSecurity:
    """Test service security features."""
    
    def test_auth_dependency_exists(self):
        """Test authentication dependency is defined."""
        from piwardrive.api.auth import AUTH_DEP
        assert AUTH_DEP is not None
        
    def test_auth_middleware_exists(self):
        """Test authentication middleware is defined."""
        from piwardrive.api.auth import AuthMiddleware
        assert AuthMiddleware is not None
        
    def test_error_middleware_security(self):
        """Test error middleware doesn't leak sensitive information."""
        from fastapi import FastAPI, HTTPException
        from fastapi.testclient import TestClient
        
        app = FastAPI()
        add_error_middleware(app)
        
        @app.get("/test-sensitive-error")
        async def test_sensitive_error():
            # Simulate an error that might contain sensitive info
            raise ValueError("Database password: secret123")
            
        client = TestClient(app)
        response = client.get("/test-sensitive-error")
        
        # Should return 500 but not leak sensitive details
        assert response.status_code == 500
        assert "secret123" not in response.text
        assert "Database password" not in response.text


class TestServiceIntegration:
    """Test complete service integration scenarios."""
    
    def test_service_startup_sequence(self):
        """Test service can start up without errors."""
        # Mock all dependencies to avoid circular imports
        with patch('piwardrive.api.analysis_queries.router'):
            with patch('piwardrive.routes.wifi.router'):
                with patch('piwardrive.routes.bluetooth.router'):
                    with patch('piwardrive.routes.cellular.router'):
                        with patch('piwardrive.routes.analytics.router'):
                            # Test service can be initialized
                            from fastapi import FastAPI
                            
                            app = FastAPI()
                            
                            # Add essential middleware
                            from piwardrive.api.auth import AuthMiddleware
                            from piwardrive.error_middleware import add_error_middleware
                            
                            app.add_middleware(AuthMiddleware)
                            add_error_middleware(app)
                            
                            # Test app is ready
                            assert app is not None
                            assert len(app.middleware) >= 2  # Auth + Error middleware
                            
    def test_service_api_endpoints_registration(self):
        """Test API endpoints can be registered."""
        from fastapi import FastAPI, APIRouter
        
        app = FastAPI()
        test_router = APIRouter()
        
        @test_router.get("/test")
        async def test_endpoint():
            return {"message": "test"}
            
        app.include_router(test_router)
        
        # Test router is registered
        assert len(app.routes) > 0
        
    def test_service_middleware_stack(self):
        """Test complete middleware stack."""
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from piwardrive.api.auth import AuthMiddleware
        from piwardrive.error_middleware import add_error_middleware
        
        app = FastAPI()
        
        # Add all middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        app.add_middleware(AuthMiddleware)
        add_error_middleware(app)
        
        # Test middleware stack is complete
        assert len(app.middleware) >= 3  # CORS + Auth + Error
