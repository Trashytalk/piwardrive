// Vite will bundle any components that match this glob so plugin widgets can be
// loaded dynamically by name. Plugin authors should place React components under
// `webui/src/components` with file names matching the Python class names.
import { useEffect, useState } from 'react';
import { reportError } from './exceptionHandler.js';
import { enhancedFetch, useConnectionStatus } from './utils/networkErrorHandler.js';
import { LoadingSpinner, LoadingOverlay } from './components/LoadingStates.jsx';
import { ErrorDisplay, ConnectionStatus } from './components/ErrorDisplay.jsx';
import ErrorBoundary from './components/ErrorBoundary.jsx';
import BatteryStatus from './components/BatteryStatus.jsx';
import ServiceStatus from './components/ServiceStatus.jsx';
import HandshakeCount from './components/HandshakeCount.jsx';
import SignalStrength from './components/SignalStrength.jsx';
import { NetworkThroughputWidget as NetworkThroughput } from './components/PerformanceWidgets.jsx';
import CPUTempGraph from './components/CPUTempGraph.jsx';
import StatsDashboard from './components/StatsDashboard.jsx';
import SystemStats from './components/SystemStats.jsx';
import TrackMap from './components/TrackMap.jsx';
import VehicleStats from './components/VehicleStats.jsx';
import GeofenceEditor from './components/GeofenceEditor.jsx';
import SettingsScreen from './components/SettingsScreen.jsx';
import MapScreen from './components/MapScreen.jsx';
import Orientation from './components/Orientation.jsx';
import VehicleInfo from './components/VehicleInfo.jsx';
import VectorTileCustomizer from './components/VectorTileCustomizer.jsx';
import './styles/errorHandling.css';
import './styles/dashboard.css';

// Plugin module loader (placeholder - would need actual dynamic import setup)
const pluginModules = {};

