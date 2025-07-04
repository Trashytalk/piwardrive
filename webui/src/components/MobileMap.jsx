import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { useEffect, useState } from 'react';
import 'leaflet/dist/leaflet.css';
import { routePrefetch, enforceCacheLimit } from '../tileCache.js';

export default function MobileMap() {
  const [position, setPosition] = useState(null);
  const [track, setTrack] = useState([]);

  useEffect(() => {
    let watch = null;
    if (navigator.geolocation) {
      watch = navigator.geolocation.watchPosition(
        (p) => {
          const pos = [p.coords.latitude, p.coords.longitude];
          setPosition(pos);
          setTrack((t) => [...t.slice(-99), pos]);
          if (track.length) routePrefetch([track[track.length - 1], pos]);
        },
        () => {},
        { enableHighAccuracy: true }
      );
    }
    enforceCacheLimit();
    return () => {
      if (watch != null) navigator.geolocation.clearWatch(watch);
    };
  }, [track]);

  return (
    <MapContainer
      center={position || [0, 0]}
      zoom={16}
      style={{ height: '80vh' }}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {position && (
        <Marker position={position}>
          <Popup>Your location</Popup>
        </Marker>
      )}
    </MapContainer>
  );
}
