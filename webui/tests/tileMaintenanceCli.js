import { execFileSync } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export function runCli(args = []) {
  const script = path.join(__dirname, 'run_tile_maintenance_cli.py');
  const out = execFileSync('python', [script, ...args], {
    cwd: path.join(__dirname, '..'),
    env: { ...process.env, PYTHONPATH: path.join('..', 'src') },
    encoding: 'utf-8',
  });
  return JSON.parse(out);
}
