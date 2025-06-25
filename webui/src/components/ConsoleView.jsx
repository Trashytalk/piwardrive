import { useEffect, useState } from 'react';

export default function ConsoleView() {
  const [logs, setLogs] = useState('');
  const [cmd, setCmd] = useState('');
  const [output, setOutput] = useState('');

  useEffect(() => {
    const load = () => {
      fetch('/logs?lines=200')
        .then(r => r.json())
        .then(d => setLogs(d.lines.join('\n')))
        .catch(() => {});
    };
    load();
    const id = setInterval(load, 2000);
    return () => clearInterval(id);
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
