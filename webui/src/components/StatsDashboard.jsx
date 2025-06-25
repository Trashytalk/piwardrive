import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js';
import { useEffect, useState } from 'react';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement);

export default function StatsDashboard() {
  const [cpu, setCpu] = useState([]);
  const [mem, setMem] = useState([]);
  const [disk, setDisk] = useState([]);
  const [labels, setLabels] = useState([]);
  const [smart, setSmart] = useState(null);
  const [kismet, setKismet] = useState(null);
  const [bettercap, setBettercap] = useState(null);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const data = await fetch('/health').then(r => r.json()).catch(() => null);
        const nextLabel = (labels[labels.length - 1] || 0) + 1;
        setLabels(l => [...l.slice(-59), nextLabel]);
        if (data && data.system) {
          const sys = data.system;
          if (sys.cpu_percent != null) setCpu(d => [...d.slice(-59), sys.cpu_percent]);
          if (sys.memory_percent != null) setMem(d => [...d.slice(-59), sys.memory_percent]);
          if (sys.disk_percent != null) setDisk(d => [...d.slice(-59), sys.disk_percent]);
          setSmart(sys.ssd_smart ?? null);
        }
        if (data && data.services) {
          setKismet(data.services.kismet);
          setBettercap(data.services.bettercap);
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
      <div>SSD Health: {smart ?? 'N/A'}</div>
      <div>Kismet: {kismet == null ? 'N/A' : kismet ? 'ok' : 'down'}</div>
      <div>BetterCAP: {bettercap == null ? 'N/A' : bettercap ? 'ok' : 'down'}</div>
    </div>
  );
}
