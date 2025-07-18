"""
User Experience Enhancements for PiWardrive
Provides guided setup wizard,
    interactive tutorials,
    customizable dashboards,
    and theme system
"""

import json
import logging
import os
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# Web framework imports
try:
    from flask import Flask, jsonify, redirect, render_template, request, url_for
    from flask_socketio import SocketIO

    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False

# UI framework imports
try:
    pass

    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False

logger = logging.getLogger(__name__)


@dataclass
class SetupStep:
    """Individual setup step in the wizard"""

    id: str
    title: str
    description: str
    required: bool
    completed: bool = False
    data: Dict[str, Any] = None

    def __post_init__(self):
        if self.data is None:
            self.data = {}

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TutorialStep:
    """Individual tutorial step"""

    id: str
    title: str
    content: str
    action: str
    target: str
    completed: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DashboardWidget:
    """Dashboard widget configuration"""

    id: str
    type: str
    title: str
    position: Dict[str, int]
    size: Dict[str, int]
    config: Dict[str, Any]
    visible: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Theme:
    """Theme configuration"""

    id: str
    name: str
    description: str
    colors: Dict[str, str]
    fonts: Dict[str, str]
    styles: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class GuidedSetupWizard:
    """Guided setup wizard for first-time users"""

    def __init__(self, config_path: str = "config/setup_wizard.json"):
        self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        self.setup_steps = []
        self.current_step = 0
        self.wizard_data = {}
        self.callbacks = {}

        self._initialize_setup_steps()
        self._load_progress()

    def _initialize_setup_steps(self):
        """Initialize the setup steps"""
        self.setup_steps = [
            SetupStep(
                id="welcome",
                title="Welcome to PiWardrive",
                description="Welcome to the PiWardrive setup wizard. This will guide you through the initial configuration.",
                required=True,
            ),
            SetupStep(
                id="hardware_detection",
                title="Hardware Detection",
                description="Detecting available wireless adapters and GPS devices.",
                required=True,
            ),
            SetupStep(
                id="network_config",
                title="Network Configuration",
                description="Configure network settings and wireless adapter preferences.",
                required=True,
            ),
            SetupStep(
                id="gps_setup",
                title="GPS Setup",
                description="Configure GPS settings and location services.",
                required=True,
            ),
            SetupStep(
                id="database_setup",
                title="Database Setup",
                description="Configure database settings and initialize storage.",
                required=True,
            ),
            SetupStep(
                id="scan_preferences",
                title="Scan Preferences",
                description="Configure default scanning parameters and preferences.",
                required=True,
            ),
            SetupStep(
                id="user_interface",
                title="User Interface",
                description="Choose interface preferences and theme settings.",
                required=False,
            ),
            SetupStep(
                id="advanced_features",
                title="Advanced Features",
                description="Enable advanced features like notifications, integrations, etc.",
                required=False,
            ),
            SetupStep(
                id="completion",
                title="Setup Complete",
                description="Your PiWardrive setup is complete! You can now start using the system.",
                required=True,
            ),
        ]

    def _load_progress(self):
        """Load setup progress from file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, "r") as f:
                    data = json.load(f)

                self.current_step = data.get("current_step", 0)
                self.wizarddata = data.get("wizard_data", {})

                # Update step completion status
                completed_steps = data.get("completed_steps", [])
                for step in self.setup_steps:
                    if step.id in completed_steps:
                        step.completed = True

        except Exception as e:
            logger.error(f"Error loading setup progress: {e}")

    def _save_progress(self):
        """Save setup progress to file"""
        try:
            data = {
                "current_step": self.current_step,
                "wizard_data": self.wizard_data,
                "completed_steps": [
                    step.id for step in self.setup_steps if step.completed
                ],
                "last_updated": datetime.now().isoformat(),
            }

            with open(self.config_path, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            logger.error(f"Error saving setup progress: {e}")

    def get_current_step(self) -> Optional[SetupStep]:
        """Get the current setup step"""
        if 0 <= self.current_step < len(self.setup_steps):
            return self.setup_steps[self.current_step]
        return None

    def get_all_steps(self) -> List[SetupStep]:
        """Get all setup steps"""
        return self.setup_steps

    def next_step(self) -> Optional[SetupStep]:
        """Move to the next step"""
        if self.current_step < len(self.setup_steps) - 1:
            self.current_step += 1
            self._save_progress()
            return self.get_current_step()
        return None

    def previous_step(self) -> Optional[SetupStep]:
        """Move to the previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self._save_progress()
            return self.get_current_step()
        return None

    def complete_step(self, step_id: str, data: Dict[str, Any] = None) -> bool:
        """Mark a step as completed"""
        for step in self.setup_steps:
            if step.id == step_id:
                step.completed = True
                if data:
                    step.data = data
                    self.wizard_data[step_id] = data

                self._save_progress()

                # Execute callback if available
                if step_id in self.callbacks:
                    try:
                        self.callbacks[step_id](data)
                    except Exception as e:
                        logger.error(
                            f"Error executing callback for step {step_id}: {e}"
                        )

                return True

        return False

    def register_callback(
        self, step_id: str, callback: Callable[[Dict[str, Any]], None]
    ):
        """Register a callback for step completion"""
        self.callbacks[step_id] = callback

    def is_setup_complete(self) -> bool:
        """Check if all required steps are completed"""
        required_steps = [step for step in self.setup_steps if step.required]
        return all(step.completed for step in required_steps)

    def get_progress_percentage(self) -> float:
        """Get setup progress as percentage"""
        if not self.setup_steps:
            return 0.0

        completed = sum(1 for step in self.setup_steps if step.completed)
        return (completed / len(self.setup_steps)) * 100

    def perform_hardware_detection(self) -> Dict[str, Any]:
        """Perform hardware detection step"""
        try:
            from ..hardware.enhanced_hardware import MultiAdapterManager

            results = {
                "wireless_adapters": [],
                "gps_devices": [],
                "environmental_sensors": [],
                "camera_devices": [],
            }

            # Detect wireless adapters
            adapter_manager = MultiAdapterManager()
            adapters = adapter_manager.discover_adapters()
            results["wireless_adapters"] = [adapter.to_dict() for adapter in adapters]

            # Detect GPS devices
            gps_ports = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyS0", "/dev/ttyAMA0"]
            for port in gps_ports:
                if Path(port).exists():
                    results["gps_devices"].append({"port": port, "available": True})

            # Detect environmental sensors (would need actual hardware detection)
            results["environmental_sensors"] = [
                {"type": "BME280", "detected": False},
                {"type": "TSL2561", "detected": False},
            ]

            # Detect camera devices
            camera_devices = []
            for i in range(3):  # Check first 3 video devices
                device_path = f"/dev/video{i}"
                if Path(device_path).exists():
                    camera_devices.append({"device": device_path, "available": True})

            results["camera_devices"] = camera_devices

            return results

        except Exception as e:
            logger.error(f"Error in hardware detection: {e}")
            return {"error": str(e)}


