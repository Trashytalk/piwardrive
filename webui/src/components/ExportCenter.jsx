import { useState } from 'react';

const FORMATS = ['csv', 'json', 'kml', 'wigle'];

export default function ExportCenter() {
  const [fmt, setFmt] = useState('csv');
  const [start, setStart] = useState('');
  const [end, setEnd] = useState('');
  const [ssid, setSsid] = useState('');
  const [progress, setProgress] = useState(null);
  const [history, setHistory] = useState([]);

  const submit = async (e) => {
    e.preventDefault();
    setProgress('running');
    try {
      const params = new URLSearchParams();
      params.set('fmt', fmt);
      if (start) params.set('start', start);
      if (end) params.set('end', end);
      if (ssid) params.set('ssid', ssid);
      const resp = await fetch(`/export/aps?${params}`);
      const blob = await resp.blob();
      const url = URL.createObjectURL(blob);
      setHistory((h) => [{ id: Date.now(), fmt, url }, ...h]);
      setProgress('done');
    } catch {
      setProgress('failed');
    }
  };

  const remove = (id) => setHistory((h) => h.filter((r) => r.id !== id));

  return (
    <div>
      <form onSubmit={submit}>
        <select value={fmt} onChange={(e) => setFmt(e.target.value)}>
          {FORMATS.map((f) => (
            <option key={f} value={f}>
              {f.toUpperCase()}
            </option>
          ))}
        </select>
        <input
          type="date"
          value={start}
          onChange={(e) => setStart(e.target.value)}
        />
        <input
          type="date"
          value={end}
          onChange={(e) => setEnd(e.target.value)}
        />
        <input
          type="text"
          placeholder="SSID"
          value={ssid}
          onChange={(e) => setSsid(e.target.value)}
        />
        <button type="submit">Start Export</button>
      </form>
      {progress === 'running' && <div>Exporting...</div>}
      {progress === 'done' && <div>Complete</div>}
      {progress === 'failed' && <div>Failed</div>}
      <ul>
        {history.map((h) => (
          <li key={h.id}>
            {h.fmt.toUpperCase()}{' '}
            <a href={h.url} download={`export.${h.fmt}`}>
              Download
            </a>{' '}
            <button onClick={() => remove(h.id)}>remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
