"""
PiWardrive Advanced Visualization System

Comprehensive visualization capabilities including:
- 4D visualization with time-based data exploration
- Virtual Reality (VR) and Augmented Reality (AR) support
- Interactive timeline scrubbing and playback
- Real-time map overlays and geospatial visualization
- Custom visualization scripting and automation
- Multi-dimensional data representation

Author: PiWardrive Development Team
License: MIT
"""

import base64
import io
import logging
import math
import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

# Visualization libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.collections import LineCollection
from matplotlib.patches import Circle, Polygon, Rectangle
from plotly.subplots import make_subplots

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VisualizationType(Enum):
    """Visualization type classifications"""

    SPATIAL_2D = "spatial_2d"
    SPATIAL_3D = "spatial_3d"
    TEMPORAL = "temporal"
    NETWORK = "network"
    HEATMAP = "heatmap"
    SIGNAL_STRENGTH = "signal_strength"
    CUSTOM = "custom"


class RenderMode(Enum):
    """Rendering mode options"""

    STATIC = "static"
    INTERACTIVE = "interactive"
    ANIMATED = "animated"
    REAL_TIME = "real_time"
    VR = "vr"
    AR = "ar"


class DataDimension(Enum):
    """Data dimension types"""

    X = "x"
    Y = "y"
    Z = "z"
    TIME = "time"
    SIGNAL_STRENGTH = "signal_strength"
    FREQUENCY = "frequency"
    DEVICE_COUNT = "device_count"
    CUSTOM = "custom"


