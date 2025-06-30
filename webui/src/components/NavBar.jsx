import { Link } from 'react-router-dom';
import { useState } from 'react';
import LoginForm from './LoginForm.jsx';

function getToken() {
  return localStorage.getItem('token');
}

export default function NavBar() {
  const [token, setToken] = useState(getToken());

  const logout = () => {
    fetch('/auth/logout', { method: 'POST' }).finally(() => {
      localStorage.removeItem('token');
      localStorage.removeItem('role');
      setToken(null);
    });
  };

  return (
    <nav style={{ marginBottom: '1em' }}>
      <Link to="/" style={{ marginRight: '1em' }}>
        Map
      </Link>
      <Link to="/console" style={{ marginRight: '1em' }}>
        Console
      </Link>
      <Link to="/settings" style={{ marginRight: '1em' }}>
        Settings
      </Link>
      {token ? (
        <button onClick={logout}>Logout</button>
      ) : (
        <LoginForm onLogin={() => setToken(getToken())} />
      )}
    </nav>
  );
}
