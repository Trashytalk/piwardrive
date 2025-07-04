import { useEffect, useState } from 'react';

export default function CriticalInfrastructure({ metrics }) {
  const [data, setData] = useState(metrics);

  useEffect(() => {
    if (metrics) {
      setData(metrics);
      return;
    }
    const load = () => {
      fetch('/critical-infra')
        .then((r) => r.json())
        .then(setData)
        .catch(() => setData(null));
    };
    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, [metrics]);

  if (!data) return <div>Critical Infrastructure: N/A</div>;
  return (
    <div>
      <div>Industrial Networks: {data.industrial_networks ?? 'N/A'}</div>
      <div>Medical Devices: {data.medical_devices ?? 'N/A'}</div>
      <div>Utility Networks: {data.utility_networks ?? 'N/A'}</div>
      <div>Public Safety Comms: {data.public_safety_comms ?? 'N/A'}</div>
    </div>
  );
}
