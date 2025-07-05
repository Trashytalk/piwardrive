import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchWigleNetworks } from '../src/wigleIntegration.js';

let origFetch;

describe('fetchWigleNetworks', () => {
  beforeEach(() => {
    origFetch = global.fetch;
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () =>
          Promise.resolve({
            results: [
              {
                netid: 'AA:BB:CC',
                ssid: 'Net',
                encryption: 'WPA2',
                trilat: 1.0,
                trilong: 2.0,
              },
            ],
          }),
      })
    );
  });

  afterEach(() => {
    global.fetch = origFetch;
  });

  it('fetches networks', async () => {
    const nets = await fetchWigleNetworks('u', 'k', 1.0, 2.0);
    expect(global.fetch).toHaveBeenCalled();
    const opts = global.fetch.mock.calls[0][1];
    expect(opts.headers.Authorization).toBe('Basic ' + btoa('u:k'));
    expect(nets).toEqual([
      {
        bssid: 'AA:BB:CC',
        ssid: 'Net',
        encryption: 'WPA2',
        lat: 1.0,
        lon: 2.0,
      },
    ]);
  });
});
