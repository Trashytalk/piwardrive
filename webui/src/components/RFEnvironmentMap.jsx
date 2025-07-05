import { useEffect, useState } from 'react';
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Polygon,
  Popup,
} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

export default function RFEnvironmentMap() {
  const [propagation, setPropagation] = useState([]);
  const [channels, setChannels] = useState([]);
  const [interference, setInterference] = useState([]);
  const [spectrum, setSpectrum] = useState([]);

  useEffect(() => {
    const load = async () => {
      try {
        const p = await fetch('/api/rf/propagation').then((r) => r.json());
        setPropagation(p.points || []);
      } catch {
        setPropagation([]);
      }
      try {
        const c = await fetch('/api/rf/channels').then((r) => r.json());
        setChannels(c.utilization || []);
      } catch {
        setChannels([]);
      }
      try {
        const i = await fetch('/api/rf/interference').then((r) => r.json());
        setInterference(i.sources || []);
      } catch {
        setInterference([]);
      }
      try {
        const s = await fetch('/api/rf/spectrum').then((r) => r.json());
        setSpectrum(s.overlays || []);
      } catch {
        setSpectrum([]);
      }
    };
    load();
  }, []);

  return (
    <MapContainer center={[0, 0]} zoom={13} style={{ height: '80vh' }}>
      <TileLayer url="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png" />
      {propagation.map(([lat, lon, h], idx) => (
        <CircleMarker
          key={`p${idx}`}
          center={[lat, lon]}
          radius={Math.min(20, Math.max(2, h))}
          pathOptions={{ color: 'blue' }}
        />
      ))}
      {channels.map((poly, idx) => (
        <Polygon
          key={`c${idx}`}
          positions={poly.points}
          pathOptions={{ color: 'purple' }}
        >
          <Popup>
            Ch {poly.channel}: {poly.util}%
          </Popup>
        </Polygon>
      ))}
      {interference.map((src, idx) => (
        <CircleMarker
          key={`i${idx}`}
          center={[src.lat, src.lon]}
          radius={8}
          pathOptions={{ color: 'red' }}
        />
      ))}
      {spectrum.map((sp, idx) => (
        <Polygon
          key={`s${idx}`}
          positions={sp.area}
          pathOptions={{ color: 'orange' }}
        />
      ))}
    </MapContainer>
  );
}
