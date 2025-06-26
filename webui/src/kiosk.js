import { spawn as _spawn } from 'child_process';
import fs from 'fs';
import path from 'path';

function which(cmd) {
  const dirs = process.env.PATH.split(path.delimiter);
  for (const d of dirs) {
    const p = path.join(d, cmd);
    try {
      fs.accessSync(p, fs.constants.X_OK);
      return p;
    } catch (e) {}
  }
  return null;
}

export async function runKiosk({ url = 'http://localhost:8000', delay = 2000, spawnFn = _spawn, whichFn = which } = {}) {
  const server = spawnFn('piwardrive-webui', []);
  try {
    await new Promise(r => setTimeout(r, delay));
    const browser = whichFn('chromium-browser') || whichFn('chromium');
    if (!browser) throw new Error('Chromium browser not found');
    spawnFn(browser, ['--kiosk', url]);
  } finally {
    if (server && server.kill) server.kill();
  }
}
