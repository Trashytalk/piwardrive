import { useEffect, useState } from 'react';

export default function VehicleInfo({ data }) {
  const [info, setInfo] = useState(data);

  useEffect(() => {
    if (!data) {
      fetch('/vehicle')
        .then(r => r.json())
        .then(setInfo)
        .catch(() => setInfo(null));
    }
  }, [data]);

  if (!info) return <div>Vehicle: N/A</div>;
  const speed = info.speed != null ? info.speed.toFixed(1) + ' km/h' : 'N/A';
  const rpm = info.rpm != null ? info.rpm.toFixed(0) : 'N/A';
  const load = info.engine_load != null ? info.engine_load.toFixed(0) + '%' : 'N/A';
  return <div>Speed: {speed} | RPM: {rpm} | Load: {load}</div>;
}
