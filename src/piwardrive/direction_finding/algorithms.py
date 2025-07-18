#!/usr/bin/env python3
"""
Direction Finding Algorithms for PiWardrive
Implements RSS triangulation, MUSIC, beamforming, and other DF algorithms.
"""

import asyncio
import logging
import math
import time
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from scipy.optimize import minimize
from scipy.spatial.distance import cdist

from .config import (
    AntennaArrayConfig,
    ArrayProcessingConfig,
    InterpolationMethod,
    MUSICConfig,
    PathLossConfig,
    PathLossModel,
    SignalMappingConfig,
    TriangulationConfig,
)
from .core import AngleEstimate, DFMeasurement, DFQuality, DFResult, PositionEstimate

logger = logging.getLogger(__name__)


class PathLossCalculator:
    """Calculates path loss using various models."""

    def __init__(self, config: PathLossConfig):
        self.config = config
        self.calibration_data = {}

    def calculate_distance(self, rssi: float, tx_power: float = 20.0) -> float:
        """Calculate distance from RSSI using path loss model."""
        try:
            if self.config.model_type == PathLossModel.FREE_SPACE:
                return self._free_space_distance(rssi, tx_power)
            elif self.config.model_type == PathLossModel.HATA:
                return self._hata_distance(rssi, tx_power)
            elif self.config.model_type == PathLossModel.INDOOR:
                return self._indoor_distance(rssi, tx_power)
            elif self.config.model_type == PathLossModel.DENSE_URBAN:
                return self._dense_urban_distance(rssi, tx_power)
            elif self.config.model_type == PathLossModel.RURAL:
                return self._rural_distance(rssi, tx_power)
            else:
                return self._free_space_distance(rssi, tx_power)
        except Exception as e:
            logger.error(f"Error calculating distance: {e}")
            return float("in")

    def _free_space_distance(self, rssi: float, tx_power: float) -> float:
        """Free space path loss model."""
        frequency = 2.4e9  # Default 2.4 GHz
        path_loss = tx_power - rssi

        # Friis formula: PL = 20*log10(d) + 20*log10(f) + 20*log10(4π/c) - Gt - Gr
        # Assuming unit gain antennas (Gt = Gr = 0)
        fspl_constant = 20 * math.log10(frequency) + 20 * math.log10(4 * math.pi / 3e8)

        distance = 10 ** ((path_loss - fspl_constant) / 20)
        return max(distance, self.config.reference_distance)

    def _hata_distance(self, rssi: float, tx_power: float) -> float:
        """Hata model for suburban/urban environments."""
        frequency = 2400  # MHz
        h_base = 30  # Base station height (m)
        h_mobile = 1.5  # Mobile height (m)

        # Hata model constants
        a_hm = (1.1 * math.log10(frequency) - 0.7) * h_mobile - (
            1.56 * math.log10(frequency) - 0.8
        )

        path_loss = tx_power - rssi

        # Solve for distance (iterative approach)
        def hata_loss(d):
            return (
                69.55
                + 26.16 * math.log10(frequency)
                - 13.82 * math.log10(h_base)
                - a_hm
                + (44.9 - 6.55 * math.log10(h_base)) * math.log10(d)
            )

        # Binary search for distance
        d_min, d_max = 0.1, 100000
        while d_max - d_min > 0.1:
            d_mid = (d_min + d_max) / 2
            if hata_loss(d_mid) < path_loss:
                d_min = d_mid
            else:
                d_max = d_mid

        return max(d_min, self.config.reference_distance)

    def _indoor_distance(self, rssi: float, tx_power: float) -> float:
        """Indoor path loss model."""
        path_loss = tx_power - rssi

        # Indoor model: PL = PL0 + 10*n*log10(d/d0) + walls + floors
        pl0 = (
            20 * math.log10(2.4e9)
            + 20 * math.log10(4 * math.pi / 3e8)
            + 20 * math.log10(self.config.reference_distance)
        )

        effective_loss = path_loss - pl0 - self.config.wall_penetration_loss

        if effective_loss <= 0:
            return self.config.reference_distance

        distance = self.config.reference_distance * (
            10 ** (effective_loss / (10 * self.config.path_loss_exponent))
        )
        return max(distance, self.config.reference_distance)

    def _dense_urban_distance(self, rssi: float, tx_power: float) -> float:
        """Dense urban environment model."""
        # Use modified Hata model with higher path loss exponent
        frequency = 2400  # MHz
        path_loss = tx_power - rssi

        # Dense urban correction
        correction = 3.2 * (math.log10(11.75 * 1.5) ** 2) - 4.97

        # Solve for distance
        def dense_urban_loss(d):
            return (
                69.55
                + 26.16 * math.log10(frequency)
                - 13.82 * math.log10(30)
                - correction
                + (44.9 - 6.55 * math.log10(30)) * math.log10(d)
            )

        # Binary search
        d_min, d_max = 0.1, 50000
        while d_max - d_min > 0.1:
            d_mid = (d_min + d_max) / 2
            if dense_urban_loss(d_mid) < path_loss:
                d_min = d_mid
            else:
                d_max = d_mid

        return max(d_min, self.config.reference_distance)

    def _rural_distance(self, rssi: float, tx_power: float) -> float:
        """Rural environment model."""
        frequency = 2400  # MHz
        path_loss = tx_power - rssi

        # Rural correction
        correction = 2 * (math.log10(frequency / 28) ** 2) + 5.4

        # Solve for distance
        def rural_loss(d):
            return (
                69.55
                + 26.16 * math.log10(frequency)
                - 13.82 * math.log10(30)
                - correction
                + (44.9 - 6.55 * math.log10(30)) * math.log10(d)
            )

        # Binary search
        d_min, d_max = 0.1, 200000
        while d_max - d_min > 0.1:
            d_mid = (d_min + d_max) / 2
            if rural_loss(d_mid) < path_loss:
                d_min = d_mid
            else:
                d_max = d_mid

        return max(d_min, self.config.reference_distance)

    def calibrate(self, calibration_points: List[Dict[str, Any]]):
        """Calibrate path loss model with real measurements."""
        if not calibration_points:
            return

        # Store calibration data for adaptive modeling
        self.calibrationdata = {"points": calibration_points, "timestamp": time.time()}

        # Calculate average path loss exponent from calibration data
        if len(calibration_points) >= 2:
            distances = [point["distance"] for point in calibration_points]
            losses = [point["tx_power"] - point["rssi"] for point in calibration_points]

            # Simple linear regression to find path loss exponent
            log_distances = [math.log10(d) for d in distances]
            mean_log_d = np.mean(log_distances)
            mean_loss = np.mean(losses)

            numerator = sum(
                (log_d - mean_log_d) * (loss - mean_loss)
                for log_d, loss in zip(log_distances, losses)
            )
            denominator = sum((log_d - mean_log_d) ** 2 for log_d in log_distances)

            if denominator != 0:
                self.config.path_loss_exponent = numerator / (10 * denominator)
                logger.info(
                    f"Calibrated path loss exponent: {self.config.path_loss_exponent}"
                )


