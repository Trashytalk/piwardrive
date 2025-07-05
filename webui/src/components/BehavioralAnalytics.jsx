import { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { MapContainer, TileLayer, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
} from 'chart.js';
import HeatmapLayer from './HeatmapLayer.jsx';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement);

function anonymize(id, enabled) {
  if (!enabled) return id;
  if (!id) return 'unknown';
  return '****' + id.slice(-4);
}

export default function BehavioralAnalytics() {
  const [track, setTrack] = useState([]);
  const [activity, setActivity] = useState([]);
  const [privacy, setPrivacy] = useState(true);
  const [showHeatmap, setShowHeatmap] = useState(false);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch('/analytics/behavioral');
        const data = await res.json();
        setTrack(data.track || []);
        setActivity(data.activity || []);
      } catch {
        setTrack([]);
        setActivity([]);
      }
    };
    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, []);

  const speed = track.map((p, i) => {
    if (i === 0) return 0;
    const [lat1, lon1, t1] = track[i - 1];
    const [lat2, lon2, t2] = p;
    const dist = Math.hypot(lat2 - lat1, lon2 - lon1) * 111139;
    const dt = (t2 - t1) / 1000;
    return dt > 0 ? dist / dt : 0;
  });

  const labels = activity.map((a) => new Date(a[0]).toLocaleTimeString());

  return (
    <div>
      <div style={{ marginBottom: '0.5em' }}>
        <label>
          <input
            type="checkbox"
            checked={privacy}
            onChange={() => setPrivacy(!privacy)}
          />
          Anonymize IDs
        </label>
        <label style={{ marginLeft: '1em' }}>
          <input
            type="checkbox"
            checked={showHeatmap}
            onChange={() => setShowHeatmap(!showHeatmap)}
          />
          Show Heatmap
        </label>
      </div>
      <MapContainer center={[0, 0]} zoom={13} style={{ height: '40vh' }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <HeatmapLayer show={showHeatmap} />
        {track.length > 1 && (
          <Polyline positions={track.map((p) => [p[0], p[1]])} color="blue" />
        )}
      </MapContainer>
      <h3>Speed Analysis</h3>
      <Line
        data={{
          labels: track.map((_, i) => i + 1),
          datasets: [
            {
              label: 'Speed m/s',
              data: speed,
              borderColor: 'red',
              tension: 0.2,
            },
          ],
        }}
        options={{ animation: false, scales: { y: { beginAtZero: true } } }}
      />
      <h3>Temporal Activity</h3>
      <Line
        data={{
          labels,
          datasets: [
            {
              label: 'Activity',
              data: activity.map((a) => a[1]),
              borderColor: 'green',
              tension: 0.2,
            },
          ],
        }}
        options={{ animation: false, scales: { y: { beginAtZero: true } } }}
      />
      <ul>
        {track.map((p) => (
          <li key={p[2]}>
            {new Date(p[2]).toLocaleString()} - {anonymize(p[3], privacy)} @{' '}
            {p[0].toFixed(5)}, {p[1].toFixed(5)}
          </li>
        ))}
      </ul>
    </div>
  );
}
