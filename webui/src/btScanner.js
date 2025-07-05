/* global global */

export async function scanBluetooth(timeout = 10) {
  if (typeof global.bleakDiscover === 'function') {
    const devices = await global.bleakDiscover(timeout);
    return devices.map(d => ({ address: d.address, name: d.name || d.address }));
  }
  if (typeof global.btctlScan === 'function') {
    return await global.btctlScan(timeout);
  }
  return [];
}
