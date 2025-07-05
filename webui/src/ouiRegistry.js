import { reportError } from './exceptionHandler.js';

let OUI_MAP = null;
export const DEFAULT_OUI_URL = '/oui.csv';

export async function loadOuiMap(url = DEFAULT_OUI_URL) {
  try {
    const resp = await fetch(url);
    const text = await resp.text();
    const map = {};
    text
      .split(/\n+/)
      .slice(1)
      .forEach((line) => {
        const [assign, vendor] = line.split(',');
        if (assign && vendor) {
          const prefix = assign.replace(/-/g, ':').toUpperCase();
          map[prefix] = vendor.trim();
        }
      });
    OUI_MAP = map;
    return map;
  } catch (e) {
    reportError(e);
    OUI_MAP = {};
    return OUI_MAP;
  }
}

export function lookupVendor(bssid, map = OUI_MAP) {
  if (!bssid || !map) return null;
  const parts = bssid.toUpperCase().replace(/-/g, ':').split(':');
  if (parts.length < 3) return null;
  const prefix = parts.slice(0, 3).join(':');
  return map[prefix] || null;
}

export async function cachedLookupVendor(bssid) {
  if (!OUI_MAP) await loadOuiMap();
  return lookupVendor(bssid);
}
