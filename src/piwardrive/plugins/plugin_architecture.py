"""
PiWardrive Plugin Architecture

A comprehensive plugin system for extending PiWardrive functionality with:
- Modular plugin system with hot-loading capabilities
- Plugin API for custom visualizations and analysis
- Hardware abstraction layer for different devices
- Algorithm plugin framework for custom analysis methods
- Plugin management and lifecycle control
- Secure plugin sandboxing and validation

Author: PiWardrive Development Team
License: MIT
"""

import abc
import ast
import importlib.util
import json
import logging
import tempfile
import threading
import zipfile
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Union

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PluginType(Enum):
    """Plugin type classifications"""

    VISUALIZATION = "visualization"
    ANALYSIS = "analysis"
    HARDWARE = "hardware"
    PROTOCOL = "protocol"
    EXPORT = "export"
    CUSTOM = "custom"


class PluginStatus(Enum):
    """Plugin status states"""

    INACTIVE = "inactive"
    LOADING = "loading"
    ACTIVE = "active"
    ERROR = "error"
    DISABLED = "disabled"


@dataclass
class PluginMetadata:
    """Plugin metadata structure"""

    name: str
    version: str
    description: str
    author: str
    plugin_type: PluginType
    dependencies: List[str] = field(default_factory=list)
    api_version: str = "1.0"
    entry_point: str = "main"
    permissions: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "plugin_type": self.plugin_type.value,
            "dependencies": self.dependencies,
            "api_version": self.api_version,
            "entry_point": self.entry_point,
            "permissions": self.permissions,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class PluginContext:
    """Plugin execution context"""

    plugin_id: str
    data_access: Dict[str, Any] = field(default_factory=dict)
    config: Dict[str, Any] = field(default_factory=dict)
    callbacks: Dict[str, Callable] = field(default_factory=dict)
    shared_state: Dict[str, Any] = field(default_factory=dict)


class PluginInterface(abc.ABC):
    """Base interface for all plugins"""

    @abc.abstractmethod
    def initialize(self, context: PluginContext) -> bool:
        """Initialize the plugin"""

    @abc.abstractmethod
    def execute(self, input_data: Any) -> Any:
        """Execute plugin functionality"""

    @abc.abstractmethod
    def cleanup(self) -> bool:
        """Cleanup plugin resources"""

    @abc.abstractmethod
    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata"""


class VisualizationPlugin(PluginInterface):
    """Base class for visualization plugins"""

    @abc.abstractmethod
    def render(self, data: Any, config: Dict[str, Any]) -> str:
        """Render visualization"""

    @abc.abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Get supported output formats"""


class AnalysisPlugin(PluginInterface):
    """Base class for analysis plugins"""

    @abc.abstractmethod
    def analyze(self, data: Any) -> Dict[str, Any]:
        """Perform analysis"""

    @abc.abstractmethod
    def get_analysis_type(self) -> str:
        """Get analysis type"""


