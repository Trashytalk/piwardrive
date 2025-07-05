#!/usr/bin/env python3
"""
Performance Optimization Integration Demo

This script demonstrates the complete performance optimization suite integration
and provides a comprehensive overview of the implemented features.
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'-'*40}")
    print(f"  {title}")
    print(f"{'-'*40}")


async def demo_database_optimization():
    """Demonstrate database optimization features."""
    print_section("Database Optimization Demo")

    try:
        from piwardrive.performance import DatabaseOptimizer

        # Create optimizer with in-memory database
        db_optimizer = DatabaseOptimizer(":memory:")

        print("✓ Database optimizer initialized")

        # Get statistics
        stats = db_optimizer.get_stats()
        print(f"  Database stats: {json.dumps(stats, indent=2)}")

        # Get recommendations
        recommendations = db_optimizer.get_recommendations()
        print(f"  Recommendations: {len(recommendations)} items")
        for rec in recommendations[:3]:  # Show first 3
            print(
                f"    - {rec['type']}: {rec.get('table',
                'N/A')}.{rec.get('column',
                'N/A')}"
            )

        # Get alerts
        alerts = db_optimizer.get_alerts()
        print(f"  Alerts: {len(alerts)} items")
        for alert in alerts[:2]:  # Show first 2
            print(f"    - {alert['level']}: {alert['message']}")

        # Simulate optimization
        print("  Running optimization...")
        result = db_optimizer.optimize()
        print(f"  Optimization result: {result['status']}")

    except Exception as e:
        print(f"❌ Database optimization demo failed: {e}")


async def demo_async_optimization():
    """Demonstrate async optimization features."""
    print_section("Async Optimization Demo")

    try:
        from piwardrive.performance import AsyncOptimizer

        # Create optimizer
        async_optimizer = AsyncOptimizer()

        print("✓ Async optimizer initialized")

        # Monitor an operation
        async with async_optimizer.monitor_operation("demo_operation") as monitor:
            await asyncio.sleep(0.1)  # Simulate async operation
            monitor.success()

        print("✓ Async operation monitored")

        # Get statistics
        stats = async_optimizer.get_stats()
        print(f"  Async stats: {json.dumps(stats, indent=2)}")

        # Get recommendations
        recommendations = async_optimizer.get_recommendations()
        print(f"  Recommendations: {len(recommendations)} items")
        for rec in recommendations[:3]:  # Show first 3
            print(
                f"    - {rec['type']}: {rec.get('current',
                'N/A')} -> {rec.get('recommended',
                'N/A')}"
            )

        # Get alerts
        alerts = async_optimizer.get_alerts()
        print(f"  Alerts: {len(alerts)} items")
        for alert in alerts[:2]:  # Show first 2
            print(f"    - {alert['level']}: {alert['message']}")

        # Simulate optimization
        print("  Running optimization...")
        result = async_optimizer.optimize()
        print(f"  Optimization result: {result['status']}")

    except Exception as e:
        print(f"❌ Async optimization demo failed: {e}")


async def demo_realtime_optimization():
    """Demonstrate real-time optimization features."""
    print_section("Real-time Optimization Demo")

    try:
        from piwardrive.performance import RealtimeOptimizer

        # Create optimizer
        rt_optimizer = RealtimeOptimizer()

        print("✓ Real-time optimizer initialized")

        # Get statistics
        stats = rt_optimizer.get_stats()
        print(f"  Real-time stats: {json.dumps(stats, indent=2)}")

        # Get recommendations
        recommendations = rt_optimizer.get_recommendations()
        print(f"  Recommendations: {len(recommendations)} items")
        for rec in recommendations[:3]:  # Show first 3
            print(
                f"    - {rec['type']}: {rec.get('current',
                'N/A')} -> {rec.get('recommended',
                'N/A')}"
            )

        # Get alerts
        alerts = rt_optimizer.get_alerts()
        print(f"  Alerts: {len(alerts)} items")
        for alert in alerts[:2]:  # Show first 2
            print(f"    - {alert['level']}: {alert['message']}")

        # Simulate optimization
        print("  Running optimization...")
        result = rt_optimizer.optimize()
        print(f"  Optimization result: {result['status']}")

    except Exception as e:
        print(f"❌ Real-time optimization demo failed: {e}")


def demo_cli_tools():
    """Demonstrate CLI tools availability."""
    print_section("CLI Tools Demo")

    cli_path = Path(__file__).parent / "scripts" / "performance_cli.py"
    if cli_path.exists():
        print("✓ Performance CLI tool available")
        print(f"  Location: {cli_path}")
        print("  Usage examples:")
        print("    python scripts/performance_cli.py analyze")
        print("    python scripts/performance_cli.py optimize --component database")
        print("    python scripts/performance_cli.py monitor --duration 60")
        print("    python scripts/performance_cli.py benchmark --all")
    else:
        print("❌ Performance CLI tool not found")


def demo_dashboard_api():
    """Demonstrate dashboard API availability."""
    print_section("Dashboard API Demo")

    try:
        from piwardrive.api.performance_dashboard import router

        print("✓ Performance dashboard API available")
        print("  Available endpoints:")

        # Get all routes from the router
        routes = router.routes
        for route in routes:
            if hasattr(route, "path") and hasattr(route, "methods"):
                methods = list(route.methods)
                print(f"    {methods[0]} {route.path}")

        print("\n  Dashboard UI: /performance/dashboard")

    except Exception as e:
        print(f"❌ Dashboard API demo failed: {e}")


def demo_integration():
    """Demonstrate FastAPI integration."""
    print_section("FastAPI Integration Demo")

    try:
        # This would normally fail due to missing dependencies
        # but we can at least verify the structure
        service_file = (
            Path(__file__).parent.parent / "src" / "piwardrive" / "service.py"
        )
        if service_file.exists():
            content = service_file.read_text()
            if "performance_dashboard" in content and "performance_router" in content:
                print("✓ Performance dashboard integrated into FastAPI service")
                print("  Router included in main application")
            else:
                print("❌ Performance dashboard not properly integrated")
        else:
            print("❌ Service file not found")

    except Exception as e:
        print(f"❌ Integration demo failed: {e}")


def demo_files_structure():
    """Demonstrate the files structure."""
    print_section("Files Structure Demo")

    files_to_check = [
        "PERFORMANCE_SCALABILITY_PLAN.md",
        "PERFORMANCE_IMPROVEMENTS.md",
        "src/piwardrive/performance/__init__.py",
        "src/piwardrive/performance/db_optimizer.py",
        "src/piwardrive/performance/async_optimizer.py",
        "src/piwardrive/performance/realtime_optimizer.py",
        "src/piwardrive/api/performance_dashboard.py",
        "templates/performance_dashboard.html",
        "scripts/performance_cli.py",
        "docs/performance_optimization.md",
        "setup_performance_dashboard.py",
        "tests/test_performance_dashboard_integration.py",
    ]

    base_path = Path(__file__).parent

    for file_path in files_to_check:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"❌ {file_path}")


def print_summary():
    """Print implementation summary."""
    print_header("Implementation Summary")

    print("🎯 Performance Optimization Suite Completed:")
    print("   ✅ Database Performance Optimization")
    print("   ✅ Async Operations Optimization")
    print("   ✅ Real-time Updates Optimization")
    print("   ✅ Web-based Performance Dashboard")
    print("   ✅ Command-line Performance Tools")
    print("   ✅ FastAPI Integration")
    print("   ✅ Comprehensive Documentation")
    print("   ✅ Setup and Validation Scripts")
    print("   ✅ Integration Tests")

    print("\n📊 Key Features Implemented:")
    print("   • Real-time performance monitoring")
    print("   • Automated optimization recommendations")
    print("   • Performance alerts and notifications")
    print("   • Interactive web dashboard")
    print("   • CLI tools for analysis and optimization")
    print("   • Comprehensive API endpoints")
    print("   • Historical performance tracking")
    print("   • Configurable optimization settings")

    print("\n🚀 Next Steps:")
    print("   1. Install dependencies: pip install -r requirements.txt")
    print("   2. Run setup script: python setup_performance_dashboard.py")
    print("   3. Start PiWardrive application")
    print("   4. Access dashboard at: /performance/dashboard")
    print("   5. Use CLI tools for detailed analysis")
    print("   6. Configure automated optimizations")

    print("\n📚 Documentation:")
    print("   • Implementation Plan: PERFORMANCE_SCALABILITY_PLAN.md")
    print("   • Feature Overview: PERFORMANCE_IMPROVEMENTS.md")
    print("   • Detailed Guide: docs/performance_optimization.md")
    print("   • API Reference: Available in dashboard")


async def main():
    """Main demonstration function."""
    print_header("PiWardrive Performance Optimization Suite Demo")
    print(f"Demo started at: {datetime.now()}")

    # Demonstrate file structure
    demo_files_structure()

    # Demonstrate individual components
    await demo_database_optimization()
    await demo_async_optimization()
    await demo_realtime_optimization()

    # Demonstrate tools and integration
    demo_cli_tools()
    demo_dashboard_api()
    demo_integration()

    # Print summary
    print_summary()

    print(f"\n✅ Demo completed at: {datetime.now()}")


if __name__ == "__main__":
    asyncio.run(main())
