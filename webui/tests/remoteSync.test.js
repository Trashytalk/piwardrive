import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { syncDatabaseToServer } from '../src/remoteSync.js';

vi.useFakeTimers();

describe('remoteSync', () => {
  let origFetch;
  beforeEach(() => { origFetch = global.fetch; });
  afterEach(() => { global.fetch = origFetch; vi.clearAllTimers(); });

  it('retries on failure', async () => {
    const fetchMock = vi.fn()
      .mockRejectedValueOnce(new Error('fail'))
      .mockResolvedValue({ ok: true });
    global.fetch = fetchMock;
    const promise = syncDatabaseToServer('db', 'http://remote', { retries: 1, timeout: 0 });
    await vi.runAllTimersAsync();
    await expect(promise).resolves.toBe(true);
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });

  it('fails after retries exhausted', async () => {
    const fetchMock = vi.fn(() => Promise.reject(new Error('boom')));
    global.fetch = fetchMock;
    const promise = syncDatabaseToServer('db', 'http://remote', { retries: 1, timeout: 0 });
    await vi.runAllTimersAsync();
    await expect(promise).rejects.toThrow('boom');
    expect(fetchMock).toHaveBeenCalledTimes(2);
  });
});
