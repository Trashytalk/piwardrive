import { describe, it, expect } from 'vitest';
import { serviceSync } from '../src/serviceSync.js';

// use actual script but override helpers

describe('serviceSync helper', () => {
  it('runs script with options', async () => {
    let uploaded = null;
    const res = await serviceSync(
      { db: 'file.db', url: 'http://x', services: ['a', 'b'] },
      {
        uploadDb: async (db, url) => { uploaded = { db, url }; },
        checkStatus: () => true,
      },
    );
    expect(uploaded).toEqual({ db: 'file.db', url: 'http://x' });
    expect(res).toEqual({ synced: true, status: { a: true, b: true } });
  });

  it('throws when db or url missing', async () => {
    await expect(serviceSync({ db: 'only.db' })).rejects.toBeInstanceOf(Error);
  });
});
