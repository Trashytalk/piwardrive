# Plugin Development Guide

This guide covers developing custom plugins and widgets for PiWardrive, including both backend Python plugins and frontend JavaScript widgets.

## Architecture Overview

PiWardrive uses a flexible plugin architecture that allows extending functionality through:
- **Backend Python plugins**: Custom data processing, external integrations, and API endpoints
- **Frontend JavaScript widgets**: Custom UI components and visualizations
- **Widget configuration**: Dynamic widget loading and configuration management

## Backend Python Plugin Development

### Plugin Structure

Backend plugins are Python modules that extend PiWardrive's core functionality:

```python
# src/piwardrive/plugins/my_plugin.py
import asyncio
from typing import Dict, Any
from piwardrive.plugin_base import PiWardrivePlugin

class MyPlugin(PiWardrivePlugin):
    """Example plugin that demonstrates the plugin interface."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.name = "my_plugin"
        self.version = "1.0.0"
    
    async def initialize(self) -> None:
        """Initialize plugin resources."""
        self.logger.info(f"Initializing {self.name} v{self.version}")
        # Setup database tables, connections, etc.
    
    async def process_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming data and return results."""
        # Transform data, call external APIs, etc.
        return {"processed": True, "data": data}
    
    async def cleanup(self) -> None:
        """Clean up plugin resources."""
        self.logger.info(f"Cleaning up {self.name}")
        # Close connections, save state, etc.
```

### Plugin Registration

Register plugins in the plugin manager:

```python
# src/piwardrive/plugins/__init__.py
from .my_plugin import MyPlugin

AVAILABLE_PLUGINS = {
    'my_plugin': MyPlugin,
}
```

### Configuration

Plugin configuration is handled through the main configuration system:

```json
{
  "plugins": {
    "my_plugin": {
      "enabled": true,
      "api_key": "your-api-key",
      "refresh_interval": 300
    }
  }
}
```

### Adding API Endpoints

Plugins can expose custom API endpoints:

```python
from fastapi import APIRouter

class MyPlugin(PiWardrivePlugin):
    def get_router(self) -> APIRouter:
        """Return FastAPI router for plugin endpoints."""
        router = APIRouter(prefix="/api/my-plugin")
        
        @router.get("/status")
        async def get_status():
            return {"status": "active", "version": self.version}
        
        @router.post("/process")
        async def process_request(data: dict):
            result = await self.process_data(data)
            return result
        
        return router
```

## Frontend JavaScript Widget Development

### Widget Structure

Frontend widgets are JavaScript modules that integrate with the PiWardrive web interface:

```javascript
// webui/src/widgets/MyWidget.js
import { BaseWidget } from './BaseWidget.js';

export class MyWidget extends BaseWidget {
    constructor(config) {
        super(config);
        this.name = 'my_widget';
        this.title = 'My Custom Widget';
        this.refreshInterval = 5000;
    }

    async initialize() {
        this.container = document.createElement('div');
        this.container.className = 'widget my-widget';
        this.container.innerHTML = `
            <div class="widget-header">
                <h3>${this.title}</h3>
                <div class="widget-controls">
                    <button class="refresh-btn">Refresh</button>
                </div>
            </div>
            <div class="widget-content">
                <div id="my-widget-data"></div>
            </div>
        `;
        
        this.setupEventListeners();
        await this.refresh();
    }

    setupEventListeners() {
        const refreshBtn = this.container.querySelector('.refresh-btn');
        refreshBtn.addEventListener('click', () => this.refresh());
    }

    async refresh() {
        try {
            const response = await fetch('/api/my-plugin/status');
            const data = await response.json();
            this.updateDisplay(data);
        } catch (error) {
            this.showError('Failed to load data');
        }
    }

    updateDisplay(data) {
        const content = this.container.querySelector('#my-widget-data');
        content.innerHTML = `
            <div class="status-item">
                <span class="label">Status:</span>
                <span class="value">${data.status}</span>
            </div>
            <div class="status-item">
                <span class="label">Version:</span>
                <span class="value">${data.version}</span>
            </div>
        `;
    }

    showError(message) {
        const content = this.container.querySelector('#my-widget-data');
        content.innerHTML = `<div class="error">${message}</div>`;
    }

    destroy() {
        if (this.container && this.container.parentNode) {
            this.container.parentNode.removeChild(this.container);
        }
    }
}
```

### Widget Registration

Register widgets in the widget manager:

```javascript
// webui/src/widgets/index.js
import { MyWidget } from './MyWidget.js';

export const AVAILABLE_WIDGETS = {
    'my_widget': MyWidget,
};
```

### Widget Configuration

Widgets can be configured through the dashboard settings:

```json
{
  "widgets": ["my_widget"],
  "layout": [
    {"cls": "my_widget", "position": {"x": 0, "y": 0, "w": 6, "h": 4}}
  ]
}
```

## Advanced Plugin Features

### Database Integration

Plugins can interact with the database:

```python
class MyPlugin(PiWardrivePlugin):
    async def initialize(self):
        # Create plugin-specific tables
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS my_plugin_data (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                data TEXT
            )
        """)
    
    async def save_data(self, data: Dict[str, Any]):
        await self.db.execute(
            "INSERT INTO my_plugin_data (timestamp, data) VALUES (?, ?)",
            (data['timestamp'], json.dumps(data))
        )
```

### External Service Integration

Plugins can integrate with external services:

```python
import aiohttp

class ExternalServicePlugin(PiWardrivePlugin):
    async def fetch_external_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                'https://api.example.com/data',
                headers={'Authorization': f'Bearer {self.config["api_key"]}'}
            ) as response:
                return await response.json()
```

