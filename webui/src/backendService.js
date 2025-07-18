import { enhancedFetch } from './utils/networkErrorHandler.js';

export function authHeaders() {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function login(username, password) {
  const data = new URLSearchParams();
  data.append('username', username);
  data.append('password', password);
  
  try {
    const resp = await enhancedFetch('/auth/login', { method: 'POST', body: data });
    const out = await resp.json();
    
    if (resp.ok) {
      localStorage.setItem('token', out.access_token);
      localStorage.setItem('role', out.role);
    }
    return out;
  } catch (error) {
    throw new Error(`Login failed: ${error.message}`);
  }
}

export async function logout() {
  try {
    await enhancedFetch('/auth/logout', { method: 'POST', headers: authHeaders() });
  } catch (error) {
    console.warn('Logout request failed:', error);
  } finally {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
  }
}

export async function fetchServiceStatuses(services) {
  try {
    const entries = await Promise.all(
      services.map(async (svc) => {
        try {
          const resp = await enhancedFetch(`/service/${svc}`, { headers: authHeaders() });
          const data = await resp.json();
          return [svc, !!data.active];
        } catch (error) {
          console.warn(`Failed to fetch status for service ${svc}:`, error);
          return [svc, false];
        }
      })
    );
    return Object.fromEntries(entries);
  } catch (error) {
    throw new Error(`Failed to fetch service statuses: ${error.message}`);
  }
}

export async function syncHealthRecords(limit = 100) {
  try {
    const resp = await enhancedFetch(`/sync?limit=${limit}`, {
      method: 'POST',
      headers: authHeaders(),
    });
    
    if (!resp.ok) {
      throw new Error(`Sync failed with status ${resp.status}`);
    }
    
    return await resp.json();
  } catch (error) {
    throw new Error(`Health record sync failed: ${error.message}`);
  }
}

export async function fetchSigintData(type) {
  try {
    const resp = await enhancedFetch(`/export/${type}?fmt=json`, {
      headers: authHeaders(),
    });
    
    if (!resp.ok) {
      throw new Error(`SIGINT data fetch failed with status ${resp.status}`);
    }
    
    return await resp.json();
  } catch (error) {
    throw new Error(`Failed to fetch SIGINT data: ${error.message}`);
  }
}

export async function fetchStatus(limit = 5) {
  try {
    const resp = await enhancedFetch(`/status?limit=${limit}`, {
      headers: authHeaders(),
    });
    
    if (!resp.ok) {
      throw new Error(`Status fetch failed with status ${resp.status}`);
    }
    
    return await resp.json();
  } catch (error) {
    throw new Error(`Failed to fetch status: ${error.message}`);
  }
}
