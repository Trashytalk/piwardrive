import { describe, it, expect, vi, beforeEach } from 'vitest';
import { purgeOldTiles, enforceCacheLimit, deg2num } from '../src/tileCache.js';

const INDEX_KEY = 'tile-cache-index';

let store;
let cache;

beforeEach(() => {
  store = {};
  global.localStorage = {
    getItem: (k) => store[k] || null,
    setItem: (k, v) => {
      store[k] = v;
    },
    removeItem: (k) => {
      delete store[k];
    },
  };
  cache = { delete: vi.fn() };
  global.caches = { open: async () => cache };
});

describe('deg2num', () => {
  it('converts lat/lon to tile numbers', () => {
    const [x, y] = deg2num(0, 0, 1);
    expect(x).toBe(1);
    expect(y).toBe(1);
  });
});

describe('purgeOldTiles', () => {
  it('deletes outdated tiles', async () => {
    const now = Date.now();
    const idx = {
      '16/1/2': { time: now - 10 * 86400 * 1000, size: 1 },
      '16/3/4': { time: now, size: 1 },
    };
    store[INDEX_KEY] = JSON.stringify(idx);

    await purgeOldTiles(5);

    expect(cache.delete).toHaveBeenCalledWith(
      'https://tile.openstreetmap.org/16/1/2.png'
    );
    const saved = JSON.parse(store[INDEX_KEY]);
    expect(saved).toEqual({ '16/3/4': idx['16/3/4'] });
  });
});

describe('enforceCacheLimit', () => {
  it('removes oldest tiles when over limit', async () => {
    const now = Date.now();
    const idx = {
      '16/1/1': { time: now - 1000, size: 200 * 1024 * 1024 },
      '16/2/2': { time: now, size: 100 * 1024 * 1024 },
    };
    store[INDEX_KEY] = JSON.stringify(idx);

    await enforceCacheLimit(250);

    expect(cache.delete).toHaveBeenCalledWith(
      'https://tile.openstreetmap.org/16/1/1.png'
    );
    const saved = JSON.parse(store[INDEX_KEY]);
    expect(Object.keys(saved)).toEqual(['16/2/2']);
  });
});
