export class TowerTracker {
  constructor() {
    this.towers = new Map();
    this.towerObs = new Map();
    this.wifiObs = new Map();
    this.btObs = new Map();
  }

  async _record(map, key, data) {
    if (!map.has(key)) map.set(key, []);
    map.get(key).push(data);
  }

  async updateTower(towerId, lat, lon, lastSeen = Date.now()) {
    this.towers.set(towerId, { tower_id: towerId, lat, lon, last_seen: lastSeen });
  }

  async getTower(towerId) {
    return this.towers.get(towerId) || null;
  }

  async allTowers() {
    return Array.from(this.towers.values());
  }

  async close() {}

  async logTower(towerId, rssi, lat = null, lon = null, timestamp = Date.now()) {
    await this._record(this.towerObs, towerId, {
      tower_id: towerId,
      rssi,
      lat,
      lon,
      timestamp,
    });
  }

  async towerHistory(towerId) {
    return (this.towerObs.get(towerId) || [])
      .slice()
      .sort((a, b) => b.timestamp - a.timestamp);
  }

  async logWifi(bssid, ssid, lat = null, lon = null, timestamp = Date.now()) {
    await this._record(this.wifiObs, bssid, {
      bssid,
      ssid,
      lat,
      lon,
      timestamp,
    });
  }

  async wifiHistory(bssid) {
    return (this.wifiObs.get(bssid) || [])
      .slice()
      .sort((a, b) => b.timestamp - a.timestamp);
  }

  async logBluetooth(address, name, lat = null, lon = null, timestamp = Date.now()) {
    await this._record(this.btObs, address, {
      address,
      name,
      lat,
      lon,
      timestamp,
    });
  }

  async bluetoothHistory(address) {
    return (this.btObs.get(address) || [])
      .slice()
      .sort((a, b) => b.timestamp - a.timestamp);
  }
}
