import { spawn as _spawn } from 'child_process';
import { fileURLToPath } from 'url';
import path from 'path';

/* global process */

export function runStartKioskScript({ args = [], env = process.env, spawnFn = _spawn } = {}) {
  const scriptPath = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', '..', 'scripts', 'start_kiosk.sh');
  return new Promise((resolve, reject) => {
    const proc = spawnFn('bash', [scriptPath, ...args], { env });
    proc.on('error', reject);
    proc.on('exit', code => {
      if (code === 0) resolve(true);
      else reject(new Error(`script exited with code ${code}`));
    });
  });
}
