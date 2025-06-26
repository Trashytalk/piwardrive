import os
import sys
import numpy as np


import pytest

from piwardrive.sigint_suite.rf.spectrum import spectrum_scan
from piwardrive.sigint_suite.rf.demod import demodulate_fm
from piwardrive.sigint_suite.rf import demod as demod_module
from piwardrive.sigint_suite.rf.utils import (
    hz_to_khz,
    hz_to_mhz,
    mhz_to_hz,
    parse_frequency,
)


class DummySdr:
    def __init__(self):
        DummySdr.instance = self
        self.sample_rate = None
        self.center_freq = None
        self.gain = None

    def read_samples(self, n):
        return np.ones(n, dtype=np.complex64)

    def close(self):
        pass


def test_spectrum_scan_returns_power(monkeypatch):
    monkeypatch.setattr("piwardrive.sigint_suite.rf.spectrum.RtlSdr", DummySdr)
    freqs, power = spectrum_scan(100.0, sample_rate=4.0, num_samples=4)
    assert len(freqs) == 4
    assert len(power) == 4
    assert freqs[0] == 100.0 - 2.0
    sdr = DummySdr.instance
    assert sdr.sample_rate == 4.0
    assert sdr.center_freq == 100.0
    assert sdr.gain == "auto"


class SignalSdr(DummySdr):
    def read_samples(self, n):
        t = np.arange(n)
        return np.exp(1j * 2 * np.pi * 0.25 * t).astype(np.complex64)


def test_demodulate_fm(monkeypatch):
    monkeypatch.setattr("piwardrive.sigint_suite.rf.demod.RtlSdr", SignalSdr)
    audio = demodulate_fm(100.0, sample_rate=8.0, audio_rate=2.0, duration=1.0)
    assert len(audio) == 2
    for val in audio:
        assert abs(val - np.pi / 2) < 1e-6
    sdr = SignalSdr.instance
    assert sdr.sample_rate == 8.0
    assert sdr.center_freq == 100.0
    assert sdr.gain == "auto"


def test_missing_rtlsdr(monkeypatch):
    monkeypatch.setattr("piwardrive.sigint_suite.rf.spectrum.RtlSdr", None)
    with pytest.raises(RuntimeError):
        spectrum_scan(100.0)
    monkeypatch.setattr("piwardrive.sigint_suite.rf.demod.RtlSdr", None)
    with pytest.raises(RuntimeError):
        demodulate_fm(100.0)


def test_fm_demodulate_basic():
    samples = np.exp(1j * np.linspace(0, np.pi, 5))
    demod = demod_module.fm_demodulate(samples)
    assert np.allclose(demod, np.full(4, np.pi / 4))


def test_frequency_conversions():
    assert mhz_to_hz(100.0) == 100.0 * 1_000_000.0
    assert hz_to_mhz(50_000_000.0) == 50.0
    assert hz_to_khz(30_000.0) == 30.0


def test_parse_frequency():
    assert parse_frequency("2.4GHz") == 2.4e9
    assert parse_frequency("100MHz") == 100e6
    assert parse_frequency("200kHz") == 200e3
    assert parse_frequency("300") == 300.0
