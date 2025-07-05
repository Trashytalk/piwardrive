import fs from 'fs/promises';
import { existsSync } from 'fs';
import path from 'path';
import { deg2num } from '../webui/src/tileCache.js';

const INDEX = 'tile-cache-index.json';

async function loadIndex(folder) {
  try {
    const data = await fs.readFile(path.join(folder, INDEX), 'utf8');
    return JSON.parse(data);
  } catch {
    return {};
  }
}

async function saveIndex(folder, idx) {
  await fs.mkdir(folder, { recursive: true });
  await fs.writeFile(path.join(folder, INDEX), JSON.stringify(idx));
}

export async function prefetch(
  bounds,
  { zoom = 16, folder = '/mnt/ssd/tiles' } = {}
) {
  const [minLat, minLon, maxLat, maxLon] = bounds.map(Number);
  const [x1, y1] = deg2num(maxLat, minLon, zoom);
  const [x2, y2] = deg2num(minLat, maxLon, zoom);
  const xMin = Math.min(x1, x2);
  const xMax = Math.max(x1, x2);
  const yMin = Math.min(y1, y2);
  const yMax = Math.max(y1, y2);
  const total = (xMax - xMin + 1) * (yMax - yMin + 1);
  let done = 0;
  const idx = await loadIndex(folder);
  for (let x = xMin; x <= xMax; x++) {
    for (let y = yMin; y <= yMax; y++) {
      const url = `https://tile.openstreetmap.org/${zoom}/${x}/${y}.png`;
      const key = `${zoom}/${x}/${y}`;
      const file = path.join(folder, `${zoom}`, `${x}`, `${y}.png`);
      await fs.mkdir(path.dirname(file), { recursive: true });
      if (!idx[key] || !existsSync(file)) {
        try {
          const resp = await fetch(url);
          if (resp.ok) {
            const buf = Buffer.from(await resp.arrayBuffer());
            await fs.writeFile(file, buf);
            idx[key] = { time: Date.now(), size: buf.length };
          }
        } catch {}
      } else {
        idx[key].time = Date.now();
      }
      done += 1;
      if (process.stdout.isTTY) {
        process.stdout.write(`${done}/${total}\r`);
      }
    }
  }
  await saveIndex(folder, idx);
  if (process.stdout.isTTY) process.stdout.write('\n');
}

export async function purgeOld(folder = '/mnt/ssd/tiles', days = 30) {
  const cutoff = Date.now() - days * 86400 * 1000;
  const idx = await loadIndex(folder);
  for (const [key, meta] of Object.entries(idx)) {
    if (meta.time < cutoff) {
      const file = path.join(folder, `${key}.png`);
      try {
        await fs.unlink(file);
      } catch {}
      delete idx[key];
    }
  }
  await saveIndex(folder, idx);
}

export async function enforceLimit(folder = '/mnt/ssd/tiles', limitMb = 512) {
  const idx = await loadIndex(folder);
  let total = Object.values(idx).reduce((a, b) => a + b.size, 0);
  const max = limitMb * 1024 * 1024;
  const entries = Object.entries(idx).sort((a, b) => a[1].time - b[1].time);
  for (const [key, meta] of entries) {
    if (total <= max) break;
    const file = path.join(folder, `${key}.png`);
    try {
      await fs.unlink(file);
    } catch {}
    total -= meta.size;
    delete idx[key];
  }
  await saveIndex(folder, idx);
}

function parseArgs(argv) {
  const opts = { folder: '/mnt/ssd/tiles' };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--zoom') opts.zoom = Number(argv[++i]);
    else if (a === '--folder') opts.folder = argv[++i];
    else if (a === '--days') opts.days = Number(argv[++i]);
    else if (a === '--limit-mb') opts.limitMb = Number(argv[++i]);
    else opts._ = (opts._ || []).concat(a);
  }
  return opts;
}

export async function main(argv = process.argv.slice(2)) {
  const [cmd, ...rest] = argv;
  const opts = parseArgs(rest);
  if (cmd === 'prefetch') {
    const box = opts._.slice(0, 4).map(Number);
    if (box.length < 4 || box.some((n) => Number.isNaN(n))) {
      console.error('bounding box required');
      return;
    }
    await prefetch(box, { zoom: opts.zoom, folder: opts.folder });
  } else if (cmd === 'purge-old') {
    await purgeOld(opts.folder, opts.days);
  } else if (cmd === 'enforce-limit') {
    await enforceLimit(opts.folder, opts.limitMb);
  } else {
    console.log(
      'Commands: prefetch <minLat> <minLon> <maxLat> <maxLon> [--zoom z] [--folder dir]'
    );
    console.log('          purge-old [--days n] [--folder dir]');
    console.log('          enforce-limit [--limit-mb m] [--folder dir]');
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
