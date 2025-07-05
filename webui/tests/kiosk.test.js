import { describe, it, expect, vi } from 'vitest';
import { runKiosk } from '../src/kiosk.js';

describe('runKiosk', () => {
  it('launches server and browser', async () => {
    const calls = [];
    const spawn = vi.fn((cmd, args) => {
      calls.push(cmd);
      return { kill: vi.fn() };
    });
    const whichFn = vi.fn((cmd) => `/bin/${cmd}`);
    await runKiosk({ delay: 0, spawnFn: spawn, whichFn });
    expect(calls).toContain('piwardrive-webui');
    expect(calls).toContain('/bin/chromium-browser');
  });
});
