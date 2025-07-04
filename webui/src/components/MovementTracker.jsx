import { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement);

function hashId(id) {
  if (!id) return 'unknown';
  let hash = 0;
  for (let i = 0; i < id.length; i++) {
    hash = (hash * 31 + id.charCodeAt(i)) >>> 0;
  }
  return hash.toString(16);
}

function cluster(devices) {
  const clusters = [];
  devices.forEach(d => {
    const found = clusters.find(c => Math.hypot(c.x - d.x, c.y - d.y) < 0.0005);
    if (found) {
      found.count += 1;
    } else {
      clusters.push({ x: d.x, y: d.y, count: 1 });
    }
  });
  return clusters;
}

export default function MovementTracker() {
  const [devices, setDevices] = useState([]);
  const [timeline, setTimeline] = useState([]);
  const [privacy, setPrivacy] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch('/analytics/movement');
        const data = await res.json();
        setDevices(data.devices || []);
        setTimeline(data.timeline || []);
      } catch {
        setDevices([]);
        setTimeline([]);
      }
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);

  const speeds = timeline.map((p, i) => {
    if (i === 0) return 0;
    const [t1, x1, y1] = timeline[i - 1];
    const [t2, x2, y2] = p;
    const dist = Math.hypot(x2 - x1, y2 - y1) * 111139;
    const dt = (t2 - t1) / 1000;
    return dt > 0 ? dist / dt : 0;
  });

  const clusters = cluster(devices);

  return (
    <div>
      <label>
        <input type="checkbox" checked={privacy} onChange={() => setPrivacy(!privacy)} />
        Anonymize Devices
      </label>
      <h3>Movement Timeline</h3>
      <Line
        data={{
          labels: timeline.map(t => new Date(t[0]).toLocaleTimeString()),
          datasets: [{ label: 'Speed m/s', data: speeds, borderColor: 'blue', tension: 0.2 }]
        }}
        options={{ animation: false, scales: { y: { beginAtZero: true } } }}
      />
      <h3>Device Clusters</h3>
      <ul>
        {clusters.map((c, idx) => (
          <li key={idx}>
            {c.count} devices near {c.x.toFixed(5)}, {c.y.toFixed(5)}
          </li>
        ))}
      </ul>
      <h3>Tracked Devices</h3>
      <ul>
        {devices.map(d => (
          <li key={d.id}>
            {privacy ? hashId(d.id) : d.id} at {d.x.toFixed(5)}, {d.y.toFixed(5)}
          </li>
        ))}
      </ul>
    </div>
  );
}
