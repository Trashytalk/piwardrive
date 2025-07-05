import { useEffect, useState } from 'react';

export default function HealthStatus() {
  const [info, setInfo] = useState(null);

  useEffect(() => {
    const load = () => {
      fetch('/status?limit=1')
        .then((r) => r.json())
        .then((d) => setInfo(d[0] || null))
        .catch(() => setInfo(null));
    };
    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, []);

  if (!info) return <div>Health: N/A</div>;
  const sys = info.system || {};
  const disk =
    sys.disk_percent != null ? sys.disk_percent.toFixed(0) + '%' : 'N/A';
  const net = info.network_ok ? 'ok' : 'down';
  const services = info.services || {};
  const svcStr = Object.entries(services)
    .map(([n, ok]) => `${n}:${ok ? 'ok' : 'down'}`)
    .join(' ');
  return (
    <div>
      Net:{net} SSD:{disk} {svcStr}
    </div>
  );
}
