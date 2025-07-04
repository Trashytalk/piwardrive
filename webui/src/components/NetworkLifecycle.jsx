import { useEffect, useState } from 'react';

export default function NetworkLifecycle({ bssid }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    const url = bssid
      ? `/api/analytics/lifecycle?bssid=${encodeURIComponent(bssid)}`
      : '/api/analytics/lifecycle';
    fetch(url)
      .then((r) => r.json())
      .then((d) => setData(d))
      .catch(() => setData(null));
  }, [bssid]);

  if (!data) return <div>Network lifecycle data unavailable</div>;

  return (
    <div>
      <h4>Upgrade Prediction Timeline (95% CI)</h4>
      <pre>{JSON.stringify(data)}</pre>
    </div>
  );
}
