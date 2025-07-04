import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
} from 'chart.js';
import { useEffect, useState } from 'react';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement);

export function DatabaseHealthWidget() {
  const [status, setStatus] = useState(null);
  useEffect(() => {
    const load = () => {
      fetch('/db-health')
        .then((r) => r.json())
        .then(setStatus)
        .catch(() => setStatus(null));
    };
    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, []);
  if (!status) return <div>DB Health: N/A</div>;
  return <div>DB Health: {status.healthy ? 'OK' : 'Fail'}</div>;
}

export function ScannerStatusWidget() {
  const [state, setState] = useState('N/A');
  useEffect(() => {
    const load = () => {
      fetch('/service/kismet')
        .then((r) => r.json())
        .then((d) => setState(d.active ? 'Running' : 'Stopped'))
        .catch(() => setState('N/A'));
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);
  return <div>Scanner: {state}</div>;
}

export function SystemResourceWidget() {
  const [stats, setStats] = useState(null);
  useEffect(() => {
    const load = () => {
      Promise.all([
        fetch('/cpu')
          .then((r) => r.json())
          .catch(() => null),
        fetch('/ram')
          .then((r) => r.json())
          .catch(() => null),
        fetch('/storage')
          .then((r) => r.json())
          .catch(() => null),
      ]).then(([c, m, d]) => {
        setStats({ cpu: c?.percent, mem: m?.percent, disk: d?.percent });
      });
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);
  if (!stats) return <div>Resources: N/A</div>;
  return (
    <div>
      CPU: {stats.cpu?.toFixed(0) ?? 'N/A'}% | RAM:{' '}
      {stats.mem?.toFixed(0) ?? 'N/A'}% | Disk:{' '}
      {stats.disk?.toFixed(0) ?? 'N/A'}%
    </div>
  );
}

export function NetworkThroughputWidget() {
  const [rx, setRx] = useState([]);
  const [tx, setTx] = useState([]);
  useEffect(() => {
    const load = () => {
      fetch('/widget-metrics')
        .then((r) => r.json())
        .then((d) => {
          if (d.rx_kbps != null)
            setRx((prev) => [...prev.slice(-59), d.rx_kbps]);
          if (d.tx_kbps != null)
            setTx((prev) => [...prev.slice(-59), d.tx_kbps]);
        })
        .catch(() => {});
    };
    load();
    const id = setInterval(load, 2000);
    return () => clearInterval(id);
  }, []);
  const labels = rx.map((_, i) => i + 1);
  const dataset = {
    labels,
    datasets: [
      { label: 'RX kbps', data: rx, borderColor: 'blue', tension: 0.2 },
      { label: 'TX kbps', data: tx, borderColor: 'green', tension: 0.2 },
    ],
  };
  const options = { animation: false, scales: { y: { beginAtZero: true } } };
  return <Line data={dataset} options={options} />;
}
