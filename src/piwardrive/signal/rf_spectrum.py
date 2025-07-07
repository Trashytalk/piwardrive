"""
RF Spectrum Intelligence Module for PiWardrive
Advanced signal analysis with FFT-based frequency domain processing
"""

import logging
import math
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, NamedTuple, Optional, Tuple

import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq

logger = logging.getLogger(__name__)


class InterferenceType(Enum):
    """Types of interference sources"""

    MICROWAVE = "microwave"
    BLUETOOTH = "bluetooth"
    ZIGBEE = "zigbee"
    RADAR = "radar"
    CORDLESS_PHONE = "cordless_phone"
    BABY_MONITOR = "baby_monitor"
    UNKNOWN = "unknown"

@dataclass
class FrequencyBand:
    """Frequency band definition"""

    start_freq: float
    end_freq: float
    center_freq: float
    bandwidth: float
    name: str

@dataclass
class SpectrumSample:
    """Spectrum analysis sample"""

    frequency: float
    power_dbm: float
    timestamp: float
    channel: Optional[int] = None

@dataclass
class InterferenceSource:
    """Detected interference source"""

    type: InterferenceType
    frequency: float
    power_dbm: float
    bandwidth: float
    confidence: float
    duration: float
    location: Optional[Tuple[float, float]] = None

@dataclass
class ChannelUtilization:
    """Channel utilization metrics"""

    channel: int
    frequency: float
    utilization_percent: float
    interference_level: float
    recommended_power: float
    quality_score: float

@dataclass
class PropagationModel:
    """Signal propagation model parameters"""

    path_loss_exponent: float
    reference_distance: float
    reference_loss: float
    shadowing_std: float
    frequency: float