class InteractiveTutorialSystem:
    """Interactive tutorial system with guided tours"""

    def __init__(self, tutorials_path: str = "config/tutorials.json"):
        self.tutorials_path = Path(tutorials_path)
        self.tutorials_path.parent.mkdir(parents=True, exist_ok=True)

        self.tutorials = {}
        self.user_progress = {}
        self.active_tutorial = None
        self.current_step = 0

        self._load_tutorials()
        self._load_user_progress()

    def _load_tutorials(self):
        """Load tutorial definitions"""
        try:
            if self.tutorials_path.exists():
                with open(self.tutorials_path, "r") as f:
                    tutorial_data = json.load(f)

                for tutorial_id, tutorial_config in tutorial_data.items():
                    self.tutorials[tutorial_id] = [
                        TutorialStep(**step)
                        for step in tutorial_config.get("steps", [])
                    ]
            else:
                self._create_default_tutorials()

        except Exception as e:
            logger.error(f"Error loading tutorials: {e}")
            self._create_default_tutorials()

    def _create_default_tutorials(self):
        """Create default tutorials"""
        # Basic navigation tutorial
        self.tutorials["basic_navigation"] = [
            TutorialStep(
                id="nav_1",
                title="Welcome to PiWardrive",
                content="Let's take a quick tour of the PiWardrive interface. Click 'Next' to continue.",
                action="highlight",
                target="main_menu",
            ),
            TutorialStep(
                id="nav_2",
                title="Main Menu",
                content="This is the main menu. From here you can access all PiWardrive features.",
                action="highlight",
                target="main_menu",
            ),
            TutorialStep(
                id="nav_3",
                title="Scan Control",
                content="Use this panel to start and stop wireless scans.",
                action="highlight",
                target="scan_control",
            ),
            TutorialStep(
                id="nav_4",
                title="Results View",
                content="Scan results will appear in this area.",
                action="highlight",
                target="results_view",
            ),
            TutorialStep(
                id="nav_5",
                title="Settings",
                content="Configure PiWardrive settings from this menu.",
                action="highlight",
                target="settings_menu",
            ),
        ]

        # Scanning tutorial
        self.tutorials["scanning_basics"] = [
            TutorialStep(
                id="scan_1",
                title="Starting Your First Scan",
                content="Let's perform your first wireless scan. Click the 'Start Scan' button.",
                action="highlight",
                target="start_scan_button",
            ),
            TutorialStep(
                id="scan_2",
                title="Scan in Progress",
                content="The scan is now running. You can see the progress indicator.",
                action="highlight",
                target="scan_progress",
            ),
            TutorialStep(
                id="scan_3",
                title="Viewing Results",
                content="Scan results are displayed here. You can sort and filter them.",
                action="highlight",
                target="results_table",
            ),
            TutorialStep(
                id="scan_4",
                title="Exporting Data",
                content="You can export your scan results using the export options.",
                action="highlight",
                target="export_menu",
            ),
        ]

        # Advanced features tutorial
        self.tutorials["advanced_features"] = [
            TutorialStep(
                id="adv_1",
                title="Advanced Visualization",
                content="PiWardrive includes advanced visualization features like 3D heatmaps.",
                action="highlight",
                target="visualization_tab",
            ),
            TutorialStep(
                id="adv_2",
                title="GPS Integration",
                content="GPS data is automatically integrated with scan results for location mapping.",
                action="highlight",
                target="gps_status",
            ),
            TutorialStep(
                id="adv_3",
                title="Real-time Monitoring",
                content="Enable real-time monitoring for continuous scanning.",
                action="highlight",
                target="realtime_toggle",
            ),
            TutorialStep(
                id="adv_4",
                title="Reporting",
                content="Generate professional reports from your scan data.",
                action="highlight",
                target="report_generator",
            ),
        ]

        self._save_tutorials()

    def _save_tutorials(self):
        """Save tutorials to file"""
        try:
            tutorial_data = {}
            for tutorial_id, steps in self.tutorials.items():
                tutorial_data[tutorial_id] = {
                    "steps": [step.to_dict() for step in steps]
                }

            with open(self.tutorials_path, "w") as f:
                json.dump(tutorial_data, f, indent=2)

        except Exception as e:
            logger.error(f"Error saving tutorials: {e}")

    def _load_user_progress(self):
        """Load user progress for tutorials"""
        try:
            progress_path = self.tutorials_path.parent / "tutorial_progress.json"

            if progress_path.exists():
                with open(progress_path, "r") as f:
                    self.user_progress = json.load(f)

        except Exception as e:
            logger.error(f"Error loading tutorial progress: {e}")

    def _save_user_progress(self):
        """Save user progress for tutorials"""
        try:
            progress_path = self.tutorials_path.parent / "tutorial_progress.json"

            with open(progress_path, "w") as f:
                json.dump(self.user_progress, f, indent=2)

        except Exception as e:
            logger.error(f"Error saving tutorial progress: {e}")

    def get_available_tutorials(self) -> List[Dict[str, Any]]:
        """Get list of available tutorials"""
        tutorials = []

        for tutorial_id, steps in self.tutorials.items():
            progress = self.user_progress.get(tutorial_id, {})
            completed_steps = progress.get("completed_steps", [])

            tutorials.append(
                {
                    "id": tutorial_id,
                    "title": tutorial_id.replace("_", " ").title(),
                    "total_steps": len(steps),
                    "completed_steps": len(completed_steps),
                    "progress": len(completed_steps) / len(steps) * 100 if steps else 0,
                }
            )

        return tutorials

    def start_tutorial(self, tutorial_id: str) -> bool:
        """Start a tutorial"""
        if tutorial_id not in self.tutorials:
            return False

        self.active_tutorial = tutorial_id
        self.current_step = 0

        # Initialize progress if not exists
        if tutorial_id not in self.user_progress:
            self.user_progress[tutorial_id] = {
                "started": datetime.now().isoformat(),
                "completed_steps": [],
            }

        self._save_user_progress()
        return True

    def get_current_tutorial_step(self) -> Optional[TutorialStep]:
        """Get current tutorial step"""
        if not self.active_tutorial:
            return None

        steps = self.tutorials.get(self.active_tutorial, [])

        if 0 <= self.current_step < len(steps):
            return steps[self.current_step]

        return None

    def next_tutorial_step(self) -> Optional[TutorialStep]:
        """Move to next tutorial step"""
        if not self.active_tutorial:
            return None

        steps = self.tutorials.get(self.active_tutorial, [])

        if self.current_step < len(steps) - 1:
            self.current_step += 1
            return steps[self.current_step]

        return None

    def complete_tutorial_step(self, step_id: str) -> bool:
        """Mark a tutorial step as completed"""
        if not self.active_tutorial:
            return False

        progress = self.user_progress.get(self.active_tutorial, {})
        completed_steps = progress.get("completed_steps", [])

        if step_id not in completed_steps:
            completed_steps.append(step_id)
            progress["completed_steps"] = completed_steps
            self.user_progress[self.active_tutorial] = progress
            self._save_user_progress()

        return True

    def finish_tutorial(self) -> bool:
        """Finish the current tutorial"""
        if not self.active_tutorial:
            return False

        progress = self.user_progress.get(self.active_tutorial, {})
        progress["completed"] = datetime.now().isoformat()
        self.user_progress[self.active_tutorial] = progress

        self.active_tutorial = None
        self.current_step = 0

        self._save_user_progress()
        return True


