"""
PiWardrive Unified Platform Integration.

This module provides the main integration layer that brings together all PiWardrive modules
into a cohesive, production-ready wireless intelligence platform.

Features:
- Unified API for all modules
- Centralized configuration and management
- Integrated dashboard and monitoring
- Automated workflows and pipelines
- Professional deployment and scaling
- Complete system orchestration

Author: PiWardrive Development Team
License: MIT
"""

import json
import logging
import os
import queue
import threading
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import yaml
from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS

from ..analysis.packet_engine import PacketAnalysisEngine
from ..enhanced.critical_additions import CriticalAdditionsManager
from ..enhanced.strategic_enhancements import StrategicEnhancementsManager
from ..geospatial.intelligence import GeospatialIntelligence
from ..integration.system_orchestration import MicroserviceOrchestrator
from ..mining.advanced_data_mining import AdvancedDataMining

# Import all PiWardrive modules
from ..ml.threat_detection import OfflineThreatDetector
from ..navigation.offline_navigation import OfflineNavigationSystem
from ..performance.optimization import PerformanceOptimizer
from ..plugins.plugin_architecture import PluginManager
from ..protocols.multi_protocol import MultiProtocolManager
from ..reporting.professional import ProfessionalReportingSuite
from ..signal.rf_spectrum import RFSpectrumIntelligence
from ..testing.automated_framework import AutomatedTestingFramework
from ..visualization.advanced_visualization import AdvancedVisualizationEngine

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SystemStatus(Enum):
    """System status enumeration."""

    INITIALIZING = "initializing"
    RUNNING = "running"
    DEGRADED = "degraded"
    STOPPED = "stopped"
    ERROR = "error"


class ModuleStatus(Enum):
    """Module status enumeration."""

    LOADED = "loaded"
    INITIALIZED = "initialized"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class ModuleInfo:
    """Module information structure."""

    name: str
    version: str
    description: str
    status: ModuleStatus = ModuleStatus.LOADED
    instance: Any = None
    dependencies: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    last_activity: datetime = field(default_factory=datetime.now)
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SystemConfiguration:
    """System configuration structure."""

    system_name: str = "PiWardrive"
    version: str = "2.0.0"
    environment: str = "production"
    debug_mode: bool = False
    api_port: int = 8080
    dashboard_port: int = 8081
    max_threads: int = 10
    data_retention_days: int = 30
    auto_backup: bool = True
    modules: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    integrations: Dict[str, Dict[str, Any]] = field(default_factory=dict)


