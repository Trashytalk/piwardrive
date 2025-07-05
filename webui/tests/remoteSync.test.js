import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { syncDatabaseToServer } from '../src/remoteSync.js';

let origFetch;

describe('syncDatabaseToServer', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    origFetch = global.fetch;
  });
  afterEach(() => {
    vi.useRealTimers();
    global.fetch = origFetch;
  });

  it('retries on error', async () => {
    const fetchMock = vi
      .fn()
      .mockRejectedValueOnce(new Error('fail'))
      .mockResolvedValueOnce({ ok: true });
    global.fetch = fetchMock;
    const p = syncDatabaseToServer('db', 'http://remote', {
      retries: 1,
      timeout: 0,
    });
    await vi.runAllTimersAsync();
    const result = await p;
    expect(result).toBe(true);
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it('throws on failure', async () => {
    global.fetch = vi.fn(() => Promise.resolve({ ok: false }));
    await expect(
      syncDatabaseToServer('db', 'http://remote', { retries: 0, timeout: 0 })
    ).rejects.toThrow();
  });
});
