import { useEffect, useState } from 'react';
import { reportError } from '../exceptionHandler.js';

function seasonForMonth(m) {
  if (m < 2 || m === 11) return 'Winter';
  if (m < 5) return 'Spring';
  if (m < 8) return 'Summer';
  return 'Autumn';
}

export default function EnvironmentalAnalytics() {
  const [analysis, setAnalysis] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const weatherResp = await fetch(
          'https://api.open-meteo.com/v1/forecast?latitude=0&longitude=0&current_weather=true'
        );
        const weather = await weatherResp.json();
        const eventResp = await fetch('/events');
        const eventData = await eventResp.json();
        const devResp = await fetch('/development');
        const devData = await devResp.json();
        const count = (eventData.list || []).length;
        const temp = weather.current_weather?.temperature;
        const corr = temp != null ? count * temp : null;
        const season = seasonForMonth(new Date().getMonth());
        setAnalysis({
          correlation: corr,
          season,
          eventCount: count,
          growth: devData.new_projects,
        });
      } catch (e) {
        reportError(e);
        setAnalysis(null);
      }
    };
    load();
  }, []);

  if (!analysis) return <div>Environmental: N/A</div>;
  const c =
    analysis.correlation != null ? analysis.correlation.toFixed(1) : 'N/A';
  return (
    <div>
      Corr:{c} Season:{analysis.season} Events:{analysis.eventCount} Growth:
      {analysis.growth}
    </div>
  );
}
