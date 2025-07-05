import { useEffect, useState } from 'react';

export default function GPSStatus({ metrics }) {
  const [fix, setFix] = useState(metrics?.gps_fix ?? null);

  useEffect(() => {
    if (metrics && metrics.gps_fix != null) {
      setFix(metrics.gps_fix);
      return;
    }
    const load = () => {
      fetch('/gps')
        .then((r) => r.json())
        .then((d) => setFix(d.fix))
        .catch(() => setFix(null));
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, [metrics]);

  return <div>GPS: {fix ?? 'N/A'}</div>;
}
