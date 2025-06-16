import os
import sys
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sigint_suite.rf.spectrum import spectrum_scan
from sigint_suite.rf.demod import demodulate_fm


class DummySdr:
    def __init__(self):
        self.sample_rate = None
        self.center_freq = None
        self.gain = None

    def read_samples(self, n):
        return np.ones(n, dtype=np.complex64)

    def close(self):
        pass


def test_spectrum_scan_returns_power(monkeypatch):
    monkeypatch.setattr("sigint_suite.rf.spectrum.RtlSdr", DummySdr)
    freqs, power = spectrum_scan(100.0, sample_rate=4.0, num_samples=4)
    assert len(freqs) == 4
    assert len(power) == 4
    assert freqs[0] == 100.0 - 2.0


class SignalSdr(DummySdr):
    def read_samples(self, n):
        t = np.arange(n)
        return np.exp(1j * 2 * np.pi * 0.25 * t).astype(np.complex64)


def test_demodulate_fm(monkeypatch):
    monkeypatch.setattr("sigint_suite.rf.demod.RtlSdr", SignalSdr)
    audio = demodulate_fm(100.0, sample_rate=8.0, audio_rate=2.0, duration=1.0)
    assert len(audio) == 2
    for val in audio:
        assert abs(val - np.pi / 2) < 1e-6
