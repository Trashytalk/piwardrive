export async function fetchServiceStatuses(services) {
  const entries = await Promise.all(
    services.map(svc =>
      fetch(`/service/${svc}`)
        .then(r => r.json())
        .then(d => [svc, !!d.active])
    )
  );
  return Object.fromEntries(entries);
}

export async function syncHealthRecords(limit = 100) {
  const resp = await fetch(`/sync?limit=${limit}`, { method: 'POST' });
  if (!resp.ok) throw new Error('sync failed');
  return await resp.json();
}

export async function fetchSigintData(type) {
  const resp = await fetch(`/export/${type}?fmt=json`);
  return await resp.json();
}
