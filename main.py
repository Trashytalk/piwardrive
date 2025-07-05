"""
PiWardrive - Main Application Entry Point

This is the main entry point for the PiWardrive Advanced Wireless Intelligence Platform.
It initializes the unified platform and starts all core services.

Usage:
    python main.py                    # Start with default configuration
    python main.py --config custom.yaml  # Start with custom configuration
    python main.py --help            # Show help message

Author: PiWardrive Development Team
License: MIT
"""

from __future__ import annotations

import argparse
import os
import sys

# Add src directory to path
SRC_PATH = os.path.join(os.path.dirname(__file__), "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

try:
    from piwardrive.unified_platform import PiWardriveUnifiedPlatform

    # Legacy support - handle potential import errors gracefully
    try:
        from piwardrive.main import PiWardriveApp
    except ImportError:
        PiWardriveApp = None
except ImportError as e:
    print(f"Error importing PiWardrive modules: {e}")
    print("Please ensure all dependencies are installed:")
    print("pip install -r config/requirements.txt")
    sys.exit(1)

__version__ = "2.0.0"
__author__ = "PiWardrive Development Team"


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="PiWardrive Advanced Wireless Intelligence Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py                           # Start with default settings
    python main.py --config custom.yaml     # Use custom configuration
    python main.py --port 8080             # Set custom API port
    python main.py --dashboard-port 8081   # Set custom dashboard port
    python main.py --debug                 # Enable debug mode
    python main.py --legacy                # Use legacy interface
        """,
    )

    parser.add_argument(
        "--version", action="version", version=f"PiWardrive {__version__}"
    )

    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file (default: config/piwardrive_config.yaml)",
    )

    parser.add_argument(
        "--port", type=int, default=8080, help="API server port (default: 8080)"
    )

    parser.add_argument(
        "--dashboard-port",
        type=int,
        default=8081,
        help="Dashboard server port (default: 8081)",
    )

    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    parser.add_argument(
        "--legacy", action="store_true", help="Use legacy PiWardrive interface"
    )

    return parser.parse_args()


def setup_configuration(config_path: str | None = None) -> str:
    """Setup configuration file path"""
    if config_path:
        if os.path.exists(config_path):
            return config_path
        else:
            print(f"Configuration file not found: {config_path}")
            sys.exit(1)

    # Default configuration paths
    default_configs = [
        "config/piwardrive_config.yaml",
        "piwardrive_config.yaml",
        "config.yaml",
    ]

    for config_file in default_configs:
        if os.path.exists(config_file):
            return config_file

    print("No configuration file found. Creating default configuration...")

    # Create default configuration
    default_config = """
system_name: PiWardrive
version: 2.0.0
environment: development
debug_mode: false
api_port: 8080
dashboard_port: 8081
max_threads: 10
data_retention_days: 30
auto_backup: true

modules:
  threat_detection:
    enabled: true
    sensitivity: high
    update_interval: 300

  rf_spectrum:
    enabled: true
    frequency_range: [2400, 5800]
    resolution: high

  geospatial:
    enabled: true
    positioning_method: trilateration
    accuracy_threshold: 5.0

integrations:
  siem:
    enabled: false
    endpoint: https://siem.example.com/api
    api_key: your_api_key_here

  monitoring:
    enabled: true
    prometheus_port: 9090
    grafana_port: 3000
"""

    os.makedirs("config", exist_ok=True)
    with open("config/piwardrive_config.yaml", "w") as f:
        f.write(default_config)

    print("Default configuration created: config/piwardrive_config.yaml")
    return "config/piwardrive_config.yaml"


def main():
    """Main application entry point"""
    print(f"PiWardrive Advanced Wireless Intelligence Platform v{__version__}")
    print("=" * 60)

    # Parse command line arguments
    args = parse_arguments()

    # Setup configuration
    config_path = setup_configuration(args.config)
    print(f"Using configuration: {config_path}")

    try:
        if args.legacy:
            # Use legacy interface
            if PiWardriveApp is None:
                print("Legacy interface not available. Using unified platform instead.")
                args.legacy = False
            else:
                print("Starting legacy PiWardrive interface...")
                app = PiWardriveApp()
                # Start the app (method name may vary)
                start_method = getattr(app, "run", None) or getattr(app, "start", None)
                if start_method:
                    start_method()
                else:
                    print("Legacy app start method not found. Using unified platform.")
                    args.legacy = False

        if not args.legacy:
            # Use unified platform
            print("Starting PiWardrive Unified Platform...")
            print(f"API Server: http://localhost:{args.port}")
            print(f"Dashboard: http://localhost:{args.dashboard_port}")
            print("Press Ctrl+C to stop")

            # Initialize platform
            platform = PiWardriveUnifiedPlatform(config_path)

            # Update configuration with command line args
            platform.config.api_port = args.port
            platform.config.dashboard_port = args.dashboard_port
            platform.config.debug_mode = args.debug

            # Start the platform
            platform.start()

    except KeyboardInterrupt:
        print("\nShutting down PiWardrive...")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting PiWardrive: {e}")
        if args.debug:
            import traceback

            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
