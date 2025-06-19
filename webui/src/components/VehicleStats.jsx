export default function VehicleStats({ metrics }) {
  if (!metrics) return <div>Vehicle: N/A</div>;
  const { vehicle_speed, vehicle_rpm, engine_load } = metrics;
  const speed = vehicle_speed != null ? vehicle_speed.toFixed(1) + ' km/h' : 'N/A';
  const rpm = vehicle_rpm != null ? vehicle_rpm.toFixed(0) : 'N/A';
  const load = engine_load != null ? engine_load.toFixed(0) + '%' : 'N/A';
  return (
    <div>
      Speed: {speed} | RPM: {rpm} | Load: {load}
    </div>
  );
}
