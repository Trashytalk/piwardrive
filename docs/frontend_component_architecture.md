# Frontend Component Architecture Documentation

This document provides comprehensive documentation for the PiWardrive frontend architecture, component design patterns, and development guidelines.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Component Hierarchy](#component-hierarchy)
- [Core Components](#core-components)
- [Widget System](#widget-system)
- [State Management](#state-management)
- [Data Flow](#data-flow)
- [Component Development Guidelines](#component-development-guidelines)
- [Testing Components](#testing-components)
- [Performance Optimization](#performance-optimization)

## Architecture Overview

The PiWardrive frontend follows a modular React architecture with a plugin-based widget system for dashboard customization.

```
Frontend Architecture
┌─────────────────────────────────────────────────────────────┐
│                     App.jsx (Root)                          │
├─────────────────────────────────────────────────────────────┤
│  Navigation Layer                                           │
│  ├── NavBar.jsx                                            │
│  └── MobileLayout.jsx                                      │
├─────────────────────────────────────────────────────────────┤
│  Core Application                                          │
│  ├── DashboardLayout.jsx (Main Dashboard)                  │
│  ├── MapScreen.jsx (Geographic View)                       │
│  ├── SettingsScreen.jsx (Configuration)                    │
│  └── LoginForm.jsx (Authentication)                        │
├─────────────────────────────────────────────────────────────┤
│  Widget System                                             │
│  ├── Widget Plugins (Pluggable Components)                 │
│  ├── Widget Manager (Plugin Loading)                       │
│  └── Widget Configuration                                  │
├─────────────────────────────────────────────────────────────┤
│  Service Layer                                             │
│  ├── webApiClient.js (API Communication)                   │
│  ├── backendService.js (Data Layer)                        │
│  └── auth.js (Authentication)                              │
├─────────────────────────────────────────────────────────────┤
│  Utility Layer                                             │
│  ├── hooks.js (Custom React Hooks)                         │
│  ├── utils.js (Helper Functions)                           │
│  └── config.js (Configuration)                             │
└─────────────────────────────────────────────────────────────┘
```

## Component Hierarchy

### Main Application Structure

```
App.jsx
├── NavBar.jsx
│   ├── LoginForm.jsx
│   └── MobileAlerts.jsx
├── DashboardLayout.jsx
│   ├── Widget Grid System
│   │   ├── SystemStats.jsx
│   │   ├── LiveMetrics.jsx
│   │   ├── GPSStatus.jsx
│   │   └── [Dynamic Widgets...]
│   └── SplitView.jsx
│       ├── MapScreen.jsx
│       └── AnalyticsWidgets.jsx
├── SettingsScreen.jsx
│   ├── SettingsForm.jsx
│   ├── SecurityConfig.jsx
│   └── ExportCenter.jsx
└── Modal Components
    ├── LogViewer.jsx
    ├── HealthImport.jsx
    └── ConfigWatcher.jsx
```

### Widget Component Hierarchy

```
Widget Base System
├── Base Widget Class
│   ├── AnalyticsWidgets.jsx
│   │   ├── BaselineAnalysis.jsx
│   │   ├── BehavioralAnalytics.jsx
│   │   └── PredictiveAnalytics.jsx
│   ├── System Widgets
│   │   ├── CPUTempGraph.jsx
│   │   ├── DiskUsageTrend.jsx
│   │   ├── NetworkThroughput.jsx
│   │   └── BatteryStatus.jsx
│   ├── Scanning Widgets
│   │   ├── ScanningStatus.jsx
│   │   ├── HandshakeCount.jsx
│   │   └── SignalStrength.jsx
│   ├── Geographic Widgets
│   │   ├── TrackMap.jsx
│   │   ├── HeatmapLayer.jsx
│   │   └── MovementTracker.jsx
│   └── Security Widgets
│       ├── SecurityWidgets.jsx
│       ├── ThreatIntelligence.jsx
│       └── VulnerabilityScanner.jsx
```

## Core Components

### DashboardLayout.jsx

The main dashboard component that orchestrates widget display and layout management.

```jsx
import React, { useState, useEffect } from 'react';
import { WidgetGrid } from './WidgetGrid';
import { SplitView } from './SplitView';
import { useWidgetManager } from '../hooks/useWidgetManager';

const DashboardLayout = () => {
  const [layout, setLayout] = useState('grid');
  const [widgets, setWidgets] = useState([]);
  const { loadWidgets, saveLayout } = useWidgetManager();

  useEffect(() => {
    const initializeDashboard = async () => {
      try {
        const loadedWidgets = await loadWidgets();
        setWidgets(loadedWidgets);
      } catch (error) {
        console.error('Failed to load widgets:', error);
      }
    };

    initializeDashboard();
  }, []);

  const handleLayoutChange = (newLayout) => {
    setLayout(newLayout);
    saveLayout(newLayout);
  };

  const handleWidgetUpdate = (widgetId, data) => {
    setWidgets(prev => prev.map(widget => 
      widget.id === widgetId 
        ? { ...widget, data }
        : widget
    ));
  };

  return (
    <div className="dashboard-layout">
      <header className="dashboard-header">
        <h1>PiWardrive Dashboard</h1>
        <div className="layout-controls">
          <button 
            onClick={() => handleLayoutChange('grid')}
            className={layout === 'grid' ? 'active' : ''}
          >
            Grid View
          </button>
          <button 
            onClick={() => handleLayoutChange('split')}
            className={layout === 'split' ? 'active' : ''}
          >
            Split View
          </button>
        </div>
      </header>

      <main className="dashboard-content">
        {layout === 'grid' ? (
          <WidgetGrid 
            widgets={widgets}
            onWidgetUpdate={handleWidgetUpdate}
          />
        ) : (
          <SplitView 
            widgets={widgets}
            onWidgetUpdate={handleWidgetUpdate}
          />
        )}
      </main>
    </div>
  );
};

export default DashboardLayout;
```

**Key Features:**
- Dynamic widget loading and management
- Layout switching between grid and split views
- Real-time widget data updates
- Responsive design support

### SystemStats.jsx

Real-time system monitoring component with performance metrics.

```jsx
import React, { useState, useEffect } from 'react';
import { useWebSocket } from '../hooks/useWebSocket';
import { MetricCard } from './MetricCard';
import { TrendChart } from './TrendChart';

const SystemStats = ({ refreshInterval = 5000 }) => {
  const [metrics, setMetrics] = useState({
    cpu: 0,
    memory: 0,
    temperature: 0,
    disk: 0
  });
  const [history, setHistory] = useState([]);
  const [alerts, setAlerts] = useState([]);

  // WebSocket connection for real-time updates
  const { data: wsData, isConnected } = useWebSocket('/ws/system/metrics');

  useEffect(() => {
    if (wsData) {
      const newMetrics = {
        cpu: wsData.cpu_usage,
        memory: wsData.memory_usage,
        temperature: wsData.temperature,
        disk: wsData.disk_usage
      };

      setMetrics(newMetrics);
      
      // Update history for trends
      setHistory(prev => {
        const updated = [...prev, { ...newMetrics, timestamp: Date.now() }];
        return updated.slice(-100); // Keep last 100 points
      });

      // Check for alerts
      checkAlerts(newMetrics);
    }
  }, [wsData]);

  const checkAlerts = (currentMetrics) => {
    const newAlerts = [];
    
    if (currentMetrics.cpu > 80) {
      newAlerts.push({ type: 'warning', message: 'High CPU usage detected' });
    }
    if (currentMetrics.temperature > 70) {
      newAlerts.push({ type: 'error', message: 'Temperature threshold exceeded' });
    }
    if (currentMetrics.memory > 90) {
      newAlerts.push({ type: 'warning', message: 'Low memory available' });
    }

    setAlerts(newAlerts);
  };

  return (
    <div className="system-stats-widget">
      <header className="widget-header">
        <h3>System Performance</h3>
        <div className="connection-status">
          <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
            {isConnected ? '🟢' : '🔴'}
          </span>
        </div>
      </header>

      {alerts.length > 0 && (
        <div className="alerts-section">
          {alerts.map((alert, index) => (
            <div key={index} className={`alert alert-${alert.type}`}>
              {alert.message}
            </div>
          ))}
        </div>
      )}

      <div className="metrics-grid">
        <MetricCard
          title="CPU Usage"
          value={metrics.cpu}
          unit="%"
          threshold={80}
          icon="🖥️"
        />
        <MetricCard
          title="Memory"
          value={metrics.memory}
          unit="%"
          threshold={90}
          icon="💾"
        />
        <MetricCard
          title="Temperature"
          value={metrics.temperature}
          unit="°C"
          threshold={70}
          icon="🌡️"
        />
        <MetricCard
          title="Disk Usage"
          value={metrics.disk}
          unit="%"
          threshold={85}
          icon="💿"
        />
      </div>

      <div className="trends-section">
        <TrendChart
          data={history}
          metrics={['cpu', 'memory', 'temperature']}
          timeWindow="1h"
        />
      </div>
    </div>
  );
};

export default SystemStats;
```

### MapScreen.jsx

Interactive map component for geographic data visualization.

```jsx
import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, HeatmapLayer } from 'react-leaflet';
import { useMapData } from '../hooks/useMapData';
import { HeatmapLayer } from './HeatmapLayer';
import { AccessPointMarker } from './AccessPointMarker';

const MapScreen = ({ 
  initialCenter = [40.7128, -74.0060], 
  initialZoom = 13,
  showHeatmap = true,
  showAccessPoints = true,
  showTrackData = true 
}) => {
  const mapRef = useRef(null);
  const [mapCenter, setMapCenter] = useState(initialCenter);
  const [zoom, setZoom] = useState(initialZoom);
  const [selectedAP, setSelectedAP] = useState(null);
  const [filters, setFilters] = useState({
    minSignalStrength: -80,
    encryption: 'all',
    timeRange: '24h'
  });

  const {
    accessPoints,
    trackData,
    heatmapData,
    isLoading,
    error,
    refresh
  } = useMapData(filters);

  useEffect(() => {
    // Auto-refresh map data every 30 seconds
    const interval = setInterval(refresh, 30000);
    return () => clearInterval(interval);
  }, [refresh]);

  const handleMarkerClick = (accessPoint) => {
    setSelectedAP(accessPoint);
    // Center map on selected access point
    setMapCenter([accessPoint.lat, accessPoint.lon]);
  };

  const handleMapMove = (event) => {
    const map = event.target;
    setMapCenter([map.getCenter().lat, map.getCenter().lng]);
    setZoom(map.getZoom());
  };

  if (error) {
    return (
      <div className="map-error">
        <p>Error loading map data: {error.message}</p>
        <button onClick={refresh}>Retry</button>
      </div>
    );
  }

  return (
    <div className="map-screen">
      <div className="map-controls">
        <div className="filter-controls">
          <label>
            Min Signal Strength:
            <input
              type="range"
              min="-100"
              max="-20"
              value={filters.minSignalStrength}
              onChange={(e) => setFilters(prev => ({
                ...prev,
                minSignalStrength: parseInt(e.target.value)
              }))}
            />
            <span>{filters.minSignalStrength} dBm</span>
          </label>

          <label>
            Encryption:
            <select
              value={filters.encryption}
              onChange={(e) => setFilters(prev => ({
                ...prev,
                encryption: e.target.value
              }))}
            >
              <option value="all">All</option>
              <option value="open">Open</option>
              <option value="wep">WEP</option>
              <option value="wpa">WPA/WPA2</option>
              <option value="wpa3">WPA3</option>
            </select>
          </label>

          <div className="layer-toggles">
            <label>
              <input
                type="checkbox"
                checked={showHeatmap}
                onChange={(e) => setShowHeatmap(e.target.checked)}
              />
              Heatmap
            </label>
            <label>
              <input
                type="checkbox"
                checked={showAccessPoints}
                onChange={(e) => setShowAccessPoints(e.target.checked)}
              />
              Access Points
            </label>
            <label>
              <input
                type="checkbox"
                checked={showTrackData}
                onChange={(e) => setShowTrackData(e.target.checked)}
              />
              Track Data
            </label>
          </div>
        </div>

        <div className="map-stats">
          <span>Access Points: {accessPoints.length}</span>
          <span>Track Points: {trackData.length}</span>
          {isLoading && <span className="loading">Loading...</span>}
        </div>
      </div>

      <MapContainer
        ref={mapRef}
        center={mapCenter}
        zoom={zoom}
        className="leaflet-map"
        onMoveEnd={handleMapMove}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />

        {/* Heatmap Layer */}
        {showHeatmap && heatmapData.length > 0 && (
          <HeatmapLayer
            points={heatmapData}
            longitudeExtractor={point => point.lon}
            latitudeExtractor={point => point.lat}
            intensityExtractor={point => point.intensity}
          />
        )}

        {/* Access Point Markers */}
        {showAccessPoints && accessPoints.map(ap => (
          <AccessPointMarker
            key={ap.bssid}
            accessPoint={ap}
            onClick={() => handleMarkerClick(ap)}
            isSelected={selectedAP?.bssid === ap.bssid}
          />
        ))}

        {/* Track Data */}
        {showTrackData && trackData.length > 1 && (
          <Polyline
            positions={trackData.map(point => [point.lat, point.lon])}
            color="blue"
            weight={2}
            opacity={0.7}
          />
        )}

        {/* Selected Access Point Popup */}
        {selectedAP && (
          <Popup
            position={[selectedAP.lat, selectedAP.lon]}
            onClose={() => setSelectedAP(null)}
          >
            <div className="ap-popup">
              <h4>{selectedAP.ssid || 'Hidden Network'}</h4>
              <p><strong>BSSID:</strong> {selectedAP.bssid}</p>
              <p><strong>Signal:</strong> {selectedAP.signal_strength} dBm</p>
              <p><strong>Channel:</strong> {selectedAP.channel}</p>
              <p><strong>Encryption:</strong> {selectedAP.encryption}</p>
              <p><strong>Vendor:</strong> {selectedAP.vendor || 'Unknown'}</p>
              <p><strong>First Seen:</strong> {new Date(selectedAP.first_seen).toLocaleString()}</p>
            </div>
          </Popup>
        )}
      </MapContainer>
    </div>
  );
};

export default MapScreen;
```

## Widget System

### Base Widget Architecture

All widgets extend from a base widget class that provides common functionality:

```jsx
// widgets/base/BaseWidget.jsx
import React, { useState, useEffect } from 'react';

export class BaseWidget extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: null,
      loading: false,
      error: null,
      lastUpdate: null
    };
  }

  componentDidMount() {
    this.initialize();
    if (this.props.autoRefresh) {
      this.startAutoRefresh();
    }
  }

  componentWillUnmount() {
    this.cleanup();
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval);
    }
  }

  async initialize() {
    // Override in child classes
  }

  async fetchData() {
    // Override in child classes
    throw new Error('fetchData must be implemented by child class');
  }

  async refresh() {
    this.setState({ loading: true, error: null });
    
    try {
      const data = await this.fetchData();
      this.setState({
        data,
        loading: false,
        lastUpdate: new Date(),
        error: null
      });
    } catch (error) {
      this.setState({
        error: error.message,
        loading: false
      });
    }
  }

  startAutoRefresh() {
    const interval = this.props.refreshInterval || 30000; // 30 seconds default
    this.refreshInterval = setInterval(() => {
      this.refresh();
    }, interval);
  }

  cleanup() {
    // Override in child classes for cleanup
  }

  renderHeader() {
    return (
      <div className="widget-header">
        <h3 className="widget-title">{this.props.title}</h3>
        <div className="widget-controls">
          <button 
            onClick={() => this.refresh()} 
            disabled={this.state.loading}
            className="refresh-button"
          >
            🔄
          </button>
          {this.props.onSettings && (
            <button 
              onClick={this.props.onSettings}
              className="settings-button"
            >
              ⚙️
            </button>
          )}
        </div>
      </div>
    );
  }

  renderError() {
    if (!this.state.error) return null;

    return (
      <div className="widget-error">
        <p>Error: {this.state.error}</p>
        <button onClick={() => this.refresh()}>Retry</button>
      </div>
    );
  }

  renderLoading() {
    if (!this.state.loading) return null;

    return (
      <div className="widget-loading">
        <div className="spinner"></div>
        <p>Loading...</p>
      </div>
    );
  }

  render() {
    return (
      <div className={`widget ${this.props.className || ''}`}>
        {this.renderHeader()}
        <div className="widget-content">
          {this.renderError()}
          {this.renderLoading()}
          {!this.state.loading && !this.state.error && this.renderContent()}
        </div>
        {this.state.lastUpdate && (
          <div className="widget-footer">
            Last updated: {this.state.lastUpdate.toLocaleTimeString()}
          </div>
        )}
      </div>
    );
  }

  renderContent() {
    // Override in child classes
    return <div>No content implemented</div>;
  }
}
```

### Widget Plugin System

Dynamic widget loading and plugin management:

```javascript
// widgetPlugins.js
class WidgetManager {
  constructor() {
    this.widgets = new Map();
    this.pluginPaths = [];
    this.loadedPlugins = new Set();
  }

  registerWidget(name, componentClass, metadata = {}) {
    this.widgets.set(name, {
      component: componentClass,
      metadata: {
        title: name,
        description: '',
        category: 'general',
        version: '1.0.0',
        author: 'Unknown',
        ...metadata
      }
    });
  }

  async loadPlugin(pluginPath) {
    if (this.loadedPlugins.has(pluginPath)) {
      return;
    }

    try {
      const plugin = await import(pluginPath);
      
      // Register all widgets from plugin
      if (plugin.widgets) {
        for (const [name, config] of Object.entries(plugin.widgets)) {
          this.registerWidget(name, config.component, config.metadata);
        }
      }

      this.loadedPlugins.add(pluginPath);
      console.log(`Loaded plugin: ${pluginPath}`);
    } catch (error) {
      console.error(`Failed to load plugin ${pluginPath}:`, error);
    }
  }

  async loadAllPlugins() {
    const pluginPromises = this.pluginPaths.map(path => this.loadPlugin(path));
    await Promise.all(pluginPromises);
  }

  getWidget(name) {
    return this.widgets.get(name);
  }

  getAllWidgets() {
    return Array.from(this.widgets.entries()).map(([name, config]) => ({
      name,
      ...config
    }));
  }

  getWidgetsByCategory(category) {
    return this.getAllWidgets().filter(widget => 
      widget.metadata.category === category
    );
  }

  createWidgetInstance(name, props = {}) {
    const widget = this.getWidget(name);
    if (!widget) {
      throw new Error(`Widget '${name}' not found`);
    }

    return React.createElement(widget.component, {
      key: `widget-${name}-${Date.now()}`,
      ...props
    });
  }
}

// Global widget manager instance
export const widgetManager = new WidgetManager();

// Auto-discover and load plugins
widgetManager.pluginPaths = [
  './plugins/system-widgets',
  './plugins/analytics-widgets',
  './plugins/security-widgets',
  './plugins/custom-widgets'
];
```

## State Management

### Global State with Context

```jsx
// context/AppContext.jsx
import React, { createContext, useContext, useReducer, useEffect } from 'react';

const AppStateContext = createContext();
const AppDispatchContext = createContext();

const initialState = {
  user: null,
  isAuthenticated: false,
  systemStatus: 'unknown',
  activeScan: null,
  notifications: [],
  widgets: [],
  settings: {
    theme: 'light',
    autoRefresh: true,
    refreshInterval: 30000
  }
};

function appReducer(state, action) {
  switch (action.type) {
    case 'SET_USER':
      return {
        ...state,
        user: action.payload,
        isAuthenticated: !!action.payload
      };

    case 'SET_SYSTEM_STATUS':
      return {
        ...state,
        systemStatus: action.payload
      };

    case 'START_SCAN':
      return {
        ...state,
        activeScan: action.payload
      };

    case 'COMPLETE_SCAN':
      return {
        ...state,
        activeScan: null
      };

    case 'ADD_NOTIFICATION':
      return {
        ...state,
        notifications: [...state.notifications, action.payload]
      };

    case 'REMOVE_NOTIFICATION':
      return {
        ...state,
        notifications: state.notifications.filter(n => n.id !== action.payload)
      };

    case 'UPDATE_WIDGETS':
      return {
        ...state,
        widgets: action.payload
      };

    case 'UPDATE_SETTINGS':
      return {
        ...state,
        settings: { ...state.settings, ...action.payload }
      };

    default:
      throw new Error(`Unhandled action type: ${action.type}`);
  }
}

export function AppProvider({ children }) {
  const [state, dispatch] = useReducer(appReducer, initialState);

  // Persist settings to localStorage
  useEffect(() => {
    const savedSettings = localStorage.getItem('piwardrive-settings');
    if (savedSettings) {
      dispatch({
        type: 'UPDATE_SETTINGS',
        payload: JSON.parse(savedSettings)
      });
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('piwardrive-settings', JSON.stringify(state.settings));
  }, [state.settings]);

  return (
    <AppStateContext.Provider value={state}>
      <AppDispatchContext.Provider value={dispatch}>
        {children}
      </AppDispatchContext.Provider>
    </AppStateContext.Provider>
  );
}

export function useAppState() {
  const context = useContext(AppStateContext);
  if (context === undefined) {
    throw new Error('useAppState must be used within an AppProvider');
  }
  return context;
}

export function useAppDispatch() {
  const context = useContext(AppDispatchContext);
  if (context === undefined) {
    throw new Error('useAppDispatch must be used within an AppProvider');
  }
  return context;
}
```

### Custom Hooks for Data Management

```jsx
// hooks/useWebSocket.js
import { useState, useEffect, useRef } from 'react';

export function useWebSocket(url, options = {}) {
  const [data, setData] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState(null);
  const [reconnectAttempts, setReconnectAttempts] = useState(0);
  
  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);

  const {
    maxReconnectAttempts = 5,
    reconnectInterval = 3000,
    onConnect,
    onDisconnect,
    onError,
    onMessage
  } = options;

  const connect = () => {
    try {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${protocol}//${window.location.host}${url}`;
      
      wsRef.current = new WebSocket(wsUrl);

      wsRef.current.onopen = () => {
        setIsConnected(true);
        setError(null);
        setReconnectAttempts(0);
        onConnect?.();
      };

      wsRef.current.onmessage = (event) => {
        try {
          const parsedData = JSON.parse(event.data);
          setData(parsedData);
          onMessage?.(parsedData);
        } catch (err) {
          console.error('Failed to parse WebSocket message:', err);
        }
      };

      wsRef.current.onclose = () => {
        setIsConnected(false);
        onDisconnect?.();
        
        // Attempt to reconnect
        if (reconnectAttempts < maxReconnectAttempts) {
          reconnectTimeoutRef.current = setTimeout(() => {
            setReconnectAttempts(prev => prev + 1);
            connect();
          }, reconnectInterval);
        }
      };

      wsRef.current.onerror = (err) => {
        setError(err);
        onError?.(err);
      };
    } catch (err) {
      setError(err);
    }
  };

  const disconnect = () => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    if (wsRef.current) {
      wsRef.current.close();
    }
  };

  const sendMessage = (message) => {
    if (wsRef.current && isConnected) {
      wsRef.current.send(JSON.stringify(message));
    }
  };

  useEffect(() => {
    connect();
    return disconnect;
  }, [url]);

  return {
    data,
    isConnected,
    error,
    reconnectAttempts,
    sendMessage,
    disconnect,
    reconnect: connect
  };
}
```

## Data Flow

### API Data Flow Architecture

```
Data Flow Architecture
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Components                       │
├─────────────────────────────────────────────────────────────┤
│  Custom Hooks Layer                                         │
│  ├── useWebSocket() - Real-time data                       │
│  ├── useApiData() - REST API calls                         │
│  ├── usePolling() - Periodic updates                       │
│  └── useCache() - Data caching                             │
├─────────────────────────────────────────────────────────────┤
│  Service Layer                                              │
│  ├── webApiClient.js - HTTP client                         │
│  ├── websocketClient.js - WebSocket client                 │
│  ├── cacheManager.js - Client-side caching                 │
│  └── errorHandler.js - Error handling                      │
├─────────────────────────────────────────────────────────────┤
│  Backend API                                                │
│  ├── REST Endpoints (/api/v1/*)                           │
│  ├── WebSocket Streams (/ws/*)                            │
│  └── Server-Sent Events (/events/*)                       │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Examples

```javascript
// Example: Real-time scan data flow
const ScanMonitor = () => {
  // 1. Component subscribes to WebSocket
  const { data: scanData, isConnected } = useWebSocket('/ws/v1/scans/active');
  
  // 2. Component manages local state
  const [accessPoints, setAccessPoints] = useState([]);
  const [scanStatus, setScanStatus] = useState('idle');

  // 3. Process incoming WebSocket data
  useEffect(() => {
    if (scanData) {
      switch (scanData.type) {
        case 'scan_started':
          setScanStatus('running');
          break;
        case 'access_point_found':
          setAccessPoints(prev => [...prev, scanData.data]);
          break;
        case 'scan_completed':
          setScanStatus('completed');
          break;
      }
    }
  }, [scanData]);

  // 4. Render with real-time updates
  return (
    <div>
      <div>Status: {scanStatus}</div>
      <div>Access Points: {accessPoints.length}</div>
      <div>Connection: {isConnected ? 'Connected' : 'Disconnected'}</div>
    </div>
  );
};
```

## Component Development Guidelines

### Component Structure Standards

```jsx
// Standard component structure
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import './ComponentName.css';

/**
 * ComponentName - Brief description of what this component does
 * 
 * @param {Object} props - Component props
 * @param {string} props.title - Component title
 * @param {Function} props.onUpdate - Update callback
 * @param {boolean} props.isActive - Active state
 */
const ComponentName = ({ 
  title = 'Default Title',
  onUpdate,
  isActive = false,
  children,
  ...otherProps 
}) => {
  // 1. State declarations
  const [localState, setLocalState] = useState(null);
  const [loading, setLoading] = useState(false);

  // 2. Effect hooks
  useEffect(() => {
    // Component initialization
  }, []);

  // 3. Event handlers
  const handleClick = (event) => {
    event.preventDefault();
    onUpdate?.(localState);
  };

  // 4. Computed values
  const computedClassName = `component-name ${isActive ? 'active' : ''} ${loading ? 'loading' : ''}`;

  // 5. Early returns for error/loading states
  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  // 6. Main render
  return (
    <div className={computedClassName} {...otherProps}>
      <header className="component-header">
        <h3>{title}</h3>
      </header>
      
      <main className="component-content">
        {children}
      </main>
      
      <footer className="component-footer">
        <button onClick={handleClick}>Update</button>
      </footer>
    </div>
  );
};

// 7. PropTypes definition
ComponentName.propTypes = {
  title: PropTypes.string,
  onUpdate: PropTypes.func,
  isActive: PropTypes.bool,
  children: PropTypes.node
};

export default ComponentName;
```

### Error Boundary Implementation

```jsx
// components/ErrorBoundary.jsx
import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      hasError: false, 
      error: null,
      errorInfo: null 
    };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error,
      errorInfo
    });

    // Log error to monitoring service
    console.error('Component Error:', error, errorInfo);
    
    // Send to error reporting service
    if (window.errorReporter) {
      window.errorReporter.captureException(error, {
        extra: errorInfo,
        tags: { component: 'ErrorBoundary' }
      });
    }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h2>Something went wrong</h2>
          <details>
            <summary>Error Details</summary>
            <pre>{this.state.error && this.state.error.toString()}</pre>
            <pre>{this.state.errorInfo.componentStack}</pre>
          </details>
          <button onClick={() => window.location.reload()}>
            Reload Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

## Testing Components

### Unit Testing with React Testing Library

```javascript
// __tests__/SystemStats.test.jsx
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SystemStats } from '../SystemStats';

// Mock WebSocket hook
jest.mock('../hooks/useWebSocket', () => ({
  useWebSocket: jest.fn()
}));

describe('SystemStats Component', () => {
  const mockWebSocket = {
    data: {
      cpu_usage: 45.5,
      memory_usage: 67.2,
      temperature: 55.0,
      disk_usage: 78.3
    },
    isConnected: true
  };

  beforeEach(() => {
    require('../hooks/useWebSocket').useWebSocket.mockReturnValue(mockWebSocket);
  });

  it('renders system metrics correctly', () => {
    render(<SystemStats />);
    
    expect(screen.getByText('System Performance')).toBeInTheDocument();
    expect(screen.getByText('45.5')).toBeInTheDocument(); // CPU
    expect(screen.getByText('67.2')).toBeInTheDocument(); // Memory
    expect(screen.getByText('55.0')).toBeInTheDocument(); // Temperature
  });

  it('shows connection status indicator', () => {
    render(<SystemStats />);
    
    const statusIndicator = screen.getByText('🟢');
    expect(statusIndicator).toBeInTheDocument();
  });

  it('displays alerts for high values', () => {
    const highTempData = {
      ...mockWebSocket,
      data: {
        ...mockWebSocket.data,
        temperature: 85.0 // Above threshold
      }
    };

    require('../hooks/useWebSocket').useWebSocket.mockReturnValue(highTempData);
    
    render(<SystemStats />);
    
    expect(screen.getByText(/Temperature threshold exceeded/)).toBeInTheDocument();
  });

  it('handles refresh button click', async () => {
    const user = userEvent.setup();
    render(<SystemStats />);
    
    const refreshButton = screen.getByRole('button', { name: /🔄/ });
    await user.click(refreshButton);
    
    // Verify refresh action was triggered
    expect(refreshButton).toBeInTheDocument();
  });
});
```

### Integration Testing

```javascript
// __tests__/integration/Dashboard.integration.test.jsx
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AppProvider } from '../../context/AppContext';
import { DashboardLayout } from '../DashboardLayout';

// Mock API calls
global.fetch = jest.fn();

const renderWithProviders = (component) => {
  return render(
    <BrowserRouter>
      <AppProvider>
        {component}
      </AppProvider>
    </BrowserRouter>
  );
};

describe('Dashboard Integration', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  it('loads and displays widgets on dashboard', async () => {
    // Mock API responses
    fetch
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          widgets: [
            { id: 'system-stats', type: 'SystemStats', enabled: true },
            { id: 'gps-status', type: 'GPSStatus', enabled: true }
          ]
        })
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          cpu_usage: 45,
          memory_usage: 67,
          temperature: 55
        })
      });

    renderWithProviders(<DashboardLayout />);

    // Wait for widgets to load
    await waitFor(() => {
      expect(screen.getByText('System Performance')).toBeInTheDocument();
    });

    // Verify API calls were made
    expect(fetch).toHaveBeenCalledWith('/api/v1/widgets/config');
    expect(fetch).toHaveBeenCalledWith('/api/v1/system/stats');
  });

  it('handles API errors gracefully', async () => {
    // Mock API error
    fetch.mockRejectedValueOnce(new Error('Network error'));

    renderWithProviders(<DashboardLayout />);

    await waitFor(() => {
      expect(screen.getByText(/Error loading widgets/)).toBeInTheDocument();
    });
  });
});
```

## Performance Optimization

### Memoization and Optimization

```jsx
// Optimized component with React.memo and useMemo
import React, { memo, useMemo, useCallback } from 'react';

const OptimizedMetricCard = memo(({ 
  title, 
  value, 
  unit, 
  threshold, 
  history = [] 
}) => {
  // Memoize expensive calculations
  const trend = useMemo(() => {
    if (history.length < 2) return 'stable';
    
    const recent = history.slice(-5);
    const avg = recent.reduce((sum, val) => sum + val, 0) / recent.length;
    const current = recent[recent.length - 1];
    
    const change = ((current - avg) / avg) * 100;
    
    if (Math.abs(change) < 2) return 'stable';
    return change > 0 ? 'increasing' : 'decreasing';
  }, [history]);

  // Memoize style calculations
  const cardStyle = useMemo(() => {
    const isHighValue = value > threshold;
    return {
      backgroundColor: isHighValue ? '#ffe6e6' : '#f0f9ff',
      borderColor: isHighValue ? '#ff4444' : '#0088cc',
      color: isHighValue ? '#cc0000' : '#333333'
    };
  }, [value, threshold]);

  // Memoize trend indicator
  const trendIndicator = useMemo(() => {
    switch (trend) {
      case 'increasing': return '📈';
      case 'decreasing': return '📉';
      default: return '➡️';
    }
  }, [trend]);

  return (
    <div className="metric-card" style={cardStyle}>
      <div className="metric-header">
        <span className="metric-title">{title}</span>
        <span className="trend-indicator">{trendIndicator}</span>
      </div>
      <div className="metric-value">
        {value.toFixed(1)}{unit}
      </div>
      <div className="metric-threshold">
        Threshold: {threshold}{unit}
      </div>
    </div>
  );
});

OptimizedMetricCard.displayName = 'OptimizedMetricCard';

export default OptimizedMetricCard;
```

### Virtual Scrolling for Large Lists

```jsx
// components/VirtualScrollList.jsx
import React, { useState, useEffect, useRef, useMemo } from 'react';

const VirtualScrollList = ({ 
  items, 
  itemHeight = 50, 
  containerHeight = 400,
  renderItem,
  overscan = 5 
}) => {
  const [scrollTop, setScrollTop] = useState(0);
  const containerRef = useRef(null);

  // Calculate visible range
  const visibleRange = useMemo(() => {
    const startIndex = Math.max(0, Math.floor(scrollTop / itemHeight) - overscan);
    const endIndex = Math.min(
      items.length - 1,
      Math.floor((scrollTop + containerHeight) / itemHeight) + overscan
    );
    
    return { startIndex, endIndex };
  }, [scrollTop, itemHeight, containerHeight, items.length, overscan]);

  // Get visible items
  const visibleItems = useMemo(() => {
    const result = [];
    for (let i = visibleRange.startIndex; i <= visibleRange.endIndex; i++) {
      result.push({
        index: i,
        data: items[i],
        offsetY: i * itemHeight
      });
    }
    return result;
  }, [items, visibleRange, itemHeight]);

  const handleScroll = (event) => {
    setScrollTop(event.target.scrollTop);
  };

  const totalHeight = items.length * itemHeight;

  return (
    <div
      ref={containerRef}
      className="virtual-scroll-container"
      style={{ height: containerHeight, overflow: 'auto' }}
      onScroll={handleScroll}
    >
      <div style={{ height: totalHeight, position: 'relative' }}>
        {visibleItems.map(({ index, data, offsetY }) => (
          <div
            key={index}
            style={{
              position: 'absolute',
              top: offsetY,
              left: 0,
              right: 0,
              height: itemHeight
            }}
          >
            {renderItem(data, index)}
          </div>
        ))}
      </div>
    </div>
  );
};

// Usage example
const AccessPointList = ({ accessPoints }) => {
  const renderAccessPoint = (ap, index) => (
    <div className="access-point-item">
      <span className="ssid">{ap.ssid}</span>
      <span className="signal">{ap.signal_strength} dBm</span>
      <span className="encryption">{ap.encryption}</span>
    </div>
  );

  return (
    <VirtualScrollList
      items={accessPoints}
      itemHeight={60}
      containerHeight={500}
      renderItem={renderAccessPoint}
    />
  );
};
```

This comprehensive frontend documentation provides detailed information about the component architecture, development patterns, state management, testing strategies, and performance optimization techniques used in the PiWardrive frontend application.
