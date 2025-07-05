"""
PiWardrive Offline Navigation System

A comprehensive WiFi-based navigation system for GPS-denied environments:
- WiFi-based positioning and navigation
- Breadcrumb trail and waypoint management
- Route optimization and pathfinding
- Compass integration and heading correction
- Indoor mapping and floor plan navigation
- Dead reckoning and sensor fusion

Author: PiWardrive Development Team
License: MIT
"""

import heapq
import json
import logging
import math
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NavigationMode(Enum):
    """Navigation modes"""

    WIFI_POSITIONING = "wifi_positioning"
    DEAD_RECKONING = "dead_reckoning"
    HYBRID = "hybrid"
    COMPASS_ONLY = "compass_only"


class PathfindingAlgorithm(Enum):
    """Pathfinding algorithms"""

    DIJKSTRA = "dijkstra"
    A_STAR = "a_star"
    BREADTH_FIRST = "breadth_first"
    DEPTH_FIRST = "depth_first"

@dataclass
class Position:
    """Position representation"""

    x: float
    y: float
    z: float = 0.0
    floor: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    accuracy: float = 1.0  # meters
    source: str = "unknown"

    def distance_to(self, other: "Position") -> float:
        """Calculate distance to another position"""
        return math.sqrt(
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "floor": self.floor,
            "timestamp": self.timestamp.isoformat(),
            "accuracy": self.accuracy,
            "source": self.source,
        }

@dataclass
class Waypoint:
    """Navigation waypoint"""

    id: str
    position: Position
    name: str
    description: str = ""
    waypoint_type: str = "user"
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "position": self.position.to_dict(),
            "name": self.name,
            "description": self.description,
            "waypoint_type": self.waypoint_type,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }

@dataclass
class Route:
    """Navigation route"""

    id: str
    waypoints: List[Waypoint]
    total_distance: float = 0.0
    estimated_time: float = 0.0  # seconds
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def calculate_total_distance(self) -> float:
        """Calculate total route distance"""
        if len(self.waypoints) < 2:
            return 0.0

        total = 0.0
        for i in range(len(self.waypoints) - 1):
            total += self.waypoints[i].position.distance_to(
                self.waypoints[i + 1].position
            )

        self.total_distance = total
        return total

    def estimate_time(self, walking_speed: float = 1.2) -> float:
        """Estimate travel time (walking speed in m/s)"""
        if self.total_distance == 0:
            self.calculate_total_distance()

        self.estimated_time = self.total_distance / walking_speed
        return self.estimated_time

