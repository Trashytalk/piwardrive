export function computeHealthStats(records) {
  if (!records || records.length === 0) return {};
  const temps = records.map(r => r.cpu_temp).filter(x => x != null);
  const cpu = records.map(r => r.cpu_percent);
  const mem = records.map(r => r.memory_percent);
  const disk = records.map(r => r.disk_percent);
  const avg = arr => arr.reduce((a, b) => a + b, 0) / arr.length;
  return {
    temp_avg: temps.length ? avg(temps) : Number.NaN,
    cpu_avg: avg(cpu),
    mem_avg: avg(mem),
    disk_avg: avg(disk),
  };
}