class PiWardriveUnifiedPlatform:
    """Main unified platform class."""

    def __init__(self, config_path: Optional[str] = None):
        """Initialize the unified platform.
        
        Args:
            config_path: Optional path to configuration file.
        """
        self.config = SystemConfiguration()
        self.status = SystemStatus.INITIALIZING
        self.modules = {}
        self.api_app = None
        self.dashboard_app = None
        self.event_queue = queue.Queue()
        self.thread_pool = []
        self.startup_time = datetime.now()

        # Load configuration
        if config_path:
            self.load_configuration(config_path)

        # Initialize modules
        self._initialize_modules()

        # Setup APIs
        self._setup_apis()

        # Setup monitoring
        self._setup_monitoring()

        logger.info("PiWardrive Unified Platform initialized")

    def load_configuration(self, config_path: str):
        """Load system configuration from file.
        
        Args:
            config_path: Path to the configuration file.
        """
        try:
            with open(config_path, "r") as f:
                if config_path.endswith(".yaml") or config_path.endswith(".yml"):
                    config_data = yaml.safe_load(f)
                else:
                    config_data = json.load(f)

            # Update configuration
            for key, value in config_data.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)

            logger.info(f"Configuration loaded from {config_path}")

        except (FileNotFoundError, PermissionError) as e:
            logger.error(f"Failed to load configuration: {e}")
        except (yaml.YAMLError, json.JSONDecodeError) as e:
            logger.error(f"Failed to parse configuration file: {e}")
        except Exception as e:
            logger.error(f"Unexpected error loading configuration: {e}")

    def _initialize_modules(self):
        """Initialize all system modules."""
        module_configs = {
            "threat_detection": {
                "class": OfflineThreatDetector,
                "description": "Machine Learning & AI Analytics",
                "capabilities": [
                    "anomaly_detection",
                    "device_fingerprinting",
                    "risk_scoring",
                ],
            },
            "rf_spectrum": {
                "class": RFSpectrumIntelligence,
                "description": "Advanced Signal Analysis",
                "capabilities": [
                    "spectrum_analysis",
                    "interference_detection",
                    "channel_optimization",
                ],
            },
            "geospatial": {
                "class": GeospatialIntelligence,
                "description": "Geospatial Intelligence Platform",
                "capabilities": [
                    "indoor_positioning",
                    "floor_plan_generation",
                    "movement_analysis",
                ],
            },
            "reporting": {
                "class": ProfessionalReportingSuite,
                "description": "Professional Reporting Suite",
                "capabilities": [
                    "html_reports",
                    "compliance_checking",
                    "vulnerability_assessment",
                ],
            },
            "packet_engine": {
                "class": PacketAnalysisEngine,
                "description": "Packet Analysis Engine",
                "capabilities": [
                    "protocol_analysis",
                    "topology_mapping",
                    "traffic_classification",
                ],
            },
            "multi_protocol": {
                "class": MultiProtocolManager,
                "description": "Multi-Protocol Support",
                "capabilities": [
                    "ble_scanning",
                    "zigbee_analysis",
                    "cellular_monitoring",
                ],
            },
            "testing": {
                "class": AutomatedTestingFramework,
                "description": "Automated Testing Framework",
                "capabilities": [
                    "hardware_validation",
                    "regression_testing",
                    "performance_benchmarking",
                ],
            },
            "data_mining": {
                "class": AdvancedDataMining,
                "description": "Advanced Data Mining",
                "capabilities": ["pattern_mining", "clustering", "predictive_modeling"],
            },
            "plugins": {
                "class": PluginManager,
                "description": "Plugin Architecture",
                "capabilities": [
                    "plugin_loading",
                    "api_integration",
                    "secure_sandboxing",
                ],
            },
            "navigation": {
                "class": OfflineNavigationSystem,
                "description": "Offline Navigation System",
                "capabilities": [
                    "wifi_positioning",
                    "pathfinding",
                    "breadcrumb_navigation",
                ],
            },
            "visualization": {
                "class": AdvancedVisualizationEngine,
                "description": "Advanced Visualization",
                "capabilities": [
                    "3d_visualization",
                    "timeline_scrubbing",
                    "custom_scripting",
                ],
            },
            "performance": {
                "class": PerformanceOptimizer,
                "description": "Performance Optimization",
                "capabilities": [
                    "multi_threading",
                    "intelligent_caching",
                    "system_monitoring",
                ],
            },
            "critical_additions": {
                "class": CriticalAdditionsManager,
                "description": "Critical Additions",
                "capabilities": [
                    "real_time_streaming",
                    "enhanced_security",
                    "iot_profiling",
                ],
            },
            "strategic_enhancements": {
                "class": StrategicEnhancementsManager,
                "description": "Strategic Enhancements",
                "capabilities": [
                    "threat_intelligence",
                    "quantum_crypto",
                    "global_intelligence",
                ],
            },
            "system_orchestration": {
                "class": MicroserviceOrchestrator,
                "description": "System Orchestration",
                "capabilities": [
                    "api_gateway",
                    "service_mesh",
                    "event_driven_architecture",
                ],
            },
        }

        for module_name, module_config in module_configs.items():
            try:
                # Create module instance
                module_class = module_config["class"]
                module_instance = module_class()

                # Create module info
                module_info = ModuleInfo(
                    name=module_name,
                    version="1.0.0",
                    description=module_config["description"],
                    status=ModuleStatus.INITIALIZED,
                    instance=module_instance,
                    capabilities=module_config["capabilities"],
                )

                self.modules[module_name] = module_info
                logger.info(f"Initialized module: {module_name}")

            except Exception as e:
                logger.error(f"Failed to initialize module {module_name}: {e}")

                # Create error module info
                module_info = ModuleInfo(
                    name=module_name,
                    version="1.0.0",
                    description=module_config["description"],
                    status=ModuleStatus.ERROR,
                    capabilities=module_config["capabilities"],
                )
                self.modules[module_name] = module_info

    def _setup_apis(self):
        """Set up REST API endpoints."""
        self.api_app = Flask(__name__)
        CORS(self.api_app)

        @self.api_app.route("/api/v1/status", methods=["GET"])
        def get_system_status():
            """Get system status."""
            return jsonify(self.get_system_status())

        @self.api_app.route("/api/v1/modules", methods=["GET"])
        def get_modules():
            """Get all modules."""
            modules_data = {}
            for name, module in self.modules.items():
                modules_data[name] = {
                    "name": module.name,
                    "description": module.description,
                    "status": module.status.value,
                    "capabilities": module.capabilities,
                    "last_activity": module.last_activity.isoformat(),
                    "metrics": module.metrics,
                }
            return jsonify(modules_data)

        @self.api_app.route("/api/v1/modules/<module_name>", methods=["GET"])
        def get_module(module_name):
            """Get specific module."""
            if module_name not in self.modules:
                return jsonify({"error": "Module not found"}), 404

            module = self.modules[module_name]
            return jsonify(
                {
                    "name": module.name,
                    "description": module.description,
                    "status": module.status.value,
                    "capabilities": module.capabilities,
                    "last_activity": module.last_activity.isoformat(),
                    "metrics": module.metrics,
                }
            )

        @self.api_app.route("/api/v1/modules/<module_name>/execute", methods=["POST"])
        def execute_module_function(module_name):
            """Execute module function."""
            if module_name not in self.modules:
                return jsonify({"error": "Module not found"}), 404

            module = self.modules[module_name]
            if module.status != ModuleStatus.INITIALIZED:
                return jsonify({"error": "Module not available"}), 503

            try:
                function_name = request.json.get("function")
                args = request.json.get("args", [])
                kwargs = request.json.get("kwargs", {})

                if hasattr(module.instance, function_name):
                    func = getattr(module.instance, function_name)
                    result = func(*args, **kwargs)

                    # Update module metrics
                    module.last_activity = datetime.now()
                    module.metrics["last_execution"] = function_name
                    module.metrics["execution_count"] = (
                        module.metrics.get("execution_count", 0) + 1
                    )

                    return jsonify({"result": result})
                else:
                    return jsonify({"error": "Function not found"}), 404

            except Exception as e:
                logger.error(f"Module execution error: {e}")
                return jsonify({"error": str(e)}), 500

        @self.api_app.route("/api/v1/scan", methods=["POST"])
        def start_scan():
            """Start comprehensive scan."""
            try:
                scan_config = request.json or {}
                scan_id = self.start_comprehensive_scan(scan_config)
                return jsonify({"scan_id": scan_id})
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.api_app.route("/api/v1/reports", methods=["GET"])
        def get_reports():
            """Get available reports."""
            try:
                reports = self.get_available_reports()
                return jsonify(reports)
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.api_app.route("/api/v1/reports/<report_id>", methods=["GET"])
        def get_report(report_id):
            """Get specific report."""
            try:
                report = self.get_report_by_id(report_id)
                if report:
                    return jsonify(report)
                else:
                    return jsonify({"error": "Report not found"}), 404
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        # Dashboard app
        self.dashboard_app = Flask(__name__)
        CORS(self.dashboard_app)

        @self.dashboard_app.route("/")
        def dashboard():
            """Serve main dashboard."""
            return render_template_string(self._get_dashboard_template())

        @self.dashboard_app.route("/dashboard/api/status")
        def dashboard_status():
            """Get dashboard API status."""
            return jsonify(self.get_system_status())

    def _setup_monitoring(self):
        """Set up system monitoring."""

        def monitor_system():
            """Monitor system thread."""
            while self.status == SystemStatus.RUNNING:
                try:
                    # Update system metrics
                    self._update_system_metrics()

                    # Check module health
                    self._check_module_health()

                    # Process events
                    self._process_events()

                    time.sleep(10)  # Monitor every 10 seconds

                except Exception as e:
                    logger.error(f"Monitoring error: {e}")
                    time.sleep(5)

        monitor_thread = threading.Thread(target=monitor_system)
        monitor_thread.daemon = True
        monitor_thread.start()

        logger.info("System monitoring started")

    def _update_system_metrics(self):
        """Update system metrics."""
        for module_name, module in self.modules.items():
            if module.status == ModuleStatus.INITIALIZED and module.instance:
                try:
                    # Get module metrics if available
                    if hasattr(module.instance, "get_metrics"):
                        metrics = module.instance.get_metrics()
                        module.metrics.update(metrics)
                except Exception as e:
                    logger.warning(f"Failed to get metrics for {module_name}: {e}")

    def _check_module_health(self):
        """Check health of all modules."""
        for module_name, module in self.modules.items():
            if module.status == ModuleStatus.INITIALIZED and module.instance:
                try:
                    # Check if module has health check method
                    if hasattr(module.instance, "health_check"):
                        healthy = module.instance.health_check()
                        if not healthy:
                            module.status = ModuleStatus.ERROR
                            logger.warning(f"Module {module_name} failed health check")
                except Exception as e:
                    logger.error(f"Health check failed for {module_name}: {e}")
                    module.status = ModuleStatus.ERROR

    def _process_events(self):
        """Process system events."""
        while not self.event_queue.empty():
            try:
                event = self.event_queue.get_nowait()
                # Process event
                logger.info(f"Processing event: {event}")
            except queue.Empty:
                break
            except Exception as e:
                logger.error(f"Event processing error: {e}")

    def start_comprehensive_scan(self, config: Dict[str, Any]) -> str:
        """Start comprehensive scan across all modules."""
        scan_id = str(uuid.uuid4())

        # Create scan configuration
        scan_config = {
            "scan_id": scan_id,
            "timestamp": datetime.now().isoformat(),
            "modules": config.get("modules", list(self.modules.keys())),
            "parameters": config.get("parameters", {}),
        }

        # Start scan in background
        def run_scan():
            try:
                results = {}

                for module_name in scan_config["modules"]:
                    if module_name in self.modules:
                        module = self.modules[module_name]
                        if (
                            module.status == ModuleStatus.INITIALIZED
                            and module.instance
                        ):
                            try:
                                # Execute scan if module supports it
                                if hasattr(module.instance, "scan"):
                                    result = module.instance.scan(
                                        scan_config["parameters"]
                                    )
                                    results[module_name] = result
                                elif hasattr(module.instance, "analyze"):
                                    result = module.instance.analyze(
                                        scan_config["parameters"]
                                    )
                                    results[module_name] = result
                                else:
                                    results[module_name] = {"status": "not_supported"}
                            except Exception as e:
                                results[module_name] = {"error": str(e)}
                                logger.error(f"Scan failed for {module_name}: {e}")

                # Store results
                self._store_scan_results(scan_id, results)

            except Exception as e:
                logger.error(f"Scan execution error: {e}")

        scan_thread = threading.Thread(target=run_scan)
        scan_thread.daemon = True
        scan_thread.start()

        return scan_id

    def _store_scan_results(self, scan_id: str, results: Dict[str, Any]):
        """Store scan results."""
        # In a real implementation, this would store to database
        results_file = f"scan_results_{scan_id}.json"
        with open(results_file, "w") as f:
            json.dump(results, f, indent=2, default=str)

        logger.info(f"Scan results stored: {results_file}")

    def get_available_reports(self) -> List[Dict[str, Any]]:
        """Get available reports."""
        reports = []

        # Look for report files
        for report_file in Path(".").glob("scan_results_*.json"):
            try:
                with open(report_file, "r") as f:
                    data = json.load(f)
                    reports.append(
                        {
                            "id": report_file.stem.replace("scan_results_", ""),
                            "filename": report_file.name,
                            "timestamp": data.get("timestamp", "unknown"),
                            "modules": (
                                list(data.keys()) if isinstance(data, dict) else []
                            ),
                        }
                    )
            except (FileNotFoundError, PermissionError) as e:
                logger.warning(f"Failed to read report {report_file}: {e}")
            except json.JSONDecodeError as e:
                logger.warning(f"Invalid JSON in report {report_file}: {e}")
            except Exception as e:
                logger.warning(f"Unexpected error reading report {report_file}: {e}")

        return reports

    def get_report_by_id(self, report_id: str) -> Optional[Dict[str, Any]]:
        """Get report by ID."""
        report_file = f"scan_results_{report_id}.json"

        if os.path.exists(report_file):
            try:
                with open(report_file, "r") as f:
                    return json.load(f)
            except (FileNotFoundError, PermissionError) as e:
                logger.error(f"Failed to access report {report_id}: {e}")
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in report {report_id}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error loading report {report_id}: {e}")

        return None

    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        uptime = datetime.now() - self.startup_time

        module_statuses = {}
        healthy_modules = 0

        for name, module in self.modules.items():
            module_statuses[name] = module.status.value
            if module.status == ModuleStatus.INITIALIZED:
                healthy_modules += 1

        return {
            "system_name": self.config.system_name,
            "version": self.config.version,
            "status": self.status.value,
            "uptime": str(uptime),
            "modules": {
                "total": len(self.modules),
                "healthy": healthy_modules,
                "statuses": module_statuses,
            },
            "configuration": {
                "environment": self.config.environment,
                "debug_mode": self.config.debug_mode,
                "api_port": self.config.api_port,
                "dashboard_port": self.config.dashboard_port,
            },
            "timestamp": datetime.now().isoformat(),
        }

    def _get_dashboard_template(self) -> str:
        """Get dashboard HTML template."""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>PiWardrive Unified Platform Dashboard</title>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <style>
                body { font-family: Arial,
                    sans-serif; margin: 20px; background-color: #f5f5f5; }
                .header { background-color: #2c3e50; color: white; padding: 20px; margin-bottom: 20px; }
                .card { background-color: white; padding: 20px; margin-bottom: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,
                    0,
                    0,
                    0.1); }
                .status-healthy { color: #27ae60; }
                .status-error { color: #e74c3c; }
                .status-degraded { color: #f39c12; }
                .module-grid { display: grid; grid-template-columns: repeat(auto-fit,
                    minmax(300px,
                    1fr)); gap: 20px; }
                .module-card { background-color: white; padding: 15px; border-radius: 5px; border-left: 4px solid #3498db; }
                .capabilities { margin-top: 10px; }
                .capability { background-color: #ecf0f1; padding: 2px 8px; margin: 2px; border-radius: 3px; display: inline-block; font-size: 12px; }
                .refresh-btn { background-color: #3498db; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
                .refresh-btn:hover { background-color: #2980b9; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>PiWardrive Unified Platform</h1>
                <p>Advanced Wireless Intelligence & Analytics Platform</p>
            </div>

            <div class="card">
                <h2>System Status</h2>
                <div id="system-status">Loading...</div>
                <button class="refresh-btn" onclick="refreshStatus()">Refresh</button>
            </div>

            <div class="card">
                <h2>Modules</h2>
                <div id="modules-grid" class="module-grid">Loading...</div>
            </div>

            <div class="card">
                <h2>System Metrics</h2>
                <canvas id="metrics-chart"></canvas>
            </div>

            <script>
                function refreshStatus() {
                    fetch('/dashboard/api/status')
                        .then(response => response.json())
                        .then(data => {
                            updateSystemStatus(data);
                            updateModules(data);
                        })
                        .catch(error => console.error('Error:', error));
                }

                function updateSystemStatus(data) {
                    const statusDiv = document.getElementById('system-status');
                    const statusClass = data.status === 'running' ? 'status-healthy' :
                                       data.status === 'error' ? 'status-error' : 'status-degraded';

                    statusDiv.innerHTML = `
                        <p><strong>Status:</strong> <span class="${statusClass}">${data.status.toUpperCase()}</span></p>
                        <p><strong>Version:</strong> ${data.version}</p>
                        <p><strong>Uptime:</strong> ${data.uptime}</p>
                        <p><strong>Modules:</strong> ${data.modules.healthy}/${data.modules.total} healthy</p>
                    `;
                }

                function updateModules(data) {
                    const modulesGrid = document.getElementById('modules-grid');
                    let html = '';

                    Object.entries(data.modules.statuses).forEach(([name, status]) => {
                        const statusClass = status === 'initialized' ? 'status-healthy' :
                                           status === 'error' ? 'status-error' : 'status-degraded';

                        html += `
                            <div class="module-card">
                                <h3>${name.replace('_', ' ').toUpperCase()}</h3>
                                <p><strong>Status:</strong> <span class="${statusClass}">${status}</span></p>
                            </div>
                        `;
                    });

                    modulesGrid.innerHTML = html;
                }

                // Initialize dashboard
                refreshStatus();

                // Auto-refresh every 30 seconds
                setInterval(refreshStatus, 30000);
            </script>
        </body>
        </html>
        """

    def start(self):
        """Start the unified platform."""
        self.status = SystemStatus.RUNNING

        # Start API server
        def run_api():
            self.api_app.run(
                host="0.0.0.0", port=self.config.api_port, debug=self.config.debug_mode
            )

        # Start dashboard server
        def run_dashboard():
            self.dashboard_app.run(
                host="0.0.0.0",
                port=self.config.dashboard_port,
                debug=self.config.debug_mode,
            )

        api_thread = threading.Thread(target=run_api)
        api_thread.daemon = True
        api_thread.start()

        dashboard_thread = threading.Thread(target=run_dashboard)
        dashboard_thread.daemon = True
        dashboard_thread.start()

        logger.info("PiWardrive Unified Platform started")
        logger.info(f"API server: http://localhost:{self.config.api_port}")
        logger.info(f"Dashboard: http://localhost:{self.config.dashboard_port}")

        # Keep main thread alive
        try:
            while self.status == SystemStatus.RUNNING:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            self.stop()

    def stop(self):
        """Stop the unified platform."""
        self.status = SystemStatus.STOPPED

        # Stop all modules
        for module_name, module in self.modules.items():
            if module.instance and hasattr(module.instance, "stop"):
                try:
                    module.instance.stop()
                    module.status = ModuleStatus.STOPPED
                except Exception as e:
                    logger.error(f"Failed to stop module {module_name}: {e}")

        logger.info("PiWardrive Unified Platform stopped")


# Demo and Test Functions
def create_sample_config():
    """Create sample configuration file."""
    __config = {
        "system_name": "PiWardrive",
        "version": "2.0.0",
        "environment": "production",
        "debug_mode": False,
        "api_port": 8080,
        "dashboard_port": 8081,
        "max_threads": 10,
        "data_retention_days": 30,
        "auto_backup": True,
        "modules": {
            "threat_detection": {
                "enabled": True,
                "config": {"sensitivity": "high", "update_interval": 300},
            },
            "rf_spectrum": {
                "enabled": True,
                "config": {"frequency_range": [2400, 5800], "resolution": "high"},
            },
        },
        "integrations": {
            "siem": {
                "enabled": False,
                "endpoint": "https://siem.example.com/api",
                "api_key": "your_api_key_here",
            }
        },
    }

    with open("piwardrive_config.yaml", "w") as f:
        yaml.dump(__config, f, default_flow_style=False)

    print("Sample configuration created: piwardrive_config.yaml")


def demo_unified_platform():
    """Demo the unified platform."""
    print("=== PiWardrive Unified Platform Demo ===\n")

    # Create sample configuration
    create_sample_config()

    # Initialize platform
    platform = PiWardriveUnifiedPlatform("piwardrive_config.yaml")

    # Display system status
    status = platform.get_system_status()
    print(f"System Status: {json.dumps(status, indent=2)}")

    # Test scan
    print("\nStarting comprehensive scan...")
    scan_id = platform.start_comprehensive_scan(
        {
            "modules": ["threat_detection", "rf_spectrum", "geospatial"],
            "parameters": {"duration": 60, "sensitivity": "high"},
        }
    )
    print(f"Scan started with ID: {scan_id}")

    # Wait a bit
    time.sleep(2)

    # Check reports
    reports = platform.get_available_reports()
    print(f"\nAvailable reports: {len(reports)}")

    print("\n=== Unified Platform Demo Complete ===")
    print(
        f"API Server would be available at: http://localhost:{platform.config.api_port}"
    )
    print(
        f"Dashboard would be available at: http://localhost:{platform.config.dashboard_port}"
    )


if __name__ == "__main__":
    demo_unified_platform()
