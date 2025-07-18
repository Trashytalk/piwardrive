"""
Advanced Data Mining Module for PiWardrive
Temporal pattern mining, clustering, association rules, and automated insights
"""

import logging
import warnings
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)


class PatternType(Enum):
    """Types of patterns that can be discovered"""

    TEMPORAL = "temporal"
    SPATIAL = "spatial"
    BEHAVIORAL = "behavioral"
    NETWORK_TOPOLOGY = "network_topology"
    TRAFFIC_FLOW = "traffic_flow"
    SECURITY_ANOMALY = "security_anomaly"
    DEVICE_ASSOCIATION = "device_association"


class InsightType(Enum):
    """Types of automated insights"""

    TREND_ANALYSIS = "trend_analysis"
    ANOMALY_DETECTION = "anomaly_detection"
    CORRELATION_DISCOVERY = "correlation_discovery"
    PREDICTION = "prediction"
    RECOMMENDATION = "recommendation"
    ALERT = "alert"


@dataclass
class Pattern:
    """Discovered pattern representation"""

    pattern_id: str
    pattern_type: PatternType
    confidence: float
    support: float
    description: str
    parameters: Dict[str, Any]
    discovery_time: datetime
    data_points: List[Any] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Insight:
    """Automated insight representation"""

    insight_id: str
    insight_type: InsightType
    title: str
    description: str
    confidence: float
    severity: str  # 'critical', 'high', 'medium', 'low', 'info'
    timestamp: datetime
    data_source: str
    recommendations: List[str] = field(default_factory=list)
    supporting_data: Dict[str, Any] = field(default_factory=dict)
    related_patterns: List[str] = field(default_factory=list)


@dataclass
class Association:
    """Association rule representation"""

    antecedent: Set[str]
    consequent: Set[str]
    support: float
    confidence: float
    lift: float
    description: str


