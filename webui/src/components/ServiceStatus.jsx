export default function ServiceStatus({ metrics }) {
  if (!metrics) return <div>Services: N/A</div>;
  const { kismet_running, bettercap_running } = metrics;
  return (
    <div>
      Kismet: {kismet_running ? 'ok' : 'down'} | BetterCAP: {bettercap_running ? 'ok' : 'down'}
    </div>
  );
}
