export default function BatteryStatus({ metrics }) {
  if (!metrics) return <div>Battery: N/A</div>;
  const { battery_percent, battery_plugged } = metrics;
  if (battery_percent == null) return <div>Battery: N/A</div>;
  return (
    <div>
      Battery: {battery_percent.toFixed(0)}%{' '}
      {battery_plugged ? 'charging' : 'discharging'}
    </div>
  );
}
