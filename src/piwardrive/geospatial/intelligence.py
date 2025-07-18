"""
Geospatial Intelligence Platform for PiWardrive
Advanced indoor positioning, floor plan generation, and spatial analytics
"""

import logging
import math
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple

import numpy as np
from scipy.optimize import minimize

logger = logging.getLogger(__name__)


class PositioningMethod(Enum):
    """Indoor positioning methods"""

    RSSI_TRILATERATION = "rssi_trilateration"
    TDOA = "tdoa"
    AOA = "aoa"
    FINGERPRINTING = "fingerprinting"
    DEAD_RECKONING = "dead_reckoning"
    HYBRID = "hybrid"


class LocationConfidence(Enum):
    """Location confidence levels"""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


@dataclass
class Position:
    """3D position with uncertainty"""

    x: float
    y: float
    z: float
    uncertainty: float
    confidence: LocationConfidence
    timestamp: datetime
    method: PositioningMethod


@dataclass
class AccessPointLocation:
    """Access point with known location"""

    bssid: str
    ssid: str
    position: Position
    tx_power: float
    antenna_gain: float
    frequency: float


@dataclass
class RSSIMeasurement:
    """RSSI measurement from access point"""

    bssid: str
    rssi: float
    timestamp: datetime
    channel: int
    frequency: float


@dataclass
class FloorPlanNode:
    """Node in floor plan graph"""

    id: str
    position: Position
    node_type: str  # 'room', 'corridor', 'junction', 'entrance'
    properties: Dict


@dataclass
class FloorPlanEdge:
    """Edge in floor plan graph"""

    from_node: str
    to_node: str
    distance: float
    traversable: bool
    properties: Dict


@dataclass
class Room:
    """Room definition"""

    id: str
    name: str
    corners: List[Tuple[float, float]]
    center: Tuple[float, float]
    area: float
    floor_level: int


@dataclass
class MovementPattern:
    """Detected movement pattern"""

    path: List[Position]
    velocity: float
    direction: float
    duration: float
    classification: str  # 'walking', 'running', 'stationary', 'vehicle'


class RSSITrilateration:
    """RSSI-based trilateration positioning"""

    def __init__(self, path_loss_exponent: float = 2.0):
        self.path_loss_exponent = path_loss_exponent
        self.reference_distance = 1.0  # meters
        self.reference_rssi = -40  # dBm at 1 meter

    def estimate_distance(self, rssi: float, tx_power: float) -> float:
        """Estimate distance from RSSI measurement"""
        if rssi >= tx_power:
            return self.reference_distance

        # Log-distance path loss model
        distance = self.reference_distance * 10 ** (
            (tx_power - rssi) / (10 * self.path_loss_exponent)
        )
        return distance

    def trilaterate(
        self,
        ap_positions: List[AccessPointLocation],
        rssi_measurements: List[RSSIMeasurement],
    ) -> Optional[Position]:
        """Perform trilateration using RSSI measurements"""
        if len(ap_positions) < 3 or len(rssi_measurements) < 3:
            return None

        # Match measurements to AP positions
        matched_data = []
        for measurement in rssi_measurements:
            for ap in ap_positions:
                if ap.bssid == measurement.bssid:
                    distance = self.estimate_distance(measurement.rssi, ap.tx_power)
                    matched_data.append((ap.position, distance))
                    break

        if len(matched_data) < 3:
            return None

        # Set up optimization problem
        def objective(pos):
            x, y, z = pos
            error = 0
            for ap_pos, distance in matched_data:
                calculated_distance = math.sqrt(
                    (x - ap_pos.x) ** 2 + (y - ap_pos.y) ** 2 + (z - ap_pos.z) ** 2
                )
                error += (calculated_distance - distance) ** 2
            return error

        # Initial guess (centroid of AP positions)
        initial_guess = [
            sum(ap_pos.x for ap_pos, _ in matched_data) / len(matched_data),
            sum(ap_pos.y for ap_pos, _ in matched_data) / len(matched_data),
            sum(ap_pos.z for ap_pos, _ in matched_data) / len(matched_data),
        ]

        # Solve optimization
        result = minimize(objective, initial_guess, method="L-BFGS-B")

        if result.success:
            # Calculate uncertainty based on residual error
            uncertainty = math.sqrt(result.fun / len(matched_data))

            # Determine confidence based on uncertainty
            if uncertainty < 2.0:
                confidence = LocationConfidence.HIGH
            elif uncertainty < 5.0:
                confidence = LocationConfidence.MEDIUM
            else:
                confidence = LocationConfidence.LOW

            return Position(
                x=result.x[0],
                y=result.x[1],
                z=result.x[2],
                uncertainty=uncertainty,
                confidence=confidence,
                timestamp=datetime.now(),
                method=PositioningMethod.RSSI_TRILATERATION,
            )

        return None


