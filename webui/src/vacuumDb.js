import { execFileSync } from 'child_process';

export function main(dbPath) {
  execFileSync('sqlite3', [dbPath, 'VACUUM']);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main(process.argv[2] || 'piwardrive.db');
}
