import { useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
} from 'chart.js';
import { useWebSocket } from '../useWebSocket.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement);

export default function LiveMetrics() {
  const [labels, setLabels] = useState([]);
  const [rates, setRates] = useState([]);
  const [perf, setPerf] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [net, setNet] = useState(null);

  const { status } = useWebSocket('/ws/metrics', {
    onMessage: (raw) => {
      try {
        const data = JSON.parse(raw);
        if (data.rate != null) {
          setLabels((l) => [...l.slice(-59), l.length]);
          setRates((r) => [...r.slice(-59), data.rate]);
        }
        if (data.perf) setPerf(data.perf);
        if (data.alert) setAlerts((a) => [...a.slice(-9), data.alert]);
        if (data.net) setNet(data.net);
      } catch (_) {}
    },
  });

  const opts = { animation: false, scales: { y: { beginAtZero: true } } };

  return (
    <div>
      <div>Connection: {status}</div>
      <Line
        data={{
          labels,
          datasets: [
            {
              label: 'Detections/s',
              data: rates,
              borderColor: 'green',
              tension: 0.2,
            },
          ],
        }}
        options={opts}
      />
      {perf && (
        <div>
          CPU: {perf.cpu}% RAM: {perf.ram}%
        </div>
      )}
      {net && (
        <div>
          Network: {net.tx}/{net.rx}
        </div>
      )}
      {alerts.map((a, i) => (
        <div key={i} style={{ color: 'red' }}>
          {a}
        </div>
      ))}
    </div>
  );
}