class FingerprintingDatabase:
    """WiFi fingerprinting database for positioning"""

    def __init__(self):
        self.fingerprints = {}  # {location_id: {bssid: rssi_stats}}
        self.locations = {}  # {location_id: Position}

    def add_fingerprint(
        self,
        location_id: str,
        position: Position,
        rssi_measurements: List[RSSIMeasurement],
    ):
        """Add fingerprint to database"""
        if location_id not in self.fingerprints:
            self.fingerprints[location_id] = {}
            self.locations[location_id] = position

        # Update RSSI statistics for each AP
        for measurement in rssi_measurements:
            bssid = measurement.bssid
            if bssid not in self.fingerprints[location_id]:
                self.fingerprints[location_id][bssid] = {
                    "rssi_values": [],
                    "mean": 0,
                    "std": 0,
                    "count": 0,
                }

            # Add measurement
            stats = self.fingerprints[location_id][bssid]
            stats["rssi_values"].append(measurement.rssi)
            stats["count"] += 1

            # Update statistics
            stats["mean"] = np.mean(stats["rssi_values"])
            stats["std"] = np.std(stats["rssi_values"])

    def match_fingerprint(
        self, rssi_measurements: List[RSSIMeasurement]
    ) -> Optional[Position]:
        """Match current measurements to fingerprint database"""
        if not self.fingerprints:
            return None

        # Create measurement vector
        measurement_dict = {m.bssid: m.rssi for m in rssi_measurements}

        best_match = None
        best_score = float("in")

        for location_id, fingerprint in self.fingerprints.items():
            # Calculate matching score using Euclidean distance
            score = 0
            common_aps = 0

            for bssid, stats in fingerprint.items():
                if bssid in measurement_dict:
                    # Weighted distance considering standard deviation
                    expected_rssi = stats["mean"]
                    measured_rssi = measurement_dict[bssid]
                    weight = 1.0 / (
                        stats["std"] + 1.0
                    )  # Higher weight for stable measurements

                    score += weight * (expected_rssi - measured_rssi) ** 2
                    common_aps += 1

            if common_aps >= 3:  # Minimum number of common APs
                normalized_score = score / common_aps

                if normalized_score < best_score:
                    best_score = normalized_score
                    best_match = location_id

        if best_match:
            position = self.locations[best_match]

            # Determine confidence based on matching score
            if best_score < 25:
                confidence = LocationConfidence.HIGH
            elif best_score < 100:
                confidence = LocationConfidence.MEDIUM
            else:
                confidence = LocationConfidence.LOW

            return Position(
                x=position.x,
                y=position.y,
                z=position.z,
                uncertainty=math.sqrt(best_score),
                confidence=confidence,
                timestamp=datetime.now(),
                method=PositioningMethod.FINGERPRINTING,
            )

        return None


