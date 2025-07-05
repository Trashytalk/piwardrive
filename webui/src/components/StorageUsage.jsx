import { useEffect, useState } from 'react';

export default function StorageUsage() {
  const [pct, setPct] = useState(null);

  useEffect(() => {
    const load = () => {
      fetch('/storage')
        .then((r) => r.json())
        .then((d) => setPct(d.percent))
        .catch(() => setPct(null));
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);

  const val = pct != null ? pct.toFixed(0) + '%' : 'N/A';
  return <div>SSD: {val}</div>;
}
