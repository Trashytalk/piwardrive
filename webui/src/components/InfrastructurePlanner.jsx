import { useEffect, useState } from 'react';
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Marker,
  Popup,
  Polygon,
} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

function haversine(p1, p2) {
  const R = 6371000;
  const lat1 = (p1[0] * Math.PI) / 180;
  const lat2 = (p2[0] * Math.PI) / 180;
  const dLat = lat2 - lat1;
  const dLon = ((p2[1] - p1[1]) * Math.PI) / 180;
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
  return 2 * R * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

function predict(point, aps) {
  return aps.reduce((acc, ap) => {
    const d = haversine(point, [ap.lat, ap.lon]);
    return acc + (ap.power || 1) / ((d || 1) ** 2);
  }, 0);
}

export default function InfrastructurePlanner() {
  const [gaps, setGaps] = useState([]);
  const [optimal, setOptimal] = useState([]);
  const [prediction, setPrediction] = useState([]);
  const [roi, setRoi] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const g = await fetch('/api/planner/gaps').then(r => r.json());
        setGaps(g.zones || []);
      } catch {
        setGaps([]);
      }
      try {
        const o = await fetch('/api/planner/optimal').then(r => r.json());
        setOptimal(o.locations || []);
      } catch {
        setOptimal([]);
      }
      try {
        const r = await fetch('/api/planner/roi').then(r => r.json());
        setRoi(r.roi ?? null);
      } catch {
        setRoi(null);
      }
    };
    load();
  }, []);

  useEffect(() => {
    if (!optimal.length) return;
    const grid = [];
    const min = [-0.01, -0.01];
    const max = [0.01, 0.01];
    for (let i = 0; i < 10; i++) {
      for (let j = 0; j < 10; j++) {
        const lat = min[0] + ((max[0] - min[0]) * i) / 9;
        const lon = min[1] + ((max[1] - min[1]) * j) / 9;
        grid.push([lat, lon]);
      }
    }
    const pred = grid.map(pt => [...pt, predict(pt, optimal)]);
    setPrediction(pred);
  }, [optimal]);

  return (
    <div>
      <MapContainer center={[0, 0]} zoom={13} style={{ height: '80vh' }}>
        <TileLayer url="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png" />
        {gaps.map((poly, idx) => (
          <Polygon key={`g${idx}`} positions={poly} pathOptions={{ color: 'gray', dashArray: '4' }} />
        ))}
        {prediction.map(([lat, lon, s], idx) => (
          <CircleMarker key={`p${idx}`} center={[lat, lon]} radius={6} pathOptions={{ color: 'green' }} />
        ))}
        {optimal.map((pt, idx) => (
          <Marker key={`o${idx}`} position={[pt.lat, pt.lon]}>
            <Popup>AP</Popup>
          </Marker>
        ))}
      </MapContainer>
      {roi != null && <div>ROI: {roi}%</div>}
    </div>
  );
}