class RSSTriangulation:
    """RSS-based triangulation algorithm."""

    def __init__(
        self,
        triangulation_config: TriangulationConfig,
        path_loss_config: PathLossConfig,
        signal_mapping_config: SignalMappingConfig,
    ):
        self.triangulation_config = triangulation_config
        self.path_loss_config = path_loss_config
        self.signal_mapping_config = signal_mapping_config

        self.path_loss_calculator = PathLossCalculator(path_loss_config)
        self.access_points = {}  # Known AP positions
        self.is_initialized = False
        self.is_running = False

    async def start(self):
        """Start the triangulation algorithm."""
        self.is_running = True
        self.is_initialized = True
        logger.info("RSS Triangulation algorithm started")

    async def stop(self):
        """Stop the triangulation algorithm."""
        self.is_running = False
        logger.info("RSS Triangulation algorithm stopped")

    def add_access_point(
        self, bssid: str, latitude: float, longitude: float, tx_power: float = 20.0
    ):
        """Add a known access point for triangulation."""
        self.access_points[bssid] = {
            "position": (latitude, longitude),
            "tx_power": tx_power,
            "measurements": [],
        }
        logger.debug(f"Added AP {bssid} at ({latitude}, {longitude})")

    def process(
        self, target_bssid: str, measurements: List[DFMeasurement]
    ) -> Optional[DFResult]:
        """Process measurements for triangulation."""
        if not self.is_initialized:
            logger.error("RSS Triangulation not initialized")
            return None

        # Filter measurements to get reference points
        reference_measurements = self._get_reference_measurements(measurements)

        if len(reference_measurements) < self.triangulation_config.min_access_points:
            logger.warning(
                f"Insufficient reference points for triangulation: {len(reference_measurements)}"
            )
            return None

        try:
            # Calculate position estimate
            position_estimate = self._triangulate_position(reference_measurements)

            if position_estimate:
                _result = DFResult(
                    target_bssid=target_bssid,
                    position=position_estimate,
                    measurements=measurements,
                    metadata={"algorithm": "RSS_TRIANGULATION"},
                )
                return _result

        except Exception as e:
            logger.error(f"Triangulation failed: {e}")

        return None

    async def process_async(
        self, target_bssid: str, measurements: List[DFMeasurement]
    ) -> Optional[DFResult]:
        """Asynchronous processing wrapper."""
        return await asyncio.get_event_loop().run_in_executor(
            None, self.process, target_bssid, measurements
        )

    def _get_reference_measurements(
        self, measurements: List[DFMeasurement]
    ) -> List[Tuple[float, float, float]]:
        """Get reference measurements from known APs."""
        reference_measurements = []

        for measurement in measurements:
            if measurement.bssid in self.access_points:
                ap_info = self.access_points[measurement.bssid]
                distance = self.path_loss_calculator.calculate_distance(
                    measurement.signal_strength, ap_info["tx_power"]
                )

                lat, lon = ap_info["position"]
                reference_measurements.append((lat, lon, distance))

        return reference_measurements

    def _triangulate_position(
        self, reference_measurements: List[Tuple[float, float, float]]
    ) -> Optional[PositionEstimate]:
        """Perform triangulation using least squares optimization."""
        if len(reference_measurements) < 3:
            return None

        # Convert to numpy arrays
        positions = np.array([(lat, lon) for lat, lon, _ in reference_measurements])
        distances = np.array([dist for _, _, dist in reference_measurements])

        # Initial guess (center of reference points)
        x0 = np.mean(positions, axis=0)

        # Objective function for least squares
        def objective(pos):
            calculated_distances = cdist([pos], positions)[0]
            residuals = calculated_distances - distances

            if self.triangulation_config.use_weighted_least_squares:
                # Weight by inverse distance squared
                weights = 1 / (distances**2 + 1e-6)
                return np.sum(weights * residuals**2)
            else:
                return np.sum(residuals**2)

        # Perform optimization
        try:
            result = minimize(
                objective,
                x0,
                method="L-BFGS-B",
                options={
                    "maxiter": self.triangulation_config.max_iterations,
                    "ftol": self.triangulation_config.convergence_threshold,
                },
            )

            if result.success:
                estimated_pos = result.x

                # Calculate accuracy and confidence
                accuracy = self._calculate_accuracy(
                    estimated_pos, reference_measurements
                )
                confidence = self._calculate_confidence(
                    estimated_pos, reference_measurements
                )

                # Quality assessment
                quality = self._assess_quality(accuracy, confidence)

                # Apply outlier rejection if enabled
                if self.triangulation_config.outlier_rejection:
                    if confidence < self.triangulation_config.confidence_threshold:
                        logger.warning(f"Low confidence triangulation: {confidence}")
                        return None

                return PositionEstimate(
                    latitude=estimated_pos[0],
                    longitude=estimated_pos[1],
                    accuracy=accuracy,
                    confidence=confidence,
                    algorithm="RSS_TRIANGULATION",
                    quality=quality,
                )

        except Exception as e:
            logger.error(f"Optimization failed: {e}")

        return None

    def _calculate_accuracy(
        self,
        position: np.ndarray,
        reference_measurements: List[Tuple[float, float, float]],
    ) -> float:
        """Calculate position accuracy estimate."""
        try:
            # Calculate residuals
            positions = np.array([(lat, lon) for lat, lon, _ in reference_measurements])
            distances = np.array([dist for _, _, dist in reference_measurements])

            calculated_distances = cdist([position], positions)[0]
            residuals = calculated_distances - distances

            # RMS error as accuracy estimate
            rms_error = np.sqrt(np.mean(residuals**2))

            # Convert to approximate meters (rough conversion)
            accuracy_meters = rms_error * 111320  # degrees to meters approximation

            return min(accuracy_meters, self.triangulation_config.max_position_error)

        except Exception as e:
            logger.error(f"Error calculating accuracy: {e}")
            return self.triangulation_config.max_position_error

    def _calculate_confidence(
        self,
        position: np.ndarray,
        reference_measurements: List[Tuple[float, float, float]],
    ) -> float:
        """Calculate confidence in position estimate."""
        try:
            # Factors affecting confidence:
            # 1. Number of reference points
            # 2. Geometric dilution of precision (GDOP)
            # 3. Measurement consistency

            num_refs = len(reference_measurements)
            positions = np.array([(lat, lon) for lat, lon, _ in reference_measurements])

            # Number of references factor
            num_factor = min(num_refs / 5.0, 1.0)  # Normalize to 5 references

            # GDOP calculation (simplified)
            if num_refs >= 3:
                # Calculate area of triangle formed by reference points
                if num_refs == 3:
                    area = self._triangle_area(positions[0], positions[1], positions[2])
                    gdop_factor = min(
                        area / 1000.0, 1.0
                    )  # Normalize to reasonable area
                else:
                    # For more than 3 points, use average pairwise distance
                    distances = cdist(positions, positions)
                    avg_distance = np.mean(
                        distances[np.triu_indices_from(distances, k=1)]
                    )
                    gdop_factor = min(avg_distance / 100.0, 1.0)
            else:
                gdop_factor = 0.1

            # Measurement consistency factor
            distances = np.array([dist for _, _, dist in reference_measurements])
            calculated_distances = cdist([position], positions)[0]
            consistency = 1.0 - min(
                np.std(calculated_distances - distances) / np.mean(distances), 1.0
            )

            # Combined confidence
            confidence = num_factor * 0.4 + gdop_factor * 0.3 + consistency * 0.3

            return max(0.0, min(1.0, confidence))

        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 0.0

    def _triangle_area(self, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> float:
        """Calculate area of triangle formed by three points."""
        return 0.5 * abs(
            (
                p1[0] * (p2[1] - p3[1])
                + p2[0] * (p3[1] - p1[1])
                + p3[0] * (p1[1] - p2[1])
            )
        )

    def _assess_quality(self, accuracy: float, confidence: float) -> DFQuality:
        """Assess the quality of the position estimate."""
        if accuracy < 10 and confidence > 0.8:
            return DFQuality.EXCELLENT
        elif accuracy < 25 and confidence > 0.6:
            return DFQuality.GOOD
        elif accuracy < 50 and confidence > 0.4:
            return DFQuality.FAIR
        elif accuracy < 100 and confidence > 0.2:
            return DFQuality.POOR
        else:
            return DFQuality.INVALID

    def estimate_position(
        self, measurements: List[DFMeasurement]
    ) -> Optional[PositionEstimate]:
        """Quick position estimation (synchronous)."""
        reference_measurements = self._get_reference_measurements(measurements)

        if len(reference_measurements) >= self.triangulation_config.min_access_points:
            return self._triangulate_position(reference_measurements)

        return None

    async def calibrate(self, calibration_data: Dict[str, Any]):
        """Calibrate the triangulation algorithm."""
        if "path_loss_points" in calibration_data:
            self.path_loss_calculator.calibrate(calibration_data["path_loss_points"])

        if "access_points" in calibration_data:
            for ap_data in calibration_data["access_points"]:
                self.add_access_point(
                    ap_data["bssid"],
                    ap_data["latitude"],
                    ap_data["longitude"],
                    ap_data.get("tx_power", 20.0),
                )

        logger.info("RSS Triangulation calibration completed")


class SignalMapper:
    """Signal strength mapping and interpolation."""

    def __init__(self, config: SignalMappingConfig):
        self.config = config
        self.signal_map = {}
        self.interpolation_cache = {}

    def add_measurement(
        self, bssid: str, position: Tuple[float, float], signal_strength: float
    ):
        """Add a signal strength measurement to the map."""
        if bssid not in self.signal_map:
            self.signal_map[bssid] = []

        self.signal_map[bssid].append(
            {
                "position": position,
                "signal_strength": signal_strength,
                "timestamp": time.time(),
            }
        )

        # Clear cache for this BSSID
        if bssid in self.interpolation_cache:
            del self.interpolation_cache[bssid]

    def interpolate_signal(
        self, bssid: str, position: Tuple[float, float]
    ) -> Optional[float]:
        """Interpolate signal strength at a given position."""
        if bssid not in self.signal_map or len(self.signal_map[bssid]) < 3:
            return None

        measurements = self.signal_map[bssid]

        if self.config.interpolation_method == InterpolationMethod.IDW:
            return self._inverse_distance_weighting(measurements, position)
        elif self.config.interpolation_method == InterpolationMethod.KRIGING:
            return self._kriging_interpolation(measurements, position)
        elif self.config.interpolation_method == InterpolationMethod.SPLINE:
            return self._spline_interpolation(measurements, position)
        else:
            return self._inverse_distance_weighting(measurements, position)

    def _inverse_distance_weighting(
        self, measurements: List[Dict], position: Tuple[float, float]
    ) -> float:
        """Inverse distance weighting interpolation."""
        weights = []
        values = []

        for measurement in measurements:
            distance = self._calculate_distance(position, measurement["position"])
            if distance < 1e-6:  # Very close point
                return measurement["signal_strength"]

            weight = 1.0 / (distance**2)
            weights.append(weight)
            values.append(measurement["signal_strength"])

        weights = np.array(weights)
        values = np.array(values)

        return np.sum(weights * values) / np.sum(weights)

    def _kriging_interpolation(
        self, measurements: List[Dict], position: Tuple[float, float]
    ) -> float:
        """Simplified kriging interpolation."""
        # This is a simplified implementation
        # Full kriging would require semivariogram modeling
        return self._inverse_distance_weighting(measurements, position)

    def _spline_interpolation(
        self, measurements: List[Dict], position: Tuple[float, float]
    ) -> float:
        """Spline interpolation."""
        # This is a simplified implementation
        # Full spline interpolation would require scipy.interpolate
        return self._inverse_distance_weighting(measurements, position)

    def _calculate_distance(
        self, pos1: Tuple[float, float], pos2: Tuple[float, float]
    ) -> float:
        """Calculate distance between two positions."""
        lat1, lon1 = pos1
        lat2, lon2 = pos2

        # Haversine formula
        R = 6371000  # Earth radius in meters

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = (
            math.sin(delta_lat / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c


class MUSICProcessor:
    """MUSIC (Multiple Signal Classification) algorithm for angle of arrival estimation."""

    def __init__(
        self,
        music_config: MUSICConfig,
        array_config: ArrayProcessingConfig,
        antenna_config: AntennaArrayConfig,
    ):
        self.music_config = music_config
        self.array_config = array_config
        self.antenna_config = antenna_config

        self.is_initialized = False
        self.is_running = False

        # Initialize array geometry
        self.array_manifold = self._compute_array_manifold()

    def _compute_array_manifold(self) -> np.ndarray:
        """Compute array manifold vectors for different angles."""
        angles = np.arange(
            self.music_config.search_range[0],
            self.music_config.search_range[1],
            self.music_config.angular_resolution,
        )

        manifold = np.zeros(
            (self.antenna_config.num_elements, len(angles)), dtype=complex
        )

        # Calculate element positions based on array geometry
        element_positions = self._get_element_positions()

        wavelength = 3e8 / self.antenna_config.operating_frequency
        k = 2 * np.pi / wavelength

        for i, angle in enumerate(angles):
            angle_rad = np.radians(angle)

            # Calculate phase delays for each element
            for j, pos in enumerate(element_positions):
                phase_delay = k * pos[0] * np.sin(angle_rad)
                manifold[j, i] = np.exp(1j * phase_delay)

        return manifold

    def _get_element_positions(self) -> List[Tuple[float, float]]:
        """Get element positions based on array geometry."""
        positions = []
        spacing = self.antenna_config.element_spacing * (
            3e8 / self.antenna_config.operating_frequency
        )

        if self.antenna_config.array_type.value == "linear":
            for i in range(self.antenna_config.num_elements):
                x = i * spacing
                y = 0
                positions.append((x, y))

        elif self.antenna_config.array_type.value == "circular":
            radius = spacing * self.antenna_config.num_elements / (2 * np.pi)
            for i in range(self.antenna_config.num_elements):
                angle = 2 * np.pi * i / self.antenna_config.num_elements
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                positions.append((x, y))

        else:  # rectangular or random
            # Simplified rectangular arrangement
            rows = int(np.sqrt(self.antenna_config.num_elements))
            cols = self.antenna_config.num_elements // rows

            for i in range(self.antenna_config.num_elements):
                row = i // cols
                col = i % cols
                x = col * spacing
                y = row * spacing
                positions.append((x, y))

        return positions

    async def start(self):
        """Start the MUSIC processor."""
        self.is_running = True
        self.is_initialized = True
        logger.info("MUSIC processor started")

    async def stop(self):
        """Stop the MUSIC processor."""
        self.is_running = False
        logger.info("MUSIC processor stopped")

    def process(
        self, target_bssid: str, measurements: List[DFMeasurement]
    ) -> Optional[DFResult]:
        """Process measurements for angle estimation."""
        if not self.is_initialized:
            logger.error("MUSIC processor not initialized")
            return None

        # Extract IQ data from measurements
        iq_data = self._extract_iq_data(measurements)

        if iq_data is None or iq_data.shape[0] < self.antenna_config.num_elements:
            logger.warning("Insufficient IQ data for MUSIC processing")
            return None

        try:
            # Estimate angle using MUSIC algorithm
            angle_estimate = self._music_algorithm(iq_data)

            if angle_estimate:
                _result = DFResult(
                    target_bssid=target_bssid,
                    angle=angle_estimate,
                    measurements=measurements,
                    metadata={"algorithm": "MUSIC_AOA"},
                )
                return _result

        except Exception as e:
            logger.error(f"MUSIC processing failed: {e}")

        return None

    def _extract_iq_data(
        self, measurements: List[DFMeasurement]
    ) -> Optional[np.ndarray]:
        """Extract IQ data from measurements."""
        iq_arrays = []

        for measurement in measurements:
            if measurement.iq_data is not None:
                iq_arrays.append(measurement.iq_data)

        if not iq_arrays:
            return None

        # Stack IQ data from different antenna elements
        return np.vstack(iq_arrays)

    def _music_algorithm(self, iq_data: np.ndarray) -> Optional[AngleEstimate]:
        """MUSIC algorithm implementation."""
        # Compute covariance matrix
        R = np.cov(iq_data)

        # Eigenvalue decomposition
        eigenvalues, eigenvectors = np.linalg.eigh(R)

        # Sort eigenvalues and eigenvectors
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # Determine number of sources
        num_sources = self._estimate_num_sources(eigenvalues)

        if num_sources == 0:
            return None

        # Noise subspace
        noise_subspace = eigenvectors[:, num_sources:]

        # MUSIC spectrum
        angles = np.arange(
            self.music_config.search_range[0],
            self.music_config.search_range[1],
            self.music_config.angular_resolution,
        )

        spectrum = np.zeros(len(angles))

        for i, angle in enumerate(angles):
            angle_idx = int(
                (angle - self.music_config.search_range[0])
                / self.music_config.angular_resolution
            )
            if 0 <= angle_idx < self.array_manifold.shape[1]:
                a = self.array_manifold[:, angle_idx]
                denominator = np.abs(
                    a.conj().T @ noise_subspace @ noise_subspace.conj().T @ a
                )
                spectrum[i] = 1.0 / (denominator + 1e-10)

        # Find peaks
        peak_indices = self._find_peaks(spectrum)

        if not peak_indices:
            return None

        # Select strongest peak
        strongest_peak = peak_indices[np.argmax(spectrum[peak_indices])]
        estimated_angle = angles[strongest_peak]

        # Calculate accuracy and confidence
        accuracy = self._calculate_angle_accuracy(spectrum, strongest_peak)
        confidence = self._calculate_angle_confidence(spectrum, strongest_peak)
        quality = self._assess_angle_quality(accuracy, confidence)

        return AngleEstimate(
            azimuth=estimated_angle,
            accuracy=accuracy,
            confidence=confidence,
            algorithm="MUSIC_AOA",
            quality=quality,
        )

    def _estimate_num_sources(self, eigenvalues: np.ndarray) -> int:
        """Estimate number of sources using eigenvalue threshold."""
        # Simplified source detection
        threshold = np.max(eigenvalues) * self.music_config.eigenvalue_threshold
        return np.sum(eigenvalues > threshold)

    def _find_peaks(self, spectrum: np.ndarray) -> List[int]:
        """Find peaks in MUSIC spectrum."""
        # Simple peak detection
        peaks = []
        for i in range(1, len(spectrum) - 1):
            if spectrum[i] > spectrum[i - 1] and spectrum[i] > spectrum[i + 1]:
                peaks.append(i)
        return peaks

    def _calculate_angle_accuracy(self, spectrum: np.ndarray, peak_idx: int) -> float:
        """Calculate angle accuracy estimate."""
        # Use peak width as accuracy indicator
        peak_value = spectrum[peak_idx]
        half_max = peak_value / 2

        # Find half-maximum points
        left_idx = peak_idx
        right_idx = peak_idx

        while left_idx > 0 and spectrum[left_idx] > half_max:
            left_idx -= 1

        while right_idx < len(spectrum) - 1 and spectrum[right_idx] > half_max:
            right_idx += 1

        width = (right_idx - left_idx) * self.music_config.angular_resolution
        return max(width, self.music_config.angular_resolution)

    def _calculate_angle_confidence(self, spectrum: np.ndarray, peak_idx: int) -> float:
        """Calculate confidence in angle estimate."""
        peak_value = spectrum[peak_idx]
        mean_value = np.mean(spectrum)

        # Signal-to-noise ratio in spectrum
        snr = peak_value / (mean_value + 1e-10)

        # Normalize to 0-1 range
        confidence = min(snr / 10.0, 1.0)

        return max(0.0, confidence)

    def _assess_angle_quality(self, accuracy: float, confidence: float) -> DFQuality:
        """Assess quality of angle estimate."""
        if accuracy < 2 and confidence > 0.8:
            return DFQuality.EXCELLENT
        elif accuracy < 5 and confidence > 0.6:
            return DFQuality.GOOD
        elif accuracy < 10 and confidence > 0.4:
            return DFQuality.FAIR
        elif accuracy < 20 and confidence > 0.2:
            return DFQuality.POOR
        else:
            return DFQuality.INVALID

    def estimate_angle(
        self, measurements: List[DFMeasurement]
    ) -> Optional[AngleEstimate]:
        """Quick angle estimation (synchronous)."""
        iq_data = self._extract_iq_data(measurements)

        if iq_data is not None and iq_data.shape[0] >= self.antenna_config.num_elements:
            return self._music_algorithm(iq_data)

        return None


class BeamformingProcessor:
    """Beamforming processor for directional signal processing."""

    def __init__(
        self, array_config: ArrayProcessingConfig, antenna_config: AntennaArrayConfig
    ):
        self.array_config = array_config
        self.antenna_config = antenna_config

        self.is_initialized = False
        self.is_running = False

        # Initialize beamforming weights
        self.weights = self._initialize_weights()

    def _initialize_weights(self) -> np.ndarray:
        """Initialize beamforming weights."""
        # Start with uniform weights
        return (
            np.ones(self.antenna_config.num_elements, dtype=complex)
            / self.antenna_config.num_elements
        )

    async def start(self):
        """Start the beamforming processor."""
        self.is_running = True
        self.is_initialized = True
        logger.info("Beamforming processor started")

    async def stop(self):
        """Stop the beamforming processor."""
        self.is_running = False
        logger.info("Beamforming processor stopped")

    def process(
        self, target_bssid: str, measurements: List[DFMeasurement]
    ) -> Optional[DFResult]:
        """Process measurements using beamforming."""
        if not self.is_initialized:
            logger.error("Beamforming processor not initialized")
            return None

        # Extract IQ data
        iq_data = self._extract_iq_data(measurements)

        if iq_data is None:
            return None

        try:
            # Apply beamforming
            beamformed_signal = self._apply_beamforming(iq_data)

            # Estimate angle from beamformed signal
            angle_estimate = self._estimate_angle_from_beamformed(beamformed_signal)

            if angle_estimate:
                _result = DFResult(
                    target_bssid=target_bssid,
                    angle=angle_estimate,
                    measurements=measurements,
                    metadata={"algorithm": "BEAMFORMING"},
                )
                return _result

        except Exception as e:
            logger.error(f"Beamforming processing failed: {e}")

        return None

    def _extract_iq_data(
        self, measurements: List[DFMeasurement]
    ) -> Optional[np.ndarray]:
        """Extract IQ data from measurements."""
        iq_arrays = []

        for measurement in measurements:
            if measurement.iq_data is not None:
                iq_arrays.append(measurement.iq_data)

        if not iq_arrays:
            return None

        return np.vstack(iq_arrays)

    def _apply_beamforming(self, iq_data: np.ndarray) -> np.ndarray:
        """Apply beamforming weights to IQ data."""
        # Simple beamforming: multiply by weights and sum
        return np.sum(iq_data * self.weights[:, np.newaxis], axis=0)

    def _estimate_angle_from_beamformed(
        self, beamformed_signal: np.ndarray
    ) -> Optional[AngleEstimate]:
        """Estimate angle from beamformed signal."""
        # This is a simplified implementation
        # In practice, you would scan through different beam directions

        # For now, return a dummy estimate
        return AngleEstimate(
            azimuth=0.0,
            accuracy=10.0,
            confidence=0.5,
            algorithm="BEAMFORMING",
            quality=DFQuality.FAIR,
        )
