import { describe, it, expect, vi } from 'vitest';
import { routePrefetch } from '../src/tileCache.js';

global.caches = {
  open: async () => ({ put: async () => {}, delete: async () => {} })
};

global.fetch = vi.fn(() => Promise.resolve({
  ok: true,
  clone: () => ({ }),
  arrayBuffer: () => Promise.resolve(new ArrayBuffer(1))
}));

describe('routePrefetch', () => {
  it('runs without error', async () => {
    const track = [ [0,0], [0.1,0.1] ];
    await expect(routePrefetch(track, 1, 0.01, 16)).resolves.toBeUndefined();
  });
});
