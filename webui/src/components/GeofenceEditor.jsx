import { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Polygon, Polyline, useMapEvents } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

export default function GeofenceEditor() {
  const [polygons, setPolygons] = useState([]);
  const [current, setCurrent] = useState([]);

  useEffect(() => {
    fetch('/geofences')
      .then(r => r.json())
      .then(setPolygons)
      .catch(() => {});
  }, []);

  const addPoint = (latlng) => {
    setCurrent([...current, [latlng.lat, latlng.lng]]);
  };

  const finishPolygon = () => {
    if (current.length < 3) {
      setCurrent([]);
      return;
    }
    const name = window.prompt('Geofence name?', 'geofence');
    fetch('/geofences', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, points: current }),
    })
      .then(r => r.json())
      .then(setPolygons)
      .catch(() => {});
    setCurrent([]);
  };

  const removePolygon = (name) => {
    fetch(`/geofences/${encodeURIComponent(name)}`, { method: 'DELETE' })
      .then(() => setPolygons(polygons.filter(p => p.name !== name)))
      .catch(() => {});
  };

  const renamePolygon = (oldName) => {
    const newName = window.prompt('New name', oldName);
    if (!newName || newName === oldName) return;
    fetch(`/geofences/${encodeURIComponent(oldName)}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: newName }),
    })
      .then(r => r.json())
      .then(() => setPolygons(polygons.map(p => p.name === oldName ? { ...p, name: newName } : p)))
      .catch(() => {});
  };

  function ClickHandler() {
    useMapEvents({
      click: (e) => addPoint(e.latlng),
    });
    return null;
  }

  return (
    <div>
      <MapContainer center={[0, 0]} zoom={2} style={{ height: '400px' }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {polygons.map((poly, idx) => (
          <Polygon key={idx} positions={poly.points} />
        ))}
        {current.length > 1 && <Polyline positions={[...current, current[0]]} />}
        <ClickHandler />
      </MapContainer>
      <button onClick={finishPolygon}>Finish</button>
      <ul>
        {polygons.map(poly => (
          <li key={poly.name}>
            {poly.name}
            <button onClick={() => renamePolygon(poly.name)}>Rename</button>
            <button onClick={() => removePolygon(poly.name)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
