import { useEffect, useState } from 'react';
import { reportError } from '../exceptionHandler.js';

function analyzeEvents(list) {
  let crowd = 0;
  let emergency = 0;
  let special = 0;
  list.forEach((e) => {
    if (e.crowd > 50) crowd += 1;
    if (e.type === 'emergency') emergency += 1;
    if (e.special) special += 1;
  });
  return { crowd, emergency, special };
}

export default function EventDetector() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const localResp = await fetch('/events');
        const localData = await localResp.json();
        const calResp = await fetch(
          'https://calendarific.com/api/v2/holidays?api_key=demo&country=US&year=2024'
        );
        const calData = await calResp.json();
        const calEvents = calData.response?.holidays || [];
        const combined = [
          ...(localData.list || []),
          ...calEvents.map((h) => ({ special: true })),
        ];
        setStats(analyzeEvents(combined));
      } catch (e) {
        reportError(e);
        setStats(null);
      }
    };
    load();
  }, []);

  if (!stats) return <div>Events: N/A</div>;
  return (
    <div>
      Crowd:{stats.crowd} Emergency:{stats.emergency} Special:{stats.special}
    </div>
  );
}
