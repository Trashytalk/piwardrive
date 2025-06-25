import { useEffect, useState } from 'react';
import MapScreen from './MapScreen.jsx';

export default function SplitScreen() {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    const load = () => {
      fetch('/widget-metrics')
        .then(r => r.json())
        .then(setMetrics)
        .catch(() => {});
    };
    load();
    const id = setInterval(load, 2000);
    return () => clearInterval(id);
  }, []);

  const cpu = metrics?.cpu_temp != null ? metrics.cpu_temp.toFixed(1) + '°C' : 'N/A';
  const handshakes = metrics?.handshake_count ?? 'N/A';
  const rssi = metrics?.avg_rssi != null ? metrics.avg_rssi.toFixed(1) + ' dBm' : 'N/A';
  const kismet = metrics?.kismet_running ? 'OK' : 'DOWN';
  const bettercap = metrics?.bettercap_running ? 'OK' : 'DOWN';
  const gps = metrics?.gps_fix ?? 'N/A';

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <div style={{ flex: 2 }}>
        <MapScreen />
      </div>
      <div style={{ flex: 1, overflowY: 'auto', padding: '0 1em' }}>
        <h3>Metrics</h3>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li>CPU: {cpu}</li>
          <li>Handshakes: {handshakes}</li>
          <li>Avg RSSI: {rssi}</li>
          <li>Kismet: {kismet}</li>
          <li>BetterCAP: {bettercap}</li>
          <li>Fix: {gps}</li>
        </ul>
      </div>
    </div>
  );
}
