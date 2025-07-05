import { useEffect, useRef, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { useWebSocket } from '../useWebSocket.js';

export default function LiveMonitoring() {
  const [feed, setFeed] = useState([]);
  const [stats, setStats] = useState({ total: 0 });
  const [markers, setMarkers] = useState([]);
  const feedRef = useRef(null);
  const { status } = useWebSocket('/ws/live', {
    onMessage: (raw) => {
      try {
        const data = JSON.parse(raw);
        if (data.detection) {
          setFeed((f) => [...f.slice(-99), data.detection]);
          if (data.detection.lat != null && data.detection.lon != null) {
            setMarkers((m) => [
              ...m.slice(-99),
              {
                lat: data.detection.lat,
                lon: data.detection.lon,
                text: data.detection.text,
              },
            ]);
          }
        }
        if (data.stats) setStats(data.stats);
      } catch (_) {}
    },
  });

  useEffect(() => {
    if (feedRef.current)
      feedRef.current.scrollTop = feedRef.current.scrollHeight;
  }, [feed]);

  const quality =
    feed.length && feed[feed.length - 1].ts
      ? Date.now() - feed[feed.length - 1].ts < 10000
        ? 'good'
        : 'stale'
      : 'unknown';

  return (
    <div>
      <div>
        Connection: {status} (data {quality})
      </div>
      <div style={{ display: 'flex' }}>
        <div
          ref={feedRef}
          style={{
            overflowY: 'auto',
            maxHeight: '200px',
            flex: 1,
            border: '1px solid #ccc',
            padding: '4px',
          }}
        >
          {feed.map((e, i) => (
            <div key={i}>{e.text || JSON.stringify(e)}</div>
          ))}
        </div>
        <div style={{ width: '300px', height: '200px', marginLeft: '1em' }}>
          <MapContainer center={[0, 0]} zoom={2} style={{ height: '100%' }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            {markers.map((m, idx) => (
              <Marker key={idx} position={[m.lat, m.lon]}>
                <Popup>{m.text}</Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>
      </div>
      <div>Detections: {stats.total ?? 0}</div>
    </div>
  );
}
