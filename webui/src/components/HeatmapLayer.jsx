import { useEffect } from 'react';
import { useMap } from 'react-leaflet';
import { reportError } from '../exceptionHandler.js';
import 'leaflet.heat';

export default function HeatmapLayer({ show }) {
  const map = useMap();
  useEffect(() => {
    if (!show) return undefined;
    let layer;
    const load = async () => {
      try {
        const resp = await fetch('/overlay?bins=50');
        const data = await resp.json();
        const pts = (data.points || []).map(([lat, lon, cnt]) => [lat, lon, cnt]);
        layer = window.L.heatLayer(pts, { radius: 25 }).addTo(map);
      } catch (e) {
        reportError(e);
      }
    };
    load();
    return () => {
      if (layer) map.removeLayer(layer);
    };
  }, [show, map]);
  return null;
}
