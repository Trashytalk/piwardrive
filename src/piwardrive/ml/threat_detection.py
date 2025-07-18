"""
Machine Learning & AI Analytics Module for PiWardrive
Provides offline threat detection,
    anomaly detection,
    device fingerprinting,
    and risk assessment
"""

import hashlib
import json
import logging
import pickle
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


@dataclass
class DeviceFingerprint:
    """Device fingerprinting data structure"""

    mac_address: str
    oui_vendor: str
    device_type: str
    probe_requests: List[str]
    signal_patterns: List[float]
    timing_patterns: List[float]
    encryption_capabilities: List[str]
    supported_rates: List[str]
    power_management: bool
    vendor_elements: List[str]
    fingerprint_hash: str
    confidence_score: float
    last_seen: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {
            **asdict(self),
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
        }


@dataclass
class ThreatIndicator:
    """Threat indicator data structure"""

    threat_id: str
    threat_type: str
    severity: str
    confidence: float
    description: str
    indicators: List[str]
    mitigation: str
    timestamp: datetime
    affected_devices: List[str]
    network_context: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {**asdict(self), "timestamp": self.timestamp.isoformat()}


@dataclass
class RiskAssessment:
    """Risk assessment result"""

    network_id: str
    risk_score: float
    risk_level: str
    risk_factors: List[str]
    recommendations: List[str]
    compliance_status: Dict[str, bool]
    timestamp: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {**asdict(self), "timestamp": self.timestamp.isoformat()}


class OUIDatabase:
    """IEEE OUI (Organizationally Unique Identifier) database manager"""

    def __init__(self, oui_file_path: str = "data/oui.txt"):
        self.oui_file_path = Path(oui_file_path)
        self.oui_db = {}
        self.device_patterns = {}
        self._load_oui_database()
        self._load_device_patterns()

    def _load_oui_database(self):
        """Load OUI database from file"""
        try:
            if self.oui_file_path.exists():
                with open(
                    self.oui_file_path, "r", encoding="utf-8", errors="ignore"
                ) as f:
                    for line in f:
                        if "(hex)" in line:
                            parts = line.strip().split("\t")
                            if len(parts) >= 2:
                                oui = parts[0].replace("-", ":").upper()
                                vendor = parts[1].strip()
                                self.oui_db[oui] = vendor
            else:
                logger.warning(f"OUI database file not found: {self.oui_file_path}")
                self._create_minimal_oui_db()

        except Exception as e:
            logger.error(f"Error loading OUI database: {e}")
            self._create_minimal_oui_db()

    def _create_minimal_oui_db(self):
        """Create minimal OUI database with common vendors"""
        self.oui_db = {
            "00:50:56": "VMware",
            "08:00:27": "VirtualBox",
            "00:0C:29": "VMware",
            "00:1B:21": "Intel",
            "00:13:02": "Apple",
            "00:16:CB": "Apple",
            "00:17:F2": "Apple",
            "00:19:E3": "Apple",
            "00:1C:B3": "Apple",
            "00:1E:C2": "Apple",
            "00:21:E9": "Apple",
            "00:23:12": "Apple",
            "00:25:00": "Apple",
            "00:26:4A": "Apple",
            "00:26:B0": "Apple",
            "00:26:BB": "Apple",
            "28:CF:E9": "Apple",
            "3C:07:54": "Apple",
            "40:A6:D9": "Apple",
            "4C:8D:79": "Apple",
            "50:EA:D6": "Apple",
            "68:D9:3C": "Apple",
            "6C:72:20": "Apple",
            "70:56:81": "Apple",
            "7C:6D:62": "Apple",
            "8C:85:90": "Apple",
            "90:27:E4": "Apple",
            "94:E9:79": "Apple",
            "A4:4E:31": "Apple",
            "A8:86:DD": "Apple",
            "B0:65:BD": "Apple",
            "B8:09:8A": "Apple",
            "B8:E8:56": "Apple",
            "BC:3B:AF": "Apple",
            "C8:B5:B7": "Apple",
            "CC:25:EF": "Apple",
            "D0:23:DB": "Apple",
            "D4:9A:20": "Apple",
            "DC:2B:61": "Apple",
            "E0:B9:BA": "Apple",
            "E8:8D:28": "Apple",
            "F0:B4:79": "Apple",
            "F4:F1:5A": "Apple",
            "F8:1E:DF": "Apple",
            "FC:25:3F": "Apple",
        }

    def _load_device_patterns(self):
        """Load device identification patterns"""
        self.device_patterns = {
            "smartphone": {
                "probe_patterns": [
                    r".*iPhone.*",
                    r".*android.*",
                    r".*Samsung.*",
                    r".*Galaxy.*",
                ],
                "oui_vendors": ["Apple", "Samsung", "LG", "HTC", "Motorola"],
                "signal_characteristics": {"tx_power": (-20, 20), "mobility": "high"},
            },
            "laptop": {
                "probe_patterns": [r".*Windows.*", r".*MacBook.*", r".*ThinkPad.*"],
                "oui_vendors": ["Intel", "Broadcom", "Realtek", "Atheros"],
                "signal_characteristics": {"tx_power": (0, 20), "mobility": "medium"},
            },
            "iot_device": {
                "probe_patterns": [r".*IoT.*", r".*Smart.*", r".*Nest.*", r".*Echo.*"],
                "oui_vendors": ["Amazon", "Google", "Nest", "Ring"],
                "signal_characteristics": {"tx_power": (-10, 10), "mobility": "static"},
            },
            "access_point": {
                "probe_patterns": [],
                "oui_vendors": ["Cisco", "Ubiquiti", "Netgear", "Linksys", "D-Link"],
                "signal_characteristics": {"tx_power": (10, 30), "mobility": "static"},
            },
        }

    def lookup_vendor(self, mac_address: str) -> str:
        """Lookup vendor from MAC address OUI"""
        try:
            oui = mac_address.upper().replace("-", ":")[:8]
            return self.oui_db.get(oui, "Unknown")
        except Exception:
            return "Unknown"

    def identify_device_type(self, fingerprint: DeviceFingerprint) -> str:
        """Identify device type based on fingerprint"""
        scores = {}

        for device_type, patterns in self.device_patterns.items():
            score = 0

            # Check OUI vendor
            if fingerprint.oui_vendor in patterns["oui_vendors"]:
                score += 3

            # Check probe request patterns
            for probe in fingerprint.probe_requests:
                for pattern in patterns["probe_patterns"]:
                    if re.search(pattern, probe, re.IGNORECASE):
                        score += 2

            scores[device_type] = score

        return max(scores, key=scores.get) if scores else "unknown"


