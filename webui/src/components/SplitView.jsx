import { useEffect, useState } from 'react';

export default function SplitView() {
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

  if (!metrics) return <div>Metrics: N/A</div>;

  const {
    cpu_temp,
    bssid_count,
    handshake_count,
    avg_rssi,
    kismet_running,
    bettercap_running,
    gps_fix,
  } = metrics;

  return (
    <div>
      <h2>Metrics</h2>
      <ul>
        <li>CPU: {cpu_temp != null ? cpu_temp.toFixed(1) + '°C' : 'N/A'}</li>
        <li>BSSIDs: {bssid_count}</li>
        <li>Handshakes: {handshake_count}</li>
        <li>Avg RSSI: {avg_rssi != null ? avg_rssi.toFixed(1) + ' dBm' : 'N/A'}</li>
        <li>Kismet: {kismet_running ? 'OK' : 'DOWN'}</li>
        <li>BetterCAP: {bettercap_running ? 'OK' : 'DOWN'}</li>
        <li>Fix: {gps_fix}</li>
      </ul>
    </div>
  );
}
