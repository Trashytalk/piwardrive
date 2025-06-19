export default function SignalStrength({ metrics }) {
  const rssi = metrics?.avg_rssi;
  return <div>RSSI: {rssi != null ? rssi.toFixed(1) + ' dBm' : 'N/A'}</div>;
}
