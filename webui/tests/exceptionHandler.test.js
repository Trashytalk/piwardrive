import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

vi.mock('../src/logconfig.js', () => ({
  setupLogging: vi.fn(() => ({ error: vi.fn() })),
}));

import { setupLogging } from '../src/logconfig.js';

let origOnError;

beforeEach(() => {
  origOnError = window.onerror;
  vi.resetModules();
});

afterEach(() => {
  window.onerror = origOnError;
});

describe('exception handler', () => {
  it('logs reported errors', async () => {
    const log = { error: vi.fn() };
    setupLogging.mockReturnValue(log);
    const mod = await import('../src/exceptionHandler.js');
    mod.reportError(new Error('boom'));
    expect(log.error).toHaveBeenCalledWith('boom');
  });

  it('installs only once', async () => {
    const add = vi.spyOn(window, 'addEventListener');
    const mod = await import('../src/exceptionHandler.js');
    mod.install();
    const first = window.onerror;
    mod.install();
    expect(window.onerror).toBe(first);
    expect(add).toHaveBeenCalledTimes(1);
    add.mockRestore();
  });
});
