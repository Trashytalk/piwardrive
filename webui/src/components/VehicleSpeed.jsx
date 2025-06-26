export default function VehicleSpeed({ metrics }) {
  const speed = metrics?.vehicle_speed;
  const val = speed != null ? speed.toFixed(1) + ' km/h' : 'N/A';
  return <div>Vehicle Speed: {val}</div>;
}
