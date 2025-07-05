import { useEffect, useState } from 'react';

export default function BaselineAnalysis() {
  const [result, setResult] = useState(null);

  useEffect(() => {
    const load = () => {
      fetch('/baseline-analysis')
        .then((r) => r.json())
        .then((d) => setResult(d))
        .catch(() => setResult(null));
    };
    load();
    const id = setInterval(load, 30000);
    return () => clearInterval(id);
  }, []);

  if (!result) return <div>Baseline: N/A</div>;
  const d = result.delta || {};
  return (
    <div>
      Temp Δ:{d.temp_avg?.toFixed(1)}°C CPU Δ:{d.cpu_avg?.toFixed(0)}%
    </div>
  );
}