class HardwarePlugin(PluginInterface):
    """Base class for hardware plugins"""

    @abc.abstractmethod
    def connect(self) -> bool:
        """Connect to hardware"""

    @abc.abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from hardware"""

    @abc.abstractmethod
    def scan(self) -> List[Dict[str, Any]]:
        """Perform hardware scan"""


class PluginValidator:
    """Plugin validation and security checks"""

    def __init__(self):
        self.allowed_imports = {
            "numpy",
            "pandas",
            "matplotlib",
            "seaborn",
            "plotly",
            "scipy",
            "sklearn",
            "json",
            "csv",
            "datetime",
            "time",
            "os",
            "sys",
            "pathlib",
            "logging",
            "threading",
            "queue",
        }
        self.forbidden_calls = {
            "exec",
            "eval",
            "compile",
            "__import__",
            "open",
            "file",
            "input",
            "raw_input",
            "execfile",
        }

    def validate_plugin(self, plugin_path: Path) -> tuple[bool, List[str]]:
        """Validate plugin code for security and compliance"""
        errors = []

        try:
            with open(plugin_path, "r") as f:
                code = f.read()

            # Parse AST for security analysis
            tree = ast.parse(code)

            # Check for forbidden operations
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in self.forbidden_calls:
                            errors.append(f"Forbidden function call: {node.func.id}")

                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name not in self.allowed_imports:
                            errors.append(f"Unauthorized import: {alias.name}")

                if isinstance(node, ast.ImportFrom):
                    if node.module not in self.allowed_imports:
                        errors.append(f"Unauthorized import from: {node.module}")

            return len(errors) == 0, errors

        except Exception as e:
            errors.append(f"Parse error: {str(e)}")
            return False, errors


class PluginSandbox:
    """Secure plugin execution environment"""

    def __init__(self, plugin_id: str):
        self.plugin_id = plugin_id
        self.restricted_builtins = {
            "__import__": None,
            "exec": None,
            "eval": None,
            "compile": None,
            "open": self._restricted_open,
            "file": None,
            "input": None,
            "raw_input": None,
        }

    def _restricted_open(self, filename, mode="r", *args, **kwargs):
        """Restricted file access"""
        # Only allow reading from specific directories
        allowed_dirs = ["/tmp", "/var/tmp", "plugins/data"]
        filepath = Path(filename).resolve()

        if not any(
            str(filepath).startswith(allowed_dir) for allowed_dir in allowed_dirs
        ):
            raise PermissionError(f"Access denied to {filename}")

        return open(filename, mode, *args, **kwargs)

    def execute_in_sandbox(self, code: str, context: PluginContext) -> Any:
        """Execute code in sandboxed environment"""
        # Create restricted globals
        restricted_globals = {
            "__builtins__": self.restricted_builtins,
            "context": context,
            "plugin_id": self.plugin_id,
        }

        # Execute with restrictions
        try:
            exec(code, restricted_globals)
            return restricted_globals.get("result")
        except Exception as e:
            logger.error(f"Plugin {self.plugin_id} execution error: {e}")
            raise


class PluginManager:
    """Central plugin management system"""

    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugins: Dict[str, Dict[str, Any]] = {}
        self.plugin_instances: Dict[str, PluginInterface] = {}
        self.plugin_contexts: Dict[str, PluginContext] = {}
        self.validator = PluginValidator()
        self.lock = threading.Lock()
        self.event_handlers: Dict[str, List[Callable]] = {}

        # Create plugin directory structure
        self._setup_plugin_directory()

    def _setup_plugin_directory(self):
        """Setup plugin directory structure"""
        self.plugin_dir.mkdir(exist_ok=True)
        (self.plugin_dir / "installed").mkdir(exist_ok=True)
        (self.plugin_dir / "data").mkdir(exist_ok=True)
        (self.plugin_dir / "config").mkdir(exist_ok=True)
        (self.plugin_dir / "logs").mkdir(exist_ok=True)

    def register_event_handler(self, event: str, handler: Callable):
        """Register event handler"""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)

    def emit_event(self, event: str, data: Any = None):
        """Emit event to handlers"""
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                try:
                    handler(data)
                except Exception as e:
                    logger.error(f"Event handler error: {e}")

    def install_plugin(self, plugin_package: Union[str, Path]) -> bool:
        """Install plugin from package"""
        try:
            package_path = Path(plugin_package)

            if package_path.suffix == ".zip":
                return self._install_from_zip(package_path)
            elif package_path.is_dir():
                return self._install_from_directory(package_path)
            else:
                logger.error(f"Unsupported plugin package format: {package_path}")
                return False

        except Exception as e:
            logger.error(f"Plugin installation failed: {e}")
            return False

    def _install_from_zip(self, zip_path: Path) -> bool:
        """Install plugin from ZIP file"""
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(temp_dir)

            return self._install_from_directory(Path(temp_dir))

    def _install_from_directory(self, dir_path: Path) -> bool:
        """Install plugin from directory"""
        # Look for plugin manifest
        manifest_path = dir_path / "plugin.json"
        if not manifest_path.exists():
            logger.error("Plugin manifest not found")
            return False

        # Load manifest
        with open(manifest_path, "r") as f:
            manifest = json.load(f)

        plugin_id = manifest["name"]

        # Validate plugin files
        main_file = dir_path / f"{manifest.get('entry_point', 'main')}.py"
        if not main_file.exists():
            logger.error(f"Plugin entry point not found: {main_file}")
            return False

        # Security validation
        is_valid, errors = self.validator.validate_plugin(main_file)
        if not is_valid:
            logger.error(f"Plugin validation failed: {errors}")
            return False

        # Install plugin
        install_path = self.plugin_dir / "installed" / plugin_id
        install_path.mkdir(exist_ok=True)

        # Copy files
        import shutil

        shutil.copytree(dir_path, install_path, dirs_exist_ok=True)

        # Register plugin
        self.plugins[plugin_id] = {
            "manifest": manifest,
            "path": install_path,
            "status": PluginStatus.INACTIVE,
            "installed_at": datetime.now(),
        }

        logger.info(f"Plugin {plugin_id} installed successfully")
        self.emit_event("plugin_installed", plugin_id)
        return True

    def load_plugin(self, plugin_id: str) -> bool:
        """Load and initialize plugin"""
        if plugin_id not in self.plugins:
            logger.error(f"Plugin {plugin_id} not found")
            return False

        try:
            with self.lock:
                plugin_info = self.plugins[plugin_id]
                plugin_info["status"] = PluginStatus.LOADING

                # Load plugin module
                plugin_path = plugin_info["path"]
                manifest = plugin_info["manifest"]

                entry_point = f"{manifest.get('entry_point', 'main')}.py"
                module_path = plugin_path / entry_point

                spec = importlib.util.spec_from_file_location(
                    f"plugin_{plugin_id}", module_path
                )
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Get plugin class
                plugin_class = getattr(module, manifest.get("class_name", "Plugin"))
                plugin_instance = plugin_class()

                # Create context
                context = PluginContext(
                    plugin_id=plugin_id,
                    config=self._load_plugin_config(plugin_id),
                    data_access=self._create_data_access(plugin_id),
                )

                # Initialize plugin
                if plugin_instance.initialize(context):
                    self.plugin_instances[plugin_id] = plugin_instance
                    self.plugin_contexts[plugin_id] = context
                    plugin_info["status"] = PluginStatus.ACTIVE

                    logger.info(f"Plugin {plugin_id} loaded successfully")
                    self.emit_event("plugin_loaded", plugin_id)
                    return True
                else:
                    plugin_info["status"] = PluginStatus.ERROR
                    logger.error(f"Plugin {plugin_id} initialization failed")
                    return False

        except Exception as e:
            self.plugins[plugin_id]["status"] = PluginStatus.ERROR
            logger.error(f"Plugin {plugin_id} loading failed: {e}")
            return False

    def unload_plugin(self, plugin_id: str) -> bool:
        """Unload plugin"""
        if plugin_id not in self.plugin_instances:
            return True

        try:
            with self.lock:
                plugin_instance = self.plugin_instances[plugin_id]

                # Cleanup plugin
                if plugin_instance.cleanup():
                    del self.plugin_instances[plugin_id]
                    del self.plugin_contexts[plugin_id]
                    self.plugins[plugin_id]["status"] = PluginStatus.INACTIVE

                    logger.info(f"Plugin {plugin_id} unloaded successfully")
                    self.emit_event("plugin_unloaded", plugin_id)
                    return True
                else:
                    logger.error(f"Plugin {plugin_id} cleanup failed")
                    return False

        except Exception as e:
            logger.error(f"Plugin {plugin_id} unloading failed: {e}")
            return False

    def execute_plugin(self, plugin_id: str, input_data: Any) -> Any:
        """Execute plugin with input data"""
        if plugin_id not in self.plugin_instances:
            logger.error(f"Plugin {plugin_id} not loaded")
            return None

        try:
            plugin_instance = self.plugin_instances[plugin_id]
            return plugin_instance.execute(input_data)
        except Exception as e:
            logger.error(f"Plugin {plugin_id} execution failed: {e}")
            return None

    def get_plugin_list(self) -> List[Dict[str, Any]]:
        """Get list of all plugins"""
        return [
            {
                "id": plugin_id,
                "manifest": info["manifest"],
                "status": info["status"].value,
                "installed_at": info["installed_at"].isoformat(),
            }
            for plugin_id, info in self.plugins.items()
        ]

    def get_active_plugins(self) -> List[str]:
        """Get list of active plugins"""
        return [
            plugin_id
            for plugin_id, info in self.plugins.items()
            if info["status"] == PluginStatus.ACTIVE
        ]

    def _load_plugin_config(self, plugin_id: str) -> Dict[str, Any]:
        """Load plugin configuration"""
        config_path = self.plugin_dir / "config" / f"{plugin_id}.json"
        if config_path.exists():
            with open(config_path, "r") as f:
                return json.load(f)
        return {}

    def _create_data_access(self, plugin_id: str) -> Dict[str, Any]:
        """Create data access interface for plugin"""
        data_dir = self.plugin_dir / "data" / plugin_id
        data_dir.mkdir(exist_ok=True)

        return {
            "data_dir": str(data_dir),
            "read_file": lambda filename: self._safe_read_file(data_dir / filename),
            "write_file": lambda filename, data: self._safe_write_file(
                data_dir / filename, data
            ),
            "list_files": lambda: list(data_dir.iterdir()),
        }

    def _safe_read_file(self, filepath: Path) -> str:
        """Safe file reading with validation"""
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, "r") as f:
            return f.read()

    def _safe_write_file(self, filepath: Path, data: str):
        """Safe file writing with validation"""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            f.write(data)


class PluginAPI:
    """Plugin API interface for external integrations"""

    def __init__(self, plugin_manager: PluginManager):
        self.plugin_manager = plugin_manager
        self.api_endpoints = {}
        self._register_core_endpoints()

    def _register_core_endpoints(self):
        """Register core API endpoints"""
        self.api_endpoints.update(
            {
                "list_plugins": self.plugin_manager.get_plugin_list,
                "load_plugin": self.plugin_manager.load_plugin,
                "unload_plugin": self.plugin_manager.unload_plugin,
                "execute_plugin": self.plugin_manager.execute_plugin,
                "get_active_plugins": self.plugin_manager.get_active_plugins,
            }
        )

    def register_endpoint(self, name: str, handler: Callable):
        """Register custom API endpoint"""
        self.api_endpoints[name] = handler

    def call_endpoint(self, endpoint: str, *args, **kwargs) -> Any:
        """Call API endpoint"""
        if endpoint not in self.api_endpoints:
            raise ValueError(f"Unknown endpoint: {endpoint}")

        return self.api_endpoints[endpoint](*args, **kwargs)


# Example plugin implementations
class ExampleVisualizationPlugin(VisualizationPlugin):
    """Example visualization plugin"""

    def __init__(self):
        self.metadata = PluginMetadata(
            name="Example Visualization",
            version="1.0.0",
            description="Example visualization plugin",
            author="PiWardrive Team",
            plugin_type=PluginType.VISUALIZATION,
        )

    def initialize(self, context: PluginContext) -> bool:
        """Initialize plugin"""
        logger.info("Example visualization plugin initialized")
        return True

    def execute(self, input_data: Any) -> Any:
        """Execute plugin"""
        return self.render(input_data, {})

    def cleanup(self) -> bool:
        """Cleanup plugin"""
        logger.info("Example visualization plugin cleaned up")
        return True

    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata"""
        return self.metadata

    def render(self, data: Any, config: Dict[str, Any]) -> str:
        """Render visualization"""
        return f"<div>Example visualization for {len(data) if hasattr(data,
            '__len__') else 'data'} items</div>"

    def get_supported_formats(self) -> List[str]:
        """Get supported formats"""
        return ["html", "png", "svg"]


