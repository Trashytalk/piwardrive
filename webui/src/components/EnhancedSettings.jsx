import { useEffect, useState } from 'react';
import DatabaseConfig from './DatabaseConfig.jsx';
import AnalyticsConfig from './AnalyticsConfig.jsx';
import SecurityConfig from './SecurityConfig.jsx';

export default function EnhancedSettings() {
  const [config, setConfig] = useState(null);
  const [tab, setTab] = useState('database');

  useEffect(() => {
    fetch('/config')
      .then((r) => r.json())
      .then(setConfig)
      .catch(() => {});
  }, []);

  const handleChange = (key, value) => {
    setConfig((prev) => ({ ...prev, [key]: value }));
  };

  const save = () => {
    fetch('/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config),
    })
      .then((r) => r.json())
      .then(setConfig)
      .catch(() => {});
  };

  if (!config) return null;

  const renderExport = () => (
    <div>
      <div>
        <label>
          Export Format
          <input
            type="text"
            value={config.export_format}
            onChange={(e) => handleChange('export_format', e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          Integration Enabled
          <input
            type="checkbox"
            checked={!!config.integration_enabled}
            onChange={(e) =>
              handleChange('integration_enabled', e.target.checked)
            }
          />
        </label>
      </div>
      <div>
        <label>
          Integration Endpoint
          <input
            type="text"
            value={config.integration_endpoint}
            onChange={(e) =>
              handleChange('integration_endpoint', e.target.value)
            }
          />
        </label>
      </div>
      <div>
        <label>
          Integration API Key
          <input
            type="text"
            value={config.integration_api_key}
            onChange={(e) =>
              handleChange('integration_api_key', e.target.value)
            }
          />
        </label>
      </div>
    </div>
  );

  return (
    <section>
      <div>
        <button onClick={() => setTab('database')}>Database</button>
        <button onClick={() => setTab('analytics')}>Analytics</button>
        <button onClick={() => setTab('security')}>Security</button>
        <button onClick={() => setTab('export')}>Export</button>
      </div>
      {tab === 'database' && (
        <DatabaseConfig config={config} onChange={handleChange} />
      )}
      {tab === 'analytics' && (
        <AnalyticsConfig config={config} onChange={handleChange} />
      )}
      {tab === 'security' && (
        <SecurityConfig config={config} onChange={handleChange} />
      )}
      {tab === 'export' && renderExport()}
      <button onClick={save}>Save</button>
    </section>
  );
}
