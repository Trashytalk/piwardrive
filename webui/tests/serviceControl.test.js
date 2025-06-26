import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { controlService } from '../src/serviceControl.js';

vi.useFakeTimers();

describe('controlService', () => {
  let origFetch;
  let origAlert;
  let origPrompt;
  let origSession;
  beforeEach(() => {
    origFetch = global.fetch;
    origAlert = global.alert;
    origPrompt = global.window ? global.window.prompt : undefined;
    origSession = global.sessionStorage;
    global.sessionStorage = {
      store: {},
      getItem: vi.fn(key => this.store[key] || null),
      setItem: vi.fn(function (key, val) { this.store[key] = val; }),
    };
  });
  afterEach(() => {
    global.fetch = origFetch;
    global.alert = origAlert;
    if (global.window) global.window.prompt = origPrompt;
    global.sessionStorage = origSession;
  });

  it('shows alert on network error', async () => {
    global.fetch = vi.fn(() => Promise.reject(new Error('fail')));
    global.alert = vi.fn();
    const ok = await controlService('svc', 'start');
    expect(ok).toBe(false);
    expect(global.alert).toHaveBeenCalled();
  });

  it('prompts for password on unauthorized', async () => {
    global.fetch = vi
      .fn()
      .mockResolvedValueOnce({ status: 401, ok: false })
      .mockResolvedValueOnce({ ok: true, status: 200 });
    if (!global.window) global.window = {};
    global.window.prompt = vi.fn(() => 'pw');
    const ok = await controlService('svc', 'start');
    expect(global.window.prompt).toHaveBeenCalled();
    expect(global.fetch).toHaveBeenCalledTimes(2);
    expect(global.sessionStorage.setItem).toHaveBeenCalledWith('adminPassword', 'pw');
    expect(ok).toBe(true);
  });
});
