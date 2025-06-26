export function cachedLookupVendor(_bssid) {
  return 'Vendor';
}

export function findSuspiciousAps(records) {
  const aps = [];
  const seenBssid = {};
  for (const rec of records) {
    const bssid = rec.bssid;
    const ssid = rec.ssid || '';
    const enc = (rec.encryption || '').toLowerCase();
    const channel = rec.channel;
    let suspicious = false;
    if (enc.includes('open') || enc.includes('wep')) {
      suspicious = true;
    }
    if (bssid) {
      seenBssid[bssid] = seenBssid[bssid] || new Set();
      seenBssid[bssid].add(ssid);
      if (seenBssid[bssid].size > 1) suspicious = true;
    }
    if (channel !== undefined && channel !== null && channel !== '') {
      try {
        const ch = parseInt(String(channel).split(' ')[0], 10);
        if (isNaN(ch) || ch < 1 || ch > 196) suspicious = true;
      } catch {
        suspicious = true;
      }
    }
    if (bssid && cachedLookupVendor(bssid) == null) {
      suspicious = true;
    }
    if (suspicious) aps.push(rec);
  }
  return aps;
}
