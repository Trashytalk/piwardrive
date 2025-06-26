import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { controlService } from '../src/serviceControl.js';

let origFetch;
let origPrompt;
let origSession;

describe('controlService', () => {
  beforeEach(() => {
    origFetch = global.fetch;
    origPrompt = window.prompt;
    origSession = global.sessionStorage;
    global.fetch = vi.fn(() => Promise.resolve({ ok: true }));
    window.prompt = vi.fn(() => 'pw');
    const store = {};
    global.sessionStorage = {
      getItem: key => store[key] || null,
      setItem: (key, val) => { store[key] = val; }
    };
  });

  afterEach(() => {
    global.fetch = origFetch;
    window.prompt = origPrompt;
    global.sessionStorage = origSession;
  });

  it('sends simple request', async () => {
    const ok = await controlService('kismet', 'start');
    expect(ok).toBe(true);
    expect(global.fetch).toHaveBeenCalledWith('/service/kismet/start', { method: 'POST', headers: {} });
  });

  it('retries on 401 with password', async () => {
    global.fetch
      .mockResolvedValueOnce({ status: 401 })
      .mockResolvedValueOnce({ ok: true });
    const ok = await controlService('kismet', 'stop');
    expect(ok).toBe(true);
    expect(window.prompt).toHaveBeenCalled();
    expect(global.fetch.mock.calls[1][1].headers['X-Admin-Password']).toBe('pw');
  });
});
