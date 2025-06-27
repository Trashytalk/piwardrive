"""Simple FM demodulation helpers using an RTL-SDR."""

from typing import List, cast

import numpy as np

try:
    from rtlsdr import RtlSdr
except Exception:  # pragma: no cover - import failure handled at runtime
    RtlSdr = None


def fm_demodulate(samples: np.ndarray) -> np.ndarray:
    """Return the demodulated FM audio from complex ``samples``."""
    return np.angle(samples[1:] * np.conj(samples[:-1]))


def demodulate_fm(
    center_freq: float,
    sample_rate: float = 2.4e6,
    audio_rate: float = 48e3,
    duration: float = 1.0,
) -> List[float]:
    """Capture ``duration`` seconds of FM audio around ``center_freq``."""
    if RtlSdr is None:
        raise RuntimeError("pyrtlsdr is not installed")

    sdr = RtlSdr()
    sdr.sample_rate = sample_rate
    sdr.center_freq = center_freq
    sdr.gain = "auto"

    num_samples = int(sample_rate * duration)
    samples = sdr.read_samples(num_samples)
    sdr.close()

    audio = fm_demodulate(samples)
    decim = max(int(sample_rate / audio_rate), 1)
    audio = audio[::decim]
    return cast(List[float], audio.tolist())
