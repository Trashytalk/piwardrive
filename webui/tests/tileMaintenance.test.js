import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
vi.mock('child_process', () => {
  const execFileSync = vi.fn();
  return { default: { execFileSync }, execFileSync };
});
import fs from 'fs';
import os from 'os';
import path from 'path';
import * as childProcess from 'child_process';
import { prefetch, purgeOld, enforceLimit, vacuumMbtiles } from '../src/tileMaintenance.js';

let origFetch;

describe('tileMaintenance helpers', () => {
  beforeEach(() => { origFetch = global.fetch; });
  afterEach(() => { global.fetch = origFetch; });

  it('prefetches and cleans tiles', async () => {
    global.fetch = vi.fn(() => Promise.resolve({
      ok: true,
      arrayBuffer: () => Promise.resolve(new ArrayBuffer(1))
    }));
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'tiles-'));
    await prefetch([0, 0, 0.1, 0.1], { zoom: 1, folder: dir });
    expect(fetch).toHaveBeenCalled();

    const idxPath = path.join(dir, 'tile-cache-index.json');
    let idx = JSON.parse(fs.readFileSync(idxPath, 'utf8'));
    const keys = Object.keys(idx);
    const key = keys[0];
    const file = path.join(dir, `${key}.png`);

    for (const k of keys) {
      idx[k].time = Date.now() - 10 * 86400 * 1000;
      idx[k].size = 1;
    }
    fs.writeFileSync(idxPath, JSON.stringify(idx));
    await purgeOld(dir, 1);
    expect(fs.existsSync(file)).toBe(false);
    idx = JSON.parse(fs.readFileSync(idxPath, 'utf8'));
    expect(idx).toEqual({});

    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, 'x');
    fs.writeFileSync(idxPath, JSON.stringify({ [key]: { time: Date.now(), size: 10 } }));
    await enforceLimit(dir, 0);
    expect(fs.existsSync(file)).toBe(false);
    idx = JSON.parse(fs.readFileSync(idxPath, 'utf8'));
    expect(idx).toEqual({});
  });

  it('vacuumMbtiles runs sqlite3', () => {
    vacuumMbtiles('test.db');
    expect(childProcess.execFileSync).toHaveBeenCalledWith('sqlite3', ['test.db', 'VACUUM']);
  });
});
