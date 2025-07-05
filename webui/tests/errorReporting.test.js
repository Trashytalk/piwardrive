import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

vi.mock('../src/logconfig.js', () => ({
  setupLogging: vi.fn(() => ({ error: vi.fn() })),
}));

import { setupLogging } from '../src/logconfig.js';

let origAlert;

beforeEach(() => {
  origAlert = global.alert;
  vi.resetModules();
});

afterEach(() => {
  global.alert = origAlert;
});

describe('reportError', () => {
  it('logs the message', async () => {
    const log = { error: vi.fn() };
    setupLogging.mockReturnValue(log);
    const mod = await import('../src/errorReporting.js');
    mod.reportError('boom');
    expect(log.error).toHaveBeenCalledWith('boom');
  });

  it('alerts when requested', async () => {
    const log = { error: vi.fn() };
    setupLogging.mockReturnValue(log);
    const alertSpy = vi.fn();
    global.alert = alertSpy;
    const mod = await import('../src/errorReporting.js');
    mod.reportError('boom', true);
    expect(alertSpy).toHaveBeenCalledWith('boom');
    expect(log.error).toHaveBeenCalledWith('boom');
  });
});
