"use strict";

let gpsd;
try {
  gpsd = require('gpsd');
} catch {
  gpsd = null;
}

class GPSDClient {
  constructor(host, port, helpers = {}) {
    this.host = host || process.env.PW_GPSD_HOST || '127.0.0.1';
    const envPort = process.env.PW_GPSD_PORT;
    this.port = port !== undefined ? port : envPort ? parseInt(envPort, 10) : 2947;
    this._connected = false;
    this._connect = helpers.connect || (gpsd && gpsd.connect);
    this._getCurrent = helpers.getCurrent || (gpsd && (gpsd.getCurrent || gpsd.get_current));
  }

  _doConnect() {
    if (!this._connect) return;
    try {
      this._connect(this.host, this.port);
      this._connected = true;
    } catch {
      this._connected = false;
    }
  }

  _ensureConnection() {
    if (!this._connected) {
      this._doConnect();
    }
  }

  _getPacket() {
    this._ensureConnection();
    if (!this._connected || !this._getCurrent) return null;
    try {
      return this._getCurrent();
    } catch {
      this._connected = false;
      return null;
    }
  }

  getPosition() {
    const pkt = this._getPacket();
    if (!pkt) return null;
    try {
      if (typeof pkt.position === 'function') return pkt.position();
      if (pkt.lat != null && pkt.lon != null) return [Number(pkt.lat), Number(pkt.lon)];
    } catch {}
    return null;
  }

  getAccuracy() {
    const pkt = this._getPacket();
    if (!pkt) return null;
    try {
      if (typeof pkt.position_precision === 'function') {
        const res = pkt.position_precision();
        return Array.isArray(res) ? Number(res[0]) : null;
      }
      if (pkt.epx != null && pkt.epy != null) return Math.max(Number(pkt.epx), Number(pkt.epy));
    } catch {}
    return null;
  }

  getFixQuality() {
    const pkt = this._getPacket();
    if (!pkt) return 'Unknown';
    const map = {1:'No Fix',2:'2D',3:'3D',4:'DGPS'};
    try {
      const mode = pkt.mode;
      if (typeof mode === 'number') return map[mode] || String(mode);
    } catch {}
    return 'Unknown';
  }
}

const client = new GPSDClient();

module.exports = { GPSDClient, client };