class CustomizableDashboard:
    """Customizable dashboard system"""

    def __init__(self, dashboard_path: str = "config/dashboard.json"):
        self.dashboard_path = Path(dashboard_path)
        self.dashboard_path.parent.mkdir(parents=True, exist_ok=True)

        self.widgets = {}
        self.layouts = {}
        self.current_layout = "default"
        self.widget_types = {}

        self._register_default_widgets()
        self._load_dashboard_config()

    def _register_default_widgets(self):
        """Register default widget types"""
        self.widget_types = {
            "scan_status": {
                "name": "Scan Status",
                "description": "Shows current scan status and progress",
                "default_size": {"width": 300, "height": 200},
                "configurable": ["refresh_rate", "show_details"],
            },
            "signal_strength": {
                "name": "Signal Strength Chart",
                "description": "Real-time signal strength visualization",
                "default_size": {"width": 400, "height": 300},
                "configurable": ["time_range", "chart_type", "channels"],
            },
            "network_list": {
                "name": "Network List",
                "description": "List of detected networks",
                "default_size": {"width": 500, "height": 400},
                "configurable": ["sort_by", "filters", "columns"],
            },
            "gps_status": {
                "name": "GPS Status",
                "description": "GPS location and satellite information",
                "default_size": {"width": 250, "height": 150},
                "configurable": ["coordinate_format", "show_satellites"],
            },
            "system_stats": {
                "name": "System Statistics",
                "description": "System performance and resource usage",
                "default_size": {"width": 300, "height": 250},
                "configurable": ["metrics", "update_rate"],
            },
            "heatmap": {
                "name": "Coverage Heatmap",
                "description": "Signal coverage heatmap visualization",
                "default_size": {"width": 600, "height": 400},
                "configurable": ["color_scheme", "opacity", "interpolation"],
            },
            "channel_usage": {
                "name": "Channel Usage",
                "description": "WiFi channel usage analysis",
                "default_size": {"width": 400, "height": 250},
                "configurable": ["band", "chart_type", "threshold"],
            },
            "environmental": {
                "name": "Environmental Sensors",
                "description": "Temperature, humidity, and other environmental data",
                "default_size": {"width": 350, "height": 200},
                "configurable": ["sensors", "units", "alerts"],
            },
        }

    def _load_dashboard_config(self):
        """Load dashboard configuration from file"""
        try:
            if self.dashboard_path.exists():
                with open(self.dashboard_path, "r") as f:
                    config = json.load(f)

                # Load widgets
                for widget_id, widget_config in config.get("widgets", {}).items():
                    self.widgets[widget_id] = DashboardWidget(**widget_config)

                # Load layouts
                self.layouts = config.get("layouts", {})
                self.current_layout = config.get("current_layout", "default")

            else:
                self._create_default_layout()

        except Exception as e:
            logger.error(f"Error loading dashboard config: {e}")
            self._create_default_layout()

    def _create_default_layout(self):
        """Create default dashboard layout"""
        # Create default widgets
        default_widgets = [
            ("scan_status", {"x": 10, "y": 10}),
            ("signal_strength", {"x": 320, "y": 10}),
            ("network_list", {"x": 10, "y": 220}),
            ("gps_status", {"x": 520, "y": 220}),
            ("system_stats", {"x": 780, "y": 10}),
        ]

        for widget_type, position in default_widgets:
            widget_id = f"{widget_type}_{uuid.uuid4().hex[:8]}"
            widget_config = self.widget_types[widget_type]

            self.widgets[widget_id] = DashboardWidget(
                id=widget_id,
                type=widget_type,
                title=widget_config["name"],
                position=position,
                size=widget_config["default_size"],
                config={},
            )

        # Create default layout
        self.layouts["default"] = {
            "name": "Default Layout",
            "widgets": list(self.widgets.keys()),
        }

        self.current_layout = "default"
        self._save_dashboard_config()

    def _save_dashboard_config(self):
        """Save dashboard configuration to file"""
        try:
            config = {
                "widgets": {
                    widget_id: widget.to_dict()
                    for widget_id, widget in self.widgets.items()
                },
                "layouts": self.layouts,
                "current_layout": self.current_layout,
                "last_updated": datetime.now().isoformat(),
            }

            with open(self.dashboard_path, "w") as f:
                json.dump(config, f, indent=2)

        except Exception as e:
            logger.error(f"Error saving dashboard config: {e}")

    def get_widget_types(self) -> Dict[str, Dict[str, Any]]:
        """Get available widget types"""
        return self.widget_types

    def add_widget(
        self,
        widget_type: str,
        position: Dict[str, int],
        title: str = None,
        config: Dict[str, Any] = None,
    ) -> str:
        """Add a new widget to the dashboard"""
        if widget_type not in self.widget_types:
            raise ValueError(f"Unknown widget type: {widget_type}")

        widget_id = f"{widget_type}_{uuid.uuid4().hex[:8]}"
        widget_config = self.widget_types[widget_type]

        if title is None:
            title = widget_config["name"]

        if config is None:
            config = {}

        widget = DashboardWidget(
            id=widget_id,
            type=widget_type,
            title=title,
            position=position,
            size=widget_config["default_size"],
            config=config,
        )

        self.widgets[widget_id] = widget
        self._save_dashboard_config()

        return widget_id

    def remove_widget(self, widget_id: str) -> bool:
        """Remove a widget from the dashboard"""
        if widget_id in self.widgets:
            del self.widgets[widget_id]
            self._save_dashboard_config()
            return True
        return False

    def update_widget(self, widget_id: str, updates: Dict[str, Any]) -> bool:
        """Update widget configuration"""
        if widget_id not in self.widgets:
            return False

        widget = self.widgets[widget_id]

        for key, value in updates.items():
            if hasattr(widget, key):
                setattr(widget, key, value)

        self._save_dashboard_config()
        return True

    def get_dashboard_layout(self, layout_name: str = None) -> Dict[str, Any]:
        """Get dashboard layout"""
        if layout_name is None:
            layout_name = self.current_layout

        if layout_name not in self.layouts:
            return {}

        layout = self.layouts[layout_name]
        widgets = []

        for widget_id in layout.get("widgets", []):
            if widget_id in self.widgets:
                widgets.append(self.widgets[widget_id].to_dict())

        return {"name": layout.get("name", layout_name), "widgets": widgets}

    def save_layout(self, layout_name: str, widget_ids: List[str]) -> bool:
        """Save a dashboard layout"""
        self.layouts[layout_name] = {
            "name": layout_name,
            "widgets": widget_ids,
            "created": datetime.now().isoformat(),
        }

        self._save_dashboard_config()
        return True

    def set_active_layout(self, layout_name: str) -> bool:
        """Set the active dashboard layout"""
        if layout_name not in self.layouts:
            return False

        self.current_layout = layout_name
        self._save_dashboard_config()
        return True

    def get_widget_data(self, widget_id: str) -> Dict[str, Any]:
        """Get data for a specific widget"""
        if widget_id not in self.widgets:
            return {}

        widget = self.widgets[widget_id]

        # This would be implemented to fetch actual data based on widget type
        # For now, return mock data
        mock_data = {
            "scan_status": {
                "status": "active",
                "networks_found": 42,
                "scan_time": "00:02:15",
                "progress": 75,
            },
            "signal_strength": {
                "current": -45,
                "average": -52,
                "max": -38,
                "min": -78,
                "history": [(-45, datetime.now().isoformat())],
            },
            "gps_status": {
                "latitude": 40.7128,
                "longitude": -74.0060,
                "satellites": 8,
                "accuracy": 3.2,
                "fix_type": "GPS",
            },
            "system_stats": {
                "cpu_usage": 35.2,
                "memory_usage": 67.8,
                "disk_usage": 45.1,
                "temperature": 42.5,
            },
        }

        return mock_data.get(widget.type, {})