class ExampleAnalysisPlugin(AnalysisPlugin):
    """Example analysis plugin"""

    def __init__(self):
        self.metadata = PluginMetadata(
            name="Example Analysis",
            version="1.0.0",
            description="Example analysis plugin",
            author="PiWardrive Team",
            plugin_type=PluginType.ANALYSIS,
        )

    def initialize(self, context: PluginContext) -> bool:
        """Initialize plugin"""
        logger.info("Example analysis plugin initialized")
        return True

    def execute(self, input_data: Any) -> Any:
        """Execute plugin"""
        return self.analyze(input_data)

    def cleanup(self) -> bool:
        """Cleanup plugin"""
        logger.info("Example analysis plugin cleaned up")
        return True

    def get_metadata(self) -> PluginMetadata:
        """Get plugin metadata"""
        return self.metadata

    def analyze(self, data: Any) -> Dict[str, Any]:
        """Perform analysis"""
        return {
            "analysis_type": self.get_analysis_type(),
            "data_size": len(data) if hasattr(data, "__len__") else 0,
            "timestamp": datetime.now().isoformat(),
            "results": {
                "processed": True,
                "summary": f"Analyzed {type(data).__name__} data",
            },
        }

    def get_analysis_type(self) -> str:
        """Get analysis type"""
        return "example_analysis"


