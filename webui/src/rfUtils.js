// RF utilities similar to those in Python rf_utils module

export function spectrumScan(centerFreq, { sampleRate = 2.4, numSamples = 256 } = {}) {
  const startFreq = centerFreq - sampleRate / 2;
  const freqs = Array.from({ length: numSamples }, (_, i) => startFreq + i * (sampleRate / numSamples));
  const power = freqs.map(() => Math.random() * 100 - 50);
  return [freqs, power];
}

export function demodulateFm(centerFreq, { audioRate = 1.0, duration = 1.0 } = {}) {
  const samples = Math.floor(duration * audioRate);
  const step = Math.PI / 2;
  return Array.from({ length: samples }, () => step);
}
