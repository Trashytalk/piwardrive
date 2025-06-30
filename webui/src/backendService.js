export function authHeaders() {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function login(username, password) {
  const data = new URLSearchParams();
  data.append('username', username);
  data.append('password', password);
  const resp = await fetch('/auth/login', { method: 'POST', body: data });
  const out = await resp.json();
  if (resp.ok) {
    localStorage.setItem('token', out.access_token);
    localStorage.setItem('role', out.role);
  }
  return out;
}

export function logout() {
  fetch('/auth/logout', { method: 'POST', headers: authHeaders() }).finally(
    () => {
      localStorage.removeItem('token');
      localStorage.removeItem('role');
    }
  );
}

export async function fetchServiceStatuses(services) {
  const entries = await Promise.all(
    services.map((svc) =>
      fetch(`/service/${svc}`, { headers: authHeaders() })
        .then((r) => r.json())
        .then((d) => [svc, !!d.active])
    )
  );
  return Object.fromEntries(entries);
}

export async function syncHealthRecords(limit = 100) {
  const resp = await fetch(`/sync?limit=${limit}`, {
    method: 'POST',
    headers: authHeaders(),
  });
  if (!resp.ok) throw new Error('sync failed');
  return await resp.json();
}

export async function fetchSigintData(type) {
  const resp = await fetch(`/export/${type}?fmt=json`, {
    headers: authHeaders(),
  });
  return await resp.json();
}

export async function fetchStatus(limit = 5) {
  const resp = await fetch(`/status?limit=${limit}`, {
    headers: authHeaders(),
  });
  return await resp.json();
}
