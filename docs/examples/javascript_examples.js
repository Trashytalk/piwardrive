// Example JavaScript (browser/React) client for the PiWardrive API
import axios from 'axios';

export async function scanWifi(token) {
  const headers = token ? { Authorization: `Bearer ${token}` } : {};
  const res = await axios.get('/wifi/scan', {
    params: { interface: 'wlan0' },
    headers,
  });
  return res.data.access_points;
}
