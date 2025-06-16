"""Spectrum scanning utilities using an RTL-SDR."""

from typing import List, Tuple

import numpy as np

try:
    from rtlsdr import RtlSdr
except Exception:  # pragma: no cover - import failure handled at runtime
    RtlSdr = None  # type: ignore


def spectrum_scan(
    center_freq: float,
    sample_rate: float = 2.4e6,
    num_samples: int = 256 * 1024,
) -> Tuple[List[float], List[float]]:
    """Return frequency and power arrays around ``center_freq`` using an RTL-SDR."""
    if RtlSdr is None:
        raise RuntimeError("pyrtlsdr is not installed")

    sdr = RtlSdr()
    sdr.sample_rate = sample_rate
    sdr.center_freq = center_freq
    sdr.gain = "auto"

    samples = sdr.read_samples(num_samples)
    sdr.close()

    spectrum = np.fft.fftshift(np.fft.fft(samples))
    power = 20 * np.log10(np.abs(spectrum))
    freqs = (
        np.fft.fftshift(np.fft.fftfreq(len(samples), 1.0 / sample_rate)) + center_freq
    )
    return freqs.tolist(), power.tolist()
