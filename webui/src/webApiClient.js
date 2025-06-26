export async function getGps() {
  const resp = await fetch('/api/gps');
  return resp.json();
}

export async function getAps() {
  const resp = await fetch('/api/aps');
  return resp.json();
}

export async function getBt() {
  const resp = await fetch('/api/bt');
  return resp.json();
}

export async function toggleKismet(state) {
  await fetch(`/api/kismet/toggle?state=${encodeURIComponent(state)}`, { method: 'POST' });
}
