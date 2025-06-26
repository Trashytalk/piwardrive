import { useEffect, useState } from 'react';
import { fetchServiceStatuses } from '../backendService.js';

export default function ServiceStatusFetcher({ services = ['kismet', 'gpsd'] }) {
  const [status, setStatus] = useState(null);
  useEffect(() => {
    fetchServiceStatuses(services).then(setStatus).catch(() => {});
  }, [services]);

  if (!status) return <div>Loading...</div>;
  return (
    <ul>
      {services.map(svc => (
        <li key={svc} data-testid={svc}>
          {svc}: {status[svc] ? 'active' : 'inactive'}
        </li>
      ))}
    </ul>
  );
}
