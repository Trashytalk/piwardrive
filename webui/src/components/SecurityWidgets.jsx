import { useEffect, useState } from 'react';

export function SuspiciousActivityWidget() {
  const [items, setItems] = useState([]);
  useEffect(() => {
    const load = () => {
      fetch('/security/suspicious?limit=5')
        .then((r) => r.json())
        .then(setItems)
        .catch(() => setItems([]));
    };
    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, []);
  return (
    <div>
      <div>Suspicious Activity:</div>
      <ul>
        {items.map((i) => (
          <li key={i.id}>{i.activity_type}</li>
        ))}
      </ul>
    </div>
  );
}

export function AlertSummaryWidget() {
  const [count, setCount] = useState(0);
  useEffect(() => {
    const load = () => {
      fetch('/widget-metrics')
        .then((r) => r.json())
        .then((d) => setCount(d.suspicious_activity_count ?? 0))
        .catch(() => setCount(0));
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);
  return <div>Alerts: {count}</div>;
}

export function ThreatMapWidget() {
  const [img, setImg] = useState(null);
  useEffect(() => {
    const load = () => {
      fetch('/security/threat-map')
        .then((r) => r.blob())
        .then((b) => setImg(URL.createObjectURL(b)))
        .catch(() => setImg(null));
    };
    load();
    const id = setInterval(load, 60000);
    return () => clearInterval(id);
  }, []);
  return img ? <img src={img} alt="Threat map" /> : <div>Threat Map: N/A</div>;
}

export function SecurityScoreWidget() {
  const [score, setScore] = useState(null);
  useEffect(() => {
    const load = () => {
      fetch('/analytics/daily-stats?limit=1')
        .then((r) => r.json())
        .then((d) => {
          const rec = d[0];
          setScore(rec ? rec.suspicious_score : null);
        })
        .catch(() => setScore(null));
    };
    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, []);
  return <div>Security Score: {score ?? 'N/A'}</div>;
}
