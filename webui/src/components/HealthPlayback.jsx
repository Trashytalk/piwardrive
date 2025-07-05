import { useEffect, useState } from 'react';

export default function HealthPlayback({ limit = 100, interval = 1.0 }) {
  const [records, setRecords] = useState([]);

  useEffect(() => {
    const params = new URLSearchParams({ limit, interval });
    const es = new EventSource(`/sse/history?${params}`);
    es.onmessage = (ev) => {
      try {
        const data = JSON.parse(ev.data);
        if (data.record) {
          setRecords((prev) => [...prev, data.record]);
        }
      } catch {
        /* ignore */
      }
    };
    return () => es.close();
  }, [limit, interval]);

  if (!records.length) return <div>No playback data</div>;

  return (
    <div>
      <h3>Playback</h3>
      <pre style={{ maxHeight: '200px', overflowY: 'auto' }}>
        {JSON.stringify(records, null, 2)}
      </pre>
    </div>
  );
}
