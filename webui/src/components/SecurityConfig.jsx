import React from 'react';

export default function SecurityConfig({ config, onChange }) {
  return (
    <div>
      <div>
        <label>
          Threat Sensitivity
          <input
            type="number"
            value={config.threat_sensitivity}
            onChange={e => onChange('threat_sensitivity', Number(e.target.value))}
          />
        </label>
      </div>
      <div>
        <label>
          Alert Policy
          <input
            type="text"
            value={config.alert_escalation_policy}
            onChange={e => onChange('alert_escalation_policy', e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          Rule Version
          <input
            type="text"
            value={config.security_rule_version}
            onChange={e => onChange('security_rule_version', e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          Whitelist
          <textarea
            value={config.whitelist}
            onChange={e => onChange('whitelist', e.target.value)}
          />
        </label>
      </div>
    </div>
  );
}