class FloorPlanGenerator:
    """Automatic floor plan generation from WiFi data"""

    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.rooms = []
        self.grid_resolution = 1.0  # meters

    def generate_floor_plan(
        self, positions: List[Position], rssi_measurements: List[List[RSSIMeasurement]]
    ) -> Dict:
        """Generate floor plan from position and RSSI data"""
        # Create spatial grid
        grid = self._create_spatial_grid(positions)

        # Identify rooms and corridors
        rooms = self._identify_rooms(grid, positions)

        # Generate connectivity graph
        nodes, edges = self._generate_connectivity_graph(rooms, positions)

        # Create floor plan structure
        floor_plan = {
            "nodes": nodes,
            "edges": edges,
            "rooms": rooms,
            "grid": grid,
            "metadata": {
                "generation_time": datetime.now(),
                "num_positions": len(positions),
                "coverage_area": self._calculate_coverage_area(positions),
                "confidence": self._calculate_plan_confidence(
                    positions, rssi_measurements
                ),
            },
        }

        return floor_plan

    def _create_spatial_grid(self, positions: List[Position]) -> np.ndarray:
        """Create spatial occupancy grid"""
        if not positions:
            return np.array([])

        # Find bounding box
        min_x = min(p.x for p in positions)
        max_x = max(p.x for p in positions)
        min_y = min(p.y for p in positions)
        max_y = max(p.y for p in positions)

        # Create grid
        grid_width = int((max_x - min_x) / self.grid_resolution) + 1
        grid_height = int((max_y - min_y) / self.grid_resolution) + 1
        grid = np.zeros((grid_height, grid_width))

        # Fill grid with position data
        for position in positions:
            grid_x = int((position.x - min_x) / self.grid_resolution)
            grid_y = int((position.y - min_y) / self.grid_resolution)

            if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
                grid[grid_y, grid_x] += 1

        return grid

    def _identify_rooms(
        self, grid: np.ndarray, positions: List[Position]
    ) -> List[Room]:
        """Identify rooms from occupancy grid"""
        if grid.size == 0:
            return []

        # Apply threshold to identify occupied areas
        threshold = np.percentile(grid[grid > 0], 50) if np.any(grid > 0) else 0
        occupied_grid = grid > threshold

        # Find connected components (rooms)
        from scipy.ndimage import label

        labeled_grid, num_features = label(occupied_grid)

        rooms = []
        for i in range(1, num_features + 1):
            room_mask = labeled_grid == i
            room_coords = np.where(room_mask)

            if len(room_coords[0]) > 4:  # Minimum size for a room
                # Calculate room properties
                corners = self._extract_room_corners(room_mask)
                center = (np.mean(room_coords[1]), np.mean(room_coords[0]))
                area = np.sum(room_mask) * self.grid_resolution**2

                room = Room(
                    id=f"room_{i}",
                    name=f"Room {i}",
                    corners=corners,
                    center=center,
                    area=area,
                    floor_level=0,
                )
                rooms.append(room)

        return rooms

    def _extract_room_corners(self, room_mask: np.ndarray) -> List[Tuple[float, float]]:
        """Extract corner coordinates of a room"""
        # Find contour of the room

        # Simple corner detection (could be improved with OpenCV)
        coords = np.where(room_mask)
        if len(coords[0]) > 0:
            # Find bounding box corners
            min_y, max_y = np.min(coords[0]), np.max(coords[0])
            min_x, max_x = np.min(coords[1]), np.max(coords[1])

            corners = [
                (min_x * self.grid_resolution, min_y * self.grid_resolution),
                (max_x * self.grid_resolution, min_y * self.grid_resolution),
                (max_x * self.grid_resolution, max_y * self.grid_resolution),
                (min_x * self.grid_resolution, max_y * self.grid_resolution),
            ]
            return corners

        return []

    def _generate_connectivity_graph(
        self, rooms: List[Room], positions: List[Position]
    ) -> Tuple[Dict, List]:
        """Generate connectivity graph between rooms"""
        nodes = {}
        edges = []

        # Create nodes for each room
        for room in rooms:
            node = FloorPlanNode(
                id=room.id,
                position=Position(
                    x=room.center[0],
                    y=room.center[1],
                    z=0,
                    uncertainty=0,
                    confidence=LocationConfidence.HIGH,
                    timestamp=datetime.now(),
                    method=PositioningMethod.FINGERPRINTING,
                ),
                node_type="room",
                properties={"area": room.area, "name": room.name},
            )
            nodes[room.id] = node

        # Create edges between adjacent rooms
        for i, room1 in enumerate(rooms):
            for j, room2 in enumerate(rooms[i + 1 :], i + 1):
                distance = math.sqrt(
                    (room1.center[0] - room2.center[0]) ** 2
                    + (room1.center[1] - room2.center[1]) ** 2
                )

                # Connect rooms if they're close enough
                if distance < 20:  # meters
                    edge = FloorPlanEdge(
                        from_node=room1.id,
                        to_node=room2.id,
                        distance=distance,
                        traversable=True,
                        properties={},
                    )
                    edges.append(edge)

        return nodes, edges

    def _calculate_coverage_area(self, positions: List[Position]) -> float:
        """Calculate total coverage area"""
        if len(positions) < 3:
            return 0

        # Calculate convex hull area
        points = [(p.x, p.y) for p in positions]

        # Simple area calculation (could use scipy.spatial.ConvexHull)
        min_x = min(p[0] for p in points)
        max_x = max(p[0] for p in points)
        min_y = min(p[1] for p in points)
        max_y = max(p[1] for p in points)

        return (max_x - min_x) * (max_y - min_y)

    def _calculate_plan_confidence(
        self, positions: List[Position], rssi_measurements: List[List[RSSIMeasurement]]
    ) -> float:
        """Calculate confidence in generated floor plan"""
        if not positions:
            return 0.0

        # Base confidence on position accuracy and measurement density
        avg_uncertainty = np.mean([p.uncertainty for p in positions])
        measurement_density = (
            len(rssi_measurements) / len(positions) if positions else 0
        )

        # Normalize to 0-1 scale
        uncertainty_score = max(0, 1 - avg_uncertainty / 10)
        density_score = min(1, measurement_density / 5)

        return (uncertainty_score + density_score) / 2


