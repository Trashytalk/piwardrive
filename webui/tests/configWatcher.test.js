import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { watchConfig } from '../src/configWatcher.js';

vi.useFakeTimers();

describe('watchConfig', () => {
  let origFetch;
  beforeEach(() => { origFetch = global.fetch; });
  afterEach(() => {
    global.fetch = origFetch;
    vi.clearAllTimers();
  });

  it('invokes callback when config changes', async () => {
    let data = { a: 1 };
    global.fetch = vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve(data) }));
    const calls = [];
    const stop = watchConfig('/config', cfg => calls.push(cfg), 1000);
    // first fetch happens immediately
    await Promise.resolve();
    expect(calls.length).toBe(1);
    // change data and advance timer
    data = { a: 2 };
    vi.advanceTimersByTime(1000);
    await Promise.resolve();
    expect(calls.length).toBe(2);
    stop();
  });
});
