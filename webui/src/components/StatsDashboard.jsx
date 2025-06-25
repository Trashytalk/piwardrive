import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js';
import { useEffect, useState } from 'react';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement);

export default function StatsDashboard() {
  const [cpu, setCpu] = useState([]);
  const [mem, setMem] = useState([]);
  const [disk, setDisk] = useState([]);
  const [labels, setLabels] = useState([]);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const [cpuRes, ramRes, diskRes] = await Promise.all([
          fetch('/cpu').then(r => r.json()).catch(() => null),
          fetch('/ram').then(r => r.json()).catch(() => null),
          fetch('/storage').then(r => r.json()).catch(() => null)
        ]);
        const nextLabel = (labels[labels.length - 1] || 0) + 1;
        setLabels(l => [...l.slice(-59), nextLabel]);
        if (cpuRes && cpuRes.percent != null) {
          setCpu(d => [...d.slice(-59), cpuRes.percent]);
        }
        if (ramRes && ramRes.percent != null) {
          setMem(d => [...d.slice(-59), ramRes.percent]);
        }
        if (diskRes && diskRes.percent != null) {
          setDisk(d => [...d.slice(-59), diskRes.percent]);
        }
      } catch (_) {}
    }, 2000);
    return () => clearInterval(interval);
  }, [labels]);

  const opts = { animation: false, scales: { y: { beginAtZero: true, max: 100 } } };
  return (
    <div>
      <h3>CPU Usage</h3>
      <Line data={{ labels, datasets: [{ label: 'CPU %', data: cpu, borderColor: 'red', tension: 0.2 }] }} options={opts} />
      <h3>Memory Usage</h3>
      <Line data={{ labels, datasets: [{ label: 'RAM %', data: mem, borderColor: 'blue', tension: 0.2 }] }} options={opts} />
      <h3>Disk Usage</h3>
      <Line data={{ labels, datasets: [{ label: 'Disk %', data: disk, borderColor: 'green', tension: 0.2 }] }} options={opts} />
    </div>
  );
}
