import { useEffect, useState } from 'react';

export default function FingerprintSummary() {
  const [items, setItems] = useState(null);

  useEffect(() => {
    const load = () => {
      fetch('/fingerprints')
        .then(r => r.json())
        .then(d => setItems(d.fingerprints || []))
        .catch(() => setItems(null));
    };
    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, []);

  if (!items) return <div>Fingerprints: N/A</div>;
  return <div>Fingerprints: {items.length}</div>;
}
