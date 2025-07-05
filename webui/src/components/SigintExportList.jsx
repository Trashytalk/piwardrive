import { useEffect, useState } from 'react';
import { fetchSigintData } from '../backendService.js';

export default function SigintExportList({ type = 'aps' }) {
  const [records, setRecords] = useState(null);
  useEffect(() => {
    fetchSigintData(type)
      .then(setRecords)
      .catch(() => {});
  }, [type]);

  if (!records) return <div>Loading...</div>;
  return <div data-testid="count">count {records.length}</div>;
}
