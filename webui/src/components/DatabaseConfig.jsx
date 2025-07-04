import React from 'react';

export default function DatabaseConfig({ config, onChange }) {
  return (
    <div>
      <div>
        <label>
          Cache Size (MB)
          <input
            type="number"
            value={config.db_cache_size}
            onChange={e => onChange('db_cache_size', Number(e.target.value))}
          />
        </label>
      </div>
      <div>
        <label>
          Data Retention (days)
          <input
            type="number"
            value={config.retention_days}
            onChange={e => onChange('retention_days', Number(e.target.value))}
          />
        </label>
      </div>
      <div>
        <label>
          Backup Enabled
          <input
            type="checkbox"
            checked={!!config.backup_enabled}
            onChange={e => onChange('backup_enabled', e.target.checked)}
          />
        </label>
      </div>
      <div>
        <label>
          Migration Running
          <input
            type="checkbox"
            checked={!!config.migration_running}
            onChange={e => onChange('migration_running', e.target.checked)}
          />
        </label>
      </div>
    </div>
  );
}
