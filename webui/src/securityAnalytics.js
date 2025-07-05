export function computeSecurityScore({
  networkScore = 0,
  encryptionStrength = 0,
  threatLevel = 0,
  configIssues = [],
} = {}) {
  let score = 0.4 * networkScore + 0.3 * encryptionStrength + 0.3 * threatLevel;
  score -= (configIssues.length || 0) * 5;
  if (score < 0) score = 0;
  if (score > 100) score = 100;
  return Math.round(score);
}
