import { useState } from 'react';
import { controlService } from '../serviceControl.js';
import { LoadingSpinner } from './LoadingStates.jsx';
import { InlineError } from './ErrorDisplay.jsx';

export default function ServiceStatus({ metrics }) {
  const [loading, setLoading] = useState({});
  const [error, setError] = useState(null);

  if (!metrics) return <div>Services: N/A</div>;
  
  const { kismet_running, bettercap_running } = metrics;

  const control = async (svc, running) => {
    setLoading(prev => ({ ...prev, [svc]: true }));
    setError(null);
    
    try {
      await controlService(svc, running ? 'stop' : 'start');
    } catch (err) {
      setError(`Failed to ${running ? 'stop' : 'start'} ${svc}: ${err.message}`);
    } finally {
      setLoading(prev => ({ ...prev, [svc]: false }));
    }
  };

  return (
    <div>
      {error && <InlineError error={error} />}
      
      <div>
        Kismet: {kismet_running ? 'ok' : 'down'}{' '}
        <button 
          onClick={() => control('kismet', kismet_running)}
          disabled={loading.kismet}
        >
          {loading.kismet ? <LoadingSpinner size="small" /> : (kismet_running ? 'Stop' : 'Start')}
        </button>
      </div>
      
      <div>
        BetterCAP: {bettercap_running ? 'ok' : 'down'}{' '}
        <button 
          onClick={() => control('bettercap', bettercap_running)}
          disabled={loading.bettercap}
        >
          {loading.bettercap ? <LoadingSpinner size="small" /> : (bettercap_running ? 'Stop' : 'Start')}
        </button>
      </div>
    </div>
  );
}
