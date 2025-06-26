import { prefetch, purgeOld, enforceLimit } from '../../scripts/tileMaintenance.js';
import { execFileSync } from 'child_process';

export { prefetch, purgeOld, enforceLimit };

export function vacuumMbtiles(path) {
  execFileSync('sqlite3', [path, 'VACUUM']);
}