### Event System

Plugins can subscribe to and emit events:

```python
class MyPlugin(PiWardrivePlugin):
    async def initialize(self):
        # Subscribe to events
        self.event_manager.subscribe('wifi_scan_complete', self.handle_wifi_scan)
        self.event_manager.subscribe('gps_location_update', self.handle_gps_update)
    
    async def handle_wifi_scan(self, data):
        # Process WiFi scan results
        processed = await self.process_wifi_data(data)
        # Emit processed data
        await self.event_manager.emit('wifi_data_processed', processed)
```

## Testing Plugins

### Unit Testing

Create unit tests for your plugin:

```python
# tests/test_my_plugin.py
import pytest
from unittest.mock import Mock, AsyncMock
from piwardrive.plugins.my_plugin import MyPlugin

@pytest.mark.asyncio
async def test_plugin_initialization():
    config = {'api_key': 'test-key'}
    plugin = MyPlugin(config)
    
    await plugin.initialize()
    assert plugin.name == 'my_plugin'
    assert plugin.version == '1.0.0'

@pytest.mark.asyncio
async def test_data_processing():
    plugin = MyPlugin({'api_key': 'test-key'})
    test_data = {'test': 'data'}
    
    result = await plugin.process_data(test_data)
    assert result['processed'] is True
    assert result['data'] == test_data
```

### Integration Testing

Test plugin integration with the main application:

```python
# tests/test_my_plugin_integration.py
import pytest
from fastapi.testclient import TestClient
from piwardrive.service import app
from piwardrive.plugins.my_plugin import MyPlugin

@pytest.fixture
def client():
    return TestClient(app)

def test_plugin_api_endpoint(client):
    # Test plugin API endpoints
    response = client.get('/api/my-plugin/status')
    assert response.status_code == 200
    assert 'status' in response.json()
```

## Widget Testing

### JavaScript Unit Testing

Use Vitest for widget testing:

```javascript
// webui/tests/MyWidget.test.js
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { MyWidget } from '../src/widgets/MyWidget.js';

describe('MyWidget', () => {
    let widget;
    
    beforeEach(() => {
        global.fetch = vi.fn();
        widget = new MyWidget({});
    });

    it('initializes correctly', async () => {
        await widget.initialize();
        expect(widget.name).toBe('my_widget');
        expect(widget.title).toBe('My Custom Widget');
    });

    it('refreshes data correctly', async () => {
        global.fetch.mockResolvedValue({
            json: () => Promise.resolve({ status: 'active', version: '1.0.0' })
        });
        
        await widget.initialize();
        await widget.refresh();
        
        expect(global.fetch).toHaveBeenCalledWith('/api/my-plugin/status');
    });
});
```

## Best Practices

### Security

- **Input validation**: Always validate and sanitize plugin inputs
- **Authentication**: Implement proper authentication for plugin APIs
- **Rate limiting**: Implement rate limiting for external API calls
- **Error handling**: Provide comprehensive error handling and logging

### Performance

- **Async operations**: Use async/await for I/O operations
- **Caching**: Implement caching for expensive operations
- **Resource cleanup**: Properly clean up resources in plugin cleanup methods
- **Memory management**: Monitor memory usage for long-running plugins

### Maintainability

- **Documentation**: Document plugin configuration and usage
- **Logging**: Implement comprehensive logging with appropriate levels
- **Configuration**: Use configuration files for plugin settings
- **Version management**: Implement proper version management and migrations

## Plugin Examples

### Weather Plugin

```python
class WeatherPlugin(PiWardrivePlugin):
    async def get_weather(self, lat: float, lon: float):
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.config['api_key'],
            'units': 'metric'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                return await response.json()
```

### Traffic Monitor Plugin

```python
class TrafficPlugin(PiWardrivePlugin):
    async def analyze_traffic(self, interface: str):
        # Monitor network traffic patterns
        stats = await self.get_interface_stats(interface)
        patterns = await self.analyze_patterns(stats)
        
        await self.event_manager.emit('traffic_analysis', {
            'interface': interface,
            'patterns': patterns,
            'timestamp': time.time()
        })
```

## Deployment and Distribution

### Plugin Packaging

Package plugins for distribution:

```python
# setup.py for plugin distribution
from setuptools import setup, find_packages

setup(
    name='piwardrive-my-plugin',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'piwardrive>=0.1.0',
        # plugin-specific dependencies
    ],
    entry_points={
        'piwardrive.plugins': [
            'my_plugin = my_plugin:MyPlugin',
        ],
    },
)
```

### Installation

Install plugins using pip:

```bash
pip install piwardrive-my-plugin
```

The plugin will be automatically discovered and available for configuration.

## Troubleshooting

### Common Issues

1. **Plugin not loading**: Check plugin registration and imports
2. **Configuration errors**: Validate plugin configuration schema
3. **API errors**: Check endpoint registration and routing
4. **Performance issues**: Profile plugin performance and optimize

### Debug Mode

Enable debug mode for detailed plugin logging:

```json
{
  "logging": {
    "level": "DEBUG",
    "plugins": {
      "my_plugin": "DEBUG"
    }
  }
}
```

## Support and Resources

- **Plugin API Reference**: See `src/piwardrive/plugin_base.py`
- **Widget Examples**: Check `webui/src/widgets/` for examples
- **Integration Tests**: See `tests/test_*_integration.py` for integration testing patterns
- **Community Plugins**: Browse community-contributed plugins

For questions and support, please refer to the project documentation and community forums.
