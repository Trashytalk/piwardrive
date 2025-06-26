const http = require('http');
const fs = require('fs');
const { spawnSync } = require('child_process');
const url = require('url');

function readGps(dbFile) {
  try {
    const res = spawnSync('sqlite3', ['-noheader', '-separator', '|', dbFile,
      'SELECT lat, lon, time FROM gps_tracks ORDER BY time DESC LIMIT 1;']);
    const output = res.stdout.toString().trim();
    if (!output) return null;
    const [lat, lon, time] = output.split('|');
    return { lat: parseFloat(lat), lon: parseFloat(lon), time };
  } catch {
    return null;
  }
}

function readGeo(file) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch {
    return { type: 'FeatureCollection', features: [] };
  }
}

function toggleService(service, state) {
  const cmd = state === 'start'
    ? ['sudo', 'systemctl', 'start', service]
    : ['sudo', 'systemctl', 'stop', service];
  if (process.env.PW_RUN_LOG) {
    fs.appendFileSync(process.env.PW_RUN_LOG, JSON.stringify(cmd) + '\n');
  } else {
    spawnSync(cmd[0], cmd.slice(1));
  }
  return { status: 'ok' };
}

function createServer(opts = {}) {
  const gpsDb = opts.gpsDb || process.env.PW_GPS_DB || '/home/pi/.config/piwardrive/db.sqlite';
  const apsFile = opts.apsFile || process.env.PW_APS_FILE || '/home/pi/.config/piwardrive/export/aps.geojson';
  const btFile = opts.btFile || process.env.PW_BT_FILE || '/home/pi/.config/piwardrive/export/bt.geojson';

  return http.createServer((req, res) => {
    const parsed = url.parse(req.url, true);
    res.setHeader('Content-Type', 'application/json');
    if (req.method === 'GET' && parsed.pathname === '/api/gps') {
      res.end(JSON.stringify(readGps(gpsDb) || { lat: null, lon: null, time: null }));
    } else if (req.method === 'GET' && parsed.pathname === '/api/aps') {
      res.end(JSON.stringify(readGeo(apsFile)));
    } else if (req.method === 'GET' && parsed.pathname === '/api/bt') {
      res.end(JSON.stringify(readGeo(btFile)));
    } else if (req.method === 'POST' && parsed.pathname === '/api/kismet/toggle') {
      res.end(JSON.stringify(toggleService('kismet', parsed.query.state)));
    } else {
      res.statusCode = 404;
      res.setHeader('Content-Type', 'text/plain');
      res.end('Not found');
    }
  });
}

if (require.main === module) {
  const port = process.env.PORT !== undefined ? Number(process.env.PORT) : 3000;
  const server = createServer();
  server.listen(port, () => {
    console.log(`Listening on ${server.address().port}`);
  });
}

module.exports = { createServer };
