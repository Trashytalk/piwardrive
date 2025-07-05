import { useEffect, useState } from 'react';

export default function IncidentResponse() {
  const [info, setInfo] = useState(null);

  useEffect(() => {
    const load = () => {
      fetch('/incident-response')
        .then((r) => r.json())
        .then(setInfo)
        .catch(() => setInfo(null));
    };
    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, []);

  if (!info) return <div>Incidents: N/A</div>;

  const correlations = info.correlations || [];
  const classifications = info.classifications || [];
  const workflows = info.workflows || [];
  const forensics = info.forensics || [];

  return (
    <div>
      <div>Correlations: {correlations.length}</div>
      <div>Classifications: {classifications.length}</div>
      <div>Workflows: {workflows.length}</div>
      <div>Forensic Items: {forensics.length}</div>
    </div>
  );
}
