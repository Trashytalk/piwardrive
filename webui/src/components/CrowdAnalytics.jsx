import { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { MapContainer, TileLayer } from 'react-leaflet';
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

export default function CrowdAnalytics() {
  const [density, setDensity] = useState([]);
  const [events, setEvents] = useState([]);
  const [recommend, setRecommend] = useState([]);
  const [showHeatmap, setShowHeatmap] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch('/analytics/crowd');
        const data = await res.json();
        setDensity(data.density || []);
        setEvents(data.events || []);
        setRecommend(data.recommend || []);
      } catch {
        setDensity([]);
        setEvents([]);
        setRecommend([]);
      }
    };
    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, []);

  const labels = density.map((d) => new Date(d[0]).toLocaleTimeString());

  return (
    <div>
      <label>
        <input
          type="checkbox"
          checked={showHeatmap}
          onChange={() => setShowHeatmap(!showHeatmap)}
        />
        Show Heatmap
      </label>
      <MapContainer
        center={[0, 0]}
        zoom={14}
        style={{ height: '40vh', marginTop: '0.5em' }}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <HeatmapLayer show={showHeatmap} />
      </MapContainer>
      <h3>Crowd Density Over Time</h3>
      <Line
        data={{
          labels,
          datasets: [
            {
              label: 'Density',
              data: density.map((d) => d[1]),
              borderColor: 'purple',
              tension: 0.2,
            },
          ],
        }}
        options={{ animation: false, scales: { y: { beginAtZero: true } } }}
      />
      <h3>Detected Events</h3>
      <ul>
        {events.map((e, idx) => (
          <li key={idx}>
            {new Date(e.time).toLocaleString()} - {e.type}
          </li>
        ))}
      </ul>
      <h3>Capacity Planning</h3>
      <ul>
        {recommend.map((r, idx) => (
          <li key={idx}>{r}</li>
        ))}
      </ul>
    </div>
  );
}
