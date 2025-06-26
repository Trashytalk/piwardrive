import { describe, it, expect, vi, beforeEach } from 'vitest';

// Mock child_process before loading the module under test so that the
// imported functions use the mocked implementation. This avoids errors
// when spying on builtin modules in ESM mode.
vi.mock('child_process', () => {
  const execSync = vi.fn();
  return { execSync, default: { execSync } };
});

import fs from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import { execSync } from 'child_process';
import { rotateLog, runNetworkTest, listUsbDevices } from '../src/diagnostics.js';

beforeEach(() => {
  vi.resetAllMocks();
});

describe('rotateLog', () => {
  it('compresses and rotates', () => {
    const dir = fs.mkdtempSync(join(tmpdir(), 'logs-'));
    const log = join(dir, 'app.log');
    fs.writeFileSync(log, 'first');
    rotateLog(log, 2);
    expect(fs.existsSync(`${log}.1.gz`)).toBe(true);
    fs.writeFileSync(log, 'second');
    rotateLog(log, 2);
    expect(fs.existsSync(`${log}.2.gz`)).toBe(true);
    fs.writeFileSync(log, 'third');
    rotateLog(log, 2);
    expect(fs.existsSync(`${log}.3.gz`)).toBe(false);
  });
});

describe('runNetworkTest', () => {
  it('uses cache on success', () => {
    execSync.mockReturnValue('');
    expect(runNetworkTest('localhost', 30)).toBe(true);
    const calls = execSync.mock.calls.length;
    expect(runNetworkTest('localhost', 30)).toBe(true);
    expect(execSync.mock.calls.length).toBe(calls);
  });

  it('handles failure', () => {
    execSync.mockImplementation(() => {
      throw new Error('fail');
    });
    expect(runNetworkTest('localhost', 0)).toBe(false);
  });
});

describe('listUsbDevices', () => {
  it('returns empty on failure', () => {
    execSync.mockImplementation(() => {
      throw new Error('boom');
    });
    expect(listUsbDevices()).toEqual([]);
  });
});
