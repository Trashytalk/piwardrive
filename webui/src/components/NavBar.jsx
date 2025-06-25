import { Link } from 'react-router-dom';

export default function NavBar() {
  return (
    <nav style={{ marginBottom: '1em' }}>
      <Link to="/" style={{ marginRight: '1em' }}>Map</Link>
      <Link to="/console" style={{ marginRight: '1em' }}>Console</Link>
      <Link to="/settings">Settings</Link>
    </nav>
  );
}
