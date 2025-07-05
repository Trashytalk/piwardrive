import { useEffect, useState } from 'react';

export default function DeviceFingerprinting({ metrics }) {
  const [devices, setDevices] = useState(metrics?.devices ?? []);

  useEffect(() => {
    if (metrics) {
      setDevices(metrics.devices || []);
      return;
    }
    const load = () => {
      fetch('/fingerprinting')
        .then((r) => r.json())
        .then((d) => setDevices(d.devices || []))
        .catch(() => setDevices([]));
    };
    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, [metrics]);

  return (
    <ul>
      {devices.map((d, i) => (
        <li key={i}>
          {d.type || d.device_type}: {d.vendor} (
          {d.confidence != null ? (d.confidence * 100).toFixed(0) + '%' : 'N/A'}
          )
        </li>
      ))}
    </ul>
  );
}
