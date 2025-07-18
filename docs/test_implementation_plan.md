# Test Coverage Implementation Plan

## Executive Summary

This document provides a concrete implementation plan to address the significant test coverage gaps identified in the PiWardrive repository. The plan prioritizes critical components and provides specific implementation steps for each testing phase.

## Current State Summary

- **Backend Python**: 66% test coverage (190/289 files)
- **Frontend JavaScript**: 5% test coverage (8/146 files)
- **Critical Gap**: Missing tests for core services, API endpoints, and entire frontend

## Implementation Strategy

### Phase 1: Test Infrastructure Setup (Week 1)

#### 1.1 Backend Test Configuration

**File: `pytest.ini`**

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --cov=src/piwardrive
    --cov-report=html:htmlcov
    --cov-report=term-missing
    --cov-report=xml
    --cov-fail-under=85
    --strict-markers
    --tb=short
markers =
    unit: Unit tests
    integration: Integration tests
    api: API tests
    slow: Slow running tests
    security: Security tests
    performance: Performance tests
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

**File: `pyproject.toml` (testing additions)**

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "--verbose",
    "--cov=src/piwardrive",
    "--cov-report=html:htmlcov",
    "--cov-report=term-missing",
    "--cov-report=xml",
    "--cov-fail-under=85",
    "--strict-markers"
]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "api: API tests",
    "slow: Slow running tests",
    "security: Security tests",
    "performance: Performance tests"
]

