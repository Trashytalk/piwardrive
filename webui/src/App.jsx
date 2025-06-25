import { useEffect, useState } from 'react';
import BatteryStatus from './components/BatteryStatus.jsx';
import ServiceStatus from './components/ServiceStatus.jsx';
import HandshakeCount from './components/HandshakeCount.jsx';
import SignalStrength from './components/SignalStrength.jsx';
import NetworkThroughput from './components/NetworkThroughput.jsx';
import CPUTempGraph from './components/CPUTempGraph.jsx';
import StatsDashboard from './components/StatsDashboard.jsx';
import VehicleStats from './components/VehicleStats.jsx';
import MapScreen from './components/MapScreen.jsx';
import Orientation from './components/Orientation.jsx';
import VehicleInfo from './components/VehicleInfo.jsx';

export default function App() {
  const [status, setStatus] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [logs, setLogs] = useState('');
  const [configData, setConfigData] = useState(null);
  const [plugins, setPlugins] = useState([]);
  const [orientationData, setOrientationData] = useState(null);
  const [vehicleData, setVehicleData] = useState(null);

  useEffect(() => {
    const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${proto}//${window.location.host}/ws/status`);
    ws.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data);
        if (data.status) setStatus(data.status);
        if (data.metrics) setMetrics(data.metrics);
      } catch (e) {
        console.error('ws parse error', e);
      }
    };
    ws.onerror = () => ws.close();

    fetch('/status')
      .then(r => r.json())
      .then(setStatus);
    fetch('/widget-metrics')
      .then(r => r.json())
      .then(setMetrics);
    fetch('/plugins')
      .then(r => r.json())
      .then(setPlugins);
    fetch('/api/widgets')
      .then(r => r.json())
      .then(d => setWidgets(d.widgets));
    fetch('/logs?lines=20')
      .then(r => r.json())
      .then(d => setLogs(d.lines.join('\n')));
    fetch('/config')
      .then(r => r.json())
      .then(setConfigData);
    fetch('/orientation')
      .then(r => r.json())
      .then(setOrientationData)
      .catch(() => setOrientationData(null));
    fetch('/vehicle')
      .then(r => r.json())
      .then(setVehicleData)
      .catch(() => setVehicleData(null));
    return () => ws.close();
  }, []);

  const handleChange = (k, v) => {
    setConfigData({ ...configData, [k]: v });
  };

  const saveConfig = () => {
    fetch('/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(configData),
    })
      .then(r => r.json())
      .then(setConfigData)
      .catch(e => console.error('save failed', e));
  };

  return (
    <div>
      <h2>Map</h2>
      <MapScreen />
      <h2>Status</h2>
      <pre>{JSON.stringify(status, null, 2)}</pre>
      <h2>Widget Metrics</h2>
      <pre>{JSON.stringify(metrics, null, 2)}</pre>
      <h2>Plugin Widgets</h2>
      <pre>{JSON.stringify(plugins, null, 2)}</pre>
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

