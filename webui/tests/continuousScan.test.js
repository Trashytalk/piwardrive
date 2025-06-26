import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { scanOnce, runContinuousScan } from '../src/continuousScan.js';

vi.useFakeTimers();

describe('continuous scanning', () => {
  let origFetch;
  beforeEach(() => { origFetch = global.fetch; });
  afterEach(() => {
    global.fetch = origFetch;
    vi.clearAllTimers();
  });

  it('scanOnce returns wifi and bluetooth data', async () => {
    global.fetch = vi.fn(url =>
      Promise.resolve({ json: () => Promise.resolve(url.includes('wifi') ? [{ ssid: 'x' }] : [{ address: 'a' }]) })
    );
    const result = await scanOnce();
    expect(result.wifi[0].ssid).toBe('x');
    expect(result.bluetooth[0].address).toBe('a');
  });

  it('runContinuousScan performs given iterations', async () => {
    global.fetch = vi.fn(() => Promise.resolve({ json: () => Promise.resolve([]) }));
    let count = 0;
    runContinuousScan({ interval: 0, iterations: 3, onResult: () => { count += 1; } });
    // first run executes immediately
    await Promise.resolve();
    // subsequent runs are scheduled with timers
    await vi.runOnlyPendingTimersAsync();
    await Promise.resolve();
    await vi.runOnlyPendingTimersAsync();
    await Promise.resolve();
    expect(count).toBe(3);
  });
});
