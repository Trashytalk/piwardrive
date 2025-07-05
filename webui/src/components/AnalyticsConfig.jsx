import React from 'react';

export default function AnalyticsConfig({ config, onChange }) {
  return (
    <div>
      <div>
        <label>
          Training Epochs
          <input
            type="number"
            value={config.ml_training_epochs}
            onChange={(e) =>
              onChange('ml_training_epochs', Number(e.target.value))
            }
          />
        </label>
      </div>
      <div>
        <label>
          Job Schedule
          <input
            type="text"
            value={config.analytics_schedule}
            onChange={(e) => onChange('analytics_schedule', e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          Alert Threshold
          <input
            type="number"
            value={config.analytics_alert_threshold}
            onChange={(e) =>
              onChange('analytics_alert_threshold', Number(e.target.value))
            }
          />
        </label>
      </div>
      <div>
        <label>
          Custom Rules
          <textarea
            value={config.custom_analysis_rules}
            onChange={(e) => onChange('custom_analysis_rules', e.target.value)}
          />
        </label>
      </div>
    </div>
  );
}
