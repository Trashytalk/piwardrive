import { describe, it, expect, vi, afterEach } from 'vitest';
import { scanBluetooth } from '../src/btScanner.js';

describe('scanBluetooth', () => {
  afterEach(() => {
    delete global.bleakDiscover;
    delete global.btctlScan;
  });

  it('uses bleakDiscover when available', async () => {
    global.bleakDiscover = vi.fn(async () => [
      { address: 'AA:BB:CC:DD:EE:FF', name: 'Foo' },
      { address: '11:22:33:44:55:66', name: null },
    ]);
    const devices = await scanBluetooth(1);
    expect(devices).toEqual([
      { address: 'AA:BB:CC:DD:EE:FF', name: 'Foo' },
      { address: '11:22:33:44:55:66', name: '11:22:33:44:55:66' },
    ]);
  });

  it('falls back to btctlScan', async () => {
    global.btctlScan = vi.fn(async () => [
      { address: 'AA:BB:CC:DD:EE:FF', name: 'Foo' },
      { address: '11:22:33:44:55:66', name: 'Bar' },
    ]);
    const devices = await scanBluetooth(1);
    expect(devices).toContainEqual({ address: 'AA:BB:CC:DD:EE:FF', name: 'Foo' });
    expect(devices).toContainEqual({ address: '11:22:33:44:55:66', name: 'Bar' });
  });
});
