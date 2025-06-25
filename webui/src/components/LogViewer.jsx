import { useEffect, useState } from 'react';

export default function LogViewer({ logPaths = [] }) {
  const defaultPath = logPaths[0] || '/var/log/syslog';
  const [path, setPath] = useState(defaultPath);
  const [filter, setFilter] = useState('');
  const [logs, setLogs] = useState('');

  useEffect(() => {
    if (logPaths.length > 0) setPath(logPaths[0]);
  }, [logPaths]);

  useEffect(() => {
    let id;
    const load = async () => {
      try {
        const resp = await fetch(
          `/logs?lines=200&path=${encodeURIComponent(path)}`,
        );
        const data = await resp.json();
        let lines = data.lines || [];
        if (filter) {
          try {
            const re = new RegExp(filter);
            lines = lines.filter(l => re.test(l));
          } catch {
            // ignore invalid regex
          }
        }
        setLogs(lines.join('\n'));
      } catch {
        /* ignore */
      }
    };
    load();
    id = setInterval(load, 2000);
    return () => clearInterval(id);
  }, [path, filter]);

  return (
    <section>
      <div style={{ marginBottom: '0.5em' }}>
        <select value={path} onChange={e => setPath(e.target.value)}>
          {logPaths.map(p => (
            <option key={p} value={p}>
              {p.split('/').pop()}
            </option>
          ))}
        </select>
        <input
          placeholder="Filter"
          value={filter}
          onChange={e => setFilter(e.target.value)}
          style={{ marginLeft: '0.5em' }}
        />
      </div>
      <pre>{logs}</pre>
    </section>
  );
}
