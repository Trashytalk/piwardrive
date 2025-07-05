// Utility functions for exporting data in various formats
import fs from 'fs';
import { stringify } from 'csv-stringify/sync';
import kml from 'gtran-kml';
import kmz from 'gtran-kmz';
import shp from 'gtran-shapefile';
import { buildGPX, BaseBuilder } from 'gpx-builder';

export const EXPORT_FORMATS = ['csv', 'json', 'gpx', 'kml', 'geojson', 'shp'];

export function filterRecords(
  records,
  { ssid, encryption, oui, minSignal, maxAge } = {}
) {
  const now = Date.now() / 1000;
  const result = [];
  for (const rec of records) {
    if (ssid && !(rec.ssid || '').includes(ssid)) continue;
    if (encryption && encryption !== rec.encryption) continue;
    if (oui && !(rec.bssid || '').startsWith(oui)) continue;
    if (minSignal !== undefined) {
      const sig = rec.signal_dbm;
      if (sig === undefined || Number(sig) < minSignal) continue;
    }
    if (maxAge !== undefined) {
      const ts = rec.last_time;
      if (ts === undefined || now - Number(ts) > maxAge) continue;
    }
    result.push({ ...rec });
  }
  return result;
}

function recordsToGeojson(records, fields) {
  const features = [];
  for (const rec of records) {
    const lat = rec.lat;
    const lon = rec.lon;
    if (lat == null || lon == null) continue;
    let props = { ...rec };
    delete props.lat;
    delete props.lon;
    if (fields) {
      props = {};
      for (const name of fields) {
        if (name !== 'lat' && name !== 'lon') props[name] = rec[name];
      }
    }
    features.push({
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [lon, lat] },
      properties: props,
    });
  }
  return { type: 'FeatureCollection', features };
}

export async function exportRecords(records, path, fmt, fields = null) {
  if (fields)
    records = records.map((r) =>
      Object.fromEntries(fields.map((f) => [f, r[f]]))
    );
  fmt = fmt.toLowerCase();
  if (!EXPORT_FORMATS.includes(fmt))
    throw new Error(`Unsupported format: ${fmt}`);

  if (fmt === 'csv') {
    const columns = fields || (records[0] ? Object.keys(records[0]) : []);
    const out = stringify(records, { header: true, columns });
    fs.writeFileSync(path, out);
    return;
  }

  if (fmt === 'json') {
    fs.writeFileSync(path, JSON.stringify(records, null, 2));
    return;
  }

  if (fmt === 'gpx') {
    const { Point } = BaseBuilder.MODELS;
    const points = [];
    for (const rec of records) {
      const lat = rec.lat;
      const lon = rec.lon;
      if (lat == null || lon == null) continue;
      const name = rec.ssid || rec.bssid;
      const opts = name ? { name: String(name) } : {};
      points.push(new Point(lat, lon, opts));
    }
    const builder = new BaseBuilder();
    builder.setWayPoints(points);
    fs.writeFileSync(path, buildGPX(builder.toObject()));
    return;
  }

  const geojson = recordsToGeojson(records, fields);

  if (fmt === 'geojson') {
    fs.writeFileSync(path, JSON.stringify(geojson));
    return;
  }

  if (fmt === 'kml') {
    await kml.fromGeoJson(geojson, path);
    return;
  }

  if (fmt === 'shp') {
    await shp.fromGeoJson(geojson, path);
    return;
  }
}

export function estimateLocationFromRssi(points) {
  let total = 0;
  let sumLat = 0;
  let sumLon = 0;
  for (const p of points) {
    const lat = parseFloat(p.lat);
    const lon = parseFloat(p.lon);
    const rssi = parseFloat(p.rssi);
    if (isNaN(lat) || isNaN(lon) || isNaN(rssi)) continue;
    const weight = 1 / Math.max(1, Math.abs(rssi));
    sumLat += lat * weight;
    sumLon += lon * weight;
    total += weight;
  }
  if (total === 0) return null;
  return [sumLat / total, sumLon / total];
}

export async function exportMapKml(
  track,
  aps,
  bts,
  path,
  { computePosition = false } = {}
) {
  const features = [];
  if (track && track.length) {
    features.push({
      type: 'Feature',
      geometry: {
        type: 'LineString',
        coordinates: track.map(([lat, lon]) => [lon, lat]),
      },
      properties: { name: 'Track' },
    });
  }
  for (const rec of aps) {
    let { lat, lon } = rec;
    if ((lat == null || lon == null) && computePosition) {
      const loc = estimateLocationFromRssi(rec.observations || []);
      if (loc) [lat, lon] = loc;
    }
    if (lat == null || lon == null) continue;
    features.push({
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [lon, lat] },
      properties: { name: rec.ssid || rec.bssid },
    });
  }
  for (const rec of bts) {
    const { lat, lon } = rec;
    if (lat == null || lon == null) continue;
    features.push({
      type: 'Feature',
      geometry: { type: 'Point', coordinates: [lon, lat] },
      properties: { name: rec.name || rec.address },
    });
  }
  const geojson = { type: 'FeatureCollection', features };
  if (path.toLowerCase().endsWith('.kmz')) {
    await kmz.fromGeoJson(geojson, path);
  } else {
    await kml.fromGeoJson(geojson, path);
  }
}
