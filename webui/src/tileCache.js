export function deg2num(lat, lon, zoom) {
  const latRad = (lat * Math.PI) / 180;
  const n = Math.pow(2, zoom);
  const x = Math.floor(((lon + 180) / 360) * n);
  const y = Math.floor(
    ((1 - Math.log(Math.tan(latRad) + 1 / Math.cos(latRad)) / Math.PI) / 2) * n
  );
  return [x, y];
}

const CACHE_NAME = 'tiles';
const INDEX_KEY = 'tile-cache-index';

function loadIndex() {
  try {
    return JSON.parse(localStorage.getItem(INDEX_KEY)) || {};
  } catch {
    return {};
  }
}

function saveIndex(idx) {
  localStorage.setItem(INDEX_KEY, JSON.stringify(idx));
}

export async function prefetchTiles(bounds, zoom = 16, progressCb) {
  const [minLat, minLon, maxLat, maxLon] = bounds;
  const [x1, y1] = deg2num(maxLat, minLon, zoom);
  const [x2, y2] = deg2num(minLat, maxLon, zoom);
  const xMin = Math.min(x1, x2);
  const xMax = Math.max(x1, x2);
  const yMin = Math.min(y1, y2);
  const yMax = Math.max(y1, y2);
  const tasks = [];
  for (let x = xMin; x <= xMax; x++) {
    for (let y = yMin; y <= yMax; y++) {
      tasks.push({ x, y });
    }
  }
  const cache = await caches.open(CACHE_NAME);
  const idx = loadIndex();
  let done = 0;
  for (const { x, y } of tasks) {
    const url = `https://tile.openstreetmap.org/${zoom}/${x}/${y}.png`;
    const key = `${zoom}/${x}/${y}`;
    if (!idx[key]) {
      try {
        const resp = await fetch(url);
        if (resp.ok) {
          const clone = resp.clone();
          await cache.put(url, clone);
          const buf = await resp.arrayBuffer();
          idx[key] = { time: Date.now(), size: buf.byteLength };
        }
      } catch (e) {
        // ignore caching failures
      }
    } else {
      idx[key].time = Date.now();
    }
    done += 1;
    if (progressCb) progressCb(done, tasks.length);
  }
  saveIndex(idx);
}

export async function purgeOldTiles(maxAgeDays = 30) {
  const cutoff = Date.now() - maxAgeDays * 86400 * 1000;
  const cache = await caches.open(CACHE_NAME);
  const idx = loadIndex();
  for (const [key, meta] of Object.entries(idx)) {
    if (meta.time < cutoff) {
      await cache.delete(`https://tile.openstreetmap.org/${key}.png`);
      delete idx[key];
    }
  }
  saveIndex(idx);
}

export async function enforceCacheLimit(limitMb = 512) {
  const cache = await caches.open(CACHE_NAME);
  const idx = loadIndex();
  let total = Object.values(idx).reduce((a, b) => a + b.size, 0);
  const entries = Object.entries(idx).sort((a, b) => a[1].time - b[1].time);
  while (total > limitMb * 1024 * 1024 && entries.length) {
    const [key, meta] = entries.shift();
    await cache.delete(`https://tile.openstreetmap.org/${key}.png`);
    delete idx[key];
    total -= meta.size;
  }
  saveIndex(idx);
}

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

function bearing(p1, p2) {
  const lat1 = (p1[0] * Math.PI) / 180;
  const lat2 = (p2[0] * Math.PI) / 180;
  const dLon = ((p2[1] - p1[1]) * Math.PI) / 180;
  const y = Math.sin(dLon) * Math.cos(lat2);
  const x =
    Math.cos(lat1) * Math.sin(lat2) -
    Math.sin(lat1) * Math.cos(lat2) * Math.cos(dLon);
  return (Math.atan2(y, x) * 180) / Math.PI + (360 % 360);
}

function destination(origin, brg, dist) {
  const r = 6371000.0;
  const ang = dist / r;
  const lat1 = (origin[0] * Math.PI) / 180;
  const lon1 = (origin[1] * Math.PI) / 180;
  const b = (brg * Math.PI) / 180;
  const lat2 = Math.asin(
    Math.sin(lat1) * Math.cos(ang) +
      Math.cos(lat1) * Math.sin(ang) * Math.cos(b)
  );
  const lon2 =
    lon1 +
    Math.atan2(
      Math.sin(b) * Math.sin(ang) * Math.cos(lat1),
      Math.cos(ang) - Math.sin(lat1) * Math.sin(lat2)
    );
  return [(lat2 * 180) / Math.PI, (((lon2 * 180) / Math.PI + 540) % 360) - 180];
}

export async function routePrefetch(
  track,
  lookahead = 5,
  delta = 0.01,
  zoom = 16
) {
  if (track.length < 2) return;
  const p1 = track[track.length - 2];
  const p2 = track[track.length - 1];
  const brg = bearing(p1, p2);
  const step = haversine(p1, p2);
  let lat = p2[0];
  let lon = p2[1];
  const points = [];
  for (let i = 0; i < lookahead; i++) {
    [lat, lon] = destination([lat, lon], brg, step);
    points.push([lat, lon]);
  }
  const lats = points.map((p) => p[0]).concat(p2[0]);
  const lons = points.map((p) => p[1]).concat(p2[1]);
  const bbox = [
    Math.min(...lats) - delta,
    Math.min(...lons) - delta,
    Math.max(...lats) + delta,
    Math.max(...lons) + delta,
  ];
  await prefetchTiles(bbox, zoom);
}