[tool.coverage.run]
source = ["src/piwardrive"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__pycache__/*",
    "*/venv/*",
    "*/node_modules/*"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:"
]
```

#### 1.2 Frontend Test Configuration

**File: `webui/vitest.config.js`**

```javascript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.js'],
    globals: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.js',
        'dist/',
        'coverage/'
      ],
      thresholds: {
        global: {
          branches: 80,
          functions: 80,
          lines: 80,
          statements: 80
        }
      }
    }
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@components': resolve(__dirname, 'src/components'),
      '@utils': resolve(__dirname, 'src/utils'),
      '@services': resolve(__dirname, 'src/services')
    }
  }
});
```

**File: `webui/src/test/setup.js`**

```javascript
import { expect, afterEach, vi } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

// Add jest-dom matchers
expect.extend(matchers);

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(), // deprecated
    removeListener: vi.fn(), // deprecated
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock ResizeObserver
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));

// Mock IntersectionObserver
global.IntersectionObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));
```

### Phase 2: Critical Backend Components (Week 2-3)

#### 2.1 Core Services Tests

**File: `tests/services/test_alerting.py`**

```python
import pytest
from unittest.mock import Mock, patch
from src.piwardrive.services.alerting import AlertingService
from src.piwardrive.models.alert import Alert, AlertLevel

class TestAlertingService:
    
    @pytest.fixture
    def alerting_service(self):
        return AlertingService()
    
    @pytest.fixture
    def mock_alert(self):
        return Alert(
            id="test-alert-1",
            level=AlertLevel.HIGH,
            message="Test alert message",
            source="test_source",
            timestamp=1234567890
        )
    
    def test_create_alert(self, alerting_service, mock_alert):
        """Test alert creation."""
        with patch.object(alerting_service, '_persist_alert') as mock_persist:
            result = alerting_service.create_alert(mock_alert)
            
            assert result is not None
            assert result.id == mock_alert.id
            mock_persist.assert_called_once_with(mock_alert)
    
    def test_get_alerts_by_level(self, alerting_service):
        """Test filtering alerts by level."""
        with patch.object(alerting_service, '_get_alerts_from_db') as mock_get:
            mock_get.return_value = [Mock(level=AlertLevel.HIGH)]
            
            alerts = alerting_service.get_alerts_by_level(AlertLevel.HIGH)
            
            assert len(alerts) == 1
            assert alerts[0].level == AlertLevel.HIGH
    
    def test_acknowledge_alert(self, alerting_service):
        """Test alert acknowledgment."""
        with patch.object(alerting_service, '_update_alert_status') as mock_update:
            alerting_service.acknowledge_alert("test-alert-1", "test_user")
            
            mock_update.assert_called_once_with(
                "test-alert-1", 
                "acknowledged", 
                "test_user"
            )
    
    @pytest.mark.asyncio
    async def test_process_alert_async(self, alerting_service, mock_alert):
        """Test asynchronous alert processing."""
        with patch.object(alerting_service, '_send_notification') as mock_send:
            await alerting_service.process_alert_async(mock_alert)
            
            mock_send.assert_called_once_with(mock_alert)
```

**File: `tests/services/test_coordinator.py`**

```python
import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.piwardrive.services.coordinator import ServiceCoordinator
from src.piwardrive.services.exceptions import CoordinationError

class TestServiceCoordinator:
    
    @pytest.fixture
    def coordinator(self):
        return ServiceCoordinator()
    
    @pytest.fixture
    def mock_services(self):
        return {
            'scanner': Mock(),
            'analyzer': Mock(),
            'exporter': Mock()
        }
    
    def test_register_service(self, coordinator, mock_services):
        """Test service registration."""
        service = mock_services['scanner']
        
        coordinator.register_service('scanner', service)
        
        assert 'scanner' in coordinator._services
        assert coordinator._services['scanner'] == service
    
    def test_start_all_services(self, coordinator, mock_services):
        """Test starting all registered services."""
        for name, service in mock_services.items():
            coordinator.register_service(name, service)
        
        coordinator.start_all_services()
        
        for service in mock_services.values():
            service.start.assert_called_once()
    
    def test_stop_all_services(self, coordinator, mock_services):
        """Test stopping all services."""
        for name, service in mock_services.items():
            coordinator.register_service(name, service)
        
        coordinator.stop_all_services()
        
        for service in mock_services.values():
            service.stop.assert_called_once()
    
    def test_service_health_check(self, coordinator, mock_services):
        """Test service health checking."""
        service = mock_services['scanner']
        service.is_healthy.return_value = True
        coordinator.register_service('scanner', service)
        
        health_status = coordinator.get_service_health('scanner')
        
        assert health_status is True
        service.is_healthy.assert_called_once()
    
    def test_coordination_error_handling(self, coordinator):
        """Test error handling during coordination."""
        failing_service = Mock()
        failing_service.start.side_effect = Exception("Service failed")
        
        coordinator.register_service('failing_service', failing_service)
        
        with pytest.raises(CoordinationError):
            coordinator.start_all_services()
```

#### 2.2 API Endpoint Tests

**File: `tests/api/test_auth_endpoints.py`**

```python
import pytest
from unittest.mock import Mock, patch
from flask import Flask
from src.piwardrive.api.auth.endpoints import auth_bp
from src.piwardrive.api.auth.models import User, AuthRequest

class TestAuthEndpoints:
    
    @pytest.fixture
    def app(self):
        app = Flask(__name__)
        app.register_blueprint(auth_bp)
        app.config['TESTING'] = True
        return app
    
    @pytest.fixture
    def client(self, app):
        return app.test_client()
    
    def test_login_success(self, client):
        """Test successful login."""
        with patch('src.piwardrive.api.auth.endpoints.authenticate_user') as mock_auth:
            mock_auth.return_value = User(id=1, username='test_user')
            
            response = client.post('/auth/login', json={
                'username': 'test_user',
                'password': 'test_password'
            })
            
            assert response.status_code == 200
            data = response.get_json()
            assert 'access_token' in data
            assert data['user']['username'] == 'test_user'
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        with patch('src.piwardrive.api.auth.endpoints.authenticate_user') as mock_auth:
            mock_auth.return_value = None
            
            response = client.post('/auth/login', json={
                'username': 'invalid_user',
                'password': 'invalid_password'
            })
            
            assert response.status_code == 401
            data = response.get_json()
            assert 'error' in data
            assert data['error'] == 'Invalid credentials'
    
    def test_logout(self, client):
        """Test user logout."""
        with patch('src.piwardrive.api.auth.endpoints.revoke_token') as mock_revoke:
            response = client.post('/auth/logout', 
                headers={'Authorization': 'Bearer valid_token'})
            
            assert response.status_code == 200
            mock_revoke.assert_called_once()
    
    def test_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without token."""
        response = client.get('/auth/profile')
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
    
    def test_protected_endpoint_with_valid_token(self, client):
        """Test accessing protected endpoint with valid token."""
        with patch('src.piwardrive.api.auth.middleware.verify_token') as mock_verify:
            mock_verify.return_value = User(id=1, username='test_user')
            
            response = client.get('/auth/profile',
                headers={'Authorization': 'Bearer valid_token'})
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['username'] == 'test_user'
```

#### 2.3 Database Layer Tests

**File: `tests/db/test_manager.py`**

```python
import pytest
from unittest.mock import Mock, patch
from src.piwardrive.db.manager import DatabaseManager
from src.piwardrive.db.exceptions import DatabaseError

class TestDatabaseManager:
    
    @pytest.fixture
    def db_manager(self):
        return DatabaseManager(connection_string='sqlite:///:memory:')
    
    @pytest.fixture
    def mock_connection(self):
        return Mock()
    
    def test_get_connection(self, db_manager):
        """Test database connection retrieval."""
        with patch.object(db_manager, '_create_connection') as mock_create:
            mock_create.return_value = Mock()
            
            connection = db_manager.get_connection()
            
            assert connection is not None
            mock_create.assert_called_once()
    
    def test_execute_query(self, db_manager, mock_connection):
        """Test query execution."""
        with patch.object(db_manager, 'get_connection') as mock_get_conn:
            mock_get_conn.return_value = mock_connection
            mock_connection.execute.return_value = Mock(fetchall=Mock(return_value=[]))
            
            result = db_manager.execute_query("SELECT * FROM test_table")
            
            assert result == []
            mock_connection.execute.assert_called_once_with("SELECT * FROM test_table")
    
    def test_execute_query_with_params(self, db_manager, mock_connection):
        """Test parameterized query execution."""
        with patch.object(db_manager, 'get_connection') as mock_get_conn:
            mock_get_conn.return_value = mock_connection
            mock_connection.execute.return_value = Mock(fetchall=Mock(return_value=[]))
            
            result = db_manager.execute_query(
                "SELECT * FROM test_table WHERE id = ?", 
                params=(1,)
            )
            
            assert result == []
            mock_connection.execute.assert_called_once_with(
                "SELECT * FROM test_table WHERE id = ?", 
                (1,)
            )
    
    def test_transaction_commit(self, db_manager, mock_connection):
        """Test transaction commit."""
        with patch.object(db_manager, 'get_connection') as mock_get_conn:
            mock_get_conn.return_value = mock_connection
            
            with db_manager.transaction():
                db_manager.execute_query("INSERT INTO test_table VALUES (1, 'test')")
            
            mock_connection.commit.assert_called_once()
    
    def test_transaction_rollback(self, db_manager, mock_connection):
        """Test transaction rollback on error."""
        with patch.object(db_manager, 'get_connection') as mock_get_conn:
            mock_get_conn.return_value = mock_connection
            mock_connection.execute.side_effect = Exception("Database error")
            
            with pytest.raises(DatabaseError):
                with db_manager.transaction():
                    db_manager.execute_query("INSERT INTO test_table VALUES (1, 'test')")
            
            mock_connection.rollback.assert_called_once()
```

### Phase 3: Frontend Component Tests (Week 4-5)

#### 3.1 Core Component Tests

**File: `webui/src/test/App.test.jsx`**

```javascript
import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import App from '../App';

// Mock the auth service
vi.mock('../auth.js', () => ({
  default: {
    isAuthenticated: vi.fn(() => true),
    getCurrentUser: vi.fn(() => ({ username: 'test_user' })),
    login: vi.fn(),
    logout: vi.fn()
  }
}));

// Mock the backend service
vi.mock('../backendService.js', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn()
  }
}));

describe('App', () => {
  it('renders without crashing', () => {
    render(<App />);
    expect(screen.getByRole('main')).toBeInTheDocument();
  });

  it('displays navigation when authenticated', () => {
    render(<App />);
    expect(screen.getByRole('navigation')).toBeInTheDocument();
  });

  it('handles authentication state changes', async () => {
    const { rerender } = render(<App />);
    
    // Should show authenticated content
    expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
    
    // Mock logout
    vi.mocked(auth.isAuthenticated).mockReturnValue(false);
    
    rerender(<App />);
    
    // Should show login form
    expect(screen.getByText(/login/i)).toBeInTheDocument();
  });
});
```

**File: `webui/src/test/auth.test.js`**

```javascript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import auth from '../auth.js';

// Mock fetch
global.fetch = vi.fn();

describe('Auth Service', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  it('should login successfully', async () => {
    const mockResponse = {
      access_token: 'mock_token',
      user: { username: 'test_user' }
    };

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    });

    const result = await auth.login('test_user', 'test_password');

    expect(result).toBe(true);
    expect(localStorage.getItem('access_token')).toBe('mock_token');
    expect(fetch).toHaveBeenCalledWith('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: 'test_user',
        password: 'test_password'
      })
    });
  });

  it('should handle login failure', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ error: 'Invalid credentials' })
    });

    const result = await auth.login('invalid_user', 'invalid_password');

    expect(result).toBe(false);
    expect(localStorage.getItem('access_token')).toBeNull();
  });

  it('should logout correctly', () => {
    localStorage.setItem('access_token', 'mock_token');
    localStorage.setItem('user', JSON.stringify({ username: 'test_user' }));

    auth.logout();

    expect(localStorage.getItem('access_token')).toBeNull();
    expect(localStorage.getItem('user')).toBeNull();
  });

  it('should check authentication status', () => {
    // Not authenticated
    expect(auth.isAuthenticated()).toBe(false);

    // Authenticated
    localStorage.setItem('access_token', 'mock_token');
    expect(auth.isAuthenticated()).toBe(true);
  });

  it('should get current user', () => {
    const mockUser = { username: 'test_user' };
    localStorage.setItem('user', JSON.stringify(mockUser));

    const user = auth.getCurrentUser();

    expect(user).toEqual(mockUser);
  });
});
```

#### 3.2 Scanner Component Tests

**File: `webui/src/test/wifiScanner.test.js`**

```javascript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import WifiScanner from '../wifiScanner.js';

// Mock backend service
vi.mock('../backendService.js', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn()
  }
}));

describe('WifiScanner', () => {
  let scanner;
  let mockBackendService;

  beforeEach(() => {
    vi.clearAllMocks();
    mockBackendService = await import('../backendService.js');
    scanner = new WifiScanner();
  });

  it('should initialize with default configuration', () => {
    expect(scanner.isScanning).toBe(false);
    expect(scanner.config).toBeDefined();
    expect(scanner.config.interval).toBe(5000);
  });

  it('should start scanning', async () => {
    mockBackendService.default.post.mockResolvedValue({
      success: true,
      scan_id: 'scan_123'
    });

    await scanner.startScan();

    expect(scanner.isScanning).toBe(true);
    expect(scanner.currentScanId).toBe('scan_123');
    expect(mockBackendService.default.post).toHaveBeenCalledWith(
      '/api/wifi/scan/start',
      expect.any(Object)
    );
  });

  it('should stop scanning', async () => {
    scanner.isScanning = true;
    scanner.currentScanId = 'scan_123';

    mockBackendService.default.post.mockResolvedValue({
      success: true
    });

    await scanner.stopScan();

    expect(scanner.isScanning).toBe(false);
    expect(scanner.currentScanId).toBeNull();
    expect(mockBackendService.default.post).toHaveBeenCalledWith(
      '/api/wifi/scan/stop',
      { scan_id: 'scan_123' }
    );
  });

  it('should get scan results', async () => {
    const mockResults = [
      { ssid: 'TestNetwork', bssid: '00:11:22:33:44:55', signal: -45 },
      { ssid: 'AnotherNetwork', bssid: '66:77:88:99:aa:bb', signal: -60 }
    ];

    mockBackendService.default.get.mockResolvedValue({
      results: mockResults
    });

    const results = await scanner.getResults();

    expect(results).toEqual(mockResults);
    expect(mockBackendService.default.get).toHaveBeenCalledWith(
      '/api/wifi/scan/results'
    );
  });

  it('should handle scan errors', async () => {
    mockBackendService.default.post.mockRejectedValue(
      new Error('Scan failed')
    );

    await expect(scanner.startScan()).rejects.toThrow('Scan failed');
    expect(scanner.isScanning).toBe(false);
  });

  it('should update scan configuration', () => {
    const newConfig = {
      interval: 10000,
      channels: [1, 6, 11]
    };

    scanner.updateConfig(newConfig);

    expect(scanner.config.interval).toBe(10000);
    expect(scanner.config.channels).toEqual([1, 6, 11]);
  });
});
```

### Phase 4: Integration Tests (Week 6-7)

#### 4.1 End-to-End API Tests

**File: `tests/integration/test_api_workflow.py`**

```python
import pytest
import requests
from unittest.mock import Mock
from src.piwardrive.unified_platform import UnifiedPlatform

class TestAPIWorkflow:
    
    @pytest.fixture
    def app(self):
        platform = UnifiedPlatform()
        app = platform.create_app()
        app.config['TESTING'] = True
        return app
    
    @pytest.fixture
    def client(self, app):
        return app.test_client()
    
    @pytest.fixture
    def auth_headers(self, client):
        """Get authentication headers for protected endpoints."""
        response = client.post('/api/auth/login', json={
            'username': 'test_user',
            'password': 'test_password'
        })
        token = response.get_json()['access_token']
        return {'Authorization': f'Bearer {token}'}
    
    def test_complete_scan_workflow(self, client, auth_headers):
        """Test complete scanning workflow."""
        # Start WiFi scan
        response = client.post('/api/wifi/scan/start', 
                             headers=auth_headers,
                             json={'duration': 30})
        assert response.status_code == 200
        scan_id = response.get_json()['scan_id']
        
        # Check scan status
        response = client.get(f'/api/wifi/scan/{scan_id}/status',
                            headers=auth_headers)
        assert response.status_code == 200
        assert response.get_json()['status'] == 'running'
        
        # Get scan results
        response = client.get(f'/api/wifi/scan/{scan_id}/results',
                            headers=auth_headers)
        assert response.status_code == 200
        results = response.get_json()['results']
        assert isinstance(results, list)
        
        # Stop scan
        response = client.post(f'/api/wifi/scan/{scan_id}/stop',
                             headers=auth_headers)
        assert response.status_code == 200
    
    def test_data_export_workflow(self, client, auth_headers):
        """Test data export workflow."""
        # Request data export
        response = client.post('/api/export/create',
                             headers=auth_headers,
                             json={
                                 'format': 'json',
                                 'date_range': '7d'
                             })
        assert response.status_code == 200
        export_id = response.get_json()['export_id']
        
        # Check export status
        response = client.get(f'/api/export/{export_id}/status',
                            headers=auth_headers)
        assert response.status_code == 200
        
        # Download export when ready
        response = client.get(f'/api/export/{export_id}/download',
                            headers=auth_headers)
        assert response.status_code == 200
```

#### 4.2 Frontend Integration Tests

**File: `webui/src/test/integration/scanWorkflow.test.jsx`**

```javascript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import userEvent from '@testing-library/user-event';
import ScanDashboard from '../components/ScanDashboard';

// Mock services
vi.mock('../services/wifiScanner.js', () => ({
  default: {
    startScan: vi.fn(),
    stopScan: vi.fn(),
    getResults: vi.fn(),
    on: vi.fn(),
    off: vi.fn()
  }
}));

describe('Scan Workflow Integration', () => {
  it('should complete full scan workflow', async () => {
    const user = userEvent.setup();
    const mockWifiScanner = await import('../services/wifiScanner.js');
    
    // Mock scan results
    const mockResults = [
      { ssid: 'TestNetwork', bssid: '00:11:22:33:44:55', signal: -45 },
      { ssid: 'AnotherNetwork', bssid: '66:77:88:99:aa:bb', signal: -60 }
    ];
    
    mockWifiScanner.default.startScan.mockResolvedValue({ success: true });
    mockWifiScanner.default.getResults.mockResolvedValue(mockResults);
    
    render(<ScanDashboard />);
    
    // Start scan
    const startButton = screen.getByText('Start Scan');
    await user.click(startButton);
    
    // Wait for scan to start
    await waitFor(() => {
      expect(screen.getByText('Scanning...')).toBeInTheDocument();
    });
    
    // Simulate scan completion
    const stopButton = screen.getByText('Stop Scan');
    await user.click(stopButton);
    
    // Wait for results to appear
    await waitFor(() => {
      expect(screen.getByText('TestNetwork')).toBeInTheDocument();
      expect(screen.getByText('AnotherNetwork')).toBeInTheDocument();
    });
    
    // Verify results display
    expect(screen.getByText('00:11:22:33:44:55')).toBeInTheDocument();
    expect(screen.getByText('-45 dBm')).toBeInTheDocument();
  });
});
```

### Phase 5: CI/CD Integration (Week 8)

#### 5.1 GitHub Actions Workflow

**File: `.github/workflows/test.yml`**

```yaml
name: Test Suite

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run backend tests
        run: |
          pytest tests/ --cov=src/piwardrive --cov-report=xml --cov-report=term-missing
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: backend
          name: backend-coverage
          fail_ci_if_error: true

  frontend-tests:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [16.x, 18.x, 20.x]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
          cache-dependency-path: 'webui/package-lock.json'
      
      - name: Install dependencies
        run: |
          cd webui
          npm ci
      
      - name: Run frontend tests
        run: |
          cd webui
          npm run test:coverage
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./webui/coverage/coverage-final.json
          flags: frontend
          name: frontend-coverage
          fail_ci_if_error: true

  integration-tests:
    runs-on: ubuntu-latest
    needs: [backend-tests, frontend-tests]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: 'webui/package-lock.json'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          cd webui && npm ci
      
      - name: Build frontend
        run: |
          cd webui
          npm run build
      
      - name: Run integration tests
        run: |
          pytest tests/integration/ -v
      
      - name: Run E2E tests
        run: |
          cd webui
          npm run test:e2e
```

## Implementation Timeline

### Week 1: Infrastructure Setup
- [ ] Configure pytest and vitest
- [ ] Set up test databases and mocks
- [ ] Create test utilities and fixtures
- [ ] Set up CI/CD pipeline

### Week 2-3: Critical Backend Tests
- [ ] Core services tests (alerting, coordinator, etc.)
- [ ] API endpoint tests (auth, monitoring, etc.)
- [ ] Database layer tests
- [ ] Error handling tests

### Week 4-5: Frontend Component Tests
- [ ] Core component tests (App, auth, config)
- [ ] Scanner component tests
- [ ] Service layer tests
- [ ] Utility function tests

### Week 6-7: Integration Tests
- [ ] API workflow tests
- [ ] Frontend integration tests
- [ ] End-to-end user workflows
- [ ] Performance tests

### Week 8: Finalization
- [ ] CI/CD integration
- [ ] Coverage reporting
- [ ] Documentation updates
- [ ] Quality gates implementation

## Success Metrics

- **Backend Coverage**: 85% (target) vs 66% (current)
- **Frontend Coverage**: 80% (target) vs 5% (current)
- **Test Execution Time**: < 5 minutes total
- **Test Reliability**: < 1% flaky tests
- **CI/CD Success Rate**: > 95%

## Resource Requirements

- **Senior Developer**: 160 hours (4 weeks × 40 hours)
- **Frontend Developer**: 120 hours (3 weeks × 40 hours)
- **QA Engineer**: 80 hours (2 weeks × 40 hours)
- **Total**: 360 hours (~9 person-weeks)

This comprehensive test implementation plan will establish a robust testing foundation for the PiWardrive project, ensuring high code quality and enabling confident development and deployment practices.
