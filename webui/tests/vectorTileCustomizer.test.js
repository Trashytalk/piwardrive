import { describe, it, expect } from 'vitest';
import { applyStyle, buildMbtiles } from '../src/vectorTileCustomizer.js';
import fs from 'fs';
import path from 'path';
import sqlite3 from 'sqlite3';

sqlite3.verbose();

function readMeta(dbPath) {
  return new Promise((resolve) => {
    const db = new sqlite3.Database(dbPath);
    db.all('SELECT name, value FROM metadata', (err, rows) => {
      db.close();
      resolve(Object.fromEntries(rows.map((r) => [r.name, r.value])));
    });
  });
}

describe('vector tile customizer', () => {
  it('applies style', async () => {
    const tmp = path.join(process.cwd(), 'test.mbtiles');
    fs.writeFileSync(tmp, '');
    applyStyle(tmp, { name: 'N', description: 'D' });
    const meta = await readMeta(tmp);
    expect(meta.name).toBe('N');
    expect(meta.description).toBe('D');
    fs.unlinkSync(tmp);
  });

  it('builds mbtiles', async () => {
    const dir = path.join(process.cwd(), 'tiles');
    fs.mkdirSync(path.join(dir, '1/2'), { recursive: true });
    fs.writeFileSync(path.join(dir, '1/2/3.pbf'), 'data');
    const out = path.join(process.cwd(), 'out.mbtiles');
    buildMbtiles(dir, out);
    const db = new sqlite3.Database(out);
    await new Promise((resolve) =>
      db.get(
        'SELECT zoom_level, tile_column, tile_row, tile_data FROM tiles',
        (err, row) => {
          db.close();
          resolve(row);
        }
      )
    ).then((row) => {
      expect(row.zoom_level).toBe(1);
    });
    fs.rmSync(dir, { recursive: true });
    fs.unlinkSync(out);
  });
});
