import { describe, it, expect } from 'vitest';
import fs from 'fs';
import os from 'os';
import path from 'path';
import { runStartKioskScript } from '../src/startKioskScript.js';

describe('runStartKioskScript', () => {
  it('launches server and browser', async () => {
    const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'kiosk-'));
    const bin = path.join(tmp, 'bin');
    fs.mkdirSync(bin);
    const log = path.join(tmp, 'log.txt');

    fs.writeFileSync(
      path.join(bin, 'piwardrive-webui'),
      `#!/bin/sh\necho server_started >> "${log}"\ntrap 'exit 0' TERM\nwhile true; do sleep 0.1; done\n`
    );
    fs.writeFileSync(
      path.join(bin, 'chromium-browser'),
      `#!/bin/sh\necho browser_called >> "${log}"\n`
    );
    fs.writeFileSync(path.join(bin, 'sleep'), '#!/bin/sh\n:');
    for (const f of ['piwardrive-webui', 'chromium-browser', 'sleep']) {
      fs.chmodSync(path.join(bin, f), 0o755);
    }

    const env = { ...process.env, PATH: `${bin}:${process.env.PATH}` };
    await runStartKioskScript({ args: ['--delay', '0'], env });

    const text = fs.readFileSync(log, 'utf8');
    expect(text).toContain('server_started');
    expect(text).toContain('browser_called');
  });
});
