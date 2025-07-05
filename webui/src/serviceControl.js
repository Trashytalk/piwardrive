import { reportError } from './exceptionHandler.js';

export async function controlService(service, action) {
  let password = sessionStorage.getItem('adminPassword') || null;
  const headers = {};
  if (password) headers['X-Admin-Password'] = password;

  let resp;
  try {
    resp = await fetch(`/service/${service}/${action}`, {
      method: 'POST',
      headers,
    });
  } catch (e) {
    reportError(e, true);
    return false;
  }
  if (resp.status === 401) {
    password = window.prompt('Admin password');
    if (!password) return false;
    sessionStorage.setItem('adminPassword', password);
    resp = await fetch(`/service/${service}/${action}`, {
      method: 'POST',
      headers: { 'X-Admin-Password': password },
    });
  }
  if (!resp.ok) {
    reportError(new Error(`Failed to ${action} ${service}`), true);
    return false;
  }
  return true;
}
