import { useEffect, useState } from 'react';

export default function DigitalEquity() {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    const load = () => {
      fetch('/demographics/equity')
        .then((r) => r.json())
        .then(setMetrics)
        .catch(() => setMetrics(null));
    };
    load();
    const id = setInterval(load, 60000);
    return () => clearInterval(id);
  }, []);

  if (!metrics) return <div>Digital Equity: N/A</div>;

  return (
    <div>
      <div>Connectivity Gap: {metrics.connectivity_gap?.toFixed(2)}</div>
      <div>Average Quality: {metrics.avg_quality?.toFixed(2)}</div>
      <div>Average Affordability: {metrics.avg_affordability?.toFixed(2)}</div>
    </div>
  );
}
