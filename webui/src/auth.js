export async function ensureAuth() {
  let token = localStorage.getItem('token');
  if (token) return token;
  const username = prompt('Username:', 'admin');
  const password = prompt('Password:');
  if (!username || !password) return null;
  const params = new URLSearchParams();
  params.append('username', username);
  params.append('password', password);
  const resp = await fetch('/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params.toString(),
  });
  if (resp.ok) {
    const data = await resp.json();
    token = data.access_token;
    localStorage.setItem('token', token);
    return token;
  }
  return null;
}

const realFetch = window.fetch.bind(window);
window.fetch = async (input, init = {}) => {
  const token = localStorage.getItem('token');
  if (token) {
    init.headers = {
      ...(init.headers || {}),
      Authorization: `Bearer ${token}`,
    };
  }
  return realFetch(input, init);
};

ensureAuth();
