import { describe, it, expect, vi } from 'vitest';
import { loadOuiMap, lookupVendor, cachedLookupVendor } from '../src/ouiRegistry.js';

describe('ouiRegistry', () => {
  it('loads file and caches vendor lookup', async () => {
    global.fetch = vi.fn().mockResolvedValue({ text: () => Promise.resolve('Assignment,Organization Name\nAA-BB-CC,VendorX\n') });
    await loadOuiMap('/oui.csv');
    const vendor = lookupVendor('AA:BB:CC:00:11:22');
    expect(vendor).toBe('VendorX');
    global.fetch.mockRejectedValue(new Error('boom'));
    const vendor2 = await cachedLookupVendor('AA:BB:CC:33:44:55');
    expect(vendor2).toBe('VendorX');
    expect(global.fetch).toHaveBeenCalledTimes(1);
    global.fetch.mockRestore();
  });

  it('logs error on load failure', async () => {
    const errSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    global.fetch = vi.fn().mockRejectedValue(new Error('fail'));
    const map = await loadOuiMap('/oui.csv');
    expect(map).toEqual({});
    expect(errSpy).toHaveBeenCalled();
    global.fetch.mockRestore();
    errSpy.mockRestore();
  });
});
