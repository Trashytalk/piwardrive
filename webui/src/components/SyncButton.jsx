import { useState } from 'react';
import { syncHealthRecords } from '../backendService.js';

export default function SyncButton({ limit = 100 }) {
  const [result, setResult] = useState(null);
  const run = () => {
    syncHealthRecords(limit)
      .then((r) => setResult(`uploaded ${r.uploaded}`))
      .catch(() => setResult('failed'));
  };
  return (
    <div>
      <button onClick={run}>Sync</button>
      {result && <span data-testid="result">{result}</span>}
    </div>
  );
}
