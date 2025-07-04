import { useEffect, useState } from 'react';

export default function MLDashboard({ metrics }) {
  const [performance, setPerformance] = useState(metrics?.performance ?? null);
  const [accuracy, setAccuracy] = useState(metrics?.accuracy ?? null);
  const [features, setFeatures] = useState(metrics?.features ?? []);
  const [progress, setProgress] = useState(metrics?.progress ?? null);

  useEffect(() => {
    if (metrics) {
      setPerformance(metrics.performance);
      setAccuracy(metrics.accuracy);
      setFeatures(metrics.features || []);
      setProgress(metrics.progress);
      return;
    }
    const load = () => {
      fetch('/ml/metrics')
        .then(r => r.json())
        .then(d => {
          setPerformance(d.performance);
          setAccuracy(d.accuracy);
          setFeatures(d.features || []);
          setProgress(d.progress);
        })
        .catch(() => {
          setPerformance(null);
          setAccuracy(null);
          setFeatures([]);
          setProgress(null);
        });
    };
    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, [metrics]);

  return (
    <div>
      <div>Performance: {performance ?? 'N/A'}</div>
      <div>Accuracy: {accuracy ?? 'N/A'}</div>
      <div>Training: {progress ?? 'N/A'}%</div>
      <ul>
        {features.map((f, idx) => (
          <li key={idx}>{f.name || f.feature}: {f.importance}</li>
        ))}
      </ul>
    </div>
  );
}
