import { useState } from 'react';

export default function LoginForm({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const submit = (e) => {
    e.preventDefault();
    const data = new URLSearchParams();
    data.append('username', username);
    data.append('password', password);
    fetch('/auth/login', { method: 'POST', body: data })
      .then((r) => r.json())
      .then((d) => {
        localStorage.setItem('token', d.access_token);
        localStorage.setItem('role', d.role);
        if (onLogin) onLogin(d.access_token, d.role);
      })
      .catch(() => {});
  };

  return (
    <form onSubmit={submit} style={{ display: 'inline-block' }}>
      <input
        type="text"
        placeholder="User"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Login</button>
    </form>
  );
}
