import { useEffect, useState } from 'react';

export default function CapacityPlanner() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('/api/analytics/capacity')
      .then((r) => r.json())
      .then((d) => setData(d))
      .catch(() => setData(null));
  }, []);

  if (!data) return <div>Capacity planning data unavailable</div>;

  return (
    <div>
      <h4>Usage Forecast (95% CI)</h4>
      <pre>{JSON.stringify(data)}</pre>
    </div>
  );
}
