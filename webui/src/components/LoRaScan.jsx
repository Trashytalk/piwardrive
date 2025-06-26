import { useEffect, useState } from 'react';

export default function LoRaScan() {
  const [count, setCount] = useState(null);

  useEffect(() => {
    const load = () => {
      fetch('/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cmd: 'lora-scan --iface lora0' }),
      })
        .then(r => r.json())
        .then(d => {
          const lines = d.output ? d.output.trim().split('\n') : [];
          setCount(lines.length);
        })
        .catch(() => setCount(null));
    };
    load();
    const id = setInterval(load, 30000);
    return () => clearInterval(id);
  }, []);

  const val = count != null ? count : 'N/A';
  return <div>LoRa Devices: {val}</div>;
}
