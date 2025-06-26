import { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement);

export default function HealthAnalysis() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const load = () => {
      fetch('/status?limit=50')
        .then(r => r.json())
        .then(recs => {
          if (!recs.length) { setStats(null); return; }
          const temps = recs.map(r => r.system.cpu_temp).filter(x => x != null);
          const avgTemp = temps.reduce((a, b) => a + b, 0) / temps.length;
          const mem = recs.map(r => r.system.mem_percent).filter(x => x != null);
          const avgMem = mem.reduce((a, b) => a + b, 0) / mem.length;
          const disk = recs.map(r => r.system.disk_percent).filter(x => x != null);
          const avgDisk = disk.reduce((a, b) => a + b, 0) / disk.length;
          setStats({ temps, avgTemp, avgMem, avgDisk });
        })
        .catch(() => setStats(null));
    };
    load();
    const id = setInterval(load, 30000);
    return () => clearInterval(id);
  }, []);

  if (!stats) return <div>Health Analysis: N/A</div>;
  const labels = stats.temps.map((_, i) => i + 1);
  const options = { animation: false, scales: { y: { beginAtZero: true } } };
  return (
    <div>
      <div>Temp:{stats.avgTemp.toFixed(1)}°C Mem:{stats.avgMem.toFixed(0)}% Disk:{stats.avgDisk.toFixed(0)}%</div>
      <Line data={{ labels, datasets: [{ label: 'CPU °C', data: stats.temps, borderColor: 'red', tension: 0.2 }] }} options={options} />
    </div>
  );
}
