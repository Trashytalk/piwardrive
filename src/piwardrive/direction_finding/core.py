#!/usr/bin/env python3
"""
Core Direction Finding Engine for PiWardrive
Provides the main engine and data structures for direction finding operations.
"""

import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np

from .config import DFAlgorithm, DFConfiguration, get_df_config

logger = logging.getLogger(__name__)


class DFQuality(Enum):
    """Quality indicators for DF results."""

    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    INVALID = "invalid"


@dataclass
class PositionEstimate:
    """Position estimate result from DF algorithms."""

    latitude: float
    longitude: float
    altitude: Optional[float] = None
    accuracy: float = 0.0  # meters
    confidence: float = 0.0  # 0-1 range
    timestamp: float = field(default_factory=time.time)
    algorithm: str = "unknown"
    quality: DFQuality = DFQuality.INVALID

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude": self.altitude,
            "accuracy": self.accuracy,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "algorithm": self.algorithm,
            "quality": self.quality.value,
        }


@dataclass
class AngleEstimate:
    """Angle of arrival estimate from DF algorithms."""

    azimuth: float  # degrees, 0-360
    elevation: Optional[float] = None  # degrees, -90 to 90
    accuracy: float = 0.0  # degrees
    confidence: float = 0.0  # 0-1 range
    timestamp: float = field(default_factory=time.time)
    algorithm: str = "unknown"
    quality: DFQuality = DFQuality.INVALID

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "azimuth": self.azimuth,
            "elevation": self.elevation,
            "accuracy": self.accuracy,
            "confidence": self.confidence,
            "timestamp": self.timestamp,
            "algorithm": self.algorithm,
            "quality": self.quality.value,
        }


@dataclass
class DFMeasurement:
    """Raw measurement data for DF processing."""

    signal_strength: float  # dBm
    frequency: float  # Hz
    bssid: str
    timestamp: float = field(default_factory=time.time)
    position: Optional[Tuple[float, float]] = None  # (lat, lon)
    angle: Optional[float] = None  # degrees
    phase: Optional[float] = None  # radians
    iq_data: Optional[np.ndarray] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "signal_strength": self.signal_strength,
            "frequency": self.frequency,
            "bssid": self.bssid,
            "timestamp": self.timestamp,
            "position": self.position,
            "angle": self.angle,
            "phase": self.phase,
            "iq_data": self.iq_data.tolist() if self.iq_data is not None else None,
        }


@dataclass
class DFResult:
    """Complete direction finding result."""

    target_bssid: str
    position: Optional[PositionEstimate] = None
    angle: Optional[AngleEstimate] = None
    measurements: List[DFMeasurement] = field(default_factory=list)
    processing_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "target_bssid": self.target_bssid,
            "position": self.position.to_dict() if self.position else None,
            "angle": self.angle.to_dict() if self.angle else None,
            "measurements": [m.to_dict() for m in self.measurements],
            "processing_time": self.processing_time,
            "metadata": self.metadata,
        }