class TemporalPatternMiner:
    """Temporal pattern mining for time-series data"""

    def __init__(self):
        self.patterns = {}
        self.time_seriesdata = defaultdict(list)
        self.pattern_cache = {}

    def add_time_series_data(self, series_name: str, timestamp: datetime, value: Any):
        """Add data point to time series"""
        self.time_series_data[series_name].append((timestamp, value))

        # Keep data sorted by timestamp
        self.time_series_data[series_name].sort(key=lambda x: x[0])

        # Limit data retention (keep last 10000 points)
        if len(self.time_series_data[series_name]) > 10000:
            self.time_series_data[series_name] = self.time_series_data[series_name][
                -10000:
            ]

    def detect_periodic_patterns(
        self, series_name: str, min_period: int = 5, max_period: int = 100
    ) -> List[Pattern]:
        """Detect periodic patterns in time series data"""
        if series_name not in self.time_series_data:
            return []

        data = self.time_series_data[series_name]
        if len(data) < min_period * 2:
            return []

        patterns = []

        # Convert to numerical values for analysis
        timestamps = [point[0] for point in data]
        values = [self._extract_numeric_value(point[1]) for point in data]

        if not all(isinstance(v, (int, float)) for v in values):
            return patterns

        # Autocorrelation analysis for period detection
        values_array = np.array(values)
        n = len(values_array)

        for period in range(min_period, min(max_period, n // 2)):
            # Calculate autocorrelation for this period
            correlation = self._calculate_autocorrelation(values_array, period)

            if correlation > 0.7:  # Strong correlation threshold
                # Verify pattern consistency
                consistency = self._verify_period_consistency(values_array, period)

                if consistency > 0.6:
                    pattern = Pattern(
                        pattern_id=f"periodic_{series_name}_{period}",
                        pattern_type=PatternType.TEMPORAL,
                        confidence=correlation,
                        support=consistency,
                        description=f"Periodic pattern in {series_name} with period {period}",
                        parameters={
                            "period": period,
                            "correlation": correlation,
                            "consistency": consistency,
                            "series_name": series_name,
                        },
                        discovery_time=datetime.now(),
                        data_points=(
                            data[-period * 3 :] if len(data) >= period * 3 else data
                        ),
                        metadata={
                            "analysis_method": "autocorrelation",
                            "data_points_analyzed": len(data),
                        },
                    )
                    patterns.append(pattern)

        return patterns

    def detect_trend_patterns(
        self, series_name: str, window_size: int = 20
    ) -> List[Pattern]:
        """Detect trend patterns (increasing, decreasing, stable)"""
        if series_name not in self.time_series_data:
            return []

        data = self.time_series_data[series_name]
        if len(data) < window_size:
            return []

        patterns = []
        values = [self._extract_numeric_value(point[1]) for point in data]

        if not all(isinstance(v, (int, float)) for v in values):
            return patterns

        # Sliding window trend analysis
        for i in range(len(values) - window_size + 1):
            window = values[i : i + window_size]
            trend_strength, trend_direction = self._analyze_trend(window)

            if trend_strength > 0.7:  # Strong trend
                pattern = Pattern(
                    pattern_id=f"trend_{series_name}_{i}",
                    pattern_type=PatternType.TEMPORAL,
                    confidence=trend_strength,
                    support=window_size / len(values),
                    description=f"{trend_direction} trend in {series_name}",
                    parameters={
                        "trend_direction": trend_direction,
                        "trend_strength": trend_strength,
                        "window_start": i,
                        "window_size": window_size,
                    },
                    discovery_time=datetime.now(),
                    data_points=data[i : i + window_size],
                )
                patterns.append(pattern)

        return patterns

    def detect_anomaly_patterns(
        self, series_name: str, contamination: float = 0.1
    ) -> List[Pattern]:
        """Detect anomalous patterns in time series"""
        if series_name not in self.time_series_data:
            return []

        data = self.time_series_data[series_name]
        if len(data) < 50:  # Need sufficient data for anomaly detection
            return []

        patterns = []
        values = [self._extract_numeric_value(point[1]) for point in data]

        if not all(isinstance(v, (int, float)) for v in values):
            return patterns

        # Prepare data for anomaly detection
        X = np.array(values).reshape(-1, 1)

        # Use Isolation Forest for anomaly detection
        clf = IsolationForest(contamination=contamination, random_state=42)
        anomaly_labels = clf.fit_predict(X)

        # Find anomalous subsequences
        anomaly_indices = np.where(anomaly_labels == -1)[0]

        if len(anomaly_indices) > 0:
            # Group consecutive anomalies
            anomaly_groups = self._group_consecutive_indices(anomaly_indices)

            for group in anomaly_groups:
                if len(group) >= 3:  # Minimum group size
                    pattern = Pattern(
                        pattern_id=f"anomaly_{series_name}_{group[0]}",
                        pattern_type=PatternType.TEMPORAL,
                        confidence=0.8,  # Based on Isolation Forest confidence
                        support=len(group) / len(values),
                        description=f"Anomalous pattern in {series_name}",
                        parameters={
                            "anomaly_start": group[0],
                            "anomaly_end": group[-1],
                            "anomaly_length": len(group),
                            "contamination": contamination,
                        },
                        discovery_time=datetime.now(),
                        data_points=[data[i] for i in group],
                    )
                    patterns.append(pattern)

        return patterns

    def _extract_numeric_value(self, value: Any) -> float:
        """Extract numeric value from various data types"""
        if isinstance(value, (int, float)):
            return float(value)
        elif isinstance(value, dict):
            # Try to find numeric fields
            for key in ["rssi", "signal_strength", "count", "value"]:
                if key in value and isinstance(value[key], (int, float)):
                    return float(value[key])
        elif isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                pass

        return 0.0  # Default value

    def _calculate_autocorrelation(self, values: np.ndarray, lag: int) -> float:
        """Calculate autocorrelation at given lag"""
        n = len(values)
        if lag >= n:
            return 0.0

        mean = np.mean(values)
        c0 = np.mean((values - mean) ** 2)

        if c0 == 0:
            return 0.0

        c_lag = np.mean((values[:-lag] - mean) * (values[lag:] - mean))
        return c_lag / c0

    def _verify_period_consistency(self, values: np.ndarray, period: int) -> float:
        """Verify consistency of periodic pattern"""
        n = len(values)
        if period * 2 > n:
            return 0.0

        # Compare segments of the period
        num_segments = n // period
        segments = [values[i * period : (i + 1) * period] for i in range(num_segments)]

        if len(segments) < 2:
            return 0.0

        # Calculate correlation between segments
        correlations = []
        for i in range(len(segments) - 1):
            corr = np.corrcoef(segments[i], segments[i + 1])[0, 1]
            if not np.isnan(corr):
                correlations.append(corr)

        return np.mean(correlations) if correlations else 0.0

    def _analyze_trend(self, values: List[float]) -> Tuple[float, str]:
        """Analyze trend strength and direction"""
        if len(values) < 3:
            return 0.0, "stable"

        # Linear regression to find trend
        x = np.arange(len(values))
        y = np.array(values)

        # Calculate slope
        slope = np.polyfit(x, y, 1)[0]

        # Calculate R-squared for trend strength
        y_pred = slope * x + np.mean(y)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)

        if ss_tot == 0:
            r_squared = 0.0
        else:
            r_squared = 1 - (ss_res / ss_tot)

        # Determine direction
        if abs(slope) < 0.01:  # Very small slope
            direction = "stable"
        elif slope > 0:
            direction = "increasing"
        else:
            direction = "decreasing"

        return r_squared, direction

    def _group_consecutive_indices(self, indices: np.ndarray) -> List[List[int]]:
        """Group consecutive indices together"""
        if len(indices) == 0:
            return []

        groups = []
        current_group = [indices[0]]

        for i in range(1, len(indices)):
            if indices[i] == indices[i - 1] + 1:
                current_group.append(indices[i])
            else:
                groups.append(current_group)
                current_group = [indices[i]]

        groups.append(current_group)
        return groups


class ClusteringAnalyzer:
    """Clustering analysis for discovering device and network relationships"""

    def __init__(self):
        self.cluster_models = {}
        self.clustering_results = {}
        self.scaler = StandardScaler()

    def cluster_devices(
        self, devices: List[Dict[str, Any]], features: List[str]
    ) -> Dict[str, Any]:
        """Cluster devices based on specified features"""
        if len(devices) < 3:
            return {}

        # Prepare feature matrix
        feature_matrix = []
        device_ids = []

        for device in devices:
            device_features = []
            device_ids.append(device.get("id", device.get("mac_address", "unknown")))

            for feature in features:
                value = self._extract_feature_value(device, feature)
                device_features.append(value)

            feature_matrix.append(device_features)

        X = np.array(feature_matrix)

        # Normalize features
        X_scaled = self.scaler.fit_transform(X)

        # Try different clustering algorithms
        clustering_results = {}

        # DBSCAN clustering
        dbscan_result = self._apply_dbscan(X_scaled, device_ids)
        if dbscan_result:
            clustering_results["dbscan"] = dbscan_result

        # K-Means clustering
        kmeans_result = self._apply_kmeans(X_scaled, device_ids)
        if kmeans_result:
            clustering_results["kmeans"] = kmeans_result

        return clustering_results

    def cluster_networks(self, networks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Cluster networks based on characteristics"""
        if len(networks) < 3:
            return {}

        # Network features for clustering

        feature_matrix = []
        network_ids = []

        for network in networks:
            network_features = []
            network_ids.append(network.get("ssid", network.get("bssid", "unknown")))

            # Channel
            network_features.append(network.get("channel", 0))

            # Signal strength
            network_features.append(network.get("signal_strength", -100))

            # Encryption type (encoded)
            encryption = network.get("encryption", "Open")
            encryption_score = {
                "Open": 0,
                "WEP": 1,
                "WPA": 2,
                "WPA2": 3,
                "WPA3": 4,
            }.get(encryption, 0)
            network_features.append(encryption_score)

            # Vendor score (based on OUI)
            vendor = network.get("vendor", "Unknown")
            vendor_score = hash(vendor) % 100  # Simple vendor encoding
            network_features.append(vendor_score)

            feature_matrix.append(network_features)

        X = np.array(feature_matrix)
        X_scaled = self.scaler.fit_transform(X)

        # Apply clustering
        clustering_results = {}

        # DBSCAN
        dbscan_result = self._apply_dbscan(X_scaled, network_ids)
        if dbscan_result:
            clustering_results["dbscan"] = dbscan_result

        # K-Means
        kmeans_result = self._apply_kmeans(X_scaled, network_ids)
        if kmeans_result:
            clustering_results["kmeans"] = kmeans_result

        return clustering_results

    def _extract_feature_value(self, item: Dict[str, Any], feature: str) -> float:
        """Extract numeric feature value from item"""
        if feature in item:
            value = item[feature]
            if isinstance(value, (int, float)):
                return float(value)
            elif isinstance(value, str):
                try:
                    return float(value)
                except ValueError:
                    # Hash string to numeric value
                    return float(hash(value) % 1000)

        return 0.0

    def _apply_dbscan(
        self, X: np.ndarray, item_ids: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Apply DBSCAN clustering"""
        try:
            # Try different eps values to find good clustering
            best_result = None
            best_score = -1

            for eps in [0.3, 0.5, 0.8, 1.0, 1.5]:
                dbscan = DBSCAN(eps=eps, min_samples=2)
                labels = dbscan.fit_predict(X)

                # Skip if all points are noise or all in one cluster
                unique_labels = set(labels)
                if len(unique_labels) <= 1 or (
                    len(unique_labels) == 2 and -1 in unique_labels
                ):
                    continue

                # Calculate silhouette score (excluding noise points)
                if -1 in labels:
                    # Filter out noise points for scoring
                    non_noise_mask = labels != -1
                    if np.sum(non_noise_mask) > 1:
                        score = silhouette_score(
                            X[non_noise_mask], labels[non_noise_mask]
                        )
                    else:
                        continue
                else:
                    score = silhouette_score(X, labels)

                if score > best_score:
                    best_score = score
                    best_result = {
                        "algorithm": "DBSCAN",
                        "labels": labels.tolist(),
                        "item_ids": item_ids,
                        "n_clusters": len(set(labels)) - (1 if -1 in labels else 0),
                        "n_noise": np.sum(labels == -1),
                        "silhouette_score": score,
                        "parameters": {"eps": eps, "min_samples": 2},
                    }

            return best_result

        except Exception as e:
            logger.error(f"Error in DBSCAN clustering: {e}")
            return None

    def _apply_kmeans(
        self, X: np.ndarray, item_ids: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Apply K-Means clustering"""
        try:
            best_result = None
            best_score = -1

            # Try different numbers of clusters
            max_k = min(len(X) - 1, 10)

            for k in range(2, max_k + 1):
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                labels = kmeans.fit_predict(X)

                # Calculate silhouette score
                score = silhouette_score(X, labels)

                if score > best_score:
                    best_score = score
                    best_result = {
                        "algorithm": "K-Means",
                        "labels": labels.tolist(),
                        "item_ids": item_ids,
                        "n_clusters": k,
                        "silhouette_score": score,
                        "cluster_centers": kmeans.cluster_centers_.tolist(),
                        "parameters": {"n_clusters": k},
                    }

            return best_result

        except Exception as e:
            logger.error(f"Error in K-Means clustering: {e}")
            return None


class AssociationRuleMiner:
    """Association rule mining for discovering relationships"""

    def __init__(self, min_support: float = 0.1, min_confidence: float = 0.5):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.frequent_itemsets = {}
        self.association_rules = []

    def mine_device_associations(
        self, transactions: List[List[str]]
    ) -> List[Association]:
        """Mine association rules from device co-occurrence data"""
        if len(transactions) < 5:
            return []

        # Generate frequent itemsets
        frequent_itemsets = self._generate_frequent_itemsets(transactions)

        # Generate association rules
        rules = self._generate_association_rules(frequent_itemsets, transactions)

        return rules

    def mine_network_associations(
        self, network_data: List[Dict[str, Any]]
    ) -> List[Association]:
        """Mine associations between network characteristics"""
        # Convert network data to transaction format
        transactions = []

        for network in network_data:
            transaction = []

            # Add characteristics as items
            if network.get("encryption"):
                transaction.append(f"encryption_{network['encryption']}")

            if network.get("vendor"):
                transaction.append(f"vendor_{network['vendor']}")

            if network.get("channel"):
                channel_band = "low" if network["channel"] <= 6 else "high"
                transaction.append(f"channel_band_{channel_band}")

            if network.get("signal_strength"):
                signal_level = "strong" if network["signal_strength"] > -60 else "weak"
                transaction.append(f"signal_{signal_level}")

            if transaction:
                transactions.append(transaction)

        return self.mine_device_associations(transactions)

    def _generate_frequent_itemsets(
        self, transactions: List[List[str]]
    ) -> Dict[int, List[Set[str]]]:
        """Generate frequent itemsets using Apriori algorithm"""
        frequent_itemsets = {}

        # Get all unique items
        all_items = set()
        for transaction in transactions:
            all_items.update(transaction)

        # Generate 1-itemsets
        k = 1
        candidates = [{item} for item in all_items]
        frequent_k = []

        for itemset in candidates:
            support = self._calculate_support(itemset, transactions)
            if support >= self.min_support:
                frequent_k.append(itemset)

        if not frequent_k:
            return frequent_itemsets

        frequent_itemsets[k] = frequent_k

        # Generate k-itemsets (k > 1)
        while frequent_itemsets[k]:
            k += 1
            candidates = self._generate_candidates(frequent_itemsets[k - 1])
            frequent_k = []

            for itemset in candidates:
                support = self._calculate_support(itemset, transactions)
                if support >= self.min_support:
                    frequent_k.append(itemset)

            if frequent_k:
                frequent_itemsets[k] = frequent_k
            else:
                break

        return frequent_itemsets

    def _generate_candidates(self, frequent_itemsets: List[Set[str]]) -> List[Set[str]]:
        """Generate candidate itemsets for next level"""
        candidates = []
        n = len(frequent_itemsets)

        for i in range(n):
            for j in range(i + 1, n):
                # Join itemsets if they differ by exactly one item
                union = frequent_itemsets[i].union(frequent_itemsets[j])
                if len(union) == len(frequent_itemsets[i]) + 1:
                    candidates.append(union)

        return candidates

    def _calculate_support(
        self, itemset: Set[str], transactions: List[List[str]]
    ) -> float:
        """Calculate support for itemset"""
        count = 0
        for transaction in transactions:
            if itemset.issubset(set(transaction)):
                count += 1

        return count / len(transactions) if transactions else 0.0

    def _generate_association_rules(
        self,
        frequent_itemsets: Dict[int, List[Set[str]]],
        transactions: List[List[str]],
    ) -> List[Association]:
        """Generate association rules from frequent itemsets"""
        rules = []

        # Generate rules from itemsets of size 2 or more
        for k in range(2, len(frequent_itemsets) + 1):
            if k not in frequent_itemsets:
                continue

            for itemset in frequent_itemsets[k]:
                # Generate all possible antecedent/consequent combinations
                for i in range(1, len(itemset)):
                    for antecedent in self._get_subsets(itemset, i):
                        consequent = itemset - antecedent

                        # Calculate confidence
                        support_itemset = self._calculate_support(itemset, transactions)
                        support_antecedent = self._calculate_support(
                            antecedent, transactions
                        )

                        if support_antecedent > 0:
                            confidence = support_itemset / support_antecedent

                            if confidence >= self.min_confidence:
                                # Calculate lift
                                support_consequent = self._calculate_support(
                                    consequent, transactions
                                )
                                lift = (
                                    confidence / support_consequent
                                    if support_consequent > 0
                                    else 0
                                )

                                rule = Association(
                                    antecedent=antecedent,
                                    consequent=consequent,
                                    support=support_itemset,
                                    confidence=confidence,
                                    lift=lift,
                                    description=f"{list(antecedent)} → {list(consequent)}",
                                )
                                rules.append(rule)

        # Sort rules by confidence
        rules.sort(key=lambda r: r.confidence, reverse=True)
        return rules

    def _get_subsets(self, itemset: Set[str], size: int) -> List[Set[str]]:
        """Get all subsets of given size"""
        from itertools import combinations

        items = list(itemset)
        return [set(combo) for combo in combinations(items, size)]


class InsightGenerator:
    """Automated insight generation from patterns and data"""

    def __init__(self):
        self.insights = []
        self.insight_rules = self._load_insight_rules()

    def generate_insights(
        self, patterns: List[Pattern], data: Dict[str, Any]
    ) -> List[Insight]:
        """Generate insights from discovered patterns and data"""
        insights = []

        # Analyze patterns for insights
        insights.extend(self._analyze_temporal_patterns(patterns))
        insights.extend(self._analyze_anomaly_patterns(patterns))
        insights.extend(self._analyze_network_data(data))
        insights.extend(self._analyze_security_implications(patterns, data))

        # Sort insights by severity and confidence
        insights.sort(
            key=lambda i: (self._severity_score(i.severity), i.confidence), reverse=True
        )

        self.insights.extend(insights)
        return insights

    def _analyze_temporal_patterns(self, patterns: List[Pattern]) -> List[Insight]:
        """Analyze temporal patterns for insights"""
        insights = []

        temporal_patterns = [
            p for p in patterns if p.pattern_type == PatternType.TEMPORAL
        ]

        for pattern in temporal_patterns:
            if "period" in pattern.parameters:
                # Periodic pattern insight
                period = pattern.parameters["period"]
                confidence = pattern.confidence

                if period < 60:  # Less than 1 minute
                    severity = "high"
                    title = "High-frequency periodic activity detected"
                    description = f"Detected periodic activity with {period}-second intervals, possibly indicating automated scanning or attacks"
                    recommendations = [
                        "Investigate source of periodic traffic",
                        "Consider implementing rate limiting",
                        "Monitor for potential security threats",
                    ]
                elif period < 3600:  # Less than 1 hour
                    severity = "medium"
                    title = "Regular periodic activity detected"
                    description = f"Detected regular activity pattern with {period/60:.1f}-minute intervals"
                    recommendations = [
                        "Verify if this is expected behavior",
                        "Document periodic activities for baseline",
                    ]
                else:
                    severity = "low"
                    title = "Long-term periodic pattern detected"
                    description = f"Detected long-term pattern with {period/3600:.1f}-hour intervals"
                    recommendations = [
                        "Monitor for consistency",
                        "Use for capacity planning",
                    ]

                insight = Insight(
                    insight_id=f"temporal_periodic_{pattern.pattern_id}",
                    insight_type=InsightType.TREND_ANALYSIS,
                    title=title,
                    description=description,
                    confidence=confidence,
                    severity=severity,
                    timestamp=datetime.now(),
                    data_source="temporal_pattern_analysis",
                    recommendations=recommendations,
                    related_patterns=[pattern.pattern_id],
                )
                insights.append(insight)

        return insights

    def _analyze_anomaly_patterns(self, patterns: List[Pattern]) -> List[Insight]:
        """Analyze anomaly patterns for insights"""
        insights = []

        anomaly_patterns = [p for p in patterns if "anomaly" in p.pattern_id.lower()]

        if len(anomaly_patterns) > 3:  # Multiple anomalies
            insight = Insight(
                insight_id="multiple_anomalies_detected",
                insight_type=InsightType.ANOMALY_DETECTION,
                title="Multiple anomalies detected",
                description=f"Detected {len(anomaly_patterns)} anomalous patterns, indicating potential security concerns",
                confidence=0.8,
                severity="high",
                timestamp=datetime.now(),
                data_source="anomaly_pattern_analysis",
                recommendations=[
                    "Investigate anomalous activities immediately",
                    "Check for potential security breaches",
                    "Review system logs for correlation",
                    "Consider implementing additional monitoring",
                ],
                related_patterns=[p.pattern_id for p in anomaly_patterns],
            )
            insights.append(insight)

        return insights

    def _analyze_network_data(self, data: Dict[str, Any]) -> List[Insight]:
        """Analyze network data for insights"""
        insights = []

        networks = data.get("networks", [])
        data.get("devices", [])

        if networks:
            # Analyze encryption distribution
            encryption_types = [n.get("encryption", "Unknown") for n in networks]
            encryption_counts = Counter(encryption_types)

            open_networks = encryption_counts.get("Open", 0)
            total_networks = len(networks)

            if open_networks > 0:
                open_percentage = (open_networks / total_networks) * 100

                if open_percentage > 20:
                    severity = "high"
                    title = "High number of open networks detected"
                    description = (
                        f"{open_percentage:.1f}% of networks are open and unencrypted"
                    )
                elif open_percentage > 5:
                    severity = "medium"
                    title = "Open networks detected"
                    description = f"{open_percentage:.1f}% of networks are open"
                else:
                    severity = "low"
                    title = "Few open networks detected"
                    description = f"{open_percentage:.1f}% of networks are open"

                insight = Insight(
                    insight_id="open_networks_analysis",
                    insight_type=InsightType.RECOMMENDATION,
                    title=title,
                    description=description,
                    confidence=0.9,
                    severity=severity,
                    timestamp=datetime.now(),
                    data_source="network_analysis",
                    recommendations=[
                        "Secure open networks with WPA2/WPA3 encryption",
                        "Educate users about wireless security",
                        "Implement network access controls",
                    ],
                    supporting_data={
                        "open_networks": open_networks,
                        "total_networks": total_networks,
                        "open_percentage": open_percentage,
                    },
                )
                insights.append(insight)

        return insights

    def _analyze_security_implications(
        self, patterns: List[Pattern], data: Dict[str, Any]
    ) -> List[Insight]:
        """Analyze security implications from patterns and data"""
        insights = []

        # Look for security-related patterns
        security_indicators = 0
        security_concerns = []

        for pattern in patterns:
            if any(
                keyword in pattern.description.lower()
                for keyword in ["anomaly", "suspicious", "unusual"]
            ):
                security_indicators += 1
                security_concerns.append(pattern.description)

        # Check for weak encryption
        networks = data.get("networks", [])
        weak_encryption_count = sum(
            1 for n in networks if n.get("encryption") in ["WEP", "Open"]
        )

        if weak_encryption_count > 0:
            security_indicators += 1
            security_concerns.append(
                f"{weak_encryption_count} networks with weak/no encryption"
            )

        # Generate security insight if multiple indicators
        if security_indicators >= 2:
            insight = Insight(
                insight_id="security_risk_assessment",
                insight_type=InsightType.ALERT,
                title="Multiple security risks detected",
                description=f"Identified {security_indicators} security indicators requiring attention",
                confidence=0.85,
                severity="high",
                timestamp=datetime.now(),
                data_source="security_analysis",
                recommendations=[
                    "Conduct immediate security assessment",
                    "Implement stronger encryption protocols",
                    "Monitor for suspicious activities",
                    "Update security policies and procedures",
                ],
                supporting_data={
                    "security_indicators": security_indicators,
                    "security_concerns": security_concerns,
                },
            )
            insights.append(insight)

        return insights

    def _load_insight_rules(self) -> Dict[str, Any]:
        """Load insight generation rules"""
        return {
            "anomaly_threshold": 0.7,
            "trend_threshold": 0.8,
            "correlation_threshold": 0.6,
            "security_keywords": ["attack", "scan", "probe", "intrusion", "malicious"],
            "performance_keywords": ["slow", "congestion", "interference", "overload"],
        }

    def _severity_score(self, severity: str) -> int:
        """Convert severity to numeric score for sorting"""
        scores = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}
        return scores.get(severity, 0)


class AdvancedDataMiner:
    """Main advanced data mining coordinator"""

    def __init__(self):
        self.temporal_miner = TemporalPatternMiner()
        self.clustering_analyzer = ClusteringAnalyzer()
        self.association_miner = AssociationRuleMiner()
        self.insight_generator = InsightGenerator()

        self.discovered_patterns = []
        self.generated_insights = []
        self.mining_history = []

    def mine_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive data mining analysis"""
        results = {
            "patterns": [],
            "clusters": {},
            "associations": [],
            "insights": [],
            "summary": {},
        }

        logger.info("Starting comprehensive data mining analysis")

        # Temporal pattern mining
        if "time_series" in data:
            for series_name, series_data in data["time_series"].items():
                for timestamp, value in series_data:
                    self.temporal_miner.add_time_series_data(
                        series_name, timestamp, value
                    )

                # Mine patterns from this series
                patterns = []
                patterns.extend(
                    self.temporal_miner.detect_periodic_patterns(series_name)
                )
                patterns.extend(self.temporal_miner.detect_trend_patterns(series_name))
                patterns.extend(
                    self.temporal_miner.detect_anomaly_patterns(series_name)
                )

                results["patterns"].extend(patterns)
                self.discovered_patterns.extend(patterns)

        # Clustering analysis
        if "devices" in data:
            device_clusters = self.clustering_analyzer.cluster_devices(
                data["devices"], ["signal_strength", "channel", "vendor_score"]
            )
            results["clusters"]["devices"] = device_clusters

        if "networks" in data:
            network_clusters = self.clustering_analyzer.cluster_networks(
                data["networks"]
            )
            results["clusters"]["networks"] = network_clusters

        # Association rule mining
        if "transactions" in data:
            associations = self.association_miner.mine_device_associations(
                data["transactions"]
            )
            results["associations"].extend(associations)

        if "networks" in data:
            network_associations = self.association_miner.mine_network_associations(
                data["networks"]
            )
            results["associations"].extend(network_associations)

        # Insight generation
        insights = self.insight_generator.generate_insights(results["patterns"], data)
        results["insights"] = insights
        self.generated_insights.extend(insights)

        # Generate summary
        results["summary"] = self._generate_mining_summary(results)

        # Store mining history
        self.mining_history.append(
            {
                "timestamp": datetime.now(),
                "data_points": len(data.get("networks", []))
                + len(data.get("devices", [])),
                "patterns_found": len(results["patterns"]),
                "insights_generated": len(results["insights"]),
            }
        )

        logger.info(
            f"Data mining completed: {len(results['patterns'])} patterns, {len(results['insights'])} insights"
        )

        return results

    def get_mining_statistics(self) -> Dict[str, Any]:
        """Get data mining statistics"""
        return {
            "total_patterns_discovered": len(self.discovered_patterns),
            "total_insights_generated": len(self.generated_insights),
            "mining_sessions": len(self.mining_history),
            "pattern_types": {
                pattern_type.value: len(
                    [
                        p
                        for p in self.discovered_patterns
                        if p.pattern_type == pattern_type
                    ]
                )
                for pattern_type in PatternType
            },
            "insight_types": {
                insight_type.value: len(
                    [
                        i
                        for i in self.generated_insights
                        if i.insight_type == insight_type
                    ]
                )
                for insight_type in InsightType
            },
            "recent_mining_activity": (
                self.mining_history[-10:] if self.mining_history else []
            ),
        }

    def _generate_mining_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate summary of mining results"""
        summary = {
            "patterns_by_type": {},
            "insights_by_severity": {},
            "clustering_quality": {},
            "association_strength": {},
            "recommendations": [],
        }

        # Patterns by type
        for pattern in results["patterns"]:
            pattern_type = pattern.pattern_type.value
            summary["patterns_by_type"][pattern_type] = (
                summary["patterns_by_type"].get(pattern_type, 0) + 1
            )

        # Insights by severity
        for insight in results["insights"]:
            severity = insight.severity
            summary["insights_by_severity"][severity] = (
                summary["insights_by_severity"].get(severity, 0) + 1
            )

        # Clustering quality
        for cluster_type, cluster_data in results["clusters"].items():
            if cluster_data:
                for algorithm, result in cluster_data.items():
                    summary["clustering_quality"][f"{cluster_type}_{algorithm}"] = (
                        result.get("silhouette_score", 0)
                    )

        # Association strength
        if results["associations"]:
            avg_confidence = np.mean([a.confidence for a in results["associations"]])
            summary["association_strength"]["average_confidence"] = avg_confidence
            summary["association_strength"]["total_rules"] = len(
                results["associations"]
            )

        # Generate recommendations
        if summary["insights_by_severity"].get("high", 0) > 0:
            summary["recommendations"].append(
                "Address high-severity insights immediately"
            )

        if summary["patterns_by_type"].get("temporal", 0) > 5:
            summary["recommendations"].append(
                "Consider trend analysis for capacity planning"
            )

        if summary["clustering_quality"]:
            avg_quality = np.mean(list(summary["clustering_quality"].values()))
            if avg_quality > 0.7:
                summary["recommendations"].append(
                    "High-quality clusters detected - consider device categorization"
                )

        return summary


# Example usage and testing
def test_advanced_data_mining():
    """Test advanced data mining functionality"""
    print("Testing Advanced Data Mining...")

    # Create data miner
    miner = AdvancedDataMiner()

    # Generate sample data
    sample_data = {
        "time_series": {
            "network_count": [
                (datetime.now() - timedelta(minutes=i), 10 + i % 5)
                for i in range(100, 0, -1)
            ],
            "signal_strength": [
                (datetime.now() - timedelta(minutes=i), -50 - (i % 20))
                for i in range(100, 0, -1)
            ],
        },
        "networks": [
            {
                "ssid": "HomeNetwork1",
                "encryption": "WPA2",
                "channel": 6,
                "signal_strength": -45,
                "vendor": "Cisco",
            },
            {
                "ssid": "GuestNetwork",
                "encryption": "Open",
                "channel": 11,
                "signal_strength": -55,
                "vendor": "Netgear",
            },
            {
                "ssid": "OfficeWiFi",
                "encryption": "WPA3",
                "channel": 1,
                "signal_strength": -40,
                "vendor": "Cisco",
            },
            {
                "ssid": "PublicHotspot",
                "encryption": "Open",
                "channel": 6,
                "signal_strength": -65,
                "vendor": "Linksys",
            },
            {
                "ssid": "SecureNet",
                "encryption": "WPA2",
                "channel": 11,
                "signal_strength": -50,
                "vendor": "Cisco",
            },
        ],
        "devices": [
            {"id": "device1", "signal_strength": -45, "channel": 6, "vendor_score": 1},
            {"id": "device2", "signal_strength": -55, "channel": 11, "vendor_score": 2},
            {"id": "device3", "signal_strength": -40, "channel": 1, "vendor_score": 1},
            {"id": "device4", "signal_strength": -65, "channel": 6, "vendor_score": 3},
            {"id": "device5", "signal_strength": -50, "channel": 11, "vendor_score": 1},
        ],
        "transactions": [
            ["device1", "network1", "cisco"],
            ["device2", "network2", "netgear"],
            ["device1", "network1", "cisco", "wpa2"],
            ["device3", "network3", "cisco", "wpa3"],
            ["device4", "network4", "linksys", "open"],
            ["device5", "network5", "cisco", "wpa2"],
        ],
    }

    # Run data mining
    results = miner.mine_data(sample_data)

    # Display results
    print("\nMining Results:")
    print(f"  Patterns discovered: {len(results['patterns'])}")
    for pattern in results["patterns"][:3]:  # Show first 3 patterns
        print(f"    - {pattern.description} (confidence: {pattern.confidence:.2f})")

    print(f"  Insights generated: {len(results['insights'])}")
    for insight in results["insights"][:3]:  # Show first 3 insights
        print(f"    - {insight.title} (severity: {insight.severity})")

    print(f"  Association rules: {len(results['associations'])}")
    for assoc in results["associations"][:2]:  # Show first 2 associations
        print(f"    - {assoc.description} (confidence: {assoc.confidence:.2f})")

    # Display clustering results
    for cluster_type, cluster_data in results["clusters"].items():
        print(f"  {cluster_type.title()} clustering:")
        for algorithm, result in cluster_data.items():
            print(
                f"    - {algorithm}: {result['n_clusters']} clusters (score: {result.get('silhouette_score', 0):.2f})"
            )

    # Get statistics
    stats = miner.get_mining_statistics()
    print("\nMining Statistics:")
    print(f"  Total patterns: {stats['total_patterns_discovered']}")
    print(f"  Total insights: {stats['total_insights_generated']}")
    print(f"  Mining sessions: {stats['mining_sessions']}")

    print("Advanced Data Mining test completed!")


if __name__ == "__main__":
    test_advanced_data_mining()