@dataclass
class Breadcrumb:
    """Navigation breadcrumb"""

    position: Position
    heading: float = 0.0  # degrees
    speed: float = 0.0  # m/s
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class WiFiPositioning:
    """WiFi-based positioning system"""

    def __init__(self):
        self.access_points: Dict[str, Dict[str, Any]] = {}
        self.fingerprint_database: Dict[str, List[Dict[str, Any]]] = {}
        self.trilateration_threshold = 3  # minimum APs for trilateration

    def add_access_point(self, mac: str, position: Position, tx_power: float = 20.0):
        """Add known access point"""
        self.access_points[mac] = {
            "position": position,
            "tx_power": tx_power,
            "last_seen": datetime.now(),
        }

    def add_fingerprint(self, position: Position, scan_results: List[Dict[str, Any]]):
        """Add WiFi fingerprint for position"""
        key = f"{position.x:.1f},{position.y:.1f},{position.floor}"

        if key not in self.fingerprint_database:
            self.fingerprint_database[key] = []

        self.fingerprint_database[key].append(
            {
                "position": position,
                "scan_results": scan_results,
                "timestamp": datetime.now(),
            }
        )

    def estimate_position_trilateration(
        self, scan_results: List[Dict[str, Any]]
    ) -> Optional[Position]:
        """Estimate position using trilateration"""
        # Filter known APs
        known_aps = []
        for result in scan_results:
            mac = result.get("mac", "")
            if mac in self.access_points:
                rssi = result.get("rssi", -100)
                distance = self._rssi_to_distance(
                    rssi, self.access_points[mac]["tx_power"]
                )

                known_aps.append(
                    {
                        "position": self.access_points[mac]["position"],
                        "distance": distance,
                        "rssi": rssi,
                    }
                )

        if len(known_aps) < self.trilateration_threshold:
            return None

        # Perform trilateration
        return self._trilaterate(known_aps[:3])

    def estimate_position_fingerprinting(
        self, scan_results: List[Dict[str, Any]]
    ) -> Optional[Position]:
        """Estimate position using fingerprinting"""
        if not self.fingerprint_database:
            return None

        # Create current fingerprint
        current_fp = {result["mac"]: result["rssi"] for result in scan_results}

        best_match = None
        best_score = float("in")

        # Compare with stored fingerprints
        for location, fingerprints in self.fingerprint_database.items():
            for fp_entry in fingerprints:
                score = self._compare_fingerprints(current_fp, fp_entry)
                if score < best_score:
                    best_score = score
                    best_match = fp_entry["position"]

        if best_match:
            # Adjust accuracy based on match quality
            accuracy = min(10.0, best_score / 10.0)
            best_match.accuracy = accuracy
            best_match.source = "fingerprinting"

        return best_match

    def _rssi_to_distance(self, rssi: float, tx_power: float) -> float:
        """Convert RSSI to distance estimate"""
        if rssi == 0:
            return -1.0

        ratio = tx_power / rssi
        if ratio < 1.0:
            return ratio**10
        else:
            accuracy = (0.89976) * (ratio**0.7) + 0.111
            return accuracy

    def _trilaterate(self, aps: List[Dict[str, Any]]) -> Optional[Position]:
        """Perform trilateration calculation"""
        if len(aps) < 3:
            return None

        # Extract positions and distances
        positions = [ap["position"] for ap in aps]
        distances = [ap["distance"] for ap in aps]

        # Solve trilateration equations
        # This is a simplified implementation
        x1, y1 = positions[0].x, positions[0].y
        x2, y2 = positions[1].x, positions[1].y
        x3, y3 = positions[2].x, positions[2].y

        r1, r2, r3 = distances[0], distances[1], distances[2]

        # Calculate position
        A = 2 * (x2 - x1)
        B = 2 * (y2 - y1)
        C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
        D = 2 * (x3 - x2)
        E = 2 * (y3 - y2)
        F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2

        denominator = A * E - B * D
        if abs(denominator) < 1e-10:
            return None

        x = (C * E - F * B) / denominator
        y = (A * F - D * C) / denominator

        # Calculate average floor
        avg_floor = sum(pos.floor for pos in positions) // len(positions)

        return Position(
            x=x,
            y=y,
            z=0.0,
            floor=avg_floor,
            accuracy=max(distances) * 0.1,
            source="trilateration",
        )

    def _compare_fingerprints(
        self, fp1: Dict[str, float], fp2_entry: Dict[str, Any]
    ) -> float:
        """Compare two fingerprints using Euclidean distance"""
        fp2 = {result["mac"]: result["rssi"] for result in fp2_entry["scan_results"]}

        # Get common MACs
        common_macs = set(fp1.keys()) & set(fp2.keys())
        if not common_macs:
            return float("in")

        # Calculate Euclidean distance
        distance = 0.0
        for mac in common_macs:
            distance += (fp1[mac] - fp2[mac]) ** 2

        return math.sqrt(distance)


