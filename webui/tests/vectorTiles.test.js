import { describe, it, expect } from 'vitest';
import { MBTiles, availableTiles } from '../src/vectorTiles.js';
import fs from 'fs';
import path from 'path';
import sqlite3 from 'sqlite3';

sqlite3.verbose();

function createDb(p) {
  return new Promise((resolve) => {
    const db = new sqlite3.Database(p);
    db.serialize(() => {
      db.run(
        'CREATE TABLE tiles (zoom_level INTEGER, tile_column INTEGER, tile_row INTEGER, tile_data BLOB)'
      );
      db.run('INSERT INTO tiles VALUES (1,2,3,?)', Buffer.from('data'));
      db.run('INSERT INTO tiles VALUES (2,0,0,?)', Buffer.from('foo'), () => {
        db.close();
        resolve();
      });
    });
  });
}

describe('vectorTiles module', () => {
  it('throws on missing file', () => {
    expect(() => new MBTiles('missing.mbtiles')).toThrow();
  });

  it('reads tiles and lists available', async () => {
    const file = path.join(process.cwd(), 'tiles.mbtiles');
    fs.writeFileSync(file, '');
    await createDb(file);
    const mb = new MBTiles(file);
    const data = await mb.tiles(1, 2, 3);
    expect(Buffer.isBuffer(data) && data.equals(Buffer.from('data'))).toBe(
      true
    );
    expect(await mb.tiles(9, 9, 9)).toBeNull();
    const tiles = await availableTiles(file);
    expect(new Set(tiles.map((t) => t.join(',')))).toEqual(
      new Set(['1,2,3', '2,0,0'])
    );
    fs.unlinkSync(file);
  });
});
