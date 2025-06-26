import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js';
import { useEffect, useState } from 'react';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement);

export default function DiskUsageTrend() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const load = () => {
      fetch('/storage')
        .then(r => r.json())
        .then(d => {
          if (d.percent != null) {
            setData(prev => [...prev.slice(-59), d.percent]);
          }
        })
        .catch(() => {});
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);

  const labels = data.map((_, i) => i + 1);
  const dataset = {
    labels,
    datasets: [{ label: 'Disk %', data, borderColor: 'green', tension: 0.2 }],
  };
  const options = { animation: false, scales: { y: { beginAtZero: true, max: 100 } } };
  return <Line data={dataset} options={options} />;
}
