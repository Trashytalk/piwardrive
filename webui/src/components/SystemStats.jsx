import { useEffect, useState } from 'react';

export default function SystemStats() {
  const [stats, setStats] = useState({ temp: null, mem: null, disk: null });

  useEffect(() => {
    const load = async () => {
      try {
        const [cpuRes, ramRes, diskRes] = await Promise.all([
          fetch('/cpu')
            .then((r) => r.json())
            .catch(() => null),
          fetch('/ram')
            .then((r) => r.json())
            .catch(() => null),
          fetch('/storage')
            .then((r) => r.json())
            .catch(() => null),
        ]);
        setStats({
          temp: cpuRes && cpuRes.temp != null ? cpuRes.temp : null,
          mem: ramRes && ramRes.percent != null ? ramRes.percent : null,
          disk: diskRes && diskRes.percent != null ? diskRes.percent : null,
        });
      } catch (_) {}
    };
    load();
    const id = setInterval(load, 2000);
    return () => clearInterval(id);
  }, []);

  const cpu = stats.temp != null ? `${stats.temp.toFixed(1)}\u00B0C` : 'N/A';
  const mem = stats.mem != null ? `${stats.mem.toFixed(0)}%` : 'N/A';
  const disk = stats.disk != null ? `${stats.disk.toFixed(0)}%` : 'N/A';

  return (
    <div>
      CPU: {cpu} | RAM: {mem} | Disk: {disk}
    </div>
  );
}
