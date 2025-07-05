import { useEffect, useState } from 'react';

export function LoRaScanStatic({ metrics }) {
  const count = metrics?.lora_devices;
  return <div>LoRa: {count != null ? count : 'N/A'}</div>;
}

export default function LoRaScan() {
  const [count, setCount] = useState(null);

  useEffect(() => {
    const load = () => {
      fetch('/lora-scan')
        .then((r) => r.json())
        .then((d) => setCount(d.count))
        .catch(() => setCount(null));
    };
    load();
    const id = setInterval(load, 30000);
    return () => clearInterval(id);
  }, []);

  const val = count != null ? count : 'N/A';
  return <div>LoRa Devices: {val}</div>;
}