class MovementAnalyzer:
    """Movement pattern analysis and tracking"""

    def __init__(self, velocity_threshold: float = 0.5):
        self.velocity_threshold = velocity_threshold
        self.position_history = []
        self.patterns = []

    def add_position(self, position: Position):
        """Add new position to tracking history"""
        self.position_history.append(position)

        # Keep only recent positions (last 100)
        if len(self.position_history) > 100:
            self.position_history.pop(0)

    def analyze_movement(self) -> List[MovementPattern]:
        """Analyze movement patterns from position history"""
        if len(self.position_history) < 2:
            return []

        patterns = []

        # Calculate velocities
        velocities = []
        for i in range(1, len(self.position_history)):
            pos1 = self.position_history[i - 1]
            pos2 = self.position_history[i]

            distance = math.sqrt(
                (pos2.x - pos1.x) ** 2 + (pos2.y - pos1.y) ** 2 + (pos2.z - pos1.z) ** 2
            )

            time_diff = (pos2.timestamp - pos1.timestamp).total_seconds()
            if time_diff > 0:
                velocity = distance / time_diff
                velocities.append(velocity)

        if not velocities:
            return patterns

        # Classify movement
        avg_velocity = np.mean(velocities)

        if avg_velocity < 0.5:
            classification = "stationary"
        elif avg_velocity < 2.0:
            classification = "walking"
        elif avg_velocity < 5.0:
            classification = "running"
        else:
            classification = "vehicle"

        # Calculate overall direction
        if len(self.position_history) >= 2:
            start_pos = self.position_history[0]
            end_pos = self.position_history[-1]

            direction = (
                math.atan2(end_pos.y - start_pos.y, end_pos.x - start_pos.x)
                * 180
                / math.pi
            )
        else:
            direction = 0

        # Create movement pattern
        pattern = MovementPattern(
            path=self.position_history.copy(),
            velocity=avg_velocity,
            direction=direction,
            duration=(
                self.position_history[-1].timestamp - self.position_history[0].timestamp
            ).total_seconds(),
            classification=classification,
        )

        patterns.append(pattern)
        return patterns