class ThemeSystem:
    """Theme system for UI customization"""

    def __init__(self, themes_path: str = "config/themes.json"):
        self.themes_path = Path(themes_path)
        self.themes_path.parent.mkdir(parents=True, exist_ok=True)

        self.themes = {}
        self.current_theme = "default"

        self._load_themes()

    def _load_themes(self):
        """Load themes from file"""
        try:
            if self.themes_path.exists():
                with open(self.themes_path, "r") as f:
                    theme_data = json.load(f)

                for theme_id, theme_config in theme_data.items():
                    self.themes[theme_id] = Theme(**theme_config)

            else:
                self._create_default_themes()

        except Exception as e:
            logger.error(f"Error loading themes: {e}")
            self._create_default_themes()

    def _create_default_themes(self):
        """Create default themes"""
        # Default theme
        self.themes["default"] = Theme(
            id="default",
            name="Default",
            description="Default PiWardrive theme",
            colors={
                "primary": "#2196F3",
                "secondary": "#FFC107",
                "success": "#4CAF50",
                "danger": "#F44336",
                "warning": "#FF9800",
                "info": "#17A2B8",
                "light": "#F8F9FA",
                "dark": "#343A40",
                "background": "#FFFFFF",
                "surface": "#F5F5F5",
                "text": "#212121",
                "text_secondary": "#757575",
            },
            fonts={
                "primary": "Arial, sans-seri",
                "secondary": "Monaco, monospace",
                "size_small": "12px",
                "size_medium": "14px",
                "size_large": "16px",
                "size_xlarge": "18px",
            },
            styles={
                "border_radius": "4px",
                "box_shadow": "0 2px 4px rgba(0,0,0,0.1)",
                "transition": "all 0.3s ease",
            },
        )

        # Dark theme
        self.themes["dark"] = Theme(
            id="dark",
            name="Dark",
            description="Dark theme for low-light environments",
            colors={
                "primary": "#BB86FC",
                "secondary": "#03DAC6",
                "success": "#4CAF50",
                "danger": "#CF6679",
                "warning": "#FF9800",
                "info": "#03DAC6",
                "light": "#1F1F1F",
                "dark": "#121212",
                "background": "#121212",
                "surface": "#1F1F1F",
                "text": "#FFFFFF",
                "text_secondary": "#B0B0B0",
            },
            fonts={
                "primary": "Arial, sans-seri",
                "secondary": "Monaco, monospace",
                "size_small": "12px",
                "size_medium": "14px",
                "size_large": "16px",
                "size_xlarge": "18px",
            },
            styles={
                "border_radius": "4px",
                "box_shadow": "0 2px 8px rgba(0,0,0,0.3)",
                "transition": "all 0.3s ease",
            },
        )

        # High contrast theme
        self.themes["high_contrast"] = Theme(
            id="high_contrast",
            name="High Contrast",
            description="High contrast theme for accessibility",
            colors={
                "primary": "#0000FF",
                "secondary": "#FFFF00",
                "success": "#00FF00",
                "danger": "#FF0000",
                "warning": "#FFA500",
                "info": "#00FFFF",
                "light": "#FFFFFF",
                "dark": "#000000",
                "background": "#FFFFFF",
                "surface": "#FFFFFF",
                "text": "#000000",
                "text_secondary": "#000000",
            },
            fonts={
                "primary": "Arial, sans-seri",
                "secondary": "Monaco, monospace",
                "size_small": "14px",
                "size_medium": "16px",
                "size_large": "18px",
                "size_xlarge": "20px",
            },
            styles={
                "border_radius": "0px",
                "box_shadow": "0 0 0 2px #000000",
                "transition": "none",
            },
        )

        # Professional theme
        self.themes["professional"] = Theme(
            id="professional",
            name="Professional",
            description="Professional theme for business use",
            colors={
                "primary": "#1976D2",
                "secondary": "#757575",
                "success": "#388E3C",
                "danger": "#D32F2F",
                "warning": "#F57C00",
                "info": "#1976D2",
                "light": "#FAFAFA",
                "dark": "#424242",
                "background": "#FAFAFA",
                "surface": "#FFFFFF",
                "text": "#212121",
                "text_secondary": "#757575",
            },
            fonts={
                "primary": "Roboto, sans-seri",
                "secondary": "Roboto Mono, monospace",
                "size_small": "12px",
                "size_medium": "14px",
                "size_large": "16px",
                "size_xlarge": "18px",
            },
            styles={
                "border_radius": "2px",
                "box_shadow": "0 1px 3px rgba(0,0,0,0.12)",
                "transition": "all 0.2s ease",
            },
        )

        self._save_themes()

    def _save_themes(self):
        """Save themes to file"""
        try:
            theme_data = {
                theme_id: theme.to_dict() for theme_id, theme in self.themes.items()
            }

            with open(self.themes_path, "w") as f:
                json.dump(theme_data, f, indent=2)

        except Exception as e:
            logger.error(f"Error saving themes: {e}")

    def get_available_themes(self) -> List[Dict[str, Any]]:
        """Get list of available themes"""
        return [
            {
                "id": theme.id,
                "name": theme.name,
                "description": theme.description,
                "is_current": theme.id == self.current_theme,
            }
            for theme in self.themes.values()
        ]

    def get_theme(self, theme_id: str = None) -> Optional[Theme]:
        """Get theme by ID"""
        if theme_id is None:
            theme_id = self.current_theme

        return self.themes.get(theme_id)

    def set_theme(self, theme_id: str) -> bool:
        """Set the current theme"""
        if theme_id not in self.themes:
            return False

        self.current_theme = theme_id
        return True

    def create_custom_theme(
        self,
        theme_id: str,
        name: str,
        description: str,
        colors: Dict[str, str],
        fonts: Dict[str, str],
        styles: Dict[str, Any],
    ) -> bool:
        """Create a custom theme"""
        try:
            theme = Theme(
                id=theme_id,
                name=name,
                description=description,
                colors=colors,
                fonts=fonts,
                styles=styles,
            )

            self.themes[theme_id] = theme
            self._save_themes()

            return True

        except Exception as e:
            logger.error(f"Error creating custom theme: {e}")
            return False

    def generate_css(self, theme_id: str = None) -> str:
        """Generate CSS for a theme"""
        theme = self.get_theme(theme_id)

        if not theme:
            return ""

        css = """
/* PiWardrive Theme: {theme.name} */
:root {{
    --primary-color: {theme.colors.get('primary', '#2196F3')};
    --secondary-color: {theme.colors.get('secondary', '#FFC107')};
    --success-color: {theme.colors.get('success', '#4CAF50')};
    --danger-color: {theme.colors.get('danger', '#F44336')};
    --warning-color: {theme.colors.get('warning', '#FF9800')};
    --info-color: {theme.colors.get('info', '#17A2B8')};
    --light-color: {theme.colors.get('light', '#F8F9FA')};
    --dark-color: {theme.colors.get('dark', '#343A40')};
    --background-color: {theme.colors.get('background', '#FFFFFF')};
    --surface-color: {theme.colors.get('surface', '#F5F5F5')};
    --text-color: {theme.colors.get('text', '#212121')};
    --text-secondary-color: {theme.colors.get('text_secondary', '#757575')};

    --font-primary: {theme.fonts.get('primary', 'Arial, sans-serif')};
    --font-secondary: {theme.fonts.get('secondary', 'Monaco, monospace')};
    --font-size-small: {theme.fonts.get('size_small', '12px')};
    --font-size-medium: {theme.fonts.get('size_medium', '14px')};
    --font-size-large: {theme.fonts.get('size_large', '16px')};
    --font-size-xlarge: {theme.fonts.get('size_xlarge', '18px')};

    --border-radius: {theme.styles.get('border_radius', '4px')};
    --box-shadow: {theme.styles.get('box_shadow', '0 2px 4px rgba(0,0,0,0.1)')};
    --transition: {theme.styles.get('transition', 'all 0.3s ease')};
}}

body {{
    background-color: var(--background-color);
    color: var(--text-color);
    font-family: var(--font-primary);
    font-size: var(--font-size-medium);
}}

.surface {{
    background-color: var(--surface-color);
    border-radius: var(--border-radius);
    box-shadow: var(--box-shadow);
}}

.btn-primary {{
    background-color: var(--primary-color);
    border-color: var(--primary-color);
    transition: var(--transition);
}}

.btn-secondary {{
    background-color: var(--secondary-color);
    border-color: var(--secondary-color);
    transition: var(--transition);
}}

.text-primary {{ color: var(--primary-color); }}
.text-secondary {{ color: var(--text-secondary-color); }}
.text-success {{ color: var(--success-color); }}
.text-danger {{ color: var(--danger-color); }}
.text-warning {{ color: var(--warning-color); }}
.text-info {{ color: var(--info-color); }}
"""

        return css


