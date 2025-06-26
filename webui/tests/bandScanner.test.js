import { describe, it, expect, vi } from 'vitest';
import { parseBandOutput, scanBands, asyncScanBands } from '../src/bandScanner.js';
import * as childProcess from 'child_process';

vi.mock('child_process');

describe('parseBandOutput', () => {
  it('parses output', () => {
    const output = 'LTE,100,-60\n5G,200,-70';
    const records = parseBandOutput(output);
    expect(records).toEqual([
      { band: 'LTE', channel: '100', rssi: '-60' },
      { band: '5G', channel: '200', rssi: '-70' }
    ]);
  });
});

describe('scanBands', () => {
  it('passes timeout', () => {
    const spy = vi.spyOn(childProcess, 'execFileSync').mockReturnValue('');
    scanBands('dummy', 5);
    expect(spy).toHaveBeenCalledWith('dummy', expect.objectContaining({ timeout: 5000, encoding: 'utf-8' }));
    spy.mockRestore();
  });
});

describe('asyncScanBands', () => {
  it('parses records', async () => {
    vi.spyOn(childProcess, 'execFile').mockImplementation((cmd, opts, cb) => {
      cb(null, 'LTE,100,-60\n5G,200,-70');
    });
    const records = await asyncScanBands('dummy');
    expect(records).toEqual([
      { band: 'LTE', channel: '100', rssi: '-60' },
      { band: '5G', channel: '200', rssi: '-70' }
    ]);
  });
});