class CompassSystem:
    """Compass and heading system"""

    def __init__(self):
        self.magnetic_declination = 0.0  # degrees
        self.calibration_offset = 0.0
        self.heading_history = deque(maxlen=10)

    def set_magnetic_declination(self, declination: float):
        """Set magnetic declination for location"""
        self.magnetic_declination = declination

    def calibrate(self, reference_heading: float, measured_heading: float):
        """Calibrate compass"""
        self.calibration_offset = reference_heading - measured_heading

    def get_true_heading(self, magnetic_heading: float) -> float:
        """Get true heading from magnetic heading"""
        true_heading = (
            magnetic_heading + self.magnetic_declination + self.calibration_offset
        ) % 360

        self.heading_history.append(true_heading)
        return true_heading

    def get_smoothed_heading(self) -> float:
        """Get smoothed heading using history"""
        if not self.heading_history:
            return 0.0

        # Handle circular averaging
        sin_sum = sum(math.sin(math.radians(h)) for h in self.heading_history)
        cos_sum = sum(math.cos(math.radians(h)) for h in self.heading_history)

        avg_heading = math.degrees(math.atan2(sin_sum, cos_sum))
        return avg_heading % 360

    def get_heading_to_target(
        self, current_pos: Position, target_pos: Position
    ) -> float:
        """Calculate heading to target position"""
        dx = target_pos.x - current_pos.x
        dy = target_pos.y - current_pos.y

        heading = math.degrees(math.atan2(dx, dy))
        return heading % 360


class DeadReckoning:
    """Dead reckoning navigation"""

    def __init__(self):
        self.last_position: Optional[Position] = None
        self.last_heading = 0.0
        self.step_length = 0.7  # meters
        self.position_history = deque(maxlen=100)

    def update_position(
        self, heading: float, steps: int = 1, time_delta: float = 1.0
    ) -> Optional[Position]:
        """Update position based on heading and movement"""
        if self.last_position is None:
            return None

        # Calculate displacement
        distance = steps * self.step_length
        dx = distance * math.sin(math.radians(heading))
        dy = distance * math.cos(math.radians(heading))

        # Update position
        new_position = Position(
            x=self.last_position.x + dx,
            y=self.last_position.y + dy,
            z=self.last_position.z,
            floor=self.last_position.floor,
            accuracy=self.last_position.accuracy + 0.5,  # Accumulate error
            source="dead_reckoning",
        )

        self.last_position = new_position
        self.last_heading = heading
        self.position_history.append(new_position)

        return new_position

    def reset_position(self, position: Position):
        """Reset position reference"""
        self.last_position = position
        self.position_history.clear()
        self.position_history.append(position)

    def get_position_confidence(self) -> float:
        """Get position confidence based on time since last fix"""
        if not self.position_history:
            return 0.0

        time_since_fix = (
            datetime.now() - self.position_history[-1].timestamp
        ).total_seconds()

        # Confidence decreases over time
        confidence = max(0.0, 1.0 - (time_since_fix / 300.0))  # 5 minutes
        return confidence


