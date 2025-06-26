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
});
