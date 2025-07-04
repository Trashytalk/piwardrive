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

function predictSignal(point, aps) {
  return aps.reduce((acc, ap) => {
    const d = haversine(point, [ap.lat, ap.lon]);
    return acc + (ap.power || 1) / ((d || 1) ** 2);
  }, 0);
}

export default function GeospatialAnalytics() {
  const [coverage, setCoverage] = useState([]);
  const [deadZones, setDeadZones] = useState([]);
  const [interference, setInterference] = useState([]);
  const [optimal, setOptimal] = useState([]);
  const [predicted, setPredicted] = useState([]);

  useEffect(() => {
    const load = async () => {
      try {
        const cov = await fetch('/api/coverage').then(r => r.json());
        setCoverage(cov.points || []);
      } catch {
        setCoverage([]);
      }
      try {
        const dz = await fetch('/api/dead_zones').then(r => r.json());
        setDeadZones(dz.zones || []);
      } catch {
        setDeadZones([]);
      }
      try {
        const intf = await fetch('/api/interference').then(r => r.json());
        setInterference(intf.sources || []);
      } catch {
        setInterference([]);
      }
      try {
        const opt = await fetch('/api/optimal_ap').then(r => r.json());
        setOptimal(opt.locations || []);
      } catch {
        setOptimal([]);
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
    const pred = grid.map(pt => [...pt, predictSignal(pt, optimal)]);
    setPredicted(pred);
  }, [optimal]);

  return (
    <MapContainer center={[0, 0]} zoom={13} style={{ height: '80vh' }}>
      <TileLayer url="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png" />
      {coverage.map(([lat, lon, str], idx) => (
        <CircleMarker
          key={`c${idx}`}
          center={[lat, lon]}
          radius={10}
          pathOptions={{ color: 'blue' }}
        >
          <Popup>{str.toFixed(1)} dBm</Popup>
        </CircleMarker>
      ))}
      {predicted.map(([lat, lon, str], idx) => (
        <CircleMarker
          key={`p${idx}`}
          center={[lat, lon]}
          radius={6}
          pathOptions={{ color: 'green' }}
        />
      ))}
      {deadZones.map((poly, idx) => (
        <Polygon key={`d${idx}`} positions={poly} pathOptions={{ color: 'gray', dashArray: '4' }} />
      ))}
      {interference.map((src, idx) => (
        <CircleMarker
          key={`i${idx}`}
          center={[src.lat, src.lon]}
          radius={8}
          pathOptions={{ color: 'red' }}
        />
      ))}
      {optimal.map((pt, idx) => (
        <Marker key={`o${idx}`} position={[pt.lat, pt.lon]}>
          <Popup>Suggested</Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}
