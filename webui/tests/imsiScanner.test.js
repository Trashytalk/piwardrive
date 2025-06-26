import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { scanImsis, registerPostProcessor, clearPostProcessors } from '../src/imsiScanner.js';

describe('scanImsis', () => {
  afterEach(() => {
    clearPostProcessors('imsi');
  });

  it('parses output and tags location', () => {
    const execSync = vi.fn(() => '12345,310,260,-50\n67890,311,480,-60');
    const getPosition = vi.fn(() => [1.0, 2.0]);
    const records = scanImsis('dummy', { execSync, getPosition });
    expect(records).toEqual([
      { imsi: '12345', mcc: '310', mnc: '260', rssi: '-50', lat: 1.0, lon: 2.0 },
      { imsi: '67890', mcc: '311', mnc: '480', rssi: '-60', lat: 1.0, lon: 2.0 },
    ]);
  });

  it('applies custom hook', () => {
    const execSync = vi.fn(() => '12345,310,260,-50');
    const getPosition = vi.fn(() => null);
    registerPostProcessor('imsi', recs => recs.map(r => ({ ...r, op: 'test' })));
    const records = scanImsis('dummy', { execSync, getPosition });
    expect(records[0].op).toBe('test');
  });
});
