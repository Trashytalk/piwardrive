import { useEffect, useRef, useState } from 'react';
import { reportError } from '../exceptionHandler.js';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
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

export default function TrackMap() {
  const [center, setCenter] = useState([0, 0]);
  const [zoom] = useState(16);
  const [follow, setFollow] = useState(true);
  const [aps, setAps] = useState([]);
  const [bts, setBts] = useState([]);
  const [filter, setFilter] = useState({ ssid: '', encryption: '', btName: '' });
  const [showHeatmap, setShowHeatmap] = useState(false);
  const [showTrack, setShowTrack] = useState(true);
  const trackRef = useRef([]);
  const [, forceUpdate] = useState(0);

  // fetch GPS periodically
  useEffect(() => {
    const id = setInterval(async () => {
      try {
        const resp = await fetch('/gps');
        const data = await resp.json();
        if (data && data.lat != null && data.lon != null) {
          if (follow) setCenter([data.lat, data.lon]);
          trackRef.current.push([data.lat, data.lon]);
          forceUpdate(n => n + 1);
        }
      } catch (e) {
        reportError(e);
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
        reportError(e);
      }
    };
    load();
  }, []);

  // fetch Bluetooth devices once
  useEffect(() => {
    const load = async () => {
      try {
        const resp = await fetch('/export/bt?fmt=geojson');
        const j = await resp.json();
        const markers = j.features.map(f => ({
          ...f.properties,
          lat: f.geometry.coordinates[1],
          lon: f.geometry.coordinates[0]
        }));
        setBts(markers);
      } catch (e) {
        reportError(e);
      }
    };
    load();
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
        reportError(e);
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

  // route prefetch hourly
  useEffect(() => {
    const id = setInterval(() => {
      routePrefetch(trackRef.current, 5, 0.01, zoom);
    }, 3600000);
    return () => clearInterval(id);
  }, [zoom]);

  const filteredAps = aps.filter(ap => {
    if (filter.ssid && !(ap.ssid || '').includes(filter.ssid)) return false;
    if (filter.encryption && filter.encryption !== ap.encryption) return false;
    return true;
  });

  const filteredBts = bts.filter(bt => {
    if (filter.btName && !(bt.name || '').includes(filter.btName)) return false;
    return true;
  });

  const prefetchView = () => {
    const bounds = [
      center[0] - 0.01,
      center[1] - 0.01,
      center[0] + 0.01,
      center[1] + 0.01
    ];
    prefetchTiles(bounds, zoom);
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
        <label style={{ marginLeft: '1em' }}>
          <input
            type="checkbox"
            checked={showTrack}
            onChange={() => setShowTrack(!showTrack)}
          />
          Show Track
        </label>
        <button onClick={prefetchView} style={{ marginLeft: '1em' }}>
          Prefetch View
        </button>
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
        <input
          placeholder="BT name"
          value={filter.btName}
          onChange={e => setFilter({ ...filter, btName: e.target.value })}
          style={{ marginLeft: '1em' }}
        />
      </div>
      <MapContainer center={center} zoom={zoom} style={{ height: '80vh' }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        <HeatmapLayer show={showHeatmap} />
        {showTrack && trackRef.current.length > 1 && (
          <Polyline positions={trackRef.current} color="red" />
        )}
        {filteredAps.map(ap => (
          <Marker key={ap.bssid} position={[ap.lat, ap.lon]}>
            <Popup>{ap.ssid || ap.bssid}</Popup>
          </Marker>
        ))}
        {filteredBts.map(bt => (
          <Marker key={bt.address} position={[bt.lat, bt.lon]}>
            <Popup>{bt.name || bt.address}</Popup>
          </Marker>
        ))}
        <GPSMarker position={center} />
      </MapContainer>
    </div>
  );
}
