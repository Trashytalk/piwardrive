import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

vi.mock('../src/ouiRegistry.js', () => ({
  cachedLookupVendor: vi.fn(
    (bssid) =>
      ({ 'AA:BB:CC': 'VendorA', '11:22:33': 'VendorB' })[bssid.slice(0, 8)] ||
      null
  ),
}));
vi.mock('../src/orientationSensors.js', () => ({
  getHeading: vi.fn(() => 45.0),
}));

import { parseIwlist } from '../src/wifiScanner.js';

const sample = `Cell 01 - Address: AA:BB:CC:DD:EE:FF
          ESSID:"TestNet"
          Frequency:2.437 GHz (Channel 6)
          Encryption key:on
          IE: WPA Version 1
          Quality=70/70  Signal level=-40 dBm
Cell 02 - Address: 11:22:33:44:55:66
          ESSID:"OpenNet"
          Frequency:2.422 GHz (Channel 3)
          Encryption key:off
          Quality=20/70  Signal level=-90 dBm`;

describe('parseIwlist', () => {
  it('parses vendor and heading', () => {
    const out = parseIwlist(sample);
    expect(out[0].vendor).toBe('VendorA');
    expect(out[1].vendor).toBe('VendorB');
    expect(out[0].channel).toBe('6');
    expect(out[0].encryption).toBe('on WPA Version 1');
    expect(out[0].heading).toBe(45.0);
  });

  it('handles missing vendor', () => {
    const data = parseIwlist(
      `Cell 01 - Address: AA:BB:CC:DD:EE:FF\n          ESSID:\"TestNet\"\n          Frequency:2.437 GHz (Channel 6)\n          Encryption key:on`
    );
    expect(data[0].vendor).toBe('VendorA');
    expect(data[0].heading).toBe(45.0);
  });
});
