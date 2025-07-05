import { useEffect, useState } from 'react';

export default function Orientation({ data }) {
  const [info, setInfo] = useState(data);

  useEffect(() => {
    if (data) {
      setInfo(data);
      return;
    }

    const load = () => {
      fetch('/orientation')
        .then((r) => r.json())
        .then(setInfo)
        .catch(() => setInfo(null));
    };

    load();
    const id = setInterval(load, 5000);
    return () => clearInterval(id);
  }, [data]);

  if (!info) return <div>Orientation: N/A</div>;
  const angle = info.angle != null ? ` (${info.angle.toFixed(0)}°)` : '';
  const orient = info.orientation != null ? info.orientation : 'N/A';
  return (
    <div>
      Orientation: {orient}
      {angle}
    </div>
  );
}
