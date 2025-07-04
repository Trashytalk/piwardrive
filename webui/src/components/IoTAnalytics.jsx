import { useEffect, useState } from 'react';

export default function IoTAnalytics({ metrics }) {
  const [data, setData] = useState(metrics);

  useEffect(() => {
    if (metrics) {
      setData(metrics);
      return;
    }
    const load = () => {
      fetch('/iot-analytics')
        .then((r) => r.json())
        .then(setData)
        .catch(() => setData(null));
    };
    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, [metrics]);

  if (!data) return <div>IoT Analytics: N/A</div>;
  return (
    <div>
      <div>Classification: {data.device_classification ?? 'N/A'}</div>
      <div>Infrastructure Map: {data.infrastructure_mapping ?? 'N/A'}</div>
      <div>
        Critical Infrastructure: {data.critical_infrastructure ?? 'N/A'}
      </div>
      <div>Privacy Risk: {data.privacy_risk ?? 'N/A'}</div>
    </div>
  );
}
