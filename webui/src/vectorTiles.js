import fs from 'fs';
import sqlite3 from 'sqlite3';

sqlite3.verbose();

export class MBTiles {
  constructor(path) {
    if (!fs.existsSync(path)) throw new Error(path);
    this.path = path;
  }

  tiles(z, x, y) {
    return new Promise(resolve => {
      const db = new sqlite3.Database(this.path);
      db.get(
        'SELECT tile_data FROM tiles WHERE zoom_level=? AND tile_column=? AND tile_row=?',
        [z, x, y],
        (err, row) => {
          db.close();
          resolve(err ? null : row ? row.tile_data : null);
        }
      );
    });
  }
}

export function availableTiles(path) {
  return new Promise(resolve => {
    const db = new sqlite3.Database(path);
    db.all('SELECT zoom_level, tile_column, tile_row FROM tiles', (err, rows) => {
      db.close();
      resolve(rows ? rows.map(r => [r.zoom_level, r.tile_column, r.tile_row]) : []);
    });
  });
}
