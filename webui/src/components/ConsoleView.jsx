import { useEffect, useState } from 'react';

export default function ConsoleView() {
  const [logs, setLogs] = useState('');
  const [cmd, setCmd] = useState('');
  const [output, setOutput] = useState('');
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

  const runCommand = () => {
    fetch('/command', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ cmd }),
    })
      .then(r => r.json())
      .then(d => setOutput(d.output || ''))
      .catch(e => setOutput(String(e)));
  };

  return (
    <div>
      <h2>Console</h2>
      {paths.length > 1 && (
        <select value={path} onChange={e => setPath(e.target.value)}>
          {paths.map(p => (
            <option key={p} value={p}>
              {p.split('/').slice(-1)[0]}
            </option>
          ))}
        </select>
      )}
      <pre>{logs}</pre>
      <div>
        <input value={cmd} onChange={e => setCmd(e.target.value)} />
        <button onClick={runCommand}>Run</button>
      </div>
      {output && (
        <>
          <h3>Command Output</h3>
          <pre>{output}</pre>
        </>
      )}
    </div>
  );
}
