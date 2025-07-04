import fs from 'fs';
import path from 'path';

export let CONFIG_DIR = process.cwd();
export let CONFIG_PATH = path.join(CONFIG_DIR, 'config.json');
export let PROFILES_DIR = path.join(CONFIG_DIR, 'profiles');
export let ACTIVE_PROFILE_FILE = path.join(CONFIG_DIR, 'active_profile');

export const DEFAULT_CONFIG = {
  theme: 'Dark',
  map_poll_gps: 10,
  map_poll_gps_max: 30,
  map_poll_bt: 60,
  map_poll_aps: 60,
  map_show_bt: false,
  offline_tile_path: '',
  disable_scanning: false,
  map_auto_prefetch: false,
  ui_font_size: 16,
  map_cluster_capacity: 8,
  route_prefetch_interval: 3600,
  route_prefetch_lookahead: 5,
  widget_battery_status: false,
  widget_detection_rate: false,
  widget_threat_level: false,
  widget_network_density: false,
  widget_device_classification: false,
  widget_suspicious_activity: false,
  widget_alert_summary: false,
  widget_threat_map: false,
  widget_security_score: false,
  widget_database_health: false,
  widget_scanner_status: false,
  widget_system_resource: false,
  health_poll_interval: 10,
  gps_movement_threshold: 1.0,
  db_cache_size: 128,
  retention_days: 30,
  backup_enabled: false,
  migration_running: false,
  ml_training_epochs: 10,
  analytics_schedule: '0 0 * * *',
  analytics_alert_threshold: 0.8,
  custom_analysis_rules: '',
  threat_sensitivity: 5,
  alert_escalation_policy: 'Immediate',
  security_rule_version: '1.0',
  whitelist: '',
  export_format: 'json',
  integration_enabled: false,
  integration_endpoint: '',
  integration_api_key: '',
};

function _profilePath(name) {
  return path.join(PROFILES_DIR, `${name}.json`);
}

export function listProfiles() {
  try {
    return fs
      .readdirSync(PROFILES_DIR)
      .filter((f) => f.endsWith('.json'))
      .map((f) => path.basename(f, '.json'));
  } catch {
    return [];
  }
}

export function setActiveProfile(name) {
  fs.mkdirSync(CONFIG_DIR, { recursive: true });
  fs.writeFileSync(ACTIVE_PROFILE_FILE, name);
}

export function getActiveProfile() {
  if (process.env.PW_PROFILE_NAME) return process.env.PW_PROFILE_NAME;
  try {
    const txt = fs.readFileSync(ACTIVE_PROFILE_FILE, 'utf8').trim();
    return txt || null;
  } catch {
    return null;
  }
}

export function getConfigPath(profile) {
  if (profile === undefined || profile === null) profile = getActiveProfile();
  return profile ? _profilePath(profile) : CONFIG_PATH;
}

export function loadConfig(profile) {
  const file = getConfigPath(profile);
  try {
    const data = JSON.parse(fs.readFileSync(file, 'utf8'));
    return { ...DEFAULT_CONFIG, ...data };
  } catch {
    return { ...DEFAULT_CONFIG };
  }
}

function validate(cfg) {
  if (cfg.map_poll_gps <= 0) throw new Error('map_poll_gps must be >0');
  if (cfg.ui_font_size <= 0) throw new Error('ui_font_size must be >0');
  if (cfg.db_cache_size < 0) throw new Error('db_cache_size must be >=0');
  if (cfg.retention_days < 0) throw new Error('retention_days must be >=0');
  if (cfg.ml_training_epochs < 1) throw new Error('ml_training_epochs must be >0');
  if (cfg.analytics_alert_threshold < 0) throw new Error('analytics_alert_threshold must be >=0');
  if (cfg.threat_sensitivity <= 0) throw new Error('threat_sensitivity must be >0');
}

export function saveConfig(cfg, profile) {
  validate(cfg);
  const file = getConfigPath(profile);
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(cfg, null, 2));
}

export function configMtime(profile) {
  const file = getConfigPath(profile);
  try {
    return fs.statSync(file).mtimeMs;
  } catch {
    return null;
  }
}

function parseEnvValue(raw, defaultVal) {
  if (typeof defaultVal === 'boolean') {
    return ['1', 'true', 'yes', 'on'].includes(raw.toLowerCase());
  }
  if (typeof defaultVal === 'number') {
    const n = Number(raw);
    return isNaN(n) ? defaultVal : n;
  }
  return raw;
}

function applyEnvOverrides(cfg) {
  const result = { ...cfg };
  for (const key of Object.keys(DEFAULT_CONFIG)) {
    const envVar = 'PW_' + key.toUpperCase();
    const raw = process.env[envVar];
    if (raw !== undefined) {
      result[key] = parseEnvValue(raw, DEFAULT_CONFIG[key]);
    }
  }
  return result;
}

export class AppConfig {
  static load() {
    const base = loadConfig();
    const merged = applyEnvOverrides(base);
    validate(merged);
    return merged;
  }
}

export function listEnvOverrides() {
  const map = {};
  for (const k of Object.keys(DEFAULT_CONFIG)) {
    map['PW_' + k.toUpperCase()] = k;
  }
  return map;
}

export function exportConfig(cfg, dest) {
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  const ext = path.extname(dest).toLowerCase();
  if (ext === '.json') {
    fs.writeFileSync(dest, JSON.stringify(cfg, null, 2));
  } else if (ext === '.yaml' || ext === '.yml') {
    const lines = Object.entries(cfg)
      .map(([k, v]) => `${k}: ${v}\n`)
      .join('');
    fs.writeFileSync(dest, lines);
  } else {
    throw new Error('Unsupported export format: ' + ext);
  }
}

export function importConfig(src) {
  const ext = path.extname(src).toLowerCase();
  const text = fs.readFileSync(src, 'utf8');
  let data;
  if (ext === '.json') {
    data = JSON.parse(text);
  } else if (ext === '.yaml' || ext === '.yml') {
    data = {};
    for (const line of text.split(/\n/)) {
      if (!line.trim()) continue;
      const idx = line.indexOf(':');
      if (idx === -1) continue;
      const key = line.slice(0, idx).trim();
      const val = line.slice(idx + 1).trim();
      if (val === 'true' || val === 'false') {
        data[key] = val === 'true';
      } else if (!isNaN(Number(val))) {
        data[key] = Number(val);
      } else {
        data[key] = val;
      }
    }
  } else {
    throw new Error('Unsupported config format: ' + ext);
  }
  return { ...DEFAULT_CONFIG, ...data };
}

export function exportProfile(name, dest) {
  fs.copyFileSync(_profilePath(name), dest);
}

export function importProfile(src, name) {
  const cfg = importConfig(src);
  if (!name) name = path.basename(src, path.extname(src));
  saveConfig(cfg, name);
  return name;
}

export function deleteProfile(name) {
  try {
    fs.unlinkSync(_profilePath(name));
  } catch {}
}
