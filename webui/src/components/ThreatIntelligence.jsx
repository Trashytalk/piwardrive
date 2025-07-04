import { useEffect, useState } from 'react';
import { computeSecurityScore } from '../securityAnalytics.js';

export default function ThreatIntelligence() {
  const [info, setInfo] = useState(null);

  useEffect(() => {
    const load = () => {
      fetch('/threat-intel')
        .then(r => r.json())
        .then(setInfo)
        .catch(() => setInfo(null));
    };
    load();
    const id = setInterval(load, 10000);
    return () => clearInterval(id);
  }, []);

  if (!info) return <div>Threat Intel: N/A</div>;

  const patterns = info.patterns || [];
  const vulnerabilities = info.vulnerabilities || [];
  const actors = info.actors || [];
  const incidents = info.incidents || [];
  const score = computeSecurityScore({
    networkScore: info.network_score,
    encryptionStrength: info.encryption_strength,
    threatLevel: info.threat_level,
    configIssues: vulnerabilities,
  });

  return (
    <div>
      <div>Attack Patterns: {patterns.length}</div>
      <div>Threat Actors: {actors.length}</div>
      <div>Incidents: {incidents.length}</div>
      <div>Security Score: {score}</div>
    </div>
  );
}
