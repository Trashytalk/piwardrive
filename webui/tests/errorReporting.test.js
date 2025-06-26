import { describe, it, expect, vi } from 'vitest';
vi.mock('../src/exceptionHandler.js', () => ({ reportError: vi.fn() }));
import { reportError } from '../src/errorReporting.js';
import { reportError as inner } from '../src/exceptionHandler.js';

describe('error reporting', () => {
  it('delegates to exception handler', () => {
    reportError('boom');
    expect(inner).toHaveBeenCalledWith('boom');
  });
});