# Flask web interface (if Flask is available)
if HAS_FLASK:

    class WebInterface:
        """Web interface for user experience enhancements"""

        def __init__(self, app: Flask = None):
            self.app = app or Flask(__name__)
            self.app.secret_key = os.urandom(24)

            self.socketio = SocketIO(self.app, cors_allowed_origins="*")

            self.setup_wizard = GuidedSetupWizard()
            self.tutorial_system = InteractiveTutorialSystem()
            self.dashboard = CustomizableDashboard()
            self.theme_system = ThemeSystem()

            self._setup_routes()

        def _setup_routes(self):
            """Setup Flask routes"""

            @self.app.route("/")
            def index():
                if not self.setup_wizard.is_setup_complete():
                    return redirect(url_for("setup_wizard"))
                return render_template("dashboard.html")

            @self.app.route("/setup")
            def setup_wizard():
                current_step = self.setup_wizard.get_current_step()
                all_steps = self.setup_wizard.get_all_steps()
                progress = self.setup_wizard.get_progress_percentage()

                return render_template(
                    "setup_wizard.html",
                    current_step=current_step,
                    all_steps=all_steps,
                    progress=progress,
                )

            @self.app.route("/api/setup/step/<step_id>", methods=["POST"])
            def complete_setup_step(step_id):
                data = request.json or {}

                if step_id == "hardware_detection":
                    self.setup_wizard.perform_hardware_detection()

                success = self.setup_wizard.complete_step(step_id, data)

                return jsonify(
                    {
                        "success": success,
                        "data": data,
                        "next_step": (
                            self.setup_wizard.next_step().to_dict() if success else None
                        ),
                    }
                )

            @self.app.route("/tutorials")
            def tutorials():
                available_tutorials = self.tutorial_system.get_available_tutorials()
                return render_template("tutorials.html", tutorials=available_tutorials)

            @self.app.route("/api/tutorial/<tutorial_id>/start", methods=["POST"])
            def start_tutorial(tutorial_id):
                success = self.tutorial_system.start_tutorial(tutorial_id)
                current_step = self.tutorial_system.get_current_tutorial_step()

                return jsonify(
                    {
                        "success": success,
                        "current_step": (
                            current_step.to_dict() if current_step else None
                        ),
                    }
                )

            @self.app.route("/dashboard")
            def dashboard():
                layout = self.dashboard.get_dashboard_layout()
                return render_template("dashboard.html", layout=layout)

            @self.app.route("/api/dashboard/widget/<widget_id>/data")
            def get_widget_data(widget_id):
                data = self.dashboard.get_widget_data(widget_id)
                return jsonify(data)

            @self.app.route("/themes")
            def themes():
                available_themes = self.theme_system.get_available_themes()
                return render_template("themes.html", themes=available_themes)

            @self.app.route("/api/theme/<theme_id>/css")
            def get_theme_css(theme_id):
                css = self.theme_system.generate_css(theme_id)
                return css, 200, {"Content-Type": "text/css"}

        def run(self, host="0.0.0.0", port=5000, debug=False):
            """Run the web interface"""
            self.socketio.run(self.app, host=host, port=port, debug=debug)