class GeospatialIntelligence:
    """Main geospatial intelligence platform"""

    def __init__(self):
        self.rssi_trilateration = RSSITrilateration()
        self.fingerprinting_db = FingerprintingDatabase()
        self.floor_plan_generator = FloorPlanGenerator()
        self.movement_analyzer = MovementAnalyzer()
        self.ap_locations = []
        self.position_history = []

    def add_access_point(self, ap_location: AccessPointLocation):
        """Add access point with known location"""
        self.ap_locations.append(ap_location)

    def estimate_position(
        self, rssi_measurements: List[RSSIMeasurement]
    ) -> Optional[Position]:
        """Estimate position using available methods"""
        # Try trilateration first
        if len(self.ap_locations) >= 3:
            position = self.rssi_trilateration.trilaterate(
                self.ap_locations, rssi_measurements
            )
            if position:
                self.position_history.append(position)
                self.movement_analyzer.add_position(position)
                return position

        # Try fingerprinting
        position = self.fingerprinting_db.match_fingerprint(rssi_measurements)
        if position:
            self.position_history.append(position)
            self.movement_analyzer.add_position(position)
            return position

        return None

    def train_fingerprinting(
        self,
        location_id: str,
        position: Position,
        rssi_measurements: List[RSSIMeasurement],
    ):
        """Train fingerprinting database"""
        self.fingerprinting_db.add_fingerprint(location_id, position, rssi_measurements)

    def generate_floor_plan(self) -> Dict:
        """Generate floor plan from collected data"""
        # Collect all RSSI measurements for each position
        rssi_by_position = []  # This would be populated from actual data

        return self.floor_plan_generator.generate_floor_plan(
            self.position_history, rssi_by_position
        )

    def analyze_movement_patterns(self) -> List[MovementPattern]:
        """Analyze movement patterns"""
        return self.movement_analyzer.analyze_movement()

    def get_positioning_stats(self) -> Dict:
        """Get positioning statistics"""
        if not self.position_history:
            return {}

        accuracies = [p.uncertainty for p in self.position_history]
        confidences = [p.confidence.value for p in self.position_history]

        return {
            "total_positions": len(self.position_history),
            "avg_accuracy": np.mean(accuracies),
            "best_accuracy": np.min(accuracies),
            "worst_accuracy": np.max(accuracies),
            "confidence_distribution": {
                conf: confidences.count(conf) for conf in set(confidences)
            },
            "coverage_area": self._calculate_coverage_area(),
            "positioning_methods": {
                method.value: sum(
                    1 for p in self.position_history if p.method == method
                )
                for method in PositioningMethod
            },
        }

    def _calculate_coverage_area(self) -> float:
        """Calculate coverage area from position history"""
        if len(self.position_history) < 3:
            return 0

        positions = [(p.x, p.y) for p in self.position_history]
        min_x = min(p[0] for p in positions)
        max_x = max(p[0] for p in positions)
        min_y = min(p[1] for p in positions)
        max_y = max(p[1] for p in positions)

        return (max_x - min_x) * (max_y - min_y)


