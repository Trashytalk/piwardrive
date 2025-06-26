import { describe, it, expect, vi } from 'vitest';
import fs from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';
import * as childProcess from 'child_process';
import { rotateLog, runNetworkTest, listUsbDevices } from '../src/diagnostics.js';

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
    const spy = vi.spyOn(childProcess, 'execSync').mockReturnValue('');
    expect(runNetworkTest('localhost', 30)).toBe(true);
    const calls = spy.mock.calls.length;
    expect(runNetworkTest('localhost', 30)).toBe(true);
    expect(spy.mock.calls.length).toBe(calls);
    spy.mockRestore();
  });

  it('handles failure', () => {
    const spy = vi.spyOn(childProcess, 'execSync').mockImplementation(() => {
      throw new Error('fail');
    });
    expect(runNetworkTest('localhost', 0)).toBe(false);
    spy.mockRestore();
  });
});

describe('listUsbDevices', () => {
  it('returns empty on failure', () => {
    const spy = vi.spyOn(childProcess, 'execSync').mockImplementation(() => {
      throw new Error('boom');
    });
    expect(listUsbDevices()).toEqual([]);
    spy.mockRestore();
  });
});
