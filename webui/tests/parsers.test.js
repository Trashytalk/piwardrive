import { describe, it, expect } from 'vitest';
import { parseImsiOutput, parseBandOutput } from '../src/cellularParsers.js';

describe('parseImsiOutput', () => {
  it('parses CSV lines into records', () => {
    const output = '12345,310,260,-50\n67890,311,480,-60';
    const recs = parseImsiOutput(output);
    expect(recs).toEqual([
      {
        imsi: '12345',
        mcc: '310',
        mnc: '260',
        rssi: '-50',
        lat: null,
        lon: null,
      },
      {
        imsi: '67890',
        mcc: '311',
        mnc: '480',
        rssi: '-60',
        lat: null,
        lon: null,
      },
    ]);
  });
});

describe('parseBandOutput', () => {
  it('parses CSV lines into records', () => {
    const output = 'LTE,100,-60\n5G,200,-70';
    const recs = parseBandOutput(output);
    expect(recs).toEqual([
      { band: 'LTE', channel: '100', rssi: '-60' },
      { band: '5G', channel: '200', rssi: '-70' },
    ]);
  });
});
