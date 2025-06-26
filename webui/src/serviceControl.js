export async function controlService(service, action) {
  let password = sessionStorage.getItem('adminPassword') || null;
  const headers = {};
  if (password) headers['X-Admin-Password'] = password;

  let resp;
  try {
    resp = await fetch(`/service/${service}/${action}`, { method: 'POST', headers });
  } catch (e) {
    alert(`Failed to ${action} ${service}`);
    return false;
  }
  if (resp.status === 401) {
    password = window.prompt('Admin password');
    if (!password) return false;
    sessionStorage.setItem('adminPassword', password);
    resp = await fetch(`/service/${service}/${action}`, { method: 'POST', headers: { 'X-Admin-Password': password } });
  }
  if (!resp.ok) {
    alert(`Failed to ${action} ${service}`);
    return false;
  }
  return true;
}
