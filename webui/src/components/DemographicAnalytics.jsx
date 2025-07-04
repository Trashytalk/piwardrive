import { useEffect, useState } from 'react';

export default function DemographicAnalytics() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const load = () => {
      fetch('/demographics/social')
        .then(r => r.json())
        .then(setData)
        .catch(() => setData(null));
    };
    load();
    const id = setInterval(load, 60000);
    return () => clearInterval(id);
  }, []);

  if (!data) return <div>Demographic analytics: N/A</div>;

  return (
    <div>
      <div>Socioeconomic Correlation: {data.socioeconomic_correlation?.correlation?.toFixed(2)}</div>
      <div>Avg Tech Adoption: {data.technology_adoption_patterns?.average_access?.toFixed(2)}</div>
      <div>Digital Divide Gap: {data.digital_divide?.gap?.toFixed(2)}</div>
      <div>Community Networks Detected: {data.community_networks?.count}</div>
    </div>
  );
}