def demo_plugin_architecture():
    """Demonstrate plugin architecture functionality"""
    print("PiWardrive Plugin Architecture Demo")
    print("=" * 50)

    # Create plugin manager
    plugin_manager = PluginManager("demo_plugins")

    # Create plugin API
    plugin_api = PluginAPI(plugin_manager)

    # Register example plugins directly (simulating installation)
    viz_plugin = ExampleVisualizationPlugin()
    analysis_plugin = ExampleAnalysisPlugin()

    # Simulate plugin registration
    plugin_manager.plugin_instances["viz_example"] = viz_plugin
    plugin_manager.plugin_instances["analysis_example"] = analysis_plugin

    plugin_manager.plugins["viz_example"] = {
        "manifest": viz_plugin.get_metadata().to_dict(),
        "status": PluginStatus.ACTIVE,
        "installed_at": datetime.now(),
    }

    plugin_manager.plugins["analysis_example"] = {
        "manifest": analysis_plugin.get_metadata().to_dict(),
        "status": PluginStatus.ACTIVE,
        "installed_at": datetime.now(),
    }

    # Test plugin listing
    print("\n1. Plugin List:")
    plugins = plugin_api.call_endpoint("list_plugins")
    for plugin in plugins:
        print(f"   - {plugin['manifest']['name']} v{plugin['manifest']['version']}")
        print(f"     Type: {plugin['manifest']['plugin_type']}")
        print(f"     Status: {plugin['status']}")

    # Test plugin execution
    print("\n2. Plugin Execution:")

    # Test visualization plugin
    test_data = [1, 2, 3, 4, 5]
    viz_result = plugin_api.call_endpoint("execute_plugin", "viz_example", test_data)
    print(f"   Visualization result: {viz_result}")

    # Test analysis plugin
    analysis_result = plugin_api.call_endpoint(
        "execute_plugin", "analysis_example", test_data
    )
    print(f"   Analysis result: {analysis_result}")

    # Test plugin validation
    print("\n3. Plugin Validation:")
    validator = PluginValidator()

    # Create test plugin code
    test_plugin_code = """
import numpy as np
import pandas as pd


class TestPlugin:
    def analyze(self, data):
        return {"result": len(data)}
"""

    # Write test plugin
    test_plugin_path = Path("test_plugin.py")
    with open(test_plugin_path, "w") as f:
        f.write(test_plugin_code)

    is_valid, errors = validator.validate_plugin(test_plugin_path)
    print(f"   Plugin validation: {'Valid' if is_valid else 'Invalid'}")
    if errors:
        print(f"   Errors: {errors}")

    # Cleanup
    test_plugin_path.unlink()

    # Test event system
    print("\n4. Event System:")

    def on_plugin_event(data):
        print(f"   Event received: {data}")

    plugin_manager.register_event_handler("test_event", on_plugin_event)
    plugin_manager.emit_event("test_event", "Hello from plugin system!")

    # Test active plugins
    print("\n5. Active Plugins:")
    active_plugins = plugin_api.call_endpoint("get_active_plugins")
    for plugin_id in active_plugins:
        print(f"   - {plugin_id}")

    print("\nPlugin Architecture Demo Complete!")
    return {
        "plugin_manager": plugin_manager,
        "plugin_api": plugin_api,
        "plugins_loaded": len(active_plugins),
    }


if __name__ == "__main__":
    demo_plugin_architecture()
