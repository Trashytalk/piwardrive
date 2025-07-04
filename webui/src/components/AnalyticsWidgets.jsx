import { useEffect, useState } from 'react';

export function DetectionRateWidget() {
  const [rate, setRate] = useState(null);
  useEffect(() => {
    const load = () => {
      fetch('/analytics/daily-stats?limit=1')
        .then((r) => r.json())
        .then((d) => {
          const rec = d[0];
          setRate(rec ? rec.total_detections : null);
        })
        .catch(() => setRate(null));
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);
  return <div>Detection Rate: {rate ?? 'N/A'}</div>;
}

export function ThreatLevelWidget() {
  const [level, setLevel] = useState('N/A');
  useEffect(() => {
    const load = () => {
      fetch('/security/suspicious?limit=1')
        .then((r) => r.json())
        .then((d) => {
          setLevel(d.length > 0 ? 'High' : 'Low');
        })
        .catch(() => setLevel('N/A'));
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);
  return <div>Threat Level: {level}</div>;
}

export function NetworkDensityWidget() {
  const [count, setCount] = useState(null);
  useEffect(() => {
    const load = () => {
      fetch('/widget-metrics')
        .then((r) => r.json())
        .then((d) => setCount(d.bssid_count))
        .catch(() => setCount(null));
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);
  return <div>Network Density: {count ?? 'N/A'}</div>;
}

export function DeviceClassificationWidget() {
  const [info, setInfo] = useState(null);
  useEffect(() => {
    const load = () => {
      fetch('/analytics/networks?limit=1')
        .then((r) => r.json())
        .then((d) => setInfo(d[0]))
        .catch(() => setInfo(null));
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);
  return (
    <div>Device Types: {info ? info.suspicious_score ?? 'N/A' : 'N/A'}</div>
  );
}
