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

export default function CPUTempGraph({ metrics }) {
  const [data, setData] = useState([]);

  useEffect(() => {
    if (metrics && metrics.cpu_temp != null) {
      setData((prev) => [...prev.slice(-59), metrics.cpu_temp]);
    }
  }, [metrics]);

  const labels = data.map((_, i) => i + 1);
  const dataset = {
    labels,
    datasets: [
      {
        label: 'CPU °C',
        data,
        borderColor: 'red',
        tension: 0.2,
      },
    ],
  };

  const options = { animation: false, scales: { y: { beginAtZero: true } } };
  return <Line data={dataset} options={options} />;
}
