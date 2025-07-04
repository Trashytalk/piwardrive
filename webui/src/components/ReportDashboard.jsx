import { useEffect, useState } from 'react';

export default function ReportDashboard() {
  const [reports, setReports] = useState([]);
  const [query, setQuery] = useState('');
  const [email, setEmail] = useState('');

  useEffect(() => {
    fetch('/reports/list')
      .then((r) => r.json())
      .then(setReports)
      .catch(() => setReports([]));
  }, []);

  const filtered = reports.filter((r) =>
    r.name.toLowerCase().includes(query.toLowerCase())
  );

  const send = async (id) => {
    await fetch('/reports/email', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, to: email }),
    });
  };

  return (
    <div>
      <h3>Report Dashboard</h3>
      <input
        placeholder="Search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <input
        type="email"
        placeholder="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <ul>
        {filtered.map((r) => (
          <li key={r.id}>
            {r.name} ({r.views || 0}) <a href={r.url}>Open</a>{' '}
            <button onClick={() => send(r.id)}>Share</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
