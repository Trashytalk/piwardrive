import { useEffect, useState } from 'react';

export default function DBStats() {
  const [info, setInfo] = useState(null);

  useEffect(() => {
    const load = () => {
      fetch('/db-stats')
        .then((r) => r.json())
        .then(setInfo)
        .catch(() => setInfo(null));
    };
    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, []);

  if (!info) return <div>DB: N/A</div>;
  const parts = Object.entries(info.tables || {})
    .map(([n, c]) => `${n}:${c}`)
    .join(' ');
  const size = info.size_kb != null ? info.size_kb.toFixed(1) + 'KB' : 'N/A';
  return (
    <div>
      DB: {size} {parts}
    </div>
  );
}
