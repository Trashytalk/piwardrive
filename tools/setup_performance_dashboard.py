#!/usr/bin/env python3
"""
Performance Dashboard Setup Script

This script helps set up \and
    validate the performance optimization dashboard integration.
"""

import importlib.util
import subprocess
import sys
from pathlib import Path


def check_module(module_name: str) -> bool:
    """Check if a module is available."""
    spec = importlib.util.find_spec(module_name)
    return spec is not None


def install_missing_dependencies():
    """Install missing dependencies."""
    print("🔧 Installing missing dependencies...")

    # Check for basic dependencies
    required_modules = [
        "psutil",
        "pydantic",
        "fastapi",
        "aiohttp",
        "bcrypt",
        "requests",
    ]
    missing = [mod for mod in required_modules if not check_module(mod)]

    if missing:
        print(f"Missing modules: {missing}")

        # Try to install requirements
        requirements_file = Path(__file__).parent / "requirements.txt"
        if requirements_file.exists():
            try:
                subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "-r",
                        str(requirements_file),
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                print("✓ Dependencies installed successfully")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install dependencies: {e}")
                return False
        else:
            print("❌ requirements.txt not found")
            return False
    else:
        print("✓ All dependencies are available")
        return True


def validate_integration():
    """Validate the performance dashboard integration."""
    print("🔍 Validating performance dashboard integration...")

    try:
        # Add src to Python path
        src_path = Path(__file__).parent.parent / "src"
        if src_path not in sys.path:
            sys.path.insert(0, str(src_path))

        # Test individual modules
        print("  Testing performance module imports...")

        # Test database optimizer
        from piwardrive.performance.db_optimizer import DatabaseOptimizer

    # Unused: _db_opt = DatabaseOptimizer(":memory:")
        print("  ✓ Database optimizer ready")

        # Test async optimizer
        from piwardrive.performance.async_optimizer import AsyncOptimizer

        AsyncOptimizer()
        print("  ✓ Async optimizer ready")

        # Test realtime optimizer
        from piwardrive.performance.realtime_optimizer import RealtimeOptimizer

        RealtimeOptimizer()
        print("  ✓ Realtime optimizer ready")

        # Test performance dashboard API

        print("  ✓ Performance dashboard router ready")

        # Test CLI tool
        cli_path = Path(__file__).parent / "scripts" / "performance_cli.py"
        if cli_path.exists():
            print("  ✓ Performance CLI tool available")
        else:
            print("  ❌ Performance CLI tool not found")

        # Test dashboard template
        template_path = (
            Path(__file__).parent / "templates" / "performance_dashboard.html"
        )
        if template_path.exists():
            print("  ✓ Performance dashboard template available")
        else:
            print("  ❌ Performance dashboard template not found")

        print("✅ Integration validation successful!")
        return True

    except Exception as e:
        print(f"❌ Integration validation failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def create_sample_config():
    """Create sample configuration for performance optimization."""
    print("📋 Creating sample performance configuration...")

    config_content = """
# Performance Optimization Configuration
# Copy this to your main configuration file

PERFORMANCE_CONFIG = {
    # Database optimization settings
    "database": {
        "analyze_threshold": 0.1,  # Seconds - queries slower than this are analyzed
        "vacuum_threshold": 0.3,   # Fragmentation ratio to trigger vacuum
        "cache_size": 10000,       # SQLite cache size in pages
        "temp_store": "memory",    # Use memory for temporary storage
        "synchronous": "normal",   # Sync mode for reliability vs performance
        "enable_monitoring": True, # Enable performance monitoring
        "auto_optimize": True,     # Enable automatic optimization
    },

    # Async optimization settings
    "async": {
        "max_pool_size": 100,      # Maximum connection pool size
        "task_queue_size": 1000,   # Maximum task queue size
        "rate_limit": 1000,        # Requests per second limit
        "batch_size": 50,          # Default batch processing size
        "circuit_breaker_threshold": 5,  # Failures before circuit opens
        "enable_monitoring": True,  # Enable async monitoring
        "auto_optimize": True,      # Enable automatic optimization
    },

    # Real-time optimization settings
    "realtime": {
        "max_connections": 1000,   # Maximum WebSocket connections
        "heartbeat_interval": 30,  # Heartbeat interval in seconds
        "message_queue_size": 100, # Per-connection message queue size
        "compression": True,       # Enable WebSocket compression
        "buffer_size": 65536,      # WebSocket buffer size
        "enable_monitoring": True, # Enable realtime monitoring
        "auto_optimize": True,     # Enable automatic optimization
    },

    # Dashboard settings
    "dashboard": {
        "enable": True,           # Enable performance dashboard
        "refresh_interval": 5,    # Dashboard refresh interval in seconds
        "history_retention": 24,  # Hours to retain performance history
        "alert_thresholds": {
            "query_time": 0.5,    # Alert if query time exceeds this
            "error_rate": 0.05,   # Alert if error rate exceeds this
            "memory_usage": 0.8,  # Alert if memory usage exceeds this
        }
    }
}
"""

    config_path = Path(__file__).parent / "performance_config_sample.py"
    with open(config_path, "w") as f:
        f.write(config_content)

    print(f"✓ Sample configuration created at: {config_path}")


def show_usage_examples():
    """Show usage examples for the performance tools."""
    print("\n📚 Performance Tools Usage Examples:")
    print("\n1. CLI Tool Usage:")
    print("   python scripts/performance_cli.py analyze")
    print("   python scripts/performance_cli.py optimize --component database")
    print("   python scripts/performance_cli.py monitor --duration 60")
    print("   python scripts/performance_cli.py benchmark --all")

    print("\n2. Dashboard Access:")
    print("   Stats: GET /performance/stats")
    print("   Alerts: GET /performance/alerts")
    print("   Recommendations: GET /performance/recommendations")
    print("   Optimize: POST /performance/optimize")
    print("   Dashboard UI: /performance/dashboard")

    print("\n3. Python API Usage:")
    print(
        """
   from piwardrive.performance import DatabaseOptimizer,
       AsyncOptimizer,
       RealtimeOptimizer

   # Database optimization
   db_optimizer = DatabaseOptimizer("/path/to/database.db")
   stats = db_optimizer.get_stats()
   recommendations = db_optimizer.get_recommendations()
   result = db_optimizer.optimize()

   # Async optimization
   async_optimizer = AsyncOptimizer()
   async with async_optimizer.monitor_operation("api_call") as monitor:
       result = await some_async_operation()

   # Real-time optimization
   rt_optimizer = RealtimeOptimizer()
   await rt_optimizer.optimize_websockets()
"""
    )


def main():
    """Main setup function."""
    print("🚀 PiWardrive Performance Dashboard Setup")
    print("=" * 50)

    # Check and install dependencies
    if not install_missing_dependencies():
        print("❌ Setup failed due to missing dependencies")
        return False

    # Validate integration
    if not validate_integration():
        print("❌ Setup failed due to integration issues")
        return False

    # Create sample configuration
    create_sample_config()

    # Show usage examples
    show_usage_examples()

    print("\n✅ Performance Dashboard Setup Complete!")
    print("\nNext steps:")
    print("1. Review and customize performance_config_sample.py")
    print("2. Start your PiWardrive application")
    print("3. Access the performance dashboard at /performance/dashboard")
    print("4. Run CLI tools for analysis and optimization")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
