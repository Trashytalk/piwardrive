import { useEffect, useState } from 'react';

export default function ConsoleView() {
  const [logs, setLogs] = useState('');
  const [path, setPath] = useState('/var/log/syslog');
  const [paths, setPaths] = useState([]);

  useEffect(() => {
    fetch('/config')
      .then(r => r.json())
      .then(cfg => {
        if (Array.isArray(cfg.log_paths) && cfg.log_paths.length) {
          setPaths(cfg.log_paths);
          setPath(cfg.log_paths[0]);
        }
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    const load = () => {
      fetch(`/logs?lines=200&path=${encodeURIComponent(path)}`)
        .then(r => r.json())
        .then(d => setLogs(d.lines.join('\n')))
        .catch(() => {});
    };
    load();
    const id = setInterval(load, 2000);
    return () => clearInterval(id);
  }, [path]);

  return (
    <div>
      <h2>Console</h2>
      <pre style={{ maxHeight: '200px', overflowY: 'auto' }}>{logs}</pre>
      {paths.length > 1 && (
        <select value={path} onChange={e => setPath(e.target.value)}>
          {paths.map(p => (
            <option key={p}>{p}</option>
          ))}
        </select>
      )}
    </div>
  );
}
