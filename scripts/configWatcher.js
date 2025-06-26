const fs = require('fs');
const path = require('path');

function watchConfig(filePath, callback) {
  const abs = path.resolve(filePath);
  const dir = path.dirname(abs);
  const base = path.basename(abs);
  const watcher = fs.watch(dir, { persistent: true }, (eventType, filename) => {
    if (!filename || filename === base) {
      callback();
    }
  });
  return watcher;
}

module.exports = { watchConfig };
