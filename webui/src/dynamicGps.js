export function adjustGpsInterval(last, speed, poll, max, threshold) {
  if (speed > threshold) return poll;
  const current = last || poll;
  return Math.min(max, Math.max(poll, current * 2));
}