class DFEngine:
    """Main Direction Finding engine that coordinates all DF operations."""

    def __init__(self, config: Optional[DFConfiguration] = None):
        self.config = config or get_df_config()
        self.algorithms = {}
        self.hardware_managers = {}
        self.is_running = False
        self.results_cache = {}
        self.performance_metrics = {
            "total_estimates": 0,
            "successful_estimates": 0,
            "average_processing_time": 0.0,
            "last_update": time.time(),
        }

        self._initialize_algorithms()
        self._initialize_hardware()

        logger.info(f"DF Engine initialized with {len(self.algorithms)} algorithms")

    def _initialize_algorithms(self):
        """Initialize DF algorithms based on configuration."""
        from .algorithms import BeamformingProcessor, MUSICProcessor, RSSTriangulation

        for algorithm in self.config.enabled_algorithms:
            try:
                if algorithm == DFAlgorithm.RSS_TRIANGULATION:
                    self.algorithms[algorithm] = RSSTriangulation(
                        self.config.triangulation,
                        self.config.path_loss,
                        self.config.signal_mapping,
                    )
                elif algorithm == DFAlgorithm.MUSIC_AOA:
                    self.algorithms[algorithm] = MUSICProcessor(
                        self.config.music,
                        self.config.array_processing,
                        self.config.antenna_array,
                    )
                elif algorithm == DFAlgorithm.BEAMFORMING:
                    self.algorithms[algorithm] = BeamformingProcessor(
                        self.config.array_processing, self.config.antenna_array
                    )

                logger.info(f"Initialized algorithm: {algorithm.value}")
            except Exception as e:
                logger.error(f"Failed to initialize algorithm {algorithm.value}: {e}")

    def _initialize_hardware(self):
        """Initialize hardware managers."""
        from .hardware import AntennaArrayManager, WiFiAdapterManager

        try:
            self.hardware_managers["wifi"] = WiFiAdapterManager(
                self.config.wifi_adapter
            )
            self.hardware_managers["antenna"] = AntennaArrayManager(
                self.config.antenna_array
            )
            logger.info("Hardware managers initialized")
        except Exception as e:
            logger.error(f"Failed to initialize hardware managers: {e}")

    async def start(self):
        """Start the DF engine."""
        if self.is_running:
            logger.warning("DF Engine is already running")
            return

        self.is_running = True

        # Start hardware managers
        for manager in self.hardware_managers.values():
            if hasattr(manager, "start"):
                await manager.start()

        # Start algorithms
        for algorithm in self.algorithms.values():
            if hasattr(algorithm, "start"):
                await algorithm.start()

        logger.info("DF Engine started")

    async def stop(self):
        """Stop the DF engine."""
        if not self.is_running:
            return

        self.is_running = False

        # Stop algorithms
        for algorithm in self.algorithms.values():
            if hasattr(algorithm, "stop"):
                await algorithm.stop()

        # Stop hardware managers
        for manager in self.hardware_managers.values():
            if hasattr(manager, "stop"):
                await manager.stop()

        logger.info("DF Engine stopped")

    async def process_measurements(
        self, measurements: List[DFMeasurement]
    ) -> List[DFResult]:
        """Process measurements and return DF results."""
        if not self.is_running:
            raise RuntimeError("DF Engine is not running")

        results = []
        start_time = time.time()

        # Group measurements by target
        targets = {}
        for measurement in measurements:
            if measurement.bssid not in targets:
                targets[measurement.bssid] = []
            targets[measurement.bssid].append(measurement)

        # Process each target
        for bssid, target_measurements in targets.items():
            try:
                result = await self._process_target(bssid, target_measurements)
                if result:
                    results.append(result)
            except Exception as e:
                logger.error(f"Failed to process target {bssid}: {e}")

        # Update performance metrics
        processing_time = time.time() - start_time
        self._update_performance_metrics(len(results), processing_time)

        return results

    async def _process_target(
        self, bssid: str, measurements: List[DFMeasurement]
    ) -> Optional[DFResult]:
        """Process measurements for a specific target."""
        start_time = time.time()

        # Use primary algorithm
        primary_algorithm = self.algorithms.get(self.config.primary_algorithm)
        if not primary_algorithm:
            logger.error(
                f"Primary algorithm {self.config.primary_algorithm.value} not available"
            )
            return None

        try:
            # Process with primary algorithm
            result = await self._run_algorithm(primary_algorithm, bssid, measurements)

            # If primary algorithm fails, try fallback
            if not result and self.config.fallback_algorithm:
                fallback_algorithm = self.algorithms.get(self.config.fallback_algorithm)
                if fallback_algorithm:
                    result = await self._run_algorithm(
                        fallback_algorithm, bssid, measurements
                    )

            if result:
                result.processing_time = time.time() - start_time
                result.metadata["algorithm"] = self.config.primary_algorithm.value

                # Cache result
                self.results_cache[bssid] = result

                return result

        except Exception as e:
            logger.error(f"Error processing target {bssid}: {e}")

        return None

    async def _run_algorithm(
        self, algorithm, bssid: str, measurements: List[DFMeasurement]
    ) -> Optional[DFResult]:
        """Run a specific algorithm on measurements."""
        try:
            if hasattr(algorithm, "process_async"):
                return await algorithm.process_async(bssid, measurements)
            elif hasattr(algorithm, "process"):
                return algorithm.process(bssid, measurements)
            else:
                logger.error(
                    f"Algorithm {algorithm.__class__.__name__} has no process method"
                )
                return None
        except Exception as e:
            logger.error(f"Algorithm {algorithm.__class__.__name__} failed: {e}")
            return None

    def _update_performance_metrics(
        self, successful_results: int, processing_time: float
    ):
        """Update performance metrics."""
        self.performance_metrics["total_estimates"] += successful_results
        self.performance_metrics["successful_estimates"] += successful_results

        # Update average processing time
        current_avg = self.performance_metrics["average_processing_time"]
        total_estimates = self.performance_metrics["total_estimates"]

        if total_estimates > 0:
            self.performance_metrics["average_processing_time"] = (
                current_avg * (total_estimates - 1) + processing_time
            ) / total_estimates

        self.performance_metrics["last_update"] = time.time()

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        return self.performance_metrics.copy()

    def get_cached_result(self, bssid: str) -> Optional[DFResult]:
        """Get cached result for a target."""
        return self.results_cache.get(bssid)

    def clear_cache(self):
        """Clear the results cache."""
        self.results_cache.clear()

    def get_algorithm_status(self) -> Dict[str, Any]:
        """Get status of all algorithms."""
        status = {}
        for algorithm_type, algorithm in self.algorithms.items():
            status[algorithm_type.value] = {
                "available": True,
                "initialized": hasattr(algorithm, "is_initialized")
                and algorithm.is_initialized,
                "running": hasattr(algorithm, "is_running") and algorithm.is_running,
                "class": algorithm.__class__.__name__,
            }
        return status

    def get_hardware_status(self) -> Dict[str, Any]:
        """Get status of all hardware managers."""
        status = {}
        for manager_type, manager in self.hardware_managers.items():
            status[manager_type] = {
                "available": True,
                "initialized": hasattr(manager, "is_initialized")
                and manager.is_initialized,
                "running": hasattr(manager, "is_running") and manager.is_running,
                "class": manager.__class__.__name__,
            }
        return status

    def update_config(self, new_config: DFConfiguration):
        """Update the engine configuration."""
        self.config = new_config

        # Reinitialize algorithms and hardware if needed
        self._initialize_algorithms()
        self._initialize_hardware()

        logger.info("DF Engine configuration updated")

    async def calibrate(self, calibration_data: Dict[str, Any]) -> bool:
        """Calibrate the DF system."""
        try:
            # Calibrate algorithms
            for algorithm in self.algorithms.values():
                if hasattr(algorithm, "calibrate"):
                    await algorithm.calibrate(calibration_data)

            # Calibrate hardware
            for manager in self.hardware_managers.values():
                if hasattr(manager, "calibrate"):
                    await manager.calibrate(calibration_data)

            logger.info("DF system calibration completed")
            return True

        except Exception as e:
            logger.error(f"DF system calibration failed: {e}")
            return False

    def get_supported_algorithms(self) -> List[str]:
        """Get list of supported algorithms."""
        return [alg.value for alg in DFAlgorithm]

    def get_enabled_algorithms(self) -> List[str]:
        """Get list of enabled algorithms."""
        return [alg.value for alg in self.config.enabled_algorithms]

    def is_algorithm_available(self, algorithm: Union[str, DFAlgorithm]) -> bool:
        """Check if an algorithm is available."""
        if isinstance(algorithm, str):
            algorithm = DFAlgorithm(algorithm)
        return algorithm in self.algorithms

    def estimate_position(
        self, measurements: List[DFMeasurement]
    ) -> Optional[PositionEstimate]:
        """Quick position estimation (synchronous)."""
        if not measurements:
            return None

        # Use RSS triangulation for quick estimates
        triangulation = self.algorithms.get(DFAlgorithm.RSS_TRIANGULATION)
        if triangulation and hasattr(triangulation, "estimate_position"):
            return triangulation.estimate_position(measurements)

        return None

    def estimate_angle(
        self, measurements: List[DFMeasurement]
    ) -> Optional[AngleEstimate]:
        """Quick angle estimation (synchronous)."""
        if not measurements:
            return None

        # Use MUSIC for angle estimates
        music = self.algorithms.get(DFAlgorithm.MUSIC_AOA)
        if music and hasattr(music, "estimate_angle"):
            return music.estimate_angle(measurements)

        return None
