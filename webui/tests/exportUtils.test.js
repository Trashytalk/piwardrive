import { describe, it, expect, vi } from 'vitest';
import fs from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';
import jszip from 'jszip';
import shapefile from 'shapefile';
import {
  filterRecords,
  exportRecords,
  exportMapKml,
} from '../src/exportUtils.js';

describe('filterRecords', () => {
  it('applies filters', () => {
    const records = [
      {
        ssid: 'A',
        encryption: 'WPA2',
        bssid: 'AA',
        lat: 1.0,
        lon: 2.0,
        signal_dbm: -40,
        last_time: 80,
      },
      {
        ssid: 'B',
        encryption: 'OPEN',
        bssid: 'BB',
        lat: 3.0,
        lon: 4.0,
        signal_dbm: -80,
        last_time: 20,
      },
    ];
    vi.spyOn(Date, 'now').mockReturnValue(100000);
    expect(filterRecords(records, { encryption: 'OPEN' })).toEqual([
      records[1],
    ]);
    expect(filterRecords(records, { oui: 'AA' })).toEqual([records[0]]);
    expect(filterRecords(records, { minSignal: -50 })).toEqual([records[0]]);
    expect(filterRecords(records, { maxAge: 30 })).toEqual([records[0]]);
    Date.now.mockRestore();
  });
});

describe('exportRecords', () => {
  it('writes all formats', async () => {
    const recs = [{ ssid: 'A', bssid: 'AA', lat: 1.0, lon: 2.0 }];
    const dir = tmpdir();

    const csvPath = join(dir, 'data.csv');
    await exportRecords(recs, csvPath, 'csv');
    expect(fs.readFileSync(csvPath, 'utf-8')).toContain('ssid');

    const jsonPath = join(dir, 'data.json');
    await exportRecords(recs, jsonPath, 'json');
    expect(JSON.parse(fs.readFileSync(jsonPath))).toEqual(recs);

    const gpxPath = join(dir, 'data.gpx');
    await exportRecords(recs, gpxPath, 'gpx');
    expect(fs.readFileSync(gpxPath, 'utf-8')).toContain('<wpt');

    const kmlPath = join(dir, 'data.kml');
    await exportRecords(recs, kmlPath, 'kml');
    expect(fs.readFileSync(kmlPath, 'utf-8')).toContain('<Placemark>');

    const geoPath = join(dir, 'data.geojson');
    await exportRecords(recs, geoPath, 'geojson');
    const gj = JSON.parse(fs.readFileSync(geoPath, 'utf-8'));
    expect(gj.features[0].geometry.coordinates).toEqual([2.0, 1.0]);

    const shpPath = join(dir, 'data.shp');
    await exportRecords(recs, shpPath, 'shp');
    const source = await shapefile.open(shpPath);
    const { value } = await source.read();
    expect(value.geometry.coordinates).toEqual([2.0, 1.0]);
  });
});

describe('exportMapKml', () => {
  it('creates kml and kmz', async () => {
    const track = [
      [1.0, 2.0],
      [3.0, 4.0],
    ];
    const aps = [{ ssid: 'A', lat: 1.0, lon: 2.0 }];
    const bts = [{ name: 'bt', lat: 5.0, lon: 6.0 }];

    const dir = tmpdir();
    const kmlFile = join(dir, 'map.kml');
    await exportMapKml(track, aps, bts, kmlFile);
    const text = fs.readFileSync(kmlFile, 'utf-8');
    expect(text).toContain('<LineString>');
    expect(text).toContain('2,1');
    expect(text).toContain('6,5');

    const kmzFile = join(dir, 'map.kmz');
    await exportMapKml(track, aps, bts, kmzFile);
    const buf = fs.readFileSync(kmzFile);
    const zip = await jszip.loadAsync(buf);
    expect(Object.keys(zip.files)).toContain('doc.kml');
  });
});
