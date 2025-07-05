import { useEffect, useState } from 'react';

export default function SettingsForm() {
  const [config, setConfig] = useState(null);

  useEffect(() => {
    fetch('/config')
      .then((r) => r.json())
      .then(setConfig);
  }, []);

  const handleChange = (key, value) => {
    setConfig({ ...config, [key]: value });
  };

  const save = () => {
    fetch('/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config),
    })
      .then((r) => r.json())
      .then(setConfig);
  };

  if (!config) return null;

  const fields = [
    ['kismet_logdir', 'Kismet Log Directory', 'text'],
    ['bettercap_caplet', 'BetterCAP Caplet', 'text'],
    ['map_poll_gps', 'GPS Poll Interval', 'number'],
    ['map_poll_gps_max', 'GPS Poll Max', 'number'],
    ['map_poll_aps', 'AP Poll Interval', 'number'],
    ['map_poll_bt', 'BT Poll Interval', 'number'],
    ['health_poll_interval', 'Health Poll Interval', 'number'],
    ['log_rotate_interval', 'Log Rotate Interval', 'number'],
    ['log_rotate_archives', 'Log Rotate Archives', 'number'],
    ['cleanup_rotated_logs', 'Cleanup Rotated Logs', 'checkbox'],
    ['offline_tile_path', 'Offline Tile Path', 'text'],
    ['tile_maintenance_interval', 'Tile Maintenance Interval', 'number'],
    ['map_use_offline', 'Use Offline Tiles', 'checkbox'],
    ['map_auto_prefetch', 'Auto Prefetch Tiles', 'checkbox'],
    ['route_prefetch_interval', 'Route Prefetch Interval', 'number'],
    ['route_prefetch_lookahead', 'Route Prefetch Lookahead', 'number'],
    ['map_show_gps', 'Show GPS', 'checkbox'],
    ['map_show_aps', 'Show APs', 'checkbox'],
    ['map_show_bt', 'Show Bluetooth', 'checkbox'],
    ['map_cluster_aps', 'Cluster APs', 'checkbox'],
    ['map_cluster_capacity', 'Cluster Capacity', 'number'],
    ['debug_mode', 'Debug Mode', 'checkbox'],
    ['widget_battery_status', 'Battery Widget', 'checkbox'],
    ['ui_font_size', 'Font Size', 'number'],
    ['theme', 'Theme', 'text'],
  ];

  return (
    <section>
      <h2>Settings</h2>
      {fields.map(([key, label, type]) => (
        <div key={key}>
          <label>
            {label}{' '}
            {type === 'checkbox' ? (
              <input
                type="checkbox"
                checked={!!config[key]}
                onChange={(e) => handleChange(key, e.target.checked)}
              />
            ) : (
              <input
                type={type}
                value={config[key] ?? ''}
                onChange={(e) =>
                  handleChange(
                    key,
                    type === 'number' ? Number(e.target.value) : e.target.value
                  )
                }
              />
            )}
          </label>
        </div>
      ))}
      <button onClick={save}>Save</button>
    </section>
  );
}
