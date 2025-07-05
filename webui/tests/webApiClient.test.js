import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { getGps, getAps, getBt, toggleKismet } from '../src/webApiClient.js';

let origFetch;

describe('webApiClient', () => {
  beforeEach(() => {
    origFetch = global.fetch;
    global.fetch = vi.fn(() =>
      Promise.resolve({ json: () => Promise.resolve({}) })
    );
  });

  afterEach(() => {
    global.fetch = origFetch;
  });

  it('fetches gps', async () => {
    global.fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ lat: 1 }),
    });
    const data = await getGps();
    expect(global.fetch).toHaveBeenCalledWith('/api/gps');
    expect(data.lat).toBe(1);
  });

  it('fetches aps', async () => {
    global.fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ features: [1] }),
    });
    const data = await getAps();
    expect(global.fetch).toHaveBeenCalledWith('/api/aps');
    expect(data.features).toEqual([1]);
  });

  it('fetches bluetooth', async () => {
    global.fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ features: [2] }),
    });
    const data = await getBt();
    expect(global.fetch).toHaveBeenCalledWith('/api/bt');
    expect(data.features).toEqual([2]);
  });

  it('toggles kismet', async () => {
    global.fetch.mockResolvedValueOnce({});
    await toggleKismet('start');
    expect(global.fetch).toHaveBeenCalledWith(
      '/api/kismet/toggle?state=start',
      { method: 'POST' }
    );
  });
});
