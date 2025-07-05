import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { PollScheduler, AsyncScheduler } from '../src/scheduler.js';

vi.useFakeTimers();

describe('PollScheduler', () => {
  afterEach(() => {
    vi.clearAllTimers();
  });

  it('accepts async widget', async () => {
    const scheduler = new PollScheduler();
    const widget = { update_interval: 1, update: vi.fn().mockResolvedValue() };
    scheduler.registerWidget(widget, 'w');
    await vi.runOnlyPendingTimersAsync();
    expect(widget.update).toHaveBeenCalled();
    scheduler.cancelAll();
  });

  it('handles async callback', async () => {
    const scheduler = new PollScheduler();
    const cb = vi.fn().mockResolvedValue();
    scheduler.schedule('job', cb, 1);
    await vi.runOnlyPendingTimersAsync();
    expect(cb).toHaveBeenCalled();
    scheduler.cancelAll();
  });

  it('metrics contain jobs', () => {
    const scheduler = new PollScheduler();
    const cb = () => {};
    scheduler.schedule('job', cb, 1);
    const metrics = scheduler.getMetrics();
    expect(metrics.job).toBeDefined();
    scheduler.cancelAll();
  });
});

describe('AsyncScheduler', () => {
  afterEach(() => {
    vi.clearAllTimers();
  });

  it('runs tasks', async () => {
    const scheduler = new AsyncScheduler();
    const cb = vi.fn().mockResolvedValue();
    scheduler.schedule('job', cb, 1);
    await vi.runOnlyPendingTimersAsync();
    expect(cb).toHaveBeenCalled();
    await scheduler.cancelAll();
  });

  it('cancelAll clears metrics', async () => {
    const scheduler = new AsyncScheduler();
    const done = vi.fn().mockResolvedValue();
    scheduler.schedule('job', done, 1);
    await vi.runOnlyPendingTimersAsync();
    await scheduler.cancelAll();
    expect(scheduler.getMetrics()).toEqual({});
  });

  it('metrics contain jobs', async () => {
    const scheduler = new AsyncScheduler();
    const cb = vi.fn().mockResolvedValue();
    scheduler.schedule('job', cb, 1);
    await vi.runOnlyPendingTimersAsync();
    const metrics = scheduler.getMetrics();
    expect(metrics.job).toBeDefined();
    await scheduler.cancelAll();
  });
});
