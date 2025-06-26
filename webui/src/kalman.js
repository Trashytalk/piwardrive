export function kalman1d(series, q, r) {
  const arr = series.map(Number);
  if (arr.length === 0) return [];
  const P = (-q + Math.sqrt(q * q + 4 * q * r)) / 2;
  const K = (P + q) / (P + q + r);
  const res = [arr[0]];
  for (let i = 1; i < arr.length; i++) {
    res[i] = res[i - 1] * (1 - K) + K * arr[i];
  }
  return res;
}
