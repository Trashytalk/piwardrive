import { useEffect, useState } from 'react';
import LogViewer from './LogViewer.jsx';

export default function ConsoleView() {
  const [cmd, setCmd] = useState('');
  const [output, setOutput] = useState('');

  const [logPaths, setLogPaths] = useState([]);

  useEffect(() => {
    fetch('/config')
      .then(r => r.json())
      .then(cfg => setLogPaths(cfg.log_paths || []))
      .catch(() => {});
  }, []);

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
      <LogViewer logPaths={logPaths} />
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
