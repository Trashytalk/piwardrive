import { useEffect, useState } from 'react';

export default function MobileAlerts() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    fetch('/alerts')
      .then((r) => r.json())
      .then(setAlerts)
      .catch(() => setAlerts([]));
  }, []);

  useEffect(() => {
    if ('Notification' in window && Notification.permission !== 'denied') {
      Notification.requestPermission();
    }
  }, []);

  useEffect(() => {
    alerts.forEach((a) => {
      if (
        a.push &&
        'Notification' in window &&
        Notification.permission === 'granted'
      ) {
        // eslint-disable-next-line no-new
        new Notification(a.title, { body: a.message });
      }
    });
  }, [alerts]);

  const dismiss = (idx) => {
    setAlerts((a) => a.filter((_, i) => i !== idx));
  };

  const handleTouch = (idx) => (e) => {
    const start = e.changedTouches[0].clientX;
    const onEnd = (ev) => {
      const dist = ev.changedTouches[0].clientX - start;
      if (Math.abs(dist) > 50) dismiss(idx);
      e.target.removeEventListener('touchend', onEnd);
    };
    e.target.addEventListener('touchend', onEnd);
  };

  return (
    <div>
      {alerts.map((a, idx) => (
        <div
          key={idx}
          onTouchStart={handleTouch(idx)}
          style={{
            padding: '0.5em',
            marginBottom: '0.5em',
            background: a.emergency ? '#b00020' : '#eee',
            color: a.emergency ? '#fff' : '#000',
          }}
        >
          <strong>{a.title}</strong>
          <div>{a.message}</div>
        </div>
      ))}
    </div>
  );
}
