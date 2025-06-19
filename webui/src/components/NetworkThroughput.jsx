import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js';
import { useEffect, useState } from 'react';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement);

export default function NetworkThroughput({ metrics }) {
  const [rx, setRx] = useState([]);
  const [tx, setTx] = useState([]);

  useEffect(() => {
    if (metrics) {
      if (metrics.rx_kbps != null) setRx(prev => [...prev.slice(-59), metrics.rx_kbps]);
      if (metrics.tx_kbps != null) setTx(prev => [...prev.slice(-59), metrics.tx_kbps]);
    }
  }, [metrics]);

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
