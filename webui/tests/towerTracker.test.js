import { describe, it, expect } from 'vitest';
import { TowerTracker } from '../src/towerTracker.js';

describe('TowerTracker', () => {
  it('updates and queries towers', async () => {
    const tr = new TowerTracker();
    await tr.updateTower('id1', 1.0, 2.0, 100);
    const rec = await tr.getTower('id1');
    expect(rec.lat).toBe(1.0);
    const all = await tr.allTowers();
    expect(all.length).toBe(1);
  });

  it('logs wifi and bluetooth', async () => {
    const tr = new TowerTracker();
    await tr.logWifi('AA', 'Test', 1, 2, 50);
    await tr.logBluetooth('11', 'Phone', 3, 4, 60);
    const wifi = await tr.wifiHistory('AA');
    const bt = await tr.bluetoothHistory('11');
    expect(wifi[0].ssid).toBe('Test');
    expect(bt[0].name).toBe('Phone');
  });

  it('async logging and retrieval', async () => {
    const tr = new TowerTracker();
    await tr.logWifi('DE:AD:BE', 'Net', undefined, undefined, 50);
    await tr.logBluetooth('AA:BB:CC', 'Headset', undefined, undefined, 60);
    const wifi = await tr.wifiHistory('DE:AD:BE');
    const bt = await tr.bluetoothHistory('AA:BB:CC');
    expect(wifi[0].timestamp).toBe(50);
    expect(bt[0].timestamp).toBe(60);
  });
});