# Example usage and testing
def test_geospatial_intelligence():
    """Test geospatial intelligence functionality"""
    print("Testing Geospatial Intelligence Platform...")

    # Create geospatial intelligence instance
    geo_intel = GeospatialIntelligence()

    # Add some sample access points
    ap1 = AccessPointLocation(
        bssid="00:11:22:33:44:55",
        ssid="TestAP1",
        position=Position(
            0,
            0,
            3,
            0.5,
            LocationConfidence.HIGH,
            datetime.now(),
            PositioningMethod.RSSI_TRILATERATION,
        ),
        tx_power=20,
        antenna_gain=2,
        frequency=2.4e9,
    )

    ap2 = AccessPointLocation(
        bssid="00:11:22:33:44:66",
        ssid="TestAP2",
        position=Position(
            10,
            0,
            3,
            0.5,
            LocationConfidence.HIGH,
            datetime.now(),
            PositioningMethod.RSSI_TRILATERATION,
        ),
        tx_power=20,
        antenna_gain=2,
        frequency=2.4e9,
    )

    ap3 = AccessPointLocation(
        bssid="00:11:22:33:44:77",
        ssid="TestAP3",
        position=Position(
            5,
            10,
            3,
            0.5,
            LocationConfidence.HIGH,
            datetime.now(),
            PositioningMethod.RSSI_TRILATERATION,
        ),
        tx_power=20,
        antenna_gain=2,
        frequency=2.4e9,
    )

    geo_intel.add_access_point(ap1)
    geo_intel.add_access_point(ap2)
    geo_intel.add_access_point(ap3)

    # Simulate RSSI measurements
    measurements = [
        RSSIMeasurement("00:11:22:33:44:55", -45, datetime.now(), 6, 2.437e9),
        RSSIMeasurement("00:11:22:33:44:66", -55, datetime.now(), 11, 2.462e9),
        RSSIMeasurement("00:11:22:33:44:77", -50, datetime.now(), 1, 2.412e9),
    ]

    # Test positioning
    position = geo_intel.estimate_position(measurements)
    if position:
        print(
            f"Estimated position: ({position.x:.2f}, "
            f"{position.y:.2f}, {position.z:.2f})"
        )
        print(f"Uncertainty: {position.uncertainty:.2f}m")
        print(f"Confidence: {position.confidence.value}")
        print(f"Method: {position.method.value}")

    # Test fingerprinting training
    training_position = Position(
        5,
        5,
        0,
        1.0,
        LocationConfidence.HIGH,
        datetime.now(),
        PositioningMethod.FINGERPRINTING,
    )
    geo_intel.train_fingerprinting("location_1", training_position, measurements)

    # Test fingerprinting positioning
    fingerprint_position = geo_intel.estimate_position(measurements)
    if fingerprint_position:
        print(
            f"Fingerprint position: ({fingerprint_position.x:.2f}, "
            f"{fingerprint_position.y:.2f})"
        )

    # Generate some movement data
    for i in range(5):
        test_measurements = [
            RSSIMeasurement("00:11:22:33:44:55", -45 - i, datetime.now(), 6, 2.437e9),
            RSSIMeasurement("00:11:22:33:44:66", -55 - i, datetime.now(), 11, 2.462e9),
            RSSIMeasurement("00:11:22:33:44:77", -50 - i, datetime.now(), 1, 2.412e9),
        ]
        geo_intel.estimate_position(test_measurements)

    # Test movement analysis
    patterns = geo_intel.analyze_movement_patterns()
    print(f"\nDetected {len(patterns)} movement patterns")
    for pattern in patterns:
        print(f"  Classification: {pattern.classification}")
        print(f"  Average velocity: {pattern.velocity:.2f} m/s")
        print(f"  Duration: {pattern.duration:.1f} seconds")

    # Test floor plan generation
    floor_plan = geo_intel.generate_floor_plan()
    print("\nFloor plan generated:")
    print(f"  Nodes: {len(floor_plan.get('nodes', {}))}")
    print(f"  Edges: {len(floor_plan.get('edges', []))}")
    print(f"  Rooms: {len(floor_plan.get('rooms', []))}")

    # Get positioning statistics
    stats = geo_intel.get_positioning_stats()
    print("\nPositioning statistics:")
    print(f"  Total positions: {stats.get('total_positions', 0)}")
    print(f"  Average accuracy: {stats.get('avg_accuracy', 0):.2f}m")
    print(f"  Coverage area: {stats.get('coverage_area', 0):.2f}m²")

    print("Geospatial Intelligence Platform test completed!")


if __name__ == "__main__":
    test_geospatial_intelligence()