class AnomalyDetector:
    """Machine learning-based anomaly detection"""

    def __init__(self, contamination: float = 0.1):
        self.contamination = contamination
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_columns = []

    def extract_features(self, scan_data: List[Dict[str, Any]]) -> np.ndarray:
        """Extract features for anomaly detection"""
        features = []

        for item in scan_data:
            feature_vector = [
                item.get("signal_strength", -100),
                item.get("channel", 0),
                item.get("frequency", 0),
                len(item.get("ssid", "")),
                1 if item.get("encryption", "") == "Open" else 0,
                1 if item.get("encryption", "").startswith("WEP") else 0,
                1 if item.get("encryption", "").startswith("WPA") else 0,
                1 if item.get("encryption", "").startswith("WPA2") else 0,
                1 if item.get("encryption", "").startswith("WPA3") else 0,
                len(item.get("bssid", "").split(":")),
                1 if item.get("ssid", "").startswith("_") else 0,
                (
                    1
                    if any(c in item.get("ssid", "") for c in ["!", "@", "#", "$"])
                    else 0
                ),
                item.get("beacon_interval", 100),
                len(item.get("vendor_elements", [])),
                1 if item.get("wps_enabled", False) else 0,
            ]
            features.append(feature_vector)

        self.feature_columns = [
            "signal_strength",
            "channel",
            "frequency",
            "ssid_length",
            "is_open",
            "is_wep",
            "is_wpa",
            "is_wpa2",
            "is_wpa3",
            "bssid_segments",
            "hidden_ssid",
            "suspicious_chars",
            "beacon_interval",
            "vendor_elements_count",
            "wps_enabled",
        ]

        return np.array(features)

    def train(self, training_data: List[Dict[str, Any]]) -> bool:
        """Train the anomaly detection model"""
        try:
            features = self.extract_features(training_data)

            if len(features) < 10:
                logger.warning("Insufficient training data for anomaly detection")
                return False

            # Scale features
            features_scaled = self.scaler.fit_transform(features)

            # Train model
            self.model.fit(features_scaled)
            self.is_trained = True

            logger.info(f"Anomaly detection model trained on {len(features)} samples")
            return True

        except Exception as e:
            logger.error(f"Error training anomaly detection model: {e}")
            return False

    def detect_anomalies(self, scan_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect anomalies in scan data"""
        if not self.is_trained:
            logger.warning("Anomaly detection model not trained")
            return []

        try:
            features = self.extract_features(scan_data)
            features_scaled = self.scaler.transform(features)

            # Predict anomalies (-1 for anomaly, 1 for normal)
            predictions = self.model.predict(features_scaled)
            anomaly_scores = self.model.decision_function(features_scaled)

            anomalies = []
            for i, (pred, score) in enumerate(zip(predictions, anomaly_scores)):
                if pred == -1:  # Anomaly detected
                    anomaly = {
                        "index": i,
                        "data": scan_data[i],
                        "anomaly_score": float(score),
                        "severity": self._calculate_severity(score),
                        "reason": self._explain_anomaly(features[i], scan_data[i]),
                    }
                    anomalies.append(anomaly)

            return anomalies

        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            return []

    def _calculate_severity(self, score: float) -> str:
        """Calculate anomaly severity based on score"""
        if score < -0.5:
            return "High"
        elif score < -0.3:
            return "Medium"
        else:
            return "Low"

    def _explain_anomaly(self, features: np.ndarray, data: Dict[str, Any]) -> str:
        """Provide explanation for detected anomaly"""
        explanations = []

        # Check for suspicious characteristics
        if features[4] == 1:  # Open network
            explanations.append("Open network (no encryption)")

        if features[5] == 1:  # WEP encryption
            explanations.append("Weak WEP encryption")

        if features[11] == 1:  # Suspicious characters
            explanations.append("Suspicious characters in SSID")

        if features[0] > -30:  # Very strong signal
            explanations.append("Unusually strong signal strength")

        if features[3] == 0:  # Empty SSID
            explanations.append("Hidden SSID")

        return (
            "; ".join(explanations) if explanations else "Statistical anomaly detected"
        )


class BehavioralProfiler:
    """Behavioral profiling for wireless environments"""

    def __init__(self, profile_window: int = 24):  # 24 hours
        self.profile_window = profile_window
        self.baseline_profiles = {}
        self.current_profiles = {}

    def create_baseline_profile(
        self, scan_history: List[Dict[str, Any]], environment_id: str
    ) -> Dict[str, Any]:
        """Create baseline behavioral profile for an environment"""
        try:
            profile = {
                "environment_id": environment_id,
                "creation_time": datetime.now(),
                "network_count": {"mean": 0, "std": 0, "min": 0, "max": 0},
                "signal_strength_distribution": {},
                "encryption_distribution": {},
                "vendor_distribution": {},
                "channel_distribution": {},
                "temporal_patterns": {},
                "typical_devices": [],
                "network_stability": 0.0,
            }

            if not scan_history:
                return profile

            # Analyze network count over time
            hourly_counts = defaultdict(list)
            all_networks = []
            all_signals = []
            encryption_types = []
            vendors = []
            channels = []

            for scan in scan_history:
                hour = datetime.fromisoformat(scan["timestamp"]).hour
                networks = scan.get("networks", [])
                hourly_counts[hour].append(len(networks))
                all_networks.extend(networks)

                for network in networks:
                    all_signals.append(network.get("signal_strength", -100))
                    encryption_types.append(network.get("encryption", "Unknown"))
                    vendors.append(network.get("vendor", "Unknown"))
                    channels.append(network.get("channel", 0))

            # Calculate network count statistics
            all_counts = [
                count for counts in hourly_counts.values() for count in counts
            ]
            if all_counts:
                profile["network_count"] = {
                    "mean": np.mean(all_counts),
                    "std": np.std(all_counts),
                    "min": min(all_counts),
                    "max": max(all_counts),
                }

            # Signal strength distribution
            if all_signals:
                profile["signal_strength_distribution"] = {
                    "mean": np.mean(all_signals),
                    "std": np.std(all_signals),
                    "percentiles": {
                        "25": np.percentile(all_signals, 25),
                        "50": np.percentile(all_signals, 50),
                        "75": np.percentile(all_signals, 75),
                        "90": np.percentile(all_signals, 90),
                    },
                }

            # Encryption distribution
            encryption_counter = Counter(encryption_types)
            total_networks = len(encryption_types)
            if total_networks > 0:
                profile["encryption_distribution"] = {
                    enc: count / total_networks
                    for enc, count in encryption_counter.items()
                }

            # Vendor distribution
            vendor_counter = Counter(vendors)
            if total_networks > 0:
                profile["vendor_distribution"] = {
                    vendor: count / total_networks
                    for vendor, count in vendor_counter.most_common(10)
                }

            # Channel distribution
            channel_counter = Counter(channels)
            if total_networks > 0:
                profile["channel_distribution"] = {
                    str(ch): count / total_networks
                    for ch, count in channel_counter.items()
                }

            # Temporal patterns
            for hour, counts in hourly_counts.items():
                if counts:
                    profile["temporal_patterns"][str(hour)] = {
                        "mean": np.mean(counts),
                        "std": np.std(counts),
                    }

            # Network stability (how consistent the network list is)
            unique_networks = set()
            for scan in scan_history[-10:]:  # Last 10 scans
                for network in scan.get("networks", []):
                    unique_networks.add(network.get("bssid", ""))

            if len(scan_history) > 1:
                stability = len(unique_networks) / max(1, len(scan_history[-10:]))
                profile["network_stability"] = min(1.0, stability)

            self.baseline_profiles[environment_id] = profile
            return profile

        except Exception as e:
            logger.error(f"Error creating baseline profile: {e}")
            return {}

    def analyze_deviation(
        self, current_scan: Dict[str, Any], environment_id: str
    ) -> Dict[str, Any]:
        """Analyze deviation from baseline profile"""
        if environment_id not in self.baseline_profiles:
            return {"error": "No baseline profile found"}

        baseline = self.baseline_profiles[environment_id]
        deviations = {}

        try:
            networks = current_scan.get("networks", [])
            current_count = len(networks)

            # Network count deviation
            expected_count = baseline["network_count"]["mean"]
            count_std = baseline["network_count"]["std"]

            if count_std > 0:
                count_deviation = abs(current_count - expected_count) / count_std
                deviations["network_count"] = {
                    "current": current_count,
                    "expected": expected_count,
                    "deviation_score": count_deviation,
                    "severity": (
                        "High"
                        if count_deviation > 3
                        else "Medium" if count_deviation > 2 else "Low"
                    ),
                }

            # Signal strength deviation
            current_signals = [n.get("signal_strength", -100) for n in networks]
            if current_signals and baseline["signal_strength_distribution"]:
                expected_mean = baseline["signal_strength_distribution"]["mean"]
                expected_std = baseline["signal_strength_distribution"]["std"]
                current_mean = np.mean(current_signals)

                if expected_std > 0:
                    signal_deviation = abs(current_mean - expected_mean) / expected_std
                    deviations["signal_strength"] = {
                        "current_mean": current_mean,
                        "expected_mean": expected_mean,
                        "deviation_score": signal_deviation,
                        "severity": (
                            "High"
                            if signal_deviation > 2
                            else "Medium" if signal_deviation > 1 else "Low"
                        ),
                    }

            # New networks detection
            baseline_networks = set(baseline.get("typical_devices", []))
            current_networks = set(n.get("bssid", "") for n in networks)
            new_networks = current_networks - baseline_networks

            if new_networks:
                deviations["new_networks"] = {
                    "count": len(new_networks),
                    "networks": list(new_networks),
                    "severity": (
                        "High"
                        if len(new_networks) > 5
                        else "Medium" if len(new_networks) > 2 else "Low"
                    ),
                }

            return deviations

        except Exception as e:
            logger.error(f"Error analyzing deviation: {e}")
            return {"error": str(e)}


class RiskScorer:
    """Risk scoring system for networks and devices"""

    def __init__(self):
        self.risk_weights = {
            "encryption_risk": 0.3,
            "signal_anomaly": 0.2,
            "device_behavior": 0.2,
            "network_characteristics": 0.15,
            "temporal_anomaly": 0.15,
        }

        self.threat_indicators = {
            "evil_twin": {
                "description": "Potential evil twin access point",
                "indicators": ["duplicate_ssid", "stronger_signal", "different_mac"],
                "base_score": 8.0,
            },
            "rogue_ap": {
                "description": "Unauthorized access point",
                "indicators": ["unknown_vendor", "suspicious_ssid", "unusual_location"],
                "base_score": 7.0,
            },
            "weak_encryption": {
                "description": "Weak or no encryption",
                "indicators": ["open_network", "wep_encryption", "weak_password"],
                "base_score": 6.0,
            },
            "suspicious_behavior": {
                "description": "Suspicious device behavior",
                "indicators": ["probe_scanning", "deauth_attacks", "unusual_traffic"],
                "base_score": 7.5,
            },
        }

    def calculate_network_risk(
        self, network_data: Dict[str, Any], context: Dict[str, Any] = None
    ) -> RiskAssessment:
        """Calculate risk score for a network"""
        try:
            risk_factors = []
            risk_score = 0.0

            # Encryption risk
            encryption_score = self._assess_encryption_risk(network_data)
            risk_score += encryption_score * self.risk_weights["encryption_risk"]
            if encryption_score > 5:
                risk_factors.append(
                    f"Weak encryption: {network_data.get('encryption', 'Unknown')}"
                )

            # Signal anomaly risk
            signal_score = self._assess_signal_anomaly(network_data, context)
            risk_score += signal_score * self.risk_weights["signal_anomaly"]
            if signal_score > 5:
                risk_factors.append("Unusual signal characteristics")

            # Network characteristics risk
            characteristics_score = self._assess_network_characteristics(network_data)
            risk_score += (
                characteristics_score * self.risk_weights["network_characteristics"]
            )
            if characteristics_score > 5:
                risk_factors.append("Suspicious network characteristics")

            # Determine risk level
            if risk_score >= 7.0:
                risk_level = "Critical"
            elif risk_score >= 5.0:
                risk_level = "High"
            elif risk_score >= 3.0:
                risk_level = "Medium"
            else:
                risk_level = "Low"

            # Generate recommendations
            recommendations = self._generate_recommendations(risk_factors, network_data)

            # Compliance status
            compliance_status = self._check_compliance(network_data)

            return RiskAssessment(
                network_id=network_data.get("bssid", "unknown"),
                risk_score=risk_score,
                risk_level=risk_level,
                risk_factors=risk_factors,
                recommendations=recommendations,
                compliance_status=compliance_status,
                timestamp=datetime.now(),
            )

        except Exception as e:
            logger.error(f"Error calculating network risk: {e}")
            return RiskAssessment(
                network_id=network_data.get("bssid", "unknown"),
                risk_score=0.0,
                risk_level="Unknown",
                risk_factors=[],
                recommendations=[],
                compliance_status={},
                timestamp=datetime.now(),
            )

    def _assess_encryption_risk(self, network_data: Dict[str, Any]) -> float:
        """Assess encryption-related risk"""
        encryption = network_data.get("encryption", "").upper()

        if encryption == "OPEN" or encryption == "":
            return 9.0
        elif "WEP" in encryption:
            return 8.0
        elif (
            "WPA" in encryption
            and "WPA2" not in encryption
            and "WPA3" not in encryption
        ):
            return 6.0
        elif "WPA2" in encryption:
            return 2.0
        elif "WPA3" in encryption:
            return 1.0
        else:
            return 5.0  # Unknown encryption

    def _assess_signal_anomaly(
        self, network_data: Dict[str, Any], context: Dict[str, Any] = None
    ) -> float:
        """Assess signal-related anomalies"""
        signal_strength = network_data.get("signal_strength", -100)

        # Very strong signal could indicate close proximity (potential evil twin)
        if signal_strength > -30:
            return 6.0
        elif signal_strength > -40:
            return 3.0
        else:
            return 1.0

    def _assess_network_characteristics(self, network_data: Dict[str, Any]) -> float:
        """Assess suspicious network characteristics"""
        score = 0.0

        ssid = network_data.get("ssid", "")
        bssid = network_data.get("bssid", "")

        # Hidden SSID
        if not ssid or ssid.startswith("_"):
            score += 2.0

        # Suspicious SSID patterns
        suspicious_patterns = ["test", "hack", "pwn", "evil", "fake", "free"]
        if any(pattern in ssid.lower() for pattern in suspicious_patterns):
            score += 4.0

        # Randomized MAC address
        if self._is_randomized_mac(bssid):
            score += 1.0

        # WPS enabled (potential vulnerability)
        if network_data.get("wps_enabled", False):
            score += 1.0

        return min(score, 10.0)

    def _is_randomized_mac(self, mac_address: str) -> bool:
        """Check if MAC address appears to be randomized"""
        if not mac_address or len(mac_address) < 17:
            return False

        # Check for locally administered bit (2nd bit of first octet)
        try:
            first_octet = int(mac_address[:2], 16)
            return bool(first_octet & 0x02)
        except ValueError:
            return False

    def _generate_recommendations(
        self, risk_factors: List[str], network_data: Dict[str, Any]
    ) -> List[str]:
        """Generate security recommendations"""
        recommendations = []

        encryption = network_data.get("encryption", "").upper()

        if "OPEN" in encryption or not encryption:
            recommendations.append("Enable WPA3 or WPA2 encryption")
        elif "WEP" in encryption:
            recommendations.append("Upgrade from WEP to WPA3 or WPA2")
        elif "WPA" in encryption and "WPA2" not in encryption:
            recommendations.append("Upgrade to WPA2 or WPA3")

        if network_data.get("wps_enabled", False):
            recommendations.append("Disable WPS to prevent brute force attacks")

        if any("signal" in factor.lower() for factor in risk_factors):
            recommendations.append(
                "Investigate unusually strong signals for potential evil twin attacks"
            )

        if any("suspicious" in factor.lower() for factor in risk_factors):
            recommendations.append("Monitor network for unauthorized access points")

        return recommendations

    def _check_compliance(self, network_data: Dict[str, Any]) -> Dict[str, bool]:
        """Check compliance with security standards"""
        compliance = {}

        encryption = network_data.get("encryption", "").upper()

        # NIST compliance (simplified)
        compliance["NIST_800_53"] = "WPA2" in encryption or "WPA3" in encryption

        # PCI DSS compliance
        compliance["PCI_DSS"] = "WPA2" in encryption or "WPA3" in encryption

        # HIPAA compliance
        compliance["HIPAA"] = "WPA3" in encryption or (
            "WPA2" in encryption and not network_data.get("wps_enabled", False)
        )

        # SOX compliance
        compliance["SOX"] = "WPA2" in encryption or "WPA3" in encryption

        return compliance


class OfflineThreatDetector:
    """Main threat detection engine coordinator"""

    def __init__(self, data_dir: str = "data/ml_models"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.oui_db = OUIDatabase()
        self.anomaly_detector = AnomalyDetector()
        self.behavioral_profiler = BehavioralProfiler()
        self.risk_scorer = RiskScorer()

        self.device_fingerprints = {}
        self.threat_history = []

    def initialize(self) -> bool:
        """Initialize the threat detection system"""
        try:
            # Load existing models and data
            self._load_models()
            self._load_device_fingerprints()

            logger.info("Offline threat detection system initialized")
            return True

        except Exception as e:
            logger.error(f"Error initializing threat detection system: {e}")
            return False

    def analyze_scan_data(
        self, scan_data: List[Dict[str, Any]], environment_id: str = "default"
    ) -> Dict[str, Any]:
        """Comprehensive analysis of scan data"""
        try:
            results = {
                "timestamp": datetime.now().isoformat(),
                "environment_id": environment_id,
                "networks_analyzed": len(scan_data),
                "anomalies": [],
                "threats": [],
                "risk_assessments": [],
                "device_fingerprints": [],
                "behavioral_analysis": {},
                "summary": {},
            }

            # Detect anomalies
            if self.anomaly_detector.is_trained:
                anomalies = self.anomaly_detector.detect_anomalies(scan_data)
                results["anomalies"] = anomalies

            # Analyze each network
            for network in scan_data:
                # Create device fingerprint
                fingerprint = self._create_device_fingerprint(network)
                if fingerprint:
                    results["device_fingerprints"].append(fingerprint.to_dict())

                # Calculate risk assessment
                risk_assessment = self.risk_scorer.calculate_network_risk(network)
                results["risk_assessments"].append(risk_assessment.to_dict())

                # Check for specific threats
                threats = self._detect_specific_threats(network, scan_data)
                results["threats"].extend(threats)

            # Behavioral analysis
            behavioral_analysis = self.behavioral_profiler.analyze_deviation(
                {"networks": scan_data}, environment_id
            )
            results["behavioral_analysis"] = behavioral_analysis

            # Generate summary
            results["summary"] = self._generate_analysis_summary(results)

            return results

        except Exception as e:
            logger.error(f"Error analyzing scan data: {e}")
            return {"error": str(e)}

    def _create_device_fingerprint(
        self, network_data: Dict[str, Any]
    ) -> Optional[DeviceFingerprint]:
        """Create device fingerprint from network data"""
        try:
            mac_address = network_data.get("bssid", "")
            if not mac_address:
                return None

            vendor = self.oui_db.lookup_vendor(mac_address)

            fingerprint = DeviceFingerprint(
                mac_address=mac_address,
                oui_vendor=vendor,
                device_type="unknown",
                probe_requests=network_data.get("probe_requests", []),
                signal_patterns=[network_data.get("signal_strength", -100)],
                timing_patterns=[],
                encryption_capabilities=[network_data.get("encryption", "")],
                supported_rates=network_data.get("supported_rates", []),
                power_management=network_data.get("power_management", False),
                vendor_elements=network_data.get("vendor_elements", []),
                fingerprint_hash="",
                confidence_score=0.8,
                last_seen=datetime.now(),
            )

            # Identify device type
            fingerprint.device_type = self.oui_db.identify_device_type(fingerprint)

            # Generate fingerprint hash
            fingerprint_str = (
                f"{vendor}_{fingerprint.device_type}_{len(fingerprint.probe_requests)}"
            )
            fingerprint.fingerprint_hash = hashlib.sha256(
                fingerprint_str.encode()
            ).hexdigest()

            # Store fingerprint
            self.device_fingerprints[mac_address] = fingerprint

            return fingerprint

        except Exception as e:
            logger.error(f"Error creating device fingerprint: {e}")
            return None

    def _detect_specific_threats(
        self, network: Dict[str, Any], all_networks: List[Dict[str, Any]]
    ) -> List[ThreatIndicator]:
        """Detect specific threat patterns"""
        threats = []

        try:
            # Evil twin detection
            evil_twin = self._detect_evil_twin(network, all_networks)
            if evil_twin:
                threats.append(evil_twin)

            # Rogue AP detection
            rogue_ap = self._detect_rogue_ap(network)
            if rogue_ap:
                threats.append(rogue_ap)

            # Weak security detection
            weak_security = self._detect_weak_security(network)
            if weak_security:
                threats.append(weak_security)

        except Exception as e:
            logger.error(f"Error detecting specific threats: {e}")

        return threats

    def _detect_evil_twin(
        self, network: Dict[str, Any], all_networks: List[Dict[str, Any]]
    ) -> Optional[ThreatIndicator]:
        """Detect potential evil twin access points"""
        ssid = network.get("ssid", "")
        bssid = network.get("bssid", "")
        signal_strength = network.get("signal_strength", -100)

        if not ssid:
            return None

        # Look for networks with same SSID but different BSSID
        for other_network in all_networks:
            other_ssid = other_network.get("ssid", "")
            other_bssid = other_network.get("bssid", "")
            other_signal = other_network.get("signal_strength", -100)

            if (
                ssid == other_ssid
                and bssid != other_bssid
                and abs(signal_strength - other_signal) < 10
            ):  # Similar signal strength

                return ThreatIndicator(
                    threat_id=f"evil_twin_{bssid[:8]}",
                    threat_type="evil_twin",
                    severity="High",
                    confidence=0.7,
                    description=f"Potential evil twin detected for SSID '{ssid}'",
                    indicators=[
                        f"Duplicate SSID: {ssid}",
                        f"Different BSSID: {bssid} vs {other_bssid}",
                        f"Similar signal strength: {signal_strength} vs {other_signal}",
                    ],
                    mitigation="Verify legitimate AP and disable the rogue device",
                    timestamp=datetime.now(),
                    affected_devices=[bssid, other_bssid],
                    network_context={
                        "ssid": ssid,
                        "signal_di": abs(signal_strength - other_signal),
                    },
                )

        return None

    def _detect_rogue_ap(self, network: Dict[str, Any]) -> Optional[ThreatIndicator]:
        """Detect unauthorized access points"""
        vendor = network.get("vendor", "Unknown")
        ssid = network.get("ssid", "")
        bssid = network.get("bssid", "")

        # Check for suspicious characteristics
        suspicious_indicators = []

        if "Unknown" in vendor or vendor == "":
            suspicious_indicators.append("Unknown vendor")

        suspicious_ssids = ["test", "hack", "pwn", "free", "guest"]
        if any(pattern in ssid.lower() for pattern in suspicious_ssids):
            suspicious_indicators.append(f"Suspicious SSID pattern: {ssid}")

        if len(suspicious_indicators) >= 1:
            return ThreatIndicator(
                threat_id=f"rogue_ap_{bssid[:8]}",
                threat_type="rogue_ap",
                severity="Medium",
                confidence=0.6,
                description="Potential rogue access point detected",
                indicators=suspicious_indicators,
                mitigation="Investigate and remove unauthorized access point",
                timestamp=datetime.now(),
                affected_devices=[bssid],
                network_context={"ssid": ssid, "vendor": vendor},
            )

        return None

    def _detect_weak_security(
        self, network: Dict[str, Any]
    ) -> Optional[ThreatIndicator]:
        """Detect weak security configurations"""
        encryption = network.get("encryption", "").upper()
        bssid = network.get("bssid", "")
        ssid = network.get("ssid", "")

        if encryption == "OPEN" or encryption == "":
            return ThreatIndicator(
                threat_id=f"open_network_{bssid[:8]}",
                threat_type="weak_security",
                severity="Medium",
                confidence=0.9,
                description="Open network detected (no encryption)",
                indicators=["No encryption enabled"],
                mitigation="Enable WPA2 or WPA3 encryption",
                timestamp=datetime.now(),
                affected_devices=[bssid],
                network_context={"ssid": ssid, "encryption": encryption},
            )
        elif "WEP" in encryption:
            return ThreatIndicator(
                threat_id=f"wep_network_{bssid[:8]}",
                threat_type="weak_security",
                severity="High",
                confidence=0.9,
                description="WEP encryption detected (weak security)",
                indicators=["WEP encryption is easily broken"],
                mitigation="Upgrade to WPA2 or WPA3 encryption",
                timestamp=datetime.now(),
                affected_devices=[bssid],
                network_context={"ssid": ssid, "encryption": encryption},
            )

        return None

    def _generate_analysis_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate analysis summary"""
        summary = {
            "total_networks": results["networks_analyzed"],
            "anomalies_detected": len(results["anomalies"]),
            "threats_detected": len(results["threats"]),
            "high_risk_networks": 0,
            "critical_risk_networks": 0,
            "compliance_issues": 0,
            "recommendations": [],
        }

        # Count risk levels
        for assessment in results["risk_assessments"]:
            if assessment["risk_level"] == "High":
                summary["high_risk_networks"] += 1
            elif assessment["risk_level"] == "Critical":
                summary["critical_risk_networks"] += 1

        # Count compliance issues
        for assessment in results["risk_assessments"]:
            compliance = assessment.get("compliance_status", {})
            if not all(compliance.values()):
                summary["compliance_issues"] += 1

        # Generate top recommendations
        if summary["critical_risk_networks"] > 0:
            summary["recommendations"].append(
                "Immediate attention required for critical risk networks"
            )
        if summary["threats_detected"] > 0:
            summary["recommendations"].append("Investigate detected security threats")
        if summary["compliance_issues"] > 0:
            summary["recommendations"].append("Address compliance violations")

        return summary

    def _load_models(self):
        """Load saved ML models"""
        try:
            model_file = self.data_dir / "anomaly_detector.pkl"
            if model_file.exists():
                with open(model_file, "rb") as f:
                    model_data = pickle.load(f)
                    self.anomaly_detector.model = model_data["model"]
                    self.anomaly_detector.scaler = model_data["scaler"]
                    self.anomaly_detector.is_trained = True
                    logger.info("Loaded anomaly detection model")
        except Exception as e:
            logger.debug(f"Could not load models: {e}")

    def _save_models(self):
        """Save ML models"""
        try:
            if self.anomaly_detector.is_trained:
                model_file = self.data_dir / "anomaly_detector.pkl"
                model_data = {
                    "model": self.anomaly_detector.model,
                    "scaler": self.anomaly_detector.scaler,
                }
                with open(model_file, "wb") as f:
                    pickle.dump(model_data, f)
                    logger.info("Saved anomaly detection model")
        except Exception as e:
            logger.error(f"Error saving models: {e}")

    def _load_device_fingerprints(self):
        """Load saved device fingerprints"""
        try:
            fingerprint_file = self.data_dir / "device_fingerprints.json"
            if fingerprint_file.exists():
                with open(fingerprint_file, "r") as f:
                    _data = json.load(f)
                    for mac, fp_data in _data.items():
                        fp_data["last_seen"] = datetime.fromisoformat(
                            fp_data["last_seen"]
                        )
                        self.device_fingerprints[mac] = DeviceFingerprint(**fp_data)
                    logger.info(
                        f"Loaded {len(self.device_fingerprints)} device fingerprints"
                    )
        except Exception as e:
            logger.debug(f"Could not load device fingerprints: {e}")

    def train_with_data(self, training_data: List[Dict[str, Any]]) -> bool:
        """Train the system with new data"""
        try:
            # Train anomaly detector
            success = self.anomaly_detector.train(training_data)

            if success:
                self._save_models()
                logger.info("Training completed successfully")
                return True
            else:
                logger.warning("Training failed")
                return False

        except Exception as e:
            logger.error(f"Error during training: {e}")
            return False


# Example usage and testing functions
def example_threat_detection():
    """Example of threat detection usage"""
    # Create threat detector
    detector = OfflineThreatDetector()
    detector.initialize()

    # Sample scan data
    sample_data = [
        {
            "bssid": "00:11:22:33:44:55",
            "ssid": "HomeWiFi",
            "signal_strength": -45,
            "encryption": "WPA2",
            "channel": 6,
            "vendor": "Linksys",
        },
        {
            "bssid": "00:11:22:33:44:66",
            "ssid": "HomeWiFi",  # Same SSID - potential evil twin
            "signal_strength": -47,
            "encryption": "Open",  # Suspicious - open network
            "channel": 6,
            "vendor": "Unknown",
        },
        {
            "bssid": "00:11:22:33:44:77",
            "ssid": "",  # Hidden SSID
            "signal_strength": -32,  # Very strong signal
            "encryption": "WEP",  # Weak encryption
            "channel": 11,
            "vendor": "Unknown",
        },
    ]

    # Analyze scan data
    results = detector.analyze_scan_data(sample_data, "office_environment")

    print("=== Threat Detection Results ===")
    print(f"Networks analyzed: {results['networks_analyzed']}")
    print(f"Threats detected: {len(results['threats'])}")
    print(f"Anomalies detected: {len(results['anomalies'])}")

    # Print threats
    for threat in results["threats"]:
        print(f"\nThreat: {threat['threat_type']}")
        print(f"Severity: {threat['severity']}")
        print(f"Description: {threat['description']}")
        print(f"Indicators: {', '.join(threat['indicators'])}")

    # Print risk assessments
    print("\n=== Risk Assessments ===")
    for assessment in results["risk_assessments"]:
        print(
            f"Network {assessment['network_id']}: {assessment['risk_level']} risk (score: {assessment['risk_score']:.1f})"
        )

    return detector


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    example_threat_detection()
