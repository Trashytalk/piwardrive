import { useState } from 'react';
import { parseJson, parseCsv } from '../healthImport.js';

export default function HealthImport() {
  const [file, setFile] = useState(null);
  const [fmt, setFmt] = useState('json');
  const [count, setCount] = useState(null);

  const handleSubmit = async e => {
    e.preventDefault();
    if (!file) return;
    const text = await file.text();
    const records = fmt === 'csv' ? await parseCsv(text) : await parseJson(text);
    setCount(records.length);
    // in a real app you'd POST records to backend here
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="file" accept=".json,.csv" onChange={e => setFile(e.target.files[0])} />
      <select value={fmt} onChange={e => setFmt(e.target.value)}>
        <option value="json">JSON</option>
        <option value="csv">CSV</option>
      </select>
      <button type="submit">Import</button>
      {count != null && <span> Imported {count} records</span>}
    </form>
  );
}
