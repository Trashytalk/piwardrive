import { useEffect, useRef, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polygon } from 'react-leaflet';
import HeatmapLayer from './HeatmapLayer.jsx';
import 'leaflet/dist/leaflet.css';
import { prefetchTiles, routePrefetch, purgeOldTiles, enforceCacheLimit } from '../tileCache.js';

function GPSMarker({ position }) {
  if (!position) return null;
  return (
    <Marker position={position}>
      <Popup>GPS</Popup>
    </Marker>
  );
}

export default function MapScreen() {
  const [center, setCenter] = useState([0, 0]);
  const [zoom] = useState(16);
  const [follow, setFollow] = useState(true);
  const [aps, setAps] = useState([]);
  const [filter, setFilter] = useState({ ssid: '', encryption: '' });
  const [showHeatmap, setShowHeatmap] = useState(false);
  const [geofences, setGeofences] = useState([]);
  const geofencesRef = useRef([]);
  const [prefetchProgress, setPrefetchProgress] = useState(null);
  const track = useRef([]);
  const [config, setConfig] = useState(null);

  // load configuration
  useEffect(() => {
    fetch('/config')
      .then(r => r.json())
      .then(setConfig)
      .catch(e => console.error('config fetch failed', e));
  }, []);

  useEffect(() => {
    geofencesRef.current = geofences;
  }, [geofences]);

  const pointInPoly = (pt, poly) => {
    let inside = false;
    for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
      const [lat1, lon1] = poly[i];
      const [lat2, lon2] = poly[j];
      if ((lon1 > pt[1]) !== (lon2 > pt[1])) {
        const intersect = (lat2 - lat1) * (pt[1] - lon1) / (lon2 - lon1) + lat1;
        if (pt[0] < intersect) inside = !inside;
      }
    }
    return inside;
  };

  // fetch GPS periodically
  useEffect(() => {
    const id = setInterval(async () => {
      try {
        const resp = await fetch('/gps');
        const data = await resp.json();
        if (data && data.lat != null && data.lon != null) {
          const pos = [data.lat, data.lon];
          if (follow) setCenter(pos);
          track.current.push(pos);
          if (geofencesRef.current.length) {
            setGeofences(gfs =>
              gfs.map(g => {
                const inside = pointInPoly(pos, g.points);
                if (inside && !g.inside && g.enter_message) {
                  alert(g.enter_message.replace('{name}', g.name));
                } else if (!inside && g.inside && g.exit_message) {
                  alert(g.exit_message.replace('{name}', g.name));
                }
                return { ...g, inside };
              })
            );
          }
        }
      } catch (e) {
        console.error('gps fetch failed', e);
      }
    }, 5000);
    return () => clearInterval(id);
  }, [follow]);

  // fetch APs once
  useEffect(() => {
    const load = async () => {
      try {
        const resp = await fetch('/export/aps?fmt=geojson');
        const j = await resp.json();
        const markers = j.features.map(f => ({
          ...f.properties,
          lat: f.geometry.coordinates[1],
          lon: f.geometry.coordinates[0]
        }));
        setAps(markers);
      } catch (e) {
        console.error('ap fetch error', e);
      }
    };
    load();
  }, []);

  useEffect(() => {
    fetch('/geofences')
      .then(r => r.json())
      .then(data => setGeofences(data.map(g => ({ ...g, inside: false }))))
      .catch(() => {});
  }, []);

  // subscribe to new APs
  useEffect(() => {
    const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    let ws;
    let es;

    const handle = (raw) => {
      try {
        const data = JSON.parse(raw);
        if (data.aps && data.aps.length) {
          setAps(prev => {
            const map = new Map(prev.map(a => [a.bssid, a]));
            data.aps.forEach(ap => map.set(ap.bssid, ap));
            return Array.from(map.values());
          });
        }
      } catch (e) {
        console.error('ap stream parse error', e);
      }
    };

    const startSse = () => {
      es = new EventSource('/sse/aps');
      es.onmessage = ev => handle(ev.data);
      es.onerror = () => es.close();
    };

    if (window.WebSocket) {
      try {
        ws = new WebSocket(`${proto}//${window.location.host}/ws/aps`);
        ws.onmessage = ev => handle(ev.data);
        ws.onerror = () => {
          ws.close();
          startSse();
        };
      } catch (e) {
        startSse();
      }
    } else {
      startSse();
    }

    return () => {
      if (ws) ws.close();
      if (es) es.close();
    };
  }, []);

  // offline cache maintenance daily
  useEffect(() => {
    const run = async () => {
      await purgeOldTiles(30);
      await enforceCacheLimit(512);
    };
    run();
    const id = setInterval(run, 86400000);
    return () => clearInterval(id);
  }, []);

  // route prefetch on interval from config
  useEffect(() => {
    if (!config) return;
    const intervalMs = (config.route_prefetch_interval || 3600) * 1000;
    const lookahead = config.route_prefetch_lookahead || 5;
    const id = setInterval(() => {
      routePrefetch(track.current, lookahead, 0.01, zoom);
    }, intervalMs);
    return () => clearInterval(id);
  }, [zoom, config]);

  const filtered = aps.filter(ap => {
    if (filter.ssid && !(ap.ssid || '').includes(filter.ssid)) return false;
    if (filter.encryption && filter.encryption !== ap.encryption) return false;
    return true;
  });

  const prefetchView = () => {
    const bounds = [
      center[0] - 0.01,
      center[1] - 0.01,
      center[0] + 0.01,
      center[1] + 0.01
    ];
    setPrefetchProgress({ done: 0, total: 0 });
    prefetchTiles(bounds, zoom, (d, t) => {
      setPrefetchProgress({ done: d, total: t });
    }).finally(() => {
      setTimeout(() => setPrefetchProgress(null), 2000);
    });
  };

  return (
    <div>
      <div style={{ marginBottom: '0.5em' }}>
        <label>
          <input
            type="checkbox"
            checked={follow}
            onChange={() => setFollow(!follow)}
          />
          Follow GPS
        </label>
        <label style={{ marginLeft: '1em' }}>
          <input
            type="checkbox"
            checked={showHeatmap}
            onChange={() => setShowHeatmap(!showHeatmap)}
          />
          Show Heatmap
        </label>
        <button onClick={prefetchView} style={{ marginLeft: '1em' }}>
          Prefetch View
        </button>
        {prefetchProgress && (
          <progress
            value={prefetchProgress.done}
            max={prefetchProgress.total}
            style={{ marginLeft: '1em' }}
          />
        )}
        <input
          placeholder="SSID filter"
          value={filter.ssid}
          onChange={e => setFilter({ ...filter, ssid: e.target.value })}
          style={{ marginLeft: '1em' }}
        />
        <input
          placeholder="Encryption"
          value={filter.encryption}
          onChange={e => setFilter({ ...filter, encryption: e.target.value })}
          style={{ marginLeft: '1em' }}
        />
      </div>
      <MapContainer center={center} zoom={zoom} style={{ height: '80vh' }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <HeatmapLayer show={showHeatmap} />
        {geofences.map((g, idx) => (
          <Polygon key={idx} positions={g.points} pathOptions={{ color: 'red' }} />
        ))}
        {filtered.map(ap => (
          <Marker key={ap.bssid} position={[ap.lat, ap.lon]}>
            <Popup>{ap.ssid || ap.bssid}</Popup>
          </Marker>
        ))}
        <GPSMarker position={center} />
      </MapContainer>
    </div>
  );
}
