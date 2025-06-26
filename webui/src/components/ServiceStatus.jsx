import { controlService } from '../serviceControl.js';

export default function ServiceStatus({ metrics }) {
  if (!metrics) return <div>Services: N/A</div>;
  const { kismet_running, bettercap_running } = metrics;

  const control = (svc, running) => {
    controlService(svc, running ? 'stop' : 'start');
  };

  return (
    <div>
      <div>
        Kismet: {kismet_running ? 'ok' : 'down'}{' '}
        <button onClick={() => control('kismet', kismet_running)}>
          {kismet_running ? 'Stop' : 'Start'}
        </button>
      </div>
      <div>
        BetterCAP: {bettercap_running ? 'ok' : 'down'}{' '}
        <button onClick={() => control('bettercap', bettercap_running)}>
          {bettercap_running ? 'Stop' : 'Start'}
        </button>
      </div>
    </div>
  );
}
