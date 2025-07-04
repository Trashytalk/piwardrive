import { useEffect, useState } from 'react';

export default function SmartCityDashboard({ metrics }) {
  const [data, setData] = useState(metrics);

  useEffect(() => {
    if (metrics) {
      setData(metrics);
      return;
    }
    const load = () => {
      fetch('/smart-city')
        .then((r) => r.json())
        .then(setData)
        .catch(() => setData(null));
    };
    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, [metrics]);

  if (!data) return <div>City Intelligence: N/A</div>;
  return (
    <div>
      <div>Deployment Map: {data.deployment_map ?? 'N/A'}</div>
      <div>Infrastructure Growth: {data.infrastructure_growth ?? 'N/A'}</div>
      <div>Service Availability: {data.service_availability ?? 'N/A'}</div>
      <div>Digital Quality: {data.digital_quality ?? 'N/A'}</div>
    </div>
  );
}
