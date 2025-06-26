import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { syncNewRecords } from '../src/remoteSyncPkg.js';
import * as remoteSync from '../src/remoteSync.js';
import * as persistence from '../src/persistence.js';

describe('remoteSyncPkg', () => {
  beforeEach(() => { localStorage.clear(); });
  afterEach(() => { vi.restoreAllMocks(); });

  it('returns 0 when no new records', async () => {
    vi.spyOn(persistence, 'loadRecentHealth').mockResolvedValue([]);
    const count = await syncNewRecords('db', 'http://x');
    expect(count).toBe(0);
  });

  it('syncs new records and updates state', async () => {
    vi.spyOn(persistence, 'loadRecentHealth').mockResolvedValue([
      { t: 1 }, { t: 2 }, { t: 3 }
    ]);
    const syncSpy = vi.spyOn(remoteSync, 'syncDatabaseToServer').mockResolvedValue(true);
    localStorage.setItem('syncState', '1');
    const count = await syncNewRecords('db', 'http://x', { stateKey: 'syncState' });
    expect(count).toBe(2);
    expect(syncSpy).toHaveBeenCalledWith('db', 'http://x', { retries: 3, rowRange: [2, 3] });
    expect(localStorage.getItem('syncState')).toBe('3');
  });
});
