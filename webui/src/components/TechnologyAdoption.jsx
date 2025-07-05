import { useEffect, useState } from 'react';

export default function TechnologyAdoption() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const load = () => {
      fetch('/demographics/adoption')
        .then((r) => r.json())
        .then(setStats)
        .catch(() => setStats(null));
    };
    load();
    const id = setInterval(load, 60000);
    return () => clearInterval(id);
  }, []);

  if (!stats) return <div>Technology Adoption: N/A</div>;

  return (
    <div>
      <div>Average Access: {stats.average_access?.toFixed(2)}</div>
      <div>Top Region: {stats.top_region}</div>
      <div>Market Penetration: {stats.market_penetration?.toFixed(2)}</div>
      <div>
        Demographic Correlation: {stats.demographic_correlation?.toFixed(2)}
      </div>
    </div>
  );
}
