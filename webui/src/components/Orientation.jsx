import { useEffect, useState } from 'react';

export default function Orientation({ data }) {
  const [info, setInfo] = useState(data);

  useEffect(() => {
    if (!data) {
      fetch('/orientation')
        .then(r => r.json())
        .then(setInfo)
        .catch(() => setInfo(null));
    }
  }, [data]);

  if (!info) return <div>Orientation: N/A</div>;
  const angle = info.angle != null ? ` (${info.angle.toFixed(0)}°)` : '';
  const orient = info.orientation != null ? info.orientation : 'N/A';
  return <div>Orientation: {orient}{angle}</div>;
}
