import { setupLogging } from './logconfig.js';

let installed = false;
let logger = null;

export function reportError(err, alertUser = false) {
  if (!logger) {
    logger = setupLogging({ logFile: 'webui-errors.log' });
  }
  const message = err && err.message ? err.message : String(err);
  logger.error(message);
  if (alertUser) {
    alert(message);
  }
}

export function install({ alertUser = false } = {}) {
  if (installed) return;
  installed = true;
  window.onerror = function (msg, src, line, col, error) {
    reportError(error || msg, alertUser);
  };
  window.addEventListener('unhandledrejection', e => {
    reportError(e.reason, alertUser);
  });
}
