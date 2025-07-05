// Simple persistence utilities mimicking the Python persistence module
// Data is stored in localStorage under various keys

export async function saveHealthRecord(rec) {
  const list = JSON.parse(localStorage.getItem('healthRecords') || '[]');
  list.push(rec);
  localStorage.setItem('healthRecords', JSON.stringify(list));
}

export async function loadRecentHealth(n) {
  const list = JSON.parse(localStorage.getItem('healthRecords') || '[]');
  return list.slice(-n);
}

export async function saveAppState(state) {
  localStorage.setItem('appState', JSON.stringify(state));
}

export async function loadAppState() {
  const data = localStorage.getItem('appState');
  return data ? JSON.parse(data) : null;
}

export async function saveDashboardSettings(settings) {
  localStorage.setItem('dashboardSettings', JSON.stringify(settings));
}

export async function loadDashboardSettings() {
  const data = localStorage.getItem('dashboardSettings');
  return data ? JSON.parse(data) : { layout: [], widgets: [] };
}

export async function purgeOldHealth(days) {
  const cutoff = Date.now() - days * 24 * 60 * 60 * 1000;
  const list = JSON.parse(localStorage.getItem('healthRecords') || '[]');
  const filtered = list.filter(
    (r) => new Date(r.timestamp).getTime() >= cutoff
  );
  localStorage.setItem('healthRecords', JSON.stringify(filtered));
  return filtered.length;
}
