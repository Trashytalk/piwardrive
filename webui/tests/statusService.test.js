import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { fetchStatus } from '../src/backendService.js';

let origFetch;

describe('fetchStatus', () => {
  beforeEach(() => { origFetch = global.fetch; });
  afterEach(() => { global.fetch = origFetch; });

  it('returns health records', async () => {
    global.fetch = vi.fn(() => Promise.resolve({ json: () => Promise.resolve([{ a: 1 }]) }));
    const data = await fetchStatus(1);
    expect(data).toEqual([{ a: 1 }]);
  });
});
