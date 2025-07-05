import { useEffect, useState } from 'react';
import {
  MapContainer,
  TileLayer,
  Polygon,
  Polyline,
  useMapEvents,
} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

export default function GeofenceEditor() {
  const [polygons, setPolygons] = useState([]);
  const [current, setCurrent] = useState([]);
  const [position, setPosition] = useState(null);

  // simple point in polygon test using ray casting
  const pointInPolygon = (pt, poly) => {
    if (!pt || !poly || poly.length < 3) return false;
    const x = pt[0];
    const y = pt[1];
    let inside = false;
    for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
      const xi = poly[i][0];
      const yi = poly[i][1];
      const xj = poly[j][0];
      const yj = poly[j][1];
      const intersect =
        yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi;
      if (intersect) inside = !inside;
    }
    return inside;
  };

  useEffect(() => {
    fetch('/geofences')
      .then((r) => r.json())
      .then(setPolygons)
      .catch(() => {});
  }, []);

  // poll GPS position
  useEffect(() => {
    const id = setInterval(async () => {
      try {
        const resp = await fetch('/gps');
        const data = await resp.json();
        if (data && data.lat != null && data.lon != null) {
          setPosition([data.lat, data.lon]);
        }
      } catch {
        // ignore
      }
    }, 5000);
    return () => clearInterval(id);
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
    const enter_message = window.prompt('Enter message (optional)', '');
    const exit_message = window.prompt('Exit message (optional)', '');
    fetch('/geofences', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        points: current,
        enter_message: enter_message || null,
        exit_message: exit_message || null,
      }),
    })
      .then((r) => r.json())
      .then(setPolygons)
      .catch(() => {});
    setCurrent([]);
  };

  const removePolygon = (name) => {
    fetch(`/geofences/${encodeURIComponent(name)}`, { method: 'DELETE' })
      .then(() => setPolygons(polygons.filter((p) => p.name !== name)))
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
      .then((r) => r.json())
      .then(() =>
        setPolygons(
          polygons.map((p) =>
            p.name === oldName ? { ...p, name: newName } : p
          )
        )
      )
      .catch(() => {});
  };

  const editMessages = (name) => {
    const poly = polygons.find((p) => p.name === name) || {};
    const enter = window.prompt('Enter message', poly.enter_message || '');
    const exit = window.prompt('Exit message', poly.exit_message || '');
    fetch(`/geofences/${encodeURIComponent(name)}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        enter_message: enter || null,
        exit_message: exit || null,
      }),
    })
      .then((r) => r.json())
      .then((updated) =>
        setPolygons(
          polygons.map((p) => (p.name === name ? { ...p, ...updated } : p))
        )
      )
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
        {current.length > 1 && (
          <Polyline positions={[...current, current[0]]} />
        )}
        <ClickHandler />
      </MapContainer>
      <button onClick={finishPolygon}>Finish</button>
      <ul>
        {polygons.map((poly) => {
          const inside = pointInPolygon(position, poly.points);
          return (
            <li key={poly.name}>
              {poly.name} - {inside ? 'inside' : 'outside'}
              <button onClick={() => renamePolygon(poly.name)}>Rename</button>
              <button onClick={() => editMessages(poly.name)}>Alerts</button>
              <button onClick={() => removePolygon(poly.name)}>Delete</button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
