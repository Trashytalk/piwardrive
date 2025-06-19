import { useEffect, useState } from 'react';
import './App.css';

export default function App() {
  const [status, setStatus] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [logs, setLogs] = useState('');
  const [configData, setConfigData] = useState(null);
  const [widgets, setWidgets] = useState([]);

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
    fetch('/api/widgets')
      .then(r => r.json())
      .then(d => setWidgets(d.widgets));
    fetch('/logs?lines=20')
      .then(r => r.json())
      .then(d => setLogs(d.lines.join('\n')));
    fetch('/config')
      .then(r => r.json())
      .then(setConfigData);
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
    <div className="container">
      <section>
        <h2>Status</h2>
        <pre>{JSON.stringify(status, null, 2)}</pre>
      </section>
      <section>
        <h2>Widget Metrics</h2>
        <pre>{JSON.stringify(metrics, null, 2)}</pre>
      </section>
      <section>
        <h2>Logs</h2>
        <pre>{logs}</pre>
      </section>
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