class Pathfinder:
    """Pathfinding and route optimization"""

    def __init__(self):
        self.graph: Dict[str, List[Dict[str, Any]]] = {}
        self.nodes: Dict[str, Position] = {}

    def add_node(self, node_id: str, position: Position):
        """Add navigation node"""
        self.nodes[node_id] = position
        if node_id not in self.graph:
            self.graph[node_id] = []

    def add_edge(self, from_node: str, to_node: str, weight: Optional[float] = None):
        """Add navigation edge"""
        if from_node not in self.graph:
            self.graph[from_node] = []

        if weight is None and from_node in self.nodes and to_node in self.nodes:
            weight = self.nodes[from_node].distance_to(self.nodes[to_node])

        self.graph[from_node].append({"node": to_node, "weight": weight or 1.0})

    def find_path(
        self,
        start: str,
        end: str,
        algorithm: PathfindingAlgorithm = PathfindingAlgorithm.A_STAR,
    ) -> Optional[List[str]]:
        """Find path between nodes"""
        if algorithm == PathfindingAlgorithm.A_STAR:
            return self._a_star(start, end)
        elif algorithm == PathfindingAlgorithm.DIJKSTRA:
            return self._dijkstra(start, end)
        elif algorithm == PathfindingAlgorithm.BREADTH_FIRST:
            return self._breadth_first(start, end)
        else:
            return None

    def _a_star(self, start: str, end: str) -> Optional[List[str]]:
        """A* pathfinding algorithm"""
        if start not in self.nodes or end not in self.nodes:
            return None

        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self._heuristic(start, end)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == end:
                return self._reconstruct_path(came_from, current)

            if current not in self.graph:
                continue

            for neighbor_info in self.graph[current]:
                neighbor = neighbor_info["node"]
                tentative_g_score = g_score[current] + neighbor_info["weight"]

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self._heuristic(
                        neighbor, end
                    )

                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None

    def _dijkstra(self, start: str, end: str) -> Optional[List[str]]:
        """Dijkstra's algorithm"""
        if start not in self.nodes:
            return None

        distances = {node: float("inf") for node in self.nodes}
        distances[start] = 0
        previous = {}
        unvisited = set(self.nodes.keys())

        while unvisited:
            current = min(unvisited, key=lambda x: distances[x])

            if current == end:
                return self._reconstruct_path(previous, current)

            unvisited.remove(current)

            if current not in self.graph:
                continue

            for neighbor_info in self.graph[current]:
                neighbor = neighbor_info["node"]
                if neighbor in unvisited:
                    alt = distances[current] + neighbor_info["weight"]
                    if alt < distances[neighbor]:
                        distances[neighbor] = alt
                        previous[neighbor] = current

        return None

    def _breadth_first(self, start: str, end: str) -> Optional[List[str]]:
        """Breadth-first search"""
        if start not in self.nodes:
            return None

        queue = deque([start])
        visited = {start}
        parent = {start: None}

        while queue:
            current = queue.popleft()

            if current == end:
                return self._reconstruct_path(parent, current)

            if current not in self.graph:
                continue

            for neighbor_info in self.graph[current]:
                neighbor = neighbor_info["node"]
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        return None

    def _heuristic(self, node1: str, node2: str) -> float:
        """Heuristic function for A*"""
        if node1 not in self.nodes or node2 not in self.nodes:
            return 0.0

        return self.nodes[node1].distance_to(self.nodes[node2])

    def _reconstruct_path(self, came_from: Dict[str, str], current: str) -> List[str]:
        """Reconstruct path from parent dictionary"""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]



