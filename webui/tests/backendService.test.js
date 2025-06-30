import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import * as backend from '../src/backendService.js';

let origFetch;

describe('backendService', () => {
  beforeEach(() => {
    origFetch = global.fetch;
  });
  afterEach(() => {
    global.fetch = origFetch;
  });

  it('fetchServiceStatuses returns status map', async () => {
    global.fetch = vi.fn((url) =>
      Promise.resolve({
        json: () => Promise.resolve({ active: url.includes('kismet') }),
      })
    );
    vi.spyOn(backend, 'authHeaders').mockReturnValue({});
    const result = await backend.fetchServiceStatuses(['kismet', 'gpsd']);
    expect(result).toEqual({ kismet: true, gpsd: false });
    expect(global.fetch).toHaveBeenCalledTimes(2);
  });

  it('syncHealthRecords success resolves json', async () => {
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ uploaded: 1 }),
      })
    );
    vi.spyOn(backend, 'authHeaders').mockReturnValue({});
    const data = await backend.syncHealthRecords(1);
    expect(global.fetch).toHaveBeenCalledWith('/sync?limit=1', {
      method: 'POST',
      headers: {},
    });
    expect(data).toEqual({ uploaded: 1 });
  });

  it('syncHealthRecords failure throws', async () => {
    global.fetch = vi.fn(() => Promise.resolve({ ok: false }));
    vi.spyOn(backend, 'authHeaders').mockReturnValue({});
    await expect(backend.syncHealthRecords()).rejects.toThrow('sync failed');
  });

  it('fetchSigintData returns parsed json', async () => {
    const records = [{ a: 1 }];
    global.fetch = vi.fn(() =>
      Promise.resolve({ json: () => Promise.resolve(records) })
    );
    vi.spyOn(backend, 'authHeaders').mockReturnValue({});
    const data = await backend.fetchSigintData('wifi');
    expect(global.fetch).toHaveBeenCalledWith('/export/wifi?fmt=json', {
      headers: {},
    });
    expect(data).toEqual(records);
  });
});
