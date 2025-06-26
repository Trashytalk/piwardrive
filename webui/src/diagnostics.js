import os from 'os';
import fs from 'fs';
import { execSync } from 'child_process';
import { gzipSync } from 'zlib';

let lastNetworkOk = 0;

function getCpuTemp() {
  try {
    const text = fs.readFileSync('/sys/class/thermal/thermal_zone0/temp', 'utf8');
    return parseFloat(text) / 1000;
  } catch (_) {
    try {
      const out = execSync('vcgencmd measure_temp', { encoding: 'utf8' });
      const m = out.match(/temp=([\d.]+)/);
      if (m) return parseFloat(m[1]);
    } catch (_) {
      return null;
    }
  }
  return null;
}

function getDiskPercent() {
  try {
    const out = execSync("df -P / | awk 'NR==2 {print $5}'", { encoding: 'utf8' });
    return parseFloat(out) || 0;
  } catch (_) {
    return 0;
  }
}

export function generateSystemReport() {
  return {
    timestamp: new Date().toISOString(),
    cpu_temp: getCpuTemp(),
    cpu_percent: (os.loadavg()[0] * 100) / os.cpus().length,
    memory_percent: (1 - os.freemem() / os.totalmem()) * 100,
    disk_percent: getDiskPercent(),
  };
}

export function runNetworkTest(host = '8.8.8.8', cacheSeconds = 30) {
  const now = Date.now() / 1000;
  if (lastNetworkOk && now - lastNetworkOk < cacheSeconds) return true;
  try {
    execSync(`ping -c 1 ${host}`, { stdio: 'ignore' });
    lastNetworkOk = now;
    return true;
  } catch (_) {
    return false;
  }
}

export function getInterfaceStatus() {
  const ifaces = os.networkInterfaces();
  const res = {};
  for (const name of Object.keys(ifaces)) {
    res[name] = (ifaces[name] || []).length > 0;
  }
  return res;
}

export function listUsbDevices() {
  try {
    const out = execSync('lsusb', { encoding: 'utf8' });
    return out.trim().split(/\r?\n/);
  } catch (_) {
    return [];
  }
}

export function getServiceStatuses(services = ['kismet', 'bettercap', 'gpsd']) {
  const result = {};
  for (const svc of services) {
    try {
      const out = execSync(`systemctl is-active ${svc}`, { encoding: 'utf8' });
      result[svc] = out.trim() === 'active';
    } catch (_) {
      result[svc] = false;
    }
  }
  return result;
}

export function rotateLog(path, maxFiles = 3) {
  if (!fs.existsSync(path)) return;
  for (const ext of ['.gz', '']) {
    const old = `${path}.${maxFiles}${ext}`;
    if (fs.existsSync(old)) fs.unlinkSync(old);
  }
  for (let i = maxFiles - 1; i >= 1; i--) {
    const srcGz = `${path}.${i}.gz`;
    const dstGz = `${path}.${i + 1}.gz`;
    if (fs.existsSync(srcGz)) {
      fs.renameSync(srcGz, dstGz);
      continue;
    }
    const src = `${path}.${i}`;
    if (fs.existsSync(src)) {
      fs.renameSync(src, dstGz);
    }
  }
  const tmp = `${path}.1`;
  fs.renameSync(path, tmp);
  const data = fs.readFileSync(tmp);
  fs.writeFileSync(`${tmp}.gz`, gzipSync(data));
  fs.unlinkSync(tmp);
}

export function selfTest() {
  return {
    system: generateSystemReport(),
    network_ok: runNetworkTest(),
    interfaces: getInterfaceStatus(),
    usb: listUsbDevices(),
    services: getServiceStatuses(),
  };
}
