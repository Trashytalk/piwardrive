import { useEffect, useState } from 'react';
import { reportError } from '../exceptionHandler.js';

export default function UrbanDevelopment() {
  const [info, setInfo] = useState(null);

  useEffect(() => {
    const load = async () => {
      try {
        const resp = await fetch('/development');
        const data = await resp.json();
        setInfo({
          growth: data.infrastructure_growth,
          pattern: data.development_pattern,
          gentrification: data.gentrification_index,
          smart: data.smart_city_score,
        });
      } catch (e) {
        reportError(e);
        setInfo(null);
      }
    };
    load();
  }, []);

  if (!info) return <div>Development: N/A</div>;
  return (
    <div>
      Growth:{info.growth} Pattern:{info.pattern} Gentrification:
      {info.gentrification} Smart:{info.smart}
    </div>
  );
}