class FFTProcessor:
    """FFT-based frequency domain processing"""

    def __init__(self, sample_rate: float = 1e6, window_size: int = 1024):
        self.sample_rate = sample_rate
        self.window_size = window_size
        self.window = signal.windows.hann(window_size)

    def compute_spectrum(self, samples: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Compute power spectrum from IQ samples"""
        # Apply window function
        windowed_samples = samples * self.window

        # Compute FFT
        fft_result = fft(windowed_samples)
        frequencies = fftfreq(len(fft_result), 1 / self.sample_rate)

        # Compute power spectrum in dBm
        power_spectrum = 20 * np.log10(np.abs(fft_result) + 1e-12)

        return frequencies, power_spectrum

    def detect_peaks(self, spectrum: np.ndarray, threshold: float = -60) -> List[int]:
        """Detect spectral peaks above threshold"""
        peaks, properties = signal.find_peaks(
            spectrum, height=threshold, distance=10, prominence=10
        )
        return peaks.tolist()



class InterferenceDetector:
    """Interference detection and source identification"""

    def __init__(self):
        self.interference_signatures = {
            InterferenceType.MICROWAVE: {
                "frequency_range": (2400e6, 2500e6),
                "bandwidth": 20e6,
                "power_threshold": -30,
                "duty_cycle": 0.5,
            },
            InterferenceType.BLUETOOTH: {
                "frequency_range": (2400e6, 2485e6),
                "bandwidth": 1e6,
                "power_threshold": -40,
                "duty_cycle": 0.1,
            },
            InterferenceType.ZIGBEE: {
                "frequency_range": (2405e6, 2480e6),
                "bandwidth": 2e6,
                "power_threshold": -50,
                "duty_cycle": 0.2,
            },
        }

    def identify_interference(
        self, spectrum_samples: List[SpectrumSample]
    ) -> List[InterferenceSource]:
        """Identify interference sources from spectrum data"""
        interference_sources = []

        for interference_type, signature in self.interference_signatures.items():
            sources = self._detect_signature(
                spectrum_samples, interference_type, signature
            )
            interference_sources.extend(sources)

        return interference_sources

    def _detect_signature(
        self,
        samples: List[SpectrumSample],
        interference_type: InterferenceType,
        signature: Dict,
    ) -> List[InterferenceSource]:
        """Detect specific interference signature"""
        sources = []
        freq_min, freq_max = signature["frequency_range"]

        # Filter samples in frequency range
        relevant_samples = [
            s
            for s in samples
            if freq_min <= s.frequency <= freq_max
            and s.power_dbm >= signature["power_threshold"]
        ]

        if not relevant_samples:
            return sources

        # Group samples by frequency clusters
        clusters = self._cluster_by_frequency(relevant_samples, signature["bandwidth"])

        for cluster in clusters:
            if len(cluster) >= 3:  # Minimum samples for detection
                center_freq = np.mean([s.frequency for s in cluster])
                avg_power = np.mean([s.power_dbm for s in cluster])
                duration = max([s.timestamp for s in cluster]) - min(
                    [s.timestamp for s in cluster]
                )

                confidence = self._calculate_confidence(cluster, signature)

                source = InterferenceSource(
                    type=interference_type,
                    frequency=center_freq,
                    power_dbm=avg_power,
                    bandwidth=signature["bandwidth"],
                    confidence=confidence,
                    duration=duration,
                )
                sources.append(source)

        return sources

    def _cluster_by_frequency(
        self, samples: List[SpectrumSample], bandwidth: float
    ) -> List[List[SpectrumSample]]:
        """Cluster samples by frequency proximity"""
        if not samples:
            return []

        # Sort by frequency
        sorted_samples = sorted(samples, key=lambda s: s.frequency)
        clusters = []
        current_cluster = [sorted_samples[0]]

        for sample in sorted_samples[1:]:
            if sample.frequency - current_cluster[-1].frequency <= bandwidth:
                current_cluster.append(sample)
            else:
                clusters.append(current_cluster)
                current_cluster = [sample]

        clusters.append(current_cluster)
        return clusters

    def _calculate_confidence(
        self, cluster: List[SpectrumSample], signature: Dict
    ) -> float:
        """Calculate confidence score for interference detection"""
        # Power consistency
        powers = [s.power_dbm for s in cluster]
        power_std = np.std(powers)
        power_score = max(0, 1 - power_std / 20)

        # Frequency consistency
        freqs = [s.frequency for s in cluster]
        freq_std = np.std(freqs)
        freq_score = max(0, 1 - freq_std / signature["bandwidth"])

        # Duration score
        duration = max([s.timestamp for s in cluster]) - min(
            [s.timestamp for s in cluster]
        )
        duration_score = min(1, duration / 60)  # Normalize to 1 minute

        return (power_score + freq_score + duration_score) / 3


class ChannelAnalyzer:
    """Channel utilization analysis with recommendations"""

    def __init__(self):
        self.wifi_channels = {
            1: 2412e6,
            2: 2417e6,
            3: 2422e6,
            4: 2427e6,
            5: 2432e6,
            6: 2437e6,
            7: 2442e6,
            8: 2447e6,
            9: 2452e6,
            10: 2457e6,
            11: 2462e6,
            12: 2467e6,
            13: 2472e6,
            36: 5180e6,
            40: 5200e6,
            44: 5220e6,
            48: 5240e6,
            52: 5260e6,
            56: 5280e6,
            60: 5300e6,
            64: 5320e6,
            100: 5500e6,
            104: 5520e6,
            108: 5540e6,
            112: 5560e6,
            116: 5580e6,
            120: 5600e6,
            124: 5620e6,
            128: 5640e6,
            132: 5660e6,
            136: 5680e6,
            140: 5700e6,
            144: 5720e6,
            149: 5745e6,
            153: 5765e6,
            157: 5785e6,
            161: 5805e6,
            165: 5825e6,
        }

    def analyze_channel_utilization(
        self,
        spectrum_samples: List[SpectrumSample],
        interference_sources: List[InterferenceSource],
    ) -> List[ChannelUtilization]:
        """Analyze channel utilization and provide recommendations"""
        channel_metrics = []

        for channel, frequency in self.wifi_channels.items():
            utilization = self._calculate_utilization(spectrum_samples, frequency)
            interference = self._calculate_interference_level(
                interference_sources, frequency
            )
            recommended_power = self._calculate_recommended_power(
                utilization, interference
            )
            quality_score = self._calculate_quality_score(utilization, interference)

            channel_metrics.append(
                ChannelUtilization(
                    channel=channel,
                    frequency=frequency,
                    utilization_percent=utilization,
                    interference_level=interference,
                    recommended_power=recommended_power,
                    quality_score=quality_score,
                )
            )

        return sorted(channel_metrics, key=lambda x: x.quality_score, reverse=True)

    def _calculate_utilization(
        self, samples: List[SpectrumSample], channel_freq: float
    ) -> float:
        """Calculate channel utilization percentage"""
        bandwidth = 20e6  # 20 MHz channel width
        freq_min = channel_freq - bandwidth / 2
        freq_max = channel_freq + bandwidth / 2

        # Get samples in channel bandwidth
        channel_samples = [s for s in samples if freq_min <= s.frequency <= freq_max]

        if not channel_samples:
            return 0.0

        # Calculate utilization based on power levels
        total_power = sum(10 ** (s.power_dbm / 10) for s in channel_samples)
        noise_floor = -95  # dBm
        noise_power = 10 ** (noise_floor / 10)

        utilization = min(100, (total_power - noise_power) / noise_power * 100)
        return max(0, utilization)

    def _calculate_interference_level(
        self, interference_sources: List[InterferenceSource], channel_freq: float
    ) -> float:
        """Calculate interference level for channel"""
        bandwidth = 20e6
        interference_level = 0

        for source in interference_sources:
            # Check if interference overlaps with channel
            if (
                abs(source.frequency - channel_freq)
                < (bandwidth + source.bandwidth) / 2
            ):
                # Calculate interference contribution
                distance = abs(source.frequency - channel_freq)
                overlap_factor = max(0, 1 - distance / (bandwidth / 2))
                interference_level += (
                    source.power_dbm * overlap_factor * source.confidence
                )

        return interference_level

    def _calculate_recommended_power(
        self, utilization: float, interference: float
    ) -> float:
        """Calculate recommended transmission power"""
        base_power = 20  # dBm

        # Adjust for utilization
        utilization_factor = 1 + (utilization / 100) * 0.5

        # Adjust for interference
        interference_factor = 1 + max(0, interference / 50)

        recommended = base_power * utilization_factor * interference_factor
        return min(30, max(10, recommended))  # Clamp between 10-30 dBm

    def _calculate_quality_score(
        self, utilization: float, interference: float
    ) -> float:
        """Calculate overall channel quality score"""
        utilization_score = max(0, 100 - utilization) / 100
        interference_score = max(0, 100 - abs(interference)) / 100

        return (utilization_score + interference_score) / 2


class PropagationModelCalculator:
    """Signal propagation modeling based on environmental factors"""

    def __init__(self):
        self.models = {
            "free_space": PropagationModel(2.0, 1.0, 32.45, 0, 2.4e9),
            "indoor": PropagationModel(3.0, 1.0, 40.0, 8.0, 2.4e9),
            "urban": PropagationModel(3.5, 1.0, 45.0, 12.0, 2.4e9),
            "suburban": PropagationModel(2.8, 1.0, 38.0, 6.0, 2.4e9),
        }

    def calculate_path_loss(
        self, distance: float, frequency: float, environment: str = "indoor"
    ) -> float:
        """Calculate path loss using propagation model"""
        if environment not in self.models:
            environment = "indoor"

        model = self.models[environment]

        # Update model frequency
        model.frequency = frequency

        # Calculate path loss in dB
        if distance <= model.reference_distance:
            return model.reference_loss

        # Log-distance path loss model
        path_loss = model.reference_loss + 10 * model.path_loss_exponent * math.log10(
            distance / model.reference_distance
        )

        return path_loss

    def predict_coverage(
        self,
        tx_power: float,
        rx_sensitivity: float,
        frequency: float,
        environment: str = "indoor",
    ) -> float:
        """Predict maximum coverage distance"""
        max_path_loss = tx_power - rx_sensitivity

        model = self.models[environment]

        # Solve for distance
        if max_path_loss <= model.reference_loss:
            return model.reference_distance

        distance = model.reference_distance * 10 ** (
            (max_path_loss - model.reference_loss) / (10 * model.path_loss_exponent)
        )

        return distance


class MultipathAnalyzer:
    """Multipath analysis for indoor positioning accuracy"""

    def __init__(self):
        self.speed_of_light = 3e8

    def analyze_multipath(
        self, channel_impulse_response: np.ndarray, sample_rate: float
    ) -> Dict:
        """Analyze multipath characteristics"""
        # Find peaks in channel impulse response
        peaks, properties = signal.find_peaks(
            np.abs(channel_impulse_response),
            height=0.1 * np.max(np.abs(channel_impulse_response)),
            distance=10,
        )

        if len(peaks) < 2:
            return {"multipath_present": False}

        # Calculate delay spread
        delays = peaks / sample_rate
        delay_spread = np.max(delays) - np.min(delays)

        # Calculate coherence bandwidth
        coherence_bandwidth = 1 / (5 * delay_spread)

        # Calculate multipath severity
        direct_path_power = np.abs(channel_impulse_response[peaks[0]]) ** 2
        total_power = np.sum(np.abs(channel_impulse_response) ** 2)
        k_factor = direct_path_power / (total_power - direct_path_power)

        return {
            "multipath_present": True,
            "delay_spread": delay_spread,
            "coherence_bandwidth": coherence_bandwidth,
            "k_factor": k_factor,
            "num_paths": len(peaks),
            "path_delays": delays.tolist(),
            "path_powers": [np.abs(channel_impulse_response[p]) ** 2 for p in peaks],
        }


class RFSpectrumIntelligence:
    """Main RF Spectrum Intelligence class"""

    def __init__(self):
        self.fft_processor = FFTProcessor()
        self.interference_detector = InterferenceDetector()
        self.channel_analyzer = ChannelAnalyzer()
        self.propagation_calculator = PropagationModelCalculator()
        self.multipath_analyzer = MultipathAnalyzer()

    def analyze_spectrum(self, iq_samples: np.ndarray, center_frequency: float) -> Dict:
        """Comprehensive spectrum analysis"""
        # Compute spectrum
        frequencies, power_spectrum = self.fft_processor.compute_spectrum(iq_samples)

        # Convert to absolute frequencies
        abs_frequencies = frequencies + center_frequency

        # Create spectrum samples
        spectrum_samples = [
            SpectrumSample(freq, power, 0.0)
            for freq, power in zip(abs_frequencies, power_spectrum)
        ]

        # Detect interference
        interference_sources = self.interference_detector.identify_interference(
            spectrum_samples
        )

        # Analyze channels
        channel_utilization = self.channel_analyzer.analyze_channel_utilization(
            spectrum_samples, interference_sources
        )

        # Find spectral peaks
        peaks = self.fft_processor.detect_peaks(power_spectrum)

        return {
            "spectrum_samples": spectrum_samples,
            "interference_sources": interference_sources,
            "channel_utilization": channel_utilization,
            "spectral_peaks": peaks,
            "frequency_range": (np.min(abs_frequencies), np.max(abs_frequencies)),
            "peak_power": np.max(power_spectrum),
            "noise_floor": np.percentile(power_spectrum, 10),
        }

    def get_channel_recommendations(self, analysis_result: Dict) -> List[Dict]:
        """Get channel recommendations based on analysis"""
        recommendations = []

        # Sort channels by quality score
        sorted_channels = sorted(
            analysis_result["channel_utilization"],
            key=lambda x: x.quality_score,
            reverse=True,
        )

        for i, channel in enumerate(sorted_channels[:5]):  # Top 5 channels
            recommendation = {
                "rank": i + 1,
                "channel": channel.channel,
                "frequency": channel.frequency,
                "quality_score": channel.quality_score,
                "utilization": channel.utilization_percent,
                "interference_level": channel.interference_level,
                "recommended_power": channel.recommended_power,
                "reason": self._get_recommendation_reason(channel),
            }
            recommendations.append(recommendation)

        return recommendations

    def _get_recommendation_reason(self, channel: ChannelUtilization) -> str:
        """Get human-readable reason for channel recommendation"""
        reasons = []

        if channel.utilization_percent < 30:
            reasons.append("low utilization")
        elif channel.utilization_percent < 60:
            reasons.append("moderate utilization")
        else:
            reasons.append("high utilization")

        if channel.interference_level < 10:
            reasons.append("minimal interference")
        elif channel.interference_level < 30:
            reasons.append("moderate interference")
        else:
            reasons.append("high interference")

        return f"Channel {channel.channel}: {', '.join(reasons)}"

# Example usage and testing
def test_rf_spectrum_intelligence():
    """Test RF spectrum intelligence functionality"""
    print("Testing RF Spectrum Intelligence...")

    # Create RF spectrum intelligence instance
    rf_intel = RFSpectrumIntelligence()

    # Generate sample IQ data (simulated)
    sample_rate = 20e6  # 20 MHz
    duration = 0.001  # 1 ms
    t = np.linspace(0, duration, int(sample_rate * duration))

    # Simulate signals
    signal1 = np.exp(1j * 2 * np.pi * 1e6 * t)  # 1 MHz offset
    signal2 = 0.5 * np.exp(1j * 2 * np.pi * 5e6 * t)  # 5 MHz offset
    noise = 0.1 * (np.random.randn(len(t)) + 1j * np.random.randn(len(t)))

    iq_samples = signal1 + signal2 + noise
    center_frequency = 2.4e9  # 2.4 GHz

    # Analyze spectrum
    analysis = rf_intel.analyze_spectrum(iq_samples, center_frequency)

    print(
        f"Frequency range: {analysis['frequency_range'][0]/1e6:.1f} - {analysis['frequency_range'][1]/1e6:.1f} MHz"
    )
    print(f"Peak power: {analysis['peak_power']:.1f} dBm")
    print(f"Noise floor: {analysis['noise_floor']:.1f} dBm")
    print(f"Detected interference sources: {len(analysis['interference_sources'])}")

    # Get channel recommendations
    recommendations = rf_intel.get_channel_recommendations(analysis)

    print("\nTop channel recommendations:")
    for rec in recommendations[:3]:
        print(
            f"  {rec['rank']}. Channel {rec['channel']} ({rec['frequency']/1e6:.0f} MHz)"
        )
        print(
            f"     Quality: {rec['quality_score']:.2f}, "
            f"Utilization: {rec['utilization']:.1f}%"
        )
        print(f"     {rec['reason']}")

    # Test propagation modeling
    print("\nPropagation modeling:")
    for distance in [1, 10, 50, 100]:
        path_loss = rf_intel.propagation_calculator.calculate_path_loss(
            distance, 2.4e9, "indoor"
        )
        print(f"  Distance {distance}m: Path loss = {path_loss:.1f} dB")

    print("RF Spectrum Intelligence test completed!")

if __name__ == "__main__":
    test_rf_spectrum_intelligence()
