import fs from 'fs';
import path from 'path';
import os from 'os';
import { execFileSync } from 'child_process';

export function applyStyle(dbPath, { stylePath, name, description } = {}) {
  const lines = [
    'CREATE TABLE IF NOT EXISTS metadata (name TEXT, value TEXT);',
  ];
  if (name != null)
    lines.push(
      `INSERT OR REPLACE INTO metadata (name,value) VALUES ('name','${name}')`
    );
  if (description != null)
    lines.push(
      `INSERT OR REPLACE INTO metadata (name,value) VALUES ('description','${description}')`
    );
  if (stylePath) {
    const style = fs.readFileSync(stylePath, 'utf-8');
    JSON.parse(style);
    lines.push(
      `INSERT OR REPLACE INTO metadata (name,value) VALUES ('style','${style.replace(/'/g, "''")}')`
    );
  }
  execFileSync('sqlite3', [dbPath], { input: lines.join('\n') });
}

export function buildMbtiles(folder, output) {
  if (!fs.existsSync(folder) || !fs.statSync(folder).isDirectory()) {
    throw new Error('Folder not found');
  }
  const sql = [];
  sql.push(
    'CREATE TABLE IF NOT EXISTS tiles (zoom_level INTEGER, tile_column INTEGER, tile_row INTEGER, tile_data BLOB, UNIQUE (zoom_level,tile_column,tile_row));'
  );
  sql.push('CREATE TABLE IF NOT EXISTS metadata (name TEXT, value TEXT);');
  for (const rootZ of fs.readdirSync(folder)) {
    const zDir = path.join(folder, rootZ);
    if (!fs.statSync(zDir).isDirectory()) continue;
    for (const xEntry of fs.readdirSync(zDir)) {
      const xDir = path.join(zDir, xEntry);
      if (!fs.statSync(xDir).isDirectory()) continue;
      for (const file of fs.readdirSync(xDir)) {
        if (!file.endsWith('.pbf')) continue;
        const yName = path.basename(file, '.pbf');
        const z = parseInt(rootZ, 10);
        const x = parseInt(xEntry, 10);
        const y = parseInt(yName, 10);
        if (Number.isNaN(z) || Number.isNaN(x) || Number.isNaN(y)) continue;
        const tileRow = Math.pow(2, z) - 1 - y;
        const data = fs.readFileSync(path.join(xDir, file));
        const hex = data.toString('hex');
        sql.push(
          `INSERT OR REPLACE INTO tiles (zoom_level,tile_column,tile_row,tile_data) VALUES (${z},${x},${tileRow},X'${hex}')`
        );
      }
    }
  }
  const tmp = path.join(os.tmpdir(), `mb-${Date.now()}.sql`);
  fs.writeFileSync(tmp, sql.join('\n'));
  execFileSync('sqlite3', [output], { input: fs.readFileSync(tmp) });
  fs.unlinkSync(tmp);
}
