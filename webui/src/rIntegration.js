// Minimal R integration stub used for testing
// In Python this wraps rpy2 to call an R script. Here we just simulate results.

export let rpy2Available = true;

export function setRpy2Available(val) {
  rpy2Available = val;
}

export async function healthSummary(csvPath, plotPath = null) {
  if (!rpy2Available) {
    throw new Error('rpy2 is required');
  }
  // Pretend to read CSV and compute a summary
  const response = await fetch(csvPath);
  const text = await response.text();
  const lines = text.trim().split(/\n+/);
  const values = lines.map((line) => parseFloat(line.split(',')[0] || '0'));
  const sum = values.reduce((a, b) => a + b, 0);
  const avg = values.length ? sum / values.length : 0;
  const result = { average: avg };
  if (plotPath) {
    // Real implementation would produce a plot; we just return the path
    result.plot = plotPath;
  }
  return result;
}