class OfflineNavigationSystem:
    """Main offline navigation system"""

    def __init__(self):
        self.wifi_positioning = WiFiPositioning()
        self.compass = CompassSystem()
        self.dead_reckoning = DeadReckoning()
        self.pathfinder = Pathfinder()

        self.current_position: Optional[Position] = None
        self.navigation_mode = NavigationMode.HYBRID
        self.waypoints: Dict[str, Waypoint] = {}
        self.breadcrumbs: List[Breadcrumb] = []
        self.active_route: Optional[Route] = None

        self.position_callbacks: List[Callable] = []
        self.navigation_callbacks: List[Callable] = []

    def add_position_callback(self, callback: Callable):
        """Add position update callback"""
        self.position_callbacks.append(callback)

    def add_navigation_callback(self, callback: Callable):
        """Add navigation update callback"""
        self.navigation_callbacks.append(callback)

    def set_navigation_mode(self, mode: NavigationMode):
        """Set navigation mode"""
        self.navigation_mode = mode
        logger.info(f"Navigation mode set to {mode.value}")

    def update_position(
        self,
        scan_results: List[Dict[str, Any]] = None,
        heading: float = None,
        steps: int = 0,
    ) -> Optional[Position]:
        """Update current position"""
        new_position = None

        if self.navigation_mode == NavigationMode.WIFI_POSITIONING and scan_results:
            # Try trilateration first
            new_position = self.wifi_positioning.estimate_position_trilateration(
                scan_results
            )

            # Fall back to fingerprinting
            if not new_position:
                new_position = self.wifi_positioning.estimate_position_fingerprinting(
                    scan_results
                )

        elif (
            self.navigation_mode == NavigationMode.DEAD_RECKONING
            and heading is not None
        ):
            new_position = self.dead_reckoning.update_position(heading, steps)

        elif self.navigation_mode == NavigationMode.HYBRID:
            # Try WiFi positioning first
            if scan_results:
                new_position = self.wifi_positioning.estimate_position_trilateration(
                    scan_results
                )

                if not new_position:
                    new_position = (
                        self.wifi_positioning.estimate_position_fingerprinting(
                            scan_results
                        )
                    )

            # If WiFi fails, use dead reckoning
            if not new_position and heading is not None:
                new_position = self.dead_reckoning.update_position(heading, steps)

        # Update current position
        if new_position:
            self.current_position = new_position

            # Reset dead reckoning if we got a WiFi fix
            if new_position.source in ["trilateration", "fingerprinting"]:
                self.dead_reckoning.reset_position(new_position)

            # Add breadcrumb
            if heading is not None:
                breadcrumb = Breadcrumb(
                    position=new_position,
                    heading=heading,
                    confidence=min(1.0, 2.0 - new_position.accuracy),
                )
                self.breadcrumbs.append(breadcrumb)

            # Notify callbacks
            for callback in self.position_callbacks:
                callback(new_position)

        return new_position

    def add_waypoint(self, waypoint: Waypoint):
        """Add navigation waypoint"""
        self.waypoints[waypoint.id] = waypoint

        # Add to pathfinder
        self.pathfinder.add_node(waypoint.id, waypoint.position)

        # Connect to nearby waypoints
        for other_id, other_waypoint in self.waypoints.items():
            if other_id != waypoint.id:
                distance = waypoint.position.distance_to(other_waypoint.position)
                if distance < 50.0:  # Connect waypoints within 50m
                    self.pathfinder.add_edge(waypoint.id, other_id, distance)
                    self.pathfinder.add_edge(other_id, waypoint.id, distance)

    def create_route(
        self, waypoint_ids: List[str], route_id: str = None
    ) -> Optional[Route]:
        """Create route from waypoints"""
        if not waypoint_ids:
            return None

        # Get waypoints
        waypoints = []
        for wp_id in waypoint_ids:
            if wp_id in self.waypoints:
                waypoints.append(self.waypoints[wp_id])

        if not waypoints:
            return None

        # Create route
        route = Route(id=route_id or f"route_{int(time.time())}", waypoints=waypoints)

        route.calculate_total_distance()
        route.estimate_time()

        return route

    def navigate_to_waypoint(self, waypoint_id: str) -> Optional[Route]:
        """Navigate to specific waypoint"""
        if waypoint_id not in self.waypoints or not self.current_position:
            return None

        # Create temporary node for current position
        current_node = "current_position"
        self.pathfinder.add_node(current_node, self.current_position)

        # Connect to nearby waypoints
        for wp_id, waypoint in self.waypoints.items():
            distance = self.current_position.distance_to(waypoint.position)
            if distance < 100.0:  # Connect within 100m
                self.pathfinder.add_edge(current_node, wp_id, distance)

        # Find path
        path = self.pathfinder.find_path(current_node, waypoint_id)

        if path and len(path) > 1:
            # Create route from path
            route_waypoints = []
            for i, node_id in enumerate(path):
                if i == 0:  # Current position
                    continue
                if node_id in self.waypoints:
                    route_waypoints.append(self.waypoints[node_id])

            if route_waypoints:
                route = Route(id=f"nav_to_{waypoint_id}", waypoints=route_waypoints)
                route.calculate_total_distance()
                route.estimate_time()

                self.active_route = route

                # Notify callbacks
                for callback in self.navigation_callbacks:
                    callback(route)

                return route

        return None

    def get_navigation_instructions(self) -> List[str]:
        """Get turn-by-turn navigation instructions"""
        if not self.active_route or not self.current_position:
            return []

        instructions = []

        # Find next waypoint
        next_waypoint = None
        for waypoint in self.active_route.waypoints:
            if self.current_position.distance_to(waypoint.position) > 5.0:
                next_waypoint = waypoint
                break

        if next_waypoint:
            distance = self.current_position.distance_to(next_waypoint.position)
            heading = self.compass.get_heading_to_target(
                self.current_position, next_waypoint.position
            )

            instructions.append(f"Head {self._heading_to_direction(heading)}")
            instructions.append(f"Distance: {distance:.1f}m")
            instructions.append(f"Destination: {next_waypoint.name}")

        return instructions

    def _heading_to_direction(self, heading: float) -> str:
        """Convert heading to direction string"""
        directions = [
            "North",
            "Northeast",
            "East",
            "Southeast",
            "South",
            "Southwest",
            "West",
            "Northwest",
        ]

        index = round(heading / 45) % 8
        return directions[index]

    def save_navigation_data(self, filepath: str):
        """Save navigation data to file"""
        __data = {
            "waypoints": [wp.to_dict() for wp in self.waypoints.values()],
            "breadcrumbs": [
                {
                    "position": bc.position.to_dict(),
                    "heading": bc.heading,
                    "speed": bc.speed,
                    "confidence": bc.confidence,
                    "metadata": bc.metadata,
                }
                for bc in self.breadcrumbs
            ],
            "fingerprints": self.wifi_positioning.fingerprint_database,
            "access_points": {
                mac: {
                    "position": ap["position"].to_dict(),
                    "tx_power": ap["tx_power"],
                    "last_seen": ap["last_seen"].isoformat(),
                }
                for mac, ap in self.wifi_positioning.access_points.items()
            },
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def load_navigation_data(self, filepath: str):
        """Load navigation data from file"""
        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            # Load waypoints
            for wp_data in data.get("waypoints", []):
                pos_data = wp_data["position"]
                position = Position(
                    x=pos_data["x"],
                    y=pos_data["y"],
                    z=pos_data["z"],
                    floor=pos_data["floor"],
                    timestamp=datetime.fromisoformat(pos_data["timestamp"]),
                    accuracy=pos_data["accuracy"],
                    source=pos_data["source"],
                )

                waypoint = Waypoint(
                    id=wp_data["id"],
                    position=position,
                    name=wp_data["name"],
                    description=wp_data["description"],
                    waypoint_type=wp_data["waypoint_type"],
                    created_at=datetime.fromisoformat(wp_data["created_at"]),
                    metadata=wp_data["metadata"],
                )

                self.add_waypoint(waypoint)

            # Load fingerprints
            self.wifi_positioning.fingerprint_database = data.get("fingerprints", {})

            # Load access points
            for mac, ap_data in data.get("access_points", {}).items():
                pos_data = ap_data["position"]
                position = Position(
                    x=pos_data["x"],
                    y=pos_data["y"],
                    z=pos_data["z"],
                    floor=pos_data["floor"],
                    timestamp=datetime.fromisoformat(pos_data["timestamp"]),
                    accuracy=pos_data["accuracy"],
                    source=pos_data["source"],
                )

                self.wifi_positioning.add_access_point(
                    mac, position, ap_data["tx_power"]
                )

            logger.info(f"Navigation data loaded from {filepath}")

        except Exception as e:
            logger.error(f"Failed to load navigation data: {e}")


def demo_offline_navigation():
    """Demonstrate offline navigation system"""
    print("PiWardrive Offline Navigation System Demo")
    print("=" * 50)

    # Create navigation system
    nav_system = OfflineNavigationSystem()

    # Setup test environment
    print("\n1. Setting up test environment...")

    # Add some access points
    ap1 = Position(x=0, y=0, z=3, floor=1)
    ap2 = Position(x=50, y=0, z=3, floor=1)
    ap3 = Position(x=25, y=43, z=3, floor=1)

    nav_system.wifi_positioning.add_access_point("AA:BB:CC:DD:EE:01", ap1, 20.0)
    nav_system.wifi_positioning.add_access_point("AA:BB:CC:DD:EE:02", ap2, 20.0)
    nav_system.wifi_positioning.add_access_point("AA:BB:CC:DD:EE:03", ap3, 20.0)

    # Add waypoints
    waypoints = [
        Waypoint("entrance", Position(x=5, y=5, floor=1), "Main Entrance"),
        Waypoint("office", Position(x=30, y=20, floor=1), "Office Area"),
        Waypoint("cafeteria", Position(x=40, y=35, floor=1), "Cafeteria"),
        Waypoint("exit", Position(x=45, y=5, floor=1), "Emergency Exit"),
    ]

    for wp in waypoints:
        nav_system.add_waypoint(wp)

    print(f"   Added {len(waypoints)} waypoints")
    print(f"   Added {len(nav_system.wifi_positioning.access_points)} access points")

    # Test position estimation
    print("\n2. Testing position estimation...")

    test_scan = [
        {"mac": "AA:BB:CC:DD:EE:01", "rssi": -45},
        {"mac": "AA:BB:CC:DD:EE:02", "rssi": -55},
        {"mac": "AA:BB:CC:DD:EE:03", "rssi": -65},
    ]

    position = nav_system.update_position(scan_results=test_scan)
    if position:
        print(
            f"   Estimated position: ({position.x:.1f},
                {position.y:.1f}) floor {position.floor}"
        )
        print(f"   Accuracy: {position.accuracy:.1f}m")
        print(f"   Source: {position.source}")

    # Test navigation
    print("\n3. Testing navigation...")

    route = nav_system.navigate_to_waypoint("cafeteria")
    if route:
        print(f"   Route created: {route.id}")
        print(f"   Total distance: {route.total_distance:.1f}m")
        print(f"   Estimated time: {route.estimated_time:.0f}s")
        print(f"   Waypoints: {[wp.name for wp in route.waypoints]}")

    # Test navigation instructions
    print("\n4. Testing navigation instructions...")

    instructions = nav_system.get_navigation_instructions()
    for instruction in instructions:
        print(f"   {instruction}")

    # Test compass system
    print("\n5. Testing compass system...")

    nav_system.compass.set_magnetic_declination(5.0)  # 5 degrees east
    true_heading = nav_system.compass.get_true_heading(90.0)  # Magnetic east
    print("   Magnetic heading: 90°")
    print(f"   True heading: {true_heading:.1f}°")

    # Test dead reckoning
    print("\n6. Testing dead reckoning...")

    if nav_system.current_position:
        nav_system.dead_reckoning.reset_position(nav_system.current_position)
        dr_position = nav_system.dead_reckoning.update_position(heading=45.0, steps=10)

        if dr_position:
            print(
                f"   Dead reckoning position: ({dr_position.x:.1f},
                    {dr_position.y:.1f})"
            )
            print(
                f"   Confidence: {nav_system.dead_reckoning.get_position_confidence():.2f}"
            )

    # Test breadcrumb trail
    print("\n7. Testing breadcrumb trail...")

    print(f"   Breadcrumbs collected: {len(nav_system.breadcrumbs)}")
    for i, bc in enumerate(nav_system.breadcrumbs[-3:]):  # Show last 3
        print(
            f"   Breadcrumb {i+1}: ({bc.position.x:.1f}, {bc.position.y:.1f}) "
            f"heading {bc.heading:.0f}° confidence {bc.confidence:.2f}"
        )

    # Test save/load
    print("\n8. Testing save/load...")

    nav_data_file = "test_navigation_data.json"
    nav_system.save_navigation_data(nav_data_file)
    print(f"   Navigation data saved to {nav_data_file}")

    # Create new system and load data
    nav_system2 = OfflineNavigationSystem()
    nav_system2.load_navigation_data(nav_data_file)
    print(f"   Loaded {len(nav_system2.waypoints)} waypoints")
    print(f"   Loaded {len(nav_system2.wifi_positioning.access_points)} access points")

    # Cleanup
    Path(nav_data_file).unlink()

    print("\nOffline Navigation System Demo Complete!")
    return {
        "nav_system": nav_system,
        "position_estimated": position is not None,
        "route_created": route is not None,
        "waypoints_loaded": len(nav_system.waypoints),
        "breadcrumbs_collected": len(nav_system.breadcrumbs),
    }

if __name__ == "__main__":
    demo_offline_navigation()
