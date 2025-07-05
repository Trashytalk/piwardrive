export async function scanOnce() {
  const [wifi, bluetooth] = await Promise.all([
    fetch('/scan/wifi')
      .then((r) => r.json())
      .catch(() => []),
    fetch('/scan/bluetooth')
      .then((r) => r.json())
      .catch(() => []),
  ]);
  return { wifi, bluetooth };
}

export function runContinuousScan({
  interval = 60,
  iterations = 0,
  onResult,
} = {}) {
  let count = 0;
  let active = true;

  const run = async () => {
    if (!active) return;
    const result = await scanOnce();
    if (onResult) onResult(result);
    count += 1;
    if (!active) return;
    if (iterations && count >= iterations) return;
    setTimeout(run, interval * 1000);
  };

  run();
  return () => {
    active = false;
  };
}