@dataclass
class VisualizationConfig:
    """Visualization configuration"""

    title: str
    viz_type: VisualizationType
    render_mode: RenderMode
    dimensions: List[DataDimension]
    color_scheme: str = "viridis"
    width: int = 800
    height: int = 600
    animation_speed: float = 1.0
    interactive_features: List[str] = field(default_factory=list)
    custom_options: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TimelineEvent:
    """Timeline event for temporal visualization"""

    timestamp: datetime
    event_type: str
    data: Dict[str, Any]
    position: Optional[Tuple[float, float, float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VisualizationLayer:
    """Visualization layer for overlays"""

    id: str
    name: str
    layer_type: str
    data: Any
    style: Dict[str, Any] = field(default_factory=dict)
    visible: bool = True
    z_order: int = 0


class ColorSchemeManager:
    """Color scheme management"""

    def __init__(self):
        self.schemes = {
            "signal_strength": {
                "colors": ["#FF0000", "#FF8000", "#FFFF00", "#80FF00", "#00FF00"],
                "values": [-90, -70, -50, -30, -10],
            },
            "device_type": {
                "ap": "#FF0000",
                "client": "#00FF00",
                "rogue": "#FF00FF",
                "unknown": "#808080",
            },
            "security": {
                "open": "#FF0000",
                "wep": "#FF8000",
                "wpa": "#FFFF00",
                "wpa2": "#80FF00",
                "wpa3": "#00FF00",
            },
            "channel": {i: plt.cm.tab20(i / 20.0) for i in range(1, 15)},
        }

    def get_color(self, scheme: str, value: Any) -> str:
        """Get color for value in scheme"""
        if scheme not in self.schemes:
            return "#000000"

        scheme_data = self.schemes[scheme]

        if isinstance(scheme_data, dict):
            if value in scheme_data:
                return scheme_data[value]
            elif "colors" in scheme_data and "values" in scheme_data:
                # Interpolate color based on value
                colors = scheme_data["colors"]
                values = scheme_data["values"]

                if value <= values[0]:
                    return colors[0]
                elif value >= values[-1]:
                    return colors[-1]
                else:
                    # Linear interpolation
                    for i in range(len(values) - 1):
                        if values[i] <= value <= values[i + 1]:
                            ratio = (value - values[i]) / (values[i + 1] - values[i])
                            return self._interpolate_color(
                                colors[i], colors[i + 1], ratio
                            )

        return "#000000"

    def _interpolate_color(self, color1: str, color2: str, ratio: float) -> str:
        """Interpolate between two colors"""
        # Simple RGB interpolation
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)

        return f"#{r:02X}{g:02X}{b:02X}"


class TimelineController:
    """Timeline control for temporal visualization"""

    def __init__(self):
        self.events: List[TimelineEvent] = []
        self.current_time: Optional[datetime] = None
        self.playback_speed = 1.0
        self.is_playing = False
        self.loop_playback = False
        self.time_range: Optional[Tuple[datetime, datetime]] = None
        self.callbacks: List[Callable] = []

    def add_event(self, event: TimelineEvent):
        """Add timeline event"""
        self.events.append(event)
        self.events.sort(key=lambda e: e.timestamp)

        # Update time range
        if not self.time_range:
            self.time_range = (event.timestamp, event.timestamp)
        else:
            start, end = self.time_range
            self.time_range = (min(start, event.timestamp), max(end, event.timestamp))

    def set_current_time(self, timestamp: datetime):
        """Set current timeline position"""
        self.current_time = timestamp
        self._notify_callbacks()

    def play(self):
        """Start timeline playback"""
        self.is_playing = True
        self._start_playback_thread()

    def pause(self):
        """Pause timeline playback"""
        self.is_playing = False

    def stop(self):
        """Stop timeline playback"""
        self.is_playing = False
        if self.time_range:
            self.current_time = self.time_range[0]
            self._notify_callbacks()

    def seek(self, position: float):
        """Seek to position (0.0 to 1.0)"""
        if self.time_range:
            start, end = self.time_range
            duration = (end - start).total_seconds()
            offset = duration * position
            self.current_time = start + timedelta(seconds=offset)
            self._notify_callbacks()

    def get_events_at_time(
        self, timestamp: datetime, window: timedelta = timedelta(seconds=1)
    ) -> List[TimelineEvent]:
        """Get events within time window"""
        return [
            event
            for event in self.events
            if abs((event.timestamp - timestamp).total_seconds())
            <= window.total_seconds()
        ]

    def add_callback(self, callback: Callable):
        """Add timeline callback"""
        self.callbacks.append(callback)

    def _notify_callbacks(self):
        """Notify timeline callbacks"""
        for callback in self.callbacks:
            try:
                callback(self.current_time)
            except Exception as e:
                logger.error(f"Timeline callback error: {e}")

    def _start_playback_thread(self):
        """Start playback thread"""

        def playback_loop():
            while self.is_playing and self.time_range:
                if not self.current_time:
                    self.current_time = self.time_range[0]

                # Advance time
                self.current_time += timedelta(seconds=self.playback_speed)

                # Check bounds
                if self.current_time > self.time_range[1]:
                    if self.loop_playback:
                        self.current_time = self.time_range[0]
                    else:
                        self.is_playing = False
                        break

                self._notify_callbacks()
                time.sleep(0.1)  # Update rate

        thread = threading.Thread(target=playback_loop)
        thread.daemon = True
        thread.start()


class MapOverlayManager:
    """Map overlay management"""

    def __init__(self):
        self.layers: Dict[str, VisualizationLayer] = {}
        self.base_map: Optional[np.ndarray] = None
        self.map_bounds: Optional[Tuple[float, float, float, float]] = None

    def set_base_map(
        self, map_data: np.ndarray, bounds: Tuple[float, float, float, float]
    ):
        """Set base map image"""
        self.base_map = map_data
        self.map_bounds = bounds  # (min_x, max_x, min_y, max_y)

    def add_layer(self, layer: VisualizationLayer):
        """Add visualization layer"""
        self.layers[layer.id] = layer

    def remove_layer(self, layer_id: str):
        """Remove visualization layer"""
        if layer_id in self.layers:
            del self.layers[layer_id]

    def set_layer_visibility(self, layer_id: str, visible: bool):
        """Set layer visibility"""
        if layer_id in self.layers:
            self.layers[layer_id].visible = visible

    def get_visible_layers(self) -> List[VisualizationLayer]:
        """Get visible layers ordered by z-order"""
        visible = [layer for layer in self.layers.values() if layer.visible]
        return sorted(visible, key=lambda l: l.z_order)

    def world_to_pixel(self, world_coords: Tuple[float, float]) -> Tuple[int, int]:
        """Convert world coordinates to pixel coordinates"""
        if not self.map_bounds or self.base_map is None:
            return (0, 0)

        x, y = world_coords
        min_x, max_x, min_y, max_y = self.map_bounds

        # Normalize coordinates
        norm_x = (x - min_x) / (max_x - min_x)
        norm_y = (y - min_y) / (max_y - min_y)

        # Convert to pixel coordinates
        height, width = self.base_map.shape[:2]
        pixel_x = int(norm_x * width)
        pixel_y = int((1 - norm_y) * height)  # Flip Y axis

        return (pixel_x, pixel_y)

    def pixel_to_world(self, pixel_coords: Tuple[int, int]) -> Tuple[float, float]:
        """Convert pixel coordinates to world coordinates"""
        if not self.map_bounds or self.base_map is None:
            return (0.0, 0.0)

        pixel_x, pixel_y = pixel_coords
        height, width = self.base_map.shape[:2]

        # Normalize pixel coordinates
        norm_x = pixel_x / width
        norm_y = 1 - (pixel_y / height)  # Flip Y axis

        # Convert to world coordinates
        min_x, max_x, min_y, max_y = self.map_bounds
        world_x = min_x + norm_x * (max_x - min_x)
        world_y = min_y + norm_y * (max_y - min_y)

        return (world_x, world_y)


class CustomVisualizationScript:
    """Custom visualization scripting"""

    def __init__(self):
        self.scripts: Dict[str, str] = {}
        self.script_globals = {
            "np": np,
            "plt": plt,
            "pd": pd,
            "go": go,
            "px": px,
            "math": math,
            "datetime": datetime,
            "timedelta": timedelta,
        }

    def register_script(self, name: str, script_code: str):
        """Register custom script"""
        self.scripts[name] = script_code

    def execute_script(
        self, name: str, data: Any, config: Dict[str, Any] = None
    ) -> Any:
        """Execute custom script"""
        if name not in self.scripts:
            raise ValueError(f"Script '{name}' not found")

        script_code = self.scripts[name]

        # Prepare execution environment
        script_locals = {"data": data, "config": config or {}, "result": None}

        # Execute script
        exec(script_code, self.script_globals, script_locals)

        return script_locals.get("result")

    def create_script_template(self, script_type: str) -> str:
        """Create script template"""
        templates = {
            "heatmap": """
# Custom heatmap visualization
import numpy as np
import matplotlib.pyplot as plt

# Process data
x = [point['x'] for point in data]
y = [point['y'] for point in data]
values = [point['value'] for point in data]

# Create heatmap
plt.figure(figsize=(10, 8))
plt.scatter(x, y, c=values, cmap='viridis')
plt.colorbar(label='Signal Strength')
plt.title(config.get('title', 'Custom Heatmap'))
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')

_result = plt.gcf()
            """,
            "network": """
# Custom network visualization
import networkx as nx
import matplotlib.pyplot as plt

# Create graph
G = nx.Graph()

# Add nodes and edges from data
for node in data.get('nodes', []):
    G.add_node(node['id'], **node.get('attributes', {}))

for edge in data.get('edges', []):
    G.add_edge(edge['source'], edge['target'], **edge.get('attributes', {}))

# Create visualization
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue',
        node_size=500, font_size=10, font_weight='bold')
plt.title(config.get('title', 'Custom Network'))

_result = plt.gcf()
            """,
            "timeline": """
# Custom timeline visualization
import matplotlib.pyplot as plt
from datetime import datetime

# Process timeline data
times = [datetime.fromisoformat(event['timestamp']) for event in data]
events = [event['type'] for event in data]

# Create timeline
plt.figure(figsize=(14, 6))
plt.plot(times, range(len(times)), 'o-')
plt.yticks(range(len(times)), events)
plt.xticks(rotation=45)
plt.title(config.get('title', 'Custom Timeline'))
plt.xlabel('Time')
plt.ylabel('Events')
plt.tight_layout()

_result = plt.gcf()
            """,
        }

        return templates.get(script_type, "# Custom script template\nresult = data")


class AdvancedVisualizationEngine:
    """Main advanced visualization engine"""

    def __init__(self):
        self.color_manager = ColorSchemeManager()
        self.timeline_controller = TimelineController()
        self.map_overlay_manager = MapOverlayManager()
        self.custom_scripts = CustomVisualizationScript()

        self.visualizations: Dict[str, Dict[str, Any]] = {}
        self.real_time_data: Dict[str, Any] = {}
        self.animation_frames: Dict[str, List[Any]] = {}

    def create_2d_spatial_visualization(
        self, data: List[Dict[str, Any]], config: VisualizationConfig
    ) -> go.Figure:
        """Create 2D spatial visualization"""
        fig = go.Figure()

        # Extract coordinates
        x_coords = [point.get("x", 0) for point in data]
        y_coords = [point.get("y", 0) for point in data]

        # Color mapping
        colors = []
        if "color_by" in config.custom_options:
            color_by = config.custom_options["color_by"]
            for point in data:
                value = point.get(color_by, 0)
                color = self.color_manager.get_color(color_by, value)
                colors.append(color)
        else:
            colors = ["blue"] * len(data)

        # Create scatter plot
        fig.add_trace(
            go.Scatter(
                x=x_coords,
                y=y_coords,
                mode="markers",
                marker=dict(
                    size=config.custom_options.get("marker_size", 10),
                    color=colors,
                    colorscale=config.color_scheme,
                ),
                text=[point.get("name", f"Point {i}") for i, point in enumerate(data)],
                hovertemplate="<b>%{text}</b><br>X: %{x}<br>Y: %{y}<extra></extra>",
            )
        )

        # Add base map if available
        if self.map_overlay_manager.base_map is not None:
            # Add base map as background image
            fig.add_layout_image(
                dict(
                    source=self._array_to_image(self.map_overlay_manager.base_map),
                    xref="x",
                    yref="y",
                    x=self.map_overlay_manager.map_bounds[0],
                    y=self.map_overlay_manager.map_bounds[3],
                    sizex=self.map_overlay_manager.map_bounds[1]
                    - self.map_overlay_manager.map_bounds[0],
                    sizey=self.map_overlay_manager.map_bounds[3]
                    - self.map_overlay_manager.map_bounds[2],
                    sizing="stretch",
                    opacity=0.7,
                    layer="below",
                )
            )

        # Add overlays
        for layer in self.map_overlay_manager.get_visible_layers():
            self._add_layer_to_figure(fig, layer)

        # Configure layout
        fig.update_layout(
            title=config.title,
            width=config.width,
            height=config.height,
            showlegend=True,
            xaxis_title="X Coordinate",
            yaxis_title="Y Coordinate",
        )

        return fig

    def create_3d_spatial_visualization(
        self, data: List[Dict[str, Any]], config: VisualizationConfig
    ) -> go.Figure:
        """Create 3D spatial visualization"""
        fig = go.Figure()

        # Extract coordinates
        x_coords = [point.get("x", 0) for point in data]
        y_coords = [point.get("y", 0) for point in data]
        z_coords = [point.get("z", 0) for point in data]

        # Color mapping
        colors = []
        if "color_by" in config.custom_options:
            color_by = config.custom_options["color_by"]
            colors = [point.get(color_by, 0) for point in data]
        else:
            colors = ["blue"] * len(data)

        # Create 3D scatter plot
        fig.add_trace(
            go.Scatter3d(
                x=x_coords,
                y=y_coords,
                z=z_coords,
                mode="markers",
                marker=dict(
                    size=config.custom_options.get("marker_size", 8),
                    color=colors,
                    colorscale=config.color_scheme,
                    showscale=True,
                ),
                text=[point.get("name", f"Point {i}") for i, point in enumerate(data)],
                hovertemplate="<b>%{text}</b><br>X: %{x}<br>Y: %{y}<br>Z: %{z}<extra></extra>",
            )
        )

        # Configure layout
        fig.update_layout(
            title=config.title,
            width=config.width,
            height=config.height,
            scene=dict(
                xaxis_title="X Coordinate",
                yaxis_title="Y Coordinate",
                zaxis_title="Z Coordinate",
            ),
        )

        return fig

    def create_temporal_visualization(
        self, events: List[TimelineEvent], config: VisualizationConfig
    ) -> go.Figure:
        """Create temporal visualization"""
        # Add events to timeline controller
        for event in events:
            self.timeline_controller.add_event(event)

        fig = go.Figure()

        # Create timeline plot
        _timestamps = [event.timestamp for event in events]
        _event_types = [event.event_type for event in events]

        # Group by event type
        event_groups = defaultdict(list)
        for event in events:
            event_groups[event.event_type].append(event)

        # Create traces for each event type
        for event_type, group_events in event_groups.items():
            times = [event.timestamp for event in group_events]
            values = [1] * len(group_events)  # Simple binary representation

            fig.add_trace(
                go.Scatter(
                    x=times,
                    y=values,
                    mode="markers",
                    name=event_type,
                    marker=dict(
                        size=config.custom_options.get("marker_size", 10),
                        symbol=config.custom_options.get("marker_symbol", "circle"),
                    ),
                    hovertemplate=f"<b>{event_type}</b><br>Time: %{{x}}<extra></extra>",
                )
            )

        # Configure layout
        fig.update_layout(
            title=config.title,
            width=config.width,
            height=config.height,
            xaxis_title="Time",
            yaxis_title="Events",
            showlegend=True,
        )

        return fig

    def create_signal_strength_heatmap(
        self, data: List[Dict[str, Any]], config: VisualizationConfig
    ) -> go.Figure:
        """Create signal strength heatmap"""
        # Extract data
        x_coords = [point.get("x", 0) for point in data]
        y_coords = [point.get("y", 0) for point in data]
        signal_values = [point.get("signal_strength", -100) for point in data]

        # Create heatmap
        fig = go.Figure(
            data=go.Heatmap(
                x=x_coords,
                y=y_coords,
                z=signal_values,
                colorscale=config.color_scheme,
                colorbar=dict(title="Signal Strength (dBm)"),
            )
        )

        # Configure layout
        fig.update_layout(
            title=config.title,
            width=config.width,
            height=config.height,
            xaxis_title="X Coordinate",
            yaxis_title="Y Coordinate",
        )

        return fig

    def create_network_topology(
        self,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]],
        config: VisualizationConfig,
    ) -> go.Figure:
        """Create network topology visualization"""
        fig = go.Figure()

        # Create edge traces
        edge_x = []
        edge_y = []

        for edge in edges:
            source = edge["source"]
            target = edge["target"]

            # Find node positions
            source_node = next((n for n in nodes if n["id"] == source), None)
            target_node = next((n for n in nodes if n["id"] == target), None)

            if source_node and target_node:
                edge_x.extend([source_node["x"], target_node["x"], None])
                edge_y.extend([source_node["y"], target_node["y"], None])

        # Add edges
        fig.add_trace(
            go.Scatter(
                x=edge_x,
                y=edge_y,
                mode="lines",
                line=dict(width=2, color="gray"),
                hoverinfo="none",
                showlegend=False,
            )
        )

        # Add nodes
        node_x = [node["x"] for node in nodes]
        node_y = [node["y"] for node in nodes]
        node_text = [node.get("name", node["id"]) for node in nodes]

        fig.add_trace(
            go.Scatter(
                x=node_x,
                y=node_y,
                mode="markers+text",
                marker=dict(
                    size=config.custom_options.get("node_size", 20),
                    color=config.custom_options.get("node_color", "lightblue"),
                    line=dict(width=2, color="black"),
                ),
                text=node_text,
                textposition="middle center",
                hovertemplate="<b>%{text}</b><br>X: %{x}<br>Y: %{y}<extra></extra>",
            )
        )

        # Configure layout
        fig.update_layout(
            title=config.title,
            width=config.width,
            height=config.height,
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        )

        return fig

    def create_animated_visualization(
        self, data: List[Dict[str, Any]], config: VisualizationConfig
    ) -> go.Figure:
        """Create animated visualization"""
        fig = go.Figure()

        # Group data by time
        time_groups = defaultdict(list)
        for point in data:
            time_key = point.get("timestamp", datetime.now())
            time_groups[time_key].append(point)

        # Create frames
        frames = []
        for timestamp, points in sorted(time_groups.items()):
            frame_data = go.Scatter(
                x=[p.get("x", 0) for p in points],
                y=[p.get("y", 0) for p in points],
                mode="markers",
                marker=dict(
                    size=config.custom_options.get("marker_size", 10),
                    color=[p.get("signal_strength", -50) for p in points],
                    colorscale=config.color_scheme,
                    showscale=True,
                ),
                text=[p.get("name", f"Point {i}") for i, p in enumerate(points)],
            )

            frames.append(go.Frame(data=[frame_data], name=str(timestamp)))

        # Add initial frame
        if frames:
            fig.add_trace(frames[0].data[0])

        # Add frames to figure
        fig.frames = frames

        # Add animation controls
        fig.update_layout(
            title=config.title,
            width=config.width,
            height=config.height,
            updatemenus=[
                dict(
                    type="buttons",
                    direction="left",
                    buttons=list(
                        [
                            dict(
                                args=[
                                    {
                                        "frame": {"duration": 500, "redraw": True},
                                        "fromcurrent": True,
                                        "transition": {"duration": 300},
                                    }
                                ],
                                label="Play",
                                method="animate",
                            ),
                            dict(
                                args=[
                                    {
                                        "frame": {"duration": 0, "redraw": True},
                                        "mode": "immediate",
                                        "transition": {"duration": 0},
                                    }
                                ],
                                label="Pause",
                                method="animate",
                            ),
                        ]
                    ),
                    pad={"r": 10, "t": 87},
                    showactive=False,
                    x=0.011,
                    xanchor="right",
                    y=0,
                    yanchor="top",
                )
            ],
        )

        return fig

    def create_vr_scene(
        self, data: List[Dict[str, Any]], config: VisualizationConfig
    ) -> Dict[str, Any]:
        """Create VR scene description"""
        # VR scene in A-Frame format
        scene = {"type": "vr_scene", "entities": []}

        # Add data points as 3D objects
        for i, point in enumerate(data):
            entity = {
                "type": "sphere",
                "position": {
                    "x": point.get("x", 0),
                    "y": point.get("z", 0),  # Y is up in VR
                    "z": point.get("y", 0),
                },
                "radius": config.custom_options.get("sphere_radius", 0.5),
                "color": self.color_manager.get_color(
                    config.custom_options.get("color_by", "signal_strength"),
                    point.get("signal_strength", -50),
                ),
                "metadata": {"name": point.get("name", f"Point {i}"), "data": point},
            }
            scene["entities"].append(entity)

        # Add lighting
        scene["entities"].append(
            {
                "type": "light",
                "light_type": "ambient",
                "color": "#fffff",
                "intensity": 0.6,
            }
        )

        scene["entities"].append(
            {
                "type": "light",
                "light_type": "directional",
                "position": {"x": 0, "y": 10, "z": 0},
                "color": "#fffff",
                "intensity": 1.0,
            }
        )

        return scene

    def export_visualization(self, fig: go.Figure, format: str, filepath: str) -> bool:
        """Export visualization to file"""
        try:
            if format.lower() == "html":
                fig.write_html(filepath)
            elif format.lower() == "png":
                fig.write_image(filepath)
            elif format.lower() == "svg":
                fig.write_image(filepath)
            elif format.lower() == "pd":
                fig.write_image(filepath)
            else:
                logger.error(f"Unsupported export format: {format}")
                return False

            logger.info(f"Visualization exported to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Export failed: {e}")
            return False

    def _array_to_image(self, array: np.ndarray) -> str:
        """Convert numpy array to base64 image"""
        if array.dtype != np.uint8:
            array = ((array - array.min()) / (array.max() - array.min()) * 255).astype(
                np.uint8
            )

        # Convert to PIL Image and then to base64
        from PIL import Image

        img = Image.fromarray(array)

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        img_str = base64.b64encode(buffer.read()).decode()
        return f"data:image/png;base64,{img_str}"

    def _add_layer_to_figure(self, fig: go.Figure, layer: VisualizationLayer):
        """Add layer to figure"""
        if layer.layer_type == "points":
            fig.add_trace(
                go.Scatter(
                    x=[p["x"] for p in layer.data],
                    y=[p["y"] for p in layer.data],
                    mode="markers",
                    marker=dict(
                        size=layer.style.get("size", 8),
                        color=layer.style.get("color", "red"),
                        symbol=layer.style.get("symbol", "circle"),
                    ),
                    name=layer.name,
                    showlegend=layer.style.get("show_legend", True),
                )
            )
        elif layer.layer_type == "lines":
            fig.add_trace(
                go.Scatter(
                    x=[p["x"] for p in layer.data],
                    y=[p["y"] for p in layer.data],
                    mode="lines",
                    line=dict(
                        width=layer.style.get("width", 2),
                        color=layer.style.get("color", "blue"),
                    ),
                    name=layer.name,
                    showlegend=layer.style.get("show_legend", True),
                )
            )