export default function App() {
  const [status, setStatus] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [logs, setLogs] = useState('');
  const [plugins, setPlugins] = useState([]);
  const [widgets, setWidgets] = useState([]);
  const [orientationData, setOrientationData] = useState(null);
  const [vehicleData, setVehicleData] = useState(null);
  const [configData, setConfigData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { isOnline, connectionQuality } = useConnectionStatus();

  const handleChange = (key, value) => {
    setConfigData((prev) => ({ ...prev, [key]: value }));
  };

  const saveConfig = async () => {
    try {
      const response = await enhancedFetch('/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(configData),
      });
      
      if (response.ok) {
        const data = await response.json();
        setConfigData(data);
        setError(null);
      }
    } catch (err) {
      setError(err);
      reportError(err);
    }
  };

  useEffect(() => {
    const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    let ws;
    let es;
    let ping;

    const handleData = (raw) => {
      try {
        const data = JSON.parse(raw);
        if (data.status) setStatus(data.status);
        if (data.metrics) setMetrics(data.metrics);
        setError(null); // Clear errors on successful data
      } catch (e) {
        setError(e);
        reportError(e);
      }
    };

    const startSse = () => {
      es = new EventSource('/sse/status');
      es.onmessage = (ev) => handleData(ev.data);
      es.onerror = (err) => {
        setError(new Error('Server-Sent Events connection failed'));
        es.close();
        setTimeout(startSse, 3000);
      };
    };

    const startWs = () => {
      if (ws) ws.close();
      try {
        ws = new WebSocket(`${proto}//${window.location.host}/ws/status`);
        ws.onopen = () => {
          setError(null); // Clear errors on successful connection
          if (ping) clearInterval(ping);
          ping = setInterval(() => {
            if (ws.readyState === WebSocket.OPEN) {
              ws.send('ping');
            }
          }, 15000);
        };
        ws.onmessage = (ev) => handleData(ev.data);
        ws.onerror = (err) => {
          setError(new Error('WebSocket connection failed'));
          ws.close();
        };
        ws.onclose = () => {
          if (ping) {
            clearInterval(ping);
            ping = null;
          }
          setTimeout(() => {
            if (window.WebSocket) {
              startWs();
            } else {
              startSse();
            }
          }, 3000);
        };
      } catch (e) {
        setError(e);
        startSse();
      }
    };

    const initializeApp = async () => {
      setLoading(true);
      try {
        // Initialize WebSocket/SSE connections
        if (window.WebSocket) {
          startWs();
        } else {
          startSse();
        }

        // Fetch initial data with enhanced error handling
        const initialRequests = [
          enhancedFetch('/status').then(r => r.json()).then(setStatus),
          enhancedFetch('/widget-metrics').then(r => r.json()).then(setMetrics),
          enhancedFetch('/api/plugins').then(r => r.json()).then(setPlugins),
          enhancedFetch('/logs?lines=20').then(r => r.json()).then(d => setLogs(d.lines.join('\n')))
        ];

        await Promise.allSettled(initialRequests);
        setError(null);
      } catch (err) {
        setError(err);
        reportError(err);
      } finally {
        setLoading(false);
      }
    };

    initializeApp();

    return () => {
      if (ping) clearInterval(ping);
      if (ws) ws.close();
      if (es) es.close();
    };
  }, []);

  useEffect(() => {
    const loadWidgets = async () => {
      try {
        const loaded = [];
        for (const name of plugins) {
          const path = `./components/${name}.jsx`;
          const importer = pluginModules[path];
          if (importer) {
            try {
              const mod = await importer();
              loaded.push({ name, Component: mod.default });
            } catch (err) {
              console.warn(`Failed to load plugin widget ${name}:`, err);
              reportError(err);
            }
          }
        }
        setWidgets(loaded);
      } catch (err) {
        setError(err);
        reportError(err);
      }
    };
    
    if (plugins.length > 0) {
      loadWidgets();
    }
  }, [plugins]);

  return (
    <div>
      <ConnectionStatus isOnline={isOnline} connectionQuality={connectionQuality} />
      
      {error && (
        <ErrorDisplay 
          error={error} 
          onRetry={() => {
            setError(null);
            window.location.reload();
          }}
        />
      )}
      
      {loading && <LoadingOverlay message="Loading PiWardrive dashboard..." />}
      
      <ErrorBoundary>
        <h2>Map</h2>
        <MapScreen />
      </ErrorBoundary>
      
      <ErrorBoundary>
        <SystemStats />
      </ErrorBoundary>
      
      <ErrorBoundary>
        <TrackMap />
      </ErrorBoundary>
      
      <h2>Status</h2>
      <pre>{JSON.stringify(status, null, 2)}</pre>
      
      <h2>Widget Metrics</h2>
      <pre>{JSON.stringify(metrics, null, 2)}</pre>
      
      <h2>Plugin Widgets</h2>
      <ul>
        {plugins.map((p) => (
          <li key={p}>{p}</li>
        ))}
      </ul>
      
      {widgets.map(({ name, Component }) => (
        <ErrorBoundary key={name} fallback={<div>Failed to load widget: {name}</div>}>
          <Component metrics={metrics} />
        </ErrorBoundary>
      ))}
      
      <h2>Dashboard</h2>
      <div className="dashboard-grid">
        <ErrorBoundary fallback={<div>Battery status unavailable</div>}>
          <BatteryStatus metrics={metrics} />
        </ErrorBoundary>
        
        <ErrorBoundary fallback={<div>Service status unavailable</div>}>
          <ServiceStatus metrics={metrics} />
        </ErrorBoundary>
        
        <ErrorBoundary fallback={<div>Handshake count unavailable</div>}>
          <HandshakeCount metrics={metrics} />
        </ErrorBoundary>
        
        <ErrorBoundary fallback={<div>Signal strength unavailable</div>}>
          <SignalStrength metrics={metrics} />
        </ErrorBoundary>
        
        <ErrorBoundary fallback={<div>Vehicle stats unavailable</div>}>
          <VehicleStats metrics={metrics} />
        </ErrorBoundary>
        
        <ErrorBoundary fallback={<div>Orientation data unavailable</div>}>
          <Orientation data={orientationData} />
        </ErrorBoundary>
        
        <ErrorBoundary fallback={<div>Vehicle info unavailable</div>}>
          <VehicleInfo data={vehicleData} />
        </ErrorBoundary>
        
        <ErrorBoundary fallback={<div>Network throughput unavailable</div>}>
          <NetworkThroughput metrics={metrics} />
        </ErrorBoundary>
        
        <ErrorBoundary fallback={<div>CPU temperature unavailable</div>}>
          <CPUTempGraph metrics={metrics} />
        </ErrorBoundary>
        
        <ErrorBoundary fallback={<div>Stats dashboard unavailable</div>}>
          <StatsDashboard />
        </ErrorBoundary>
      </div>

      <h2>Logs</h2>
      <pre>{logs}</pre>
      
      <ErrorBoundary>
        <h2>Geofences</h2>
        <GeofenceEditor />
      </ErrorBoundary>
      
      <ErrorBoundary>
        <VectorTileCustomizer />
      </ErrorBoundary>
      
      <ErrorBoundary>
        <SettingsScreen />
      </ErrorBoundary>
    </div>
  );
}
