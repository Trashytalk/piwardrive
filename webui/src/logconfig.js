import fs from 'fs';

/* global process */

const LEVELS = { DEBUG: 10, INFO: 20, WARNING: 30, ERROR: 40 };

export function setupLogging({ logFile, level = 'INFO', stdout = false } = {}) {
  const env = process.env.PW_LOG_LEVEL;
  if (env) {
    if (/^\d+$/.test(env)) {
      const num = parseInt(env, 10);
      level = Object.keys(LEVELS).find(k => LEVELS[k] === num) || level;
    } else if (LEVELS[env.toUpperCase()]) {
      level = env.toUpperCase();
    }
  }
  const current = LEVELS[level.toUpperCase()] || LEVELS.INFO;

  function log(levelName, message) {
    if (LEVELS[levelName] >= current) {
      const line = JSON.stringify({ level: levelName, message }) + '\n';
      fs.appendFileSync(logFile, line);
      if (stdout) process.stdout.write(line);
    }
  }

  return {
    level: current,
    debug: msg => log('DEBUG', msg),
    info: msg => log('INFO', msg),
    warning: msg => log('WARNING', msg),
    error: msg => log('ERROR', msg)
  };
}
