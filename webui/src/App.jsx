import { useEffect, useState } from "react";
import BatteryStatus from "./components/BatteryStatus.jsx";
import ServiceStatus from "./components/ServiceStatus.jsx";
import HandshakeCount from "./components/HandshakeCount.jsx";
import SignalStrength from "./components/SignalStrength.jsx";
import NetworkThroughput from "./components/NetworkThroughput.jsx";
import CPUTempGraph from "./components/CPUTempGraph.jsx";
import StatsDashboard from "./components/StatsDashboard.jsx";
import VehicleStats from "./components/VehicleStats.jsx";
import GeofenceEditor from "./components/GeofenceEditor.jsx";
import SettingsScreen from "./components/SettingsScreen.jsx";
import MapScreen from "./components/MapScreen.jsx";
import Orientation from "./components/Orientation.jsx";
import VehicleInfo from "./components/VehicleInfo.jsx";
import VectorTileCustomizer from "./components/VectorTileCustomizer.jsx";

export default function App() {
  const [status, setStatus] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [logs, setLogs] = useState("");
  const [plugins, setPlugins] = useState([]);
  const [widgets, setWidgets] = useState([]);
  const [orientationData, setOrientationData] = useState(null);
  const [vehicleData, setVehicleData] = useState(null);

  useEffect(() => {
    const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
    let ws;
    let es;

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
      es = new EventSource("/sse/status");
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
        {plugins.map((p) => (
          <li key={p}>{p}</li>
        ))}
      </ul>
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
      <SettingsScreen />
    </div>
  );
}
