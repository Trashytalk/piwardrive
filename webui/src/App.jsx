import { useEffect, useState } from 'react';

// Vite will bundle any components that match this glob so plugin widgets can be
// loaded dynamically by name. Plugin authors should place React components under
// `webui/src/components` with file names matching the Python class names.
const pluginModules = import.meta.glob('./components/*.jsx');
import BatteryStatus from './components/BatteryStatus.jsx';
import ServiceStatus from './components/ServiceStatus.jsx';
import HandshakeCount from './components/HandshakeCount.jsx';
import SignalStrength from './components/SignalStrength.jsx';
import NetworkThroughput from './components/NetworkThroughput.jsx';
import CPUTempGraph from './components/CPUTempGraph.jsx';
import StatsDashboard from './components/StatsDashboard.jsx';
import SystemStats from './components/SystemStats.jsx';
import VehicleStats from './components/VehicleStats.jsx';
import GeofenceEditor from './components/GeofenceEditor.jsx';
import SettingsForm from './components/SettingsForm.jsx';
import TrackMap from './components/TrackMap.jsx';
import Orientation from './components/Orientation.jsx';
import VehicleInfo from './components/VehicleInfo.jsx';
import VectorTileCustomizer from './components/VectorTileCustomizer.jsx';

export default function App() {
  const [status, setStatus] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [logs, setLogs] = useState("");
  const [plugins, setPlugins] = useState([]);
  const [widgets, setWidgets] = useState([]);
  const [orientationData, setOrientationData] = useState(null);
  const [vehicleData, setVehicleData] = useState(null);
  const [configData, setConfigData] = useState(null);

  const handleChange = (key, value) => {
    setConfigData(prev => ({ ...prev, [key]: value }));
  };

  const saveConfig = () => {
    fetch('/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(configData),
    })
      .then(r => r.json())
      .then(setConfigData)
      .catch(() => {});
  };

  useEffect(() => {
    const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
    let ws;
    let es;
    let ping;

    const handleData = (raw) => {
      try {
        const data = JSON.parse(raw);
        if (data.status) setStatus(data.status);
        if (data.metrics) setMetrics(data.metrics);
      } catch (e) {
        console.error("status parse error", e);
      }
    };

    const startSse = () => {
      if (es) es.close();
      es = new EventSource("/sse/status");
      es.onmessage = (ev) => handleData(ev.data);
      es.onerror = () => {
        es.close();
        setTimeout(startSse, 3000);
      };
    };

    const startWs = () => {
      if (ws) ws.close();
      try {
        ws = new WebSocket(`${proto}//${window.location.host}/ws/status`);
        ws.onopen = () => {
          if (ping) clearInterval(ping);
          ping = setInterval(() => {
            if (ws.readyState === WebSocket.OPEN) {
              ws.send("ping");
            }
          }, 15000);
        };
        ws.onmessage = (ev) => handleData(ev.data);
        ws.onerror = () => ws.close();
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
        startSse();
      }
    };

    if (window.WebSocket) {
      startWs();
    } else {
      startSse();
    }

    fetch("/status")
      .then((r) => r.json())
      .then(setStatus);
    fetch("/widget-metrics")
      .then((r) => r.json())
      .then(setMetrics);
    fetch("/api/plugins")
      .then((r) => r.json())
      .then(setPlugins);
    fetch("/logs?lines=20")
      .then((r) => r.json())
      .then((d) => setLogs(d.lines.join("\n")));
    fetch("/config")
      .then((r) => r.json())
      .then(setConfigData);
    return () => {
      if (ping) clearInterval(ping);
      if (ws) ws.close();
      if (es) es.close();
    };
  }, []);

  useEffect(() => {
    const loadWidgets = async () => {
      const loaded = [];
      for (const name of plugins) {
        const path = `./components/${name}.jsx`;
        const importer = pluginModules[path];
        if (importer) {
          try {
            const mod = await importer();
            loaded.push({ name, Component: mod.default });
          } catch (err) {
            console.error('Failed loading plugin component', name, err);
          }
        }
      }
      setWidgets(loaded);
    };
    loadWidgets();
  }, [plugins]);

  return (
    <div>
      <h2>Map</h2>
      <MapScreen />
      <SystemStats />
      <TrackMap />
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
        <Component key={name} metrics={metrics} />
      ))}
      <h2>Dashboard</h2>
      <BatteryStatus metrics={metrics} />
      <ServiceStatus metrics={metrics} />
      <HandshakeCount metrics={metrics} />
      <SignalStrength metrics={metrics} />
      <VehicleStats metrics={metrics} />
      <Orientation data={orientationData} />
      <VehicleInfo data={vehicleData} />
      <NetworkThroughput metrics={metrics} />
      <CPUTempGraph metrics={metrics} />
      <StatsDashboard />

      <h2>Logs</h2>
      <pre>{logs}</pre>
      <h2>Geofences</h2>
      <GeofenceEditor />
      <VectorTileCustomizer />
      {configData && (
        <section>
          <h2>Settings</h2>
          {Object.keys(configData).map((k) => (
            <div key={k}>
              <label>{k}</label>
              <input
                value={configData[k] ?? ""}
                onChange={(e) => handleChange(k, e.target.value)}
              />
            </div>
          ))}
          <button onClick={saveConfig}>Save</button>
        </section>
      )}
    </div>
  );
}
