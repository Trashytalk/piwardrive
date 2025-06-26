import { describe, it, expect, vi } from 'vitest';
import fs from 'fs';
import os from 'os';
import path from 'path';
import { main } from '../scripts/tileMaintenance.js';

describe('tileMaintenance cli', () => {
  it('invokes commands', async () => {
    global.fetch = vi.fn(() => Promise.resolve({
      ok: true,
      arrayBuffer: () => Promise.resolve(new ArrayBuffer(1))
    }));
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'tiles-'));
    await main(['prefetch', '0', '0', '0.1', '0.1', '--zoom', '1', '--folder', dir]);
    await main(['purge-old', '--folder', dir, '--days', '1']);
    await main(['enforce-limit', '--folder', dir, '--limit-mb', '1']);
    expect(fetch).toHaveBeenCalled();
  });
});
