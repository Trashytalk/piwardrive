import { useState } from 'react';
import { useWebSocket } from '../useWebSocket.js';

export default function ScanningStatus() {
  const [progress, setProgress] = useState(0);
  const [device, setDevice] = useState({});
  const [history, setHistory] = useState([]);

  const { status } = useWebSocket('/ws/scan', {
    onMessage: (raw) => {
      try {
        const data = JSON.parse(raw);
        if (data.progress != null) setProgress(data.progress);
        if (data.device) setDevice(data.device);
        if (data.history) setHistory(data.history);
      } catch (_) {}
    },
  });

  return (
    <div>
      <div>Connection: {status}</div>
      <progress value={progress} max={100} />
      <div>
        Device: {device.name || 'N/A'} health: {device.health || 'N/A'}
      </div>
      {device.config && (
        <div>Scan configuration: {JSON.stringify(device.config)}</div>
      )}
      {history.length > 0 && (
        <ul>
          {history.map((h, i) => (
            <li key={i}>
              {h.scan} - {h.result}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
