import { describe, it, expect } from 'vitest';
import { findSuspiciousAps } from '../src/networkAnalytics.js';

describe('findSuspiciousAps', () => {
  it('returns empty for empty input', () => {
    expect(findSuspiciousAps([])).toEqual([]);
  });

  it('flags open networks', () => {
    const rec = { bssid: 'AA:BB:CC:DD:EE:FF', ssid: 'OpenNet', encryption: 'open' };
    expect(findSuspiciousAps([rec])).toEqual([rec]);
  });

  it('flags only second of duplicate BSSID with different SSIDs', () => {
    const r1 = { bssid: '11:22:33:44:55:66', ssid: 'Net1', encryption: 'wpa2' };
    const r2 = { bssid: '11:22:33:44:55:66', ssid: 'Net2', encryption: 'wpa2' };
    expect(findSuspiciousAps([r1, r2])).toEqual([r2]);
  });

  it('handles missing fields gracefully', () => {
    const r1 = { ssid: 'Net', encryption: 'open' };
    const r2 = { bssid: 'CC:DD:EE:FF:00:11' };
    expect(findSuspiciousAps([r1, r2])).toEqual([r1]);
  });

  it('combines open network and duplicates', () => {
    const r1 = { bssid: 'AA:AA:AA:AA:AA:AA', ssid: 'Open1', encryption: 'open' };
    const r2 = { bssid: 'AA:AA:AA:AA:AA:AA', ssid: 'Secure', encryption: 'wpa2' };
    const r3 = { bssid: 'BB:BB:BB:BB:BB:BB', ssid: 'Other', encryption: 'wpa2' };
    expect(findSuspiciousAps([r1, r2, r3])).toEqual([r1, r2]);
  });
});
