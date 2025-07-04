import { useEffect, useState } from 'react';

export default function AnomalyDetection({ metrics }) {
  const [anomalies, setAnomalies] = useState(metrics?.anomalies ?? []);
  const [baseline, setBaseline] = useState(metrics?.baseline ?? null);

  useEffect(() => {
    if (metrics) {
      setAnomalies(metrics.anomalies || []);
      setBaseline(metrics.baseline ?? null);
      return;
    }
    const load = () => {
      fetch('/anomaly')
        .then(r => r.json())
        .then(d => {
          setAnomalies(d.anomalies || []);
          setBaseline(d.baseline || null);
        })
        .catch(() => {
          setAnomalies([]);
          setBaseline(null);
        });
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, [metrics]);

  return (
    <div>
      <div>Baseline: {baseline ?? 'N/A'}</div>
      <ul>
        {anomalies.map((a, i) => (
          <li key={i}>{a}</li>
        ))}
      </ul>
    </div>
  );
}
