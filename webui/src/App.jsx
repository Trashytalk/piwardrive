import { useEffect, useState } from 'react';

export default function App() {
  const [status, setStatus] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [logs, setLogs] = useState('');

  useEffect(() => {
    fetch('/status')
      .then(r => r.json())
      .then(setStatus);
    fetch('/widget-metrics')
      .then(r => r.json())
      .then(setMetrics);
    fetch('/logs?lines=20')
      .then(r => r.json())
      .then(d => setLogs(d.lines.join('\n')));
  }, []);

  return (
    <div>
      <h2>Status</h2>
      <pre>{JSON.stringify(status, null, 2)}</pre>
      <h2>Widget Metrics</h2>
      <pre>{JSON.stringify(metrics, null, 2)}</pre>
      <h2>Logs</h2>
      <pre>{logs}</pre>
    </div>
  );
}
