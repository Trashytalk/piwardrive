import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { fetchServiceStatuses, syncHealthRecords, fetchSigintData } from '../src/backendService.js';

let origFetch;

describe('backendService', () => {
  beforeEach(() => { origFetch = global.fetch; });
  afterEach(() => { global.fetch = origFetch; });

  it('fetchServiceStatuses returns status map', async () => {
    global.fetch = vi.fn(url => Promise.resolve({
      json: () => Promise.resolve({ active: url.includes('kismet') })
    }));
    const result = await fetchServiceStatuses(['kismet', 'gpsd']);
    expect(result).toEqual({ kismet: true, gpsd: false });
    expect(global.fetch).toHaveBeenCalledTimes(2);
  });

  it('syncHealthRecords success resolves json', async () => {
    global.fetch = vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve({ uploaded: 1 }) }));
    const data = await syncHealthRecords(1);
    expect(global.fetch).toHaveBeenCalledWith('/sync?limit=1', { method: 'POST' });
    expect(data).toEqual({ uploaded: 1 });
  });

  it('syncHealthRecords failure throws', async () => {
    global.fetch = vi.fn(() => Promise.resolve({ ok: false }));
    await expect(syncHealthRecords()).rejects.toThrow('sync failed');
  });

  it('fetchSigintData returns parsed json', async () => {
    const records = [{ a: 1 }];
    global.fetch = vi.fn(() => Promise.resolve({ json: () => Promise.resolve(records) }));
    const data = await fetchSigintData('wifi');
    expect(global.fetch).toHaveBeenCalledWith('/export/wifi?fmt=json');
    expect(data).toEqual(records);
  });
});