def demo_advanced_visualization():
    """Demonstrate advanced visualization capabilities"""
    print("PiWardrive Advanced Visualization System Demo")
    print("=" * 50)

    # Create visualization engine
    viz_engine = AdvancedVisualizationEngine()

    # Generate sample data
    np.random.seed(42)
    n_points = 50

    sample_data = []
    for i in range(n_points):
        sample_data.append(
            {
                "x": np.random.uniform(0, 100),
                "y": np.random.uniform(0, 100),
                "z": np.random.uniform(0, 10),
                "signal_strength": np.random.uniform(-90, -20),
                "timestamp": datetime.now() - timedelta(seconds=i * 10),
                "name": f"Device_{i}",
                "type": np.random.choice(["AP", "Client", "Rogue"]),
            }
        )

    print(f"\n1. Generated {len(sample_data)} sample data points")

    # Test 2D spatial visualization
    print("\n2. Creating 2D spatial visualization...")
    config_2d = VisualizationConfig(
        title="2D WiFi Network Visualization",
        viz_type=VisualizationType.SPATIAL_2D,
        render_mode=RenderMode.INTERACTIVE,
        dimensions=[DataDimension.X, DataDimension.Y],
        custom_options={"color_by": "signal_strength", "marker_size": 12},
    )

    fig_2d = viz_engine.create_2d_spatial_visualization(sample_data, config_2d)
    print(f"   Created 2D visualization with {len(fig_2d.data)} traces")

    # Test 3D spatial visualization
    print("\n3. Creating 3D spatial visualization...")
    config_3d = VisualizationConfig(
        title="3D WiFi Network Visualization",
        viz_type=VisualizationType.SPATIAL_3D,
        render_mode=RenderMode.INTERACTIVE,
        dimensions=[DataDimension.X, DataDimension.Y, DataDimension.Z],
        custom_options={"color_by": "signal_strength", "marker_size": 8},
    )

    fig_3d = viz_engine.create_3d_spatial_visualization(sample_data, config_3d)
    print(f"   Created 3D visualization with {len(fig_3d.data)} traces")

    # Test temporal visualization
    print("\n4. Creating temporal visualization...")

    # Create timeline events
    timeline_events = []
    for i, point in enumerate(sample_data[:20]):
        event = TimelineEvent(
            timestamp=point["timestamp"],
            event_type=point["type"],
            data=point,
            position=(point["x"], point["y"], point["z"]),
        )
        timeline_events.append(event)

    config_temporal = VisualizationConfig(
        title="Network Events Timeline",
        viz_type=VisualizationType.TEMPORAL,
        render_mode=RenderMode.INTERACTIVE,
        dimensions=[DataDimension.TIME],
    )

    _fig_temporal = viz_engine.create_temporal_visualization(
        timeline_events, config_temporal
    )
    print(f"   Created temporal visualization with {len(timeline_events)} events")

    # Test signal strength heatmap
    print("\n5. Creating signal strength heatmap...")
    config_heatmap = VisualizationConfig(
        title="Signal Strength Heatmap",
        viz_type=VisualizationType.HEATMAP,
        render_mode=RenderMode.STATIC,
        dimensions=[DataDimension.X, DataDimension.Y, DataDimension.SIGNAL_STRENGTH],
    )

    _fig_heatmap = viz_engine.create_signal_strength_heatmap(
        sample_data, config_heatmap
    )
    print("   Created heatmap visualization")

    # Test network topology
    print("\n6. Creating network topology...")

    # Create network data
    nodes = [
        {"id": "AP1", "x": 25, "y": 25, "name": "Access Point 1"},
        {"id": "AP2", "x": 75, "y": 25, "name": "Access Point 2"},
        {"id": "AP3", "x": 50, "y": 75, "name": "Access Point 3"},
        {"id": "Client1", "x": 30, "y": 30, "name": "Client Device 1"},
        {"id": "Client2", "x": 70, "y": 30, "name": "Client Device 2"},
    ]

    edges = [
        {"source": "AP1", "target": "Client1"},
        {"source": "AP2", "target": "Client2"},
        {"source": "AP1", "target": "AP3"},
        {"source": "AP2", "target": "AP3"},
    ]

    config_network = VisualizationConfig(
        title="Network Topology",
        viz_type=VisualizationType.NETWORK,
        render_mode=RenderMode.INTERACTIVE,
        dimensions=[DataDimension.X, DataDimension.Y],
        custom_options={"node_size": 30, "node_color": "lightblue"},
    )

    _fig_network = viz_engine.create_network_topology(nodes, edges, config_network)
    print(f"   Created network topology with {len(nodes)} nodes and {len(edges)} edges")

    # Test custom scripting
    print("\n7. Testing custom scripting...")

    # Register custom script
    custom_script = """
# Custom scatter plot with regression line
import numpy as np
import plotly.graph_objects as go

# Extract data
xdata = np.array([point['x'] for point in data])
y_data = np.array([point['y'] for point in data])

# Create figure
fig = go.Figure()

# Add scatter points
fig.add_trace(go.Scatter(
    x=x_data,
    y=y_data,
    mode='markers',
    name='Data Points',
    marker=dict(size=8, color='blue')
))

# Add simple trend line
z = np.polyfit(x_data, y_data, 1)
p = np.poly1d(z)
fig.add_trace(go.Scatter(
    x=x_data,
    y=p(x_data),
    mode='lines',
    name='Trend Line',
    line=dict(color='red', width=2)
))

fig.update_layout(
    title='Custom Analysis: X vs Y with Trend Line',
    xaxis_title='X Coordinate',
    yaxis_title='Y Coordinate'
)

_result = fig
"""

    viz_engine.custom_scripts.register_script("trend_plot", custom_script)

    try:
        _custom_fig = viz_engine.custom_scripts.execute_script(
            "trend_plot", sample_data, {"title": "Custom Trend Analysis"}
        )
        print("   Custom script executed successfully")
    except Exception as e:
        print(f"   Custom script failed: {e}")

    # Test timeline controller
    print("\n8. Testing timeline controller...")

    def timeline_callback(current_time):
        print(f"   Timeline position: {current_time}")

    viz_engine.timeline_controller.add_callback(timeline_callback)

    # Test seeking
    viz_engine.timeline_controller.seek(0.5)  # Seek to middle
    print(f"   Timeline has {len(viz_engine.timeline_controller.events)} events")

    # Test VR scene creation
    print("\n9. Creating VR scene...")

    config_vr = VisualizationConfig(
        title="VR Network Visualization",
        viz_type=VisualizationType.SPATIAL_3D,
        render_mode=RenderMode.VR,
        dimensions=[DataDimension.X, DataDimension.Y, DataDimension.Z],
        custom_options={"color_by": "signal_strength", "sphere_radius": 0.5},
    )

    vr_scene = viz_engine.create_vr_scene(sample_data[:10], config_vr)
    print(f"   Created VR scene with {len(vr_scene['entities'])} entities")

    # Test export functionality
    print("\n10. Testing export functionality...")

    export_path = "test_visualization.html"
    success = viz_engine.export_visualization(fig_2d, "html", export_path)

    if success and Path(export_path).exists():
        print(f"   Successfully exported visualization to {export_path}")
        # Cleanup
        Path(export_path).unlink()
    else:
        print("   Export failed or file not created")

    print("\nAdvanced Visualization System Demo Complete!")
    return {
        "viz_engine": viz_engine,
        "visualizations_created": 6,
        "timeline_events": len(timeline_events),
        "custom_scripts": len(viz_engine.custom_scripts.scripts),
        "vr_entities": len(vr_scene["entities"]),
    }


if __name__ == "__main__":
    demo_advanced_visualization()
