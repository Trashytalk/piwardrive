import { useEffect, useState } from 'react';
import BatteryStatus from './components/BatteryStatus.jsx';
import ServiceStatus from './components/ServiceStatus.jsx';
import HandshakeCount from './components/HandshakeCount.jsx';
import SignalStrength from './components/SignalStrength.jsx';
import NetworkThroughput from './components/NetworkThroughput.jsx';
import CPUTempGraph from './components/CPUTempGraph.jsx';
import VehicleStats from './components/VehicleStats.jsx';
import SettingsForm from './components/SettingsForm.jsx';

export default function App() {
  const [status, setStatus] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [logs, setLogs] = useState('');
  const [plugins, setPlugins] = useState([]);

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
    fetch('/logs?lines=20')
      .then(r => r.json())
      .then(d => setLogs(d.lines.join('\n')));
    return () => ws.close();
  }, []);

  return (
    <div>
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
      <NetworkThroughput metrics={metrics} />
      <CPUTempGraph metrics={metrics} />

      <h2>Logs</h2>
      <pre>{logs}</pre>
      <SettingsForm />
    </div>
  );
}

