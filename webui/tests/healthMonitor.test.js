import { describe, it, expect, vi } from 'vitest';
import { HealthMonitor } from '../src/healthMonitor.js';
import { PollScheduler } from '../src/scheduler.js';

describe('HealthMonitor', () => {
  it('schedules poll', async () => {
    vi.useFakeTimers();
    const scheduler = new PollScheduler();
    const collector = { collect: vi.fn().mockResolvedValue({ ok: true }) };
    new HealthMonitor(scheduler, 1, collector);
    await vi.runOnlyPendingTimersAsync();
    expect(collector.collect).toHaveBeenCalled();
    scheduler.cancelAll();
    vi.useRealTimers();
  });
});
