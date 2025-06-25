import { useEffect, useState } from 'react';
import DashboardLayout from './components/DashboardLayout.jsx';
import GeofenceEditor from './components/GeofenceEditor.jsx';
import SettingsForm from './components/SettingsForm.jsx';
import MapScreen from './components/MapScreen.jsx';
import VectorTileCustomizer from './components/VectorTileCustomizer.jsx';

export default function App() {
  const [status, setStatus] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [logs, setLogs] = useState('');
  const [plugins, setPlugins] = useState([]);
  const [widgets, setWidgets] = useState([]);

  useEffect(() => {
    const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    let ws;
    let es;

    const handleData = (raw) => {
      try {
        const data = JSON.parse(raw);
        if (data.status) setStatus(data.status);
        if (data.metrics) setMetrics(data.metrics);
      } catch (e) {
        console.error('status parse error', e);
      }
    };

    const startSse = () => {
      es = new EventSource('/sse/status');
      es.onmessage = (ev) => handleData(ev.data);
      es.onerror = () => es.close();
    };

    if (window.WebSocket) {
      try {
        ws = new WebSocket(`${proto}//${window.location.host}/ws/status`);
        ws.onmessage = (ev) => handleData(ev.data);
        ws.onerror = () => {
          ws.close();
          startSse();
        };
      } catch (e) {
        startSse();
      }
    } else {
      startSse();
    }

    fetch('/status')
      .then(r => r.json())
      .then(setStatus);
    fetch('/widget-metrics')
      .then(r => r.json())
      .then(setMetrics);
    fetch('/api/plugins')
      .then(r => r.json())
      .then(setPlugins);
    fetch('/logs?lines=20')
      .then(r => r.json())
      .then(d => setLogs(d.lines.join('\n')));
    fetch('/config')
      .then(r => r.json())
      .then(setConfigData);
    return () => {
      if (ws) ws.close();
      if (es) es.close();
    };
  }, []);

  return (
    <div>
      <h2>Map</h2>
      <MapScreen />
      <h2>Status</h2>
      <pre>{JSON.stringify(status, null, 2)}</pre>
      <h2>Widget Metrics</h2>
      <pre>{JSON.stringify(metrics, null, 2)}</pre>
      <h2>Plugin Widgets</h2>
      <ul>
        {plugins.map(p => (
          <li key={p}>{p}</li>
        ))}
      </ul>
      <h2>Dashboard</h2>
      <DashboardLayout metrics={metrics} />

      <h2>Logs</h2>
      <pre>{logs}</pre>
      <h2>Geofences</h2>
      <GeofenceEditor />
      <VectorTileCustomizer />
      {configData && (
        <section>
          <h2>Settings</h2>
          {Object.keys(configData).map(k => (
            <div key={k}>
              <label>{k}</label>
              <input
                value={configData[k] ?? ''}
                onChange={e => handleChange(k, e.target.value)}
              />
            </div>
          ))}
          <button onClick={saveConfig}>Save</button>
        </section>
      )}
    </div>
  );
}