# Example usage functions
def example_setup_wizard():
    """Example of guided setup wizard"""
    wizard = GuidedSetupWizard()

    # Register callbacks
    def hardware_callback(data):
        logger.info(f"Hardware detection completed: {data}")

    wizard.register_callback("hardware_detection", hardware_callback)

    # Simulate setup process
    current_step = wizard.get_current_step()
    logger.info(f"Current step: {current_step.title}")

    # Complete hardware detection
    hardware_data = wizard.perform_hardware_detection()
    wizard.complete_step("hardware_detection", hardware_data)

    progress = wizard.get_progress_percentage()
    logger.info(f"Setup progress: {progress}%")

    return wizard


def example_tutorial_system():
    """Example of tutorial system"""
    tutorials = InteractiveTutorialSystem()

    # Get available tutorials
    available = tutorials.get_available_tutorials()
    logger.info(f"Available tutorials: {len(available)}")

    # Start basic navigation tutorial
    if tutorials.start_tutorial("basic_navigation"):
        logger.info("Started basic navigation tutorial")

        # Simulate tutorial progression
        for i in range(3):
            current_step = tutorials.get_current_tutorial_step()
            if current_step:
                logger.info(f"Tutorial step: {current_step.title}")
                tutorials.complete_tutorial_step(current_step.id)
                tutorials.next_tutorial_step()
            else:
                break

        tutorials.finish_tutorial()

    return tutorials


def example_dashboard():
    """Example of customizable dashboard"""
    dashboard = CustomizableDashboard()

    # Add a new widget
    widget_id = dashboard.add_widget(
        "signal_strength", {"x": 100, "y": 100}, "Custom Signal Chart"
    )

    logger.info(f"Added widget: {widget_id}")

    # Get dashboard layout
    layout = dashboard.get_dashboard_layout()
    logger.info(f"Dashboard has {len(layout['widgets'])} widgets")

    return dashboard


def example_theme_system():
    """Example of theme system"""
    themes = ThemeSystem()

    # Get available themes
    available = themes.get_available_themes()
    logger.info(f"Available themes: {[t['name'] for t in available]}")

    # Set dark theme
    if themes.set_theme("dark"):
        logger.info("Set dark theme")

    # Generate CSS
    css = themes.generate_css()
    logger.info(f"Generated CSS: {len(css)} characters")

    return themes


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Run examples
    example_setup_wizard()
    example_tutorial_system()
    example_dashboard()
    example_theme_system()

    # Start web interface if Flask is available
    if HAS_FLASK:
        web_interface = WebInterface()
        logger.info("Starting web interface on http://localhost:5000")
        web_interface.run(debug=False)
