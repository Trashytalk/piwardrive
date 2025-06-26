import { describe, it, expect, beforeEach } from 'vitest';
import { saveHealthRecord, loadRecentHealth, saveAppState, loadAppState, saveDashboardSettings, loadDashboardSettings, purgeOldHealth } from '../src/persistence.js';

// clear localStorage before each test
beforeEach(() => {
  localStorage.clear();
});

describe('persistence utilities', () => {
  it('saves and loads health record', async () => {
    const rec = { timestamp: 't', cpu_temp: 1.0, cpu_percent: 2.0, memory_percent: 3.0, disk_percent: 4.0 };
    await saveHealthRecord(rec);
    const rows = await loadRecentHealth(1);
    expect(rows.length).toBe(1);
    expect(rows[0].cpu_temp).toBe(1.0);
  });

  it('saves and loads app state', async () => {
    const state = { last_screen: 'Stats', last_start: 'now', first_run: false };
    await saveAppState(state);
    const loaded = await loadAppState();
    expect(loaded).toEqual(state);
  });

  it('saves and loads dashboard settings', async () => {
    const settings = { layout: [{ cls: 'TestWidget', pos: [1, 2] }], widgets: ['TestWidget'] };
    await saveDashboardSettings(settings);
    const loaded = await loadDashboardSettings();
    expect(loaded).toEqual(settings);
  });

  it('purges old health records', async () => {
    const old = { timestamp: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(), cpu_temp: 1, cpu_percent: 1, memory_percent: 1, disk_percent: 1 };
    const newer = { timestamp: new Date().toISOString(), cpu_temp: 2, cpu_percent: 2, memory_percent: 2, disk_percent: 2 };
    await saveHealthRecord(old);
    await saveHealthRecord(newer);
    const remaining = await purgeOldHealth(1);
    expect(remaining).toBe(1);
    const rows = await loadRecentHealth(10);
    expect(rows.length).toBe(1);
    expect(rows[0].timestamp).toBe(newer.timestamp);
  });
});
