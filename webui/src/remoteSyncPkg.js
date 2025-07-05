// Additional helper wrapping remoteSync for incremental record syncing
import { syncDatabaseToServer } from './remoteSync.js';
import { loadRecentHealth } from './persistence.js';

export async function syncNewRecords(
  dbPath,
  url,
  { stateKey = 'syncState', retries = 3 } = {}
) {
  const lastSynced = parseInt(localStorage.getItem(stateKey) || '0', 10);
  const records = await loadRecentHealth(Infinity);
  const newRecords = records.slice(lastSynced);
  if (!newRecords.length) return 0;
  await syncDatabaseToServer(dbPath, url, {
    retries,
    rowRange: [lastSynced + 1, records.length],
  });
  localStorage.setItem(stateKey, String(records.length));
  return newRecords.length;
}
