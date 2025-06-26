export async function fetchWigleNetworks(apiName, apiKey, lat, lon, { radius = 0.01 } = {}) {
  const params = new URLSearchParams({
    latrange1: lat - radius,
    latrange2: lat + radius,
    longrange1: lon - radius,
    longrange2: lon + radius,
    resultsPerPage: 100
  });
  const creds = btoa(`${apiName}:${apiKey}`);
  const resp = await fetch(`https://api.wigle.net/api/v2/network/search?${params.toString()}`, {
    headers: { Authorization: `Basic ${creds}` }
  });
  if (!resp.ok) throw new Error('WiGLE request failed');
  const data = await resp.json();
  const nets = [];
  for (const rec of data.results || []) {
    if (rec.trilat == null || rec.trilong == null) continue;
    nets.push({
      bssid: rec.netid,
      ssid: rec.ssid,
      encryption: rec.encryption,
      lat: rec.trilat,
      lon: rec.trilong
    });
  }
  return nets;
}
