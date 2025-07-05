"""
Performance monitoring dashboard for PiWardrive.

This module provides a web-based dashboard for monitoring and visualizing
database, async, and real-time performance metrics.
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from piwardrive.api.auth import AUTH_DEP
from piwardrive.performance.async_optimizer import get_global_monitor
from piwardrive.performance.db_optimizer import (
    DatabaseOptimizer,
    run_performance_analysis,
)
from piwardrive.performance.realtime_optimizer import get_global_optimizer

router = APIRouter(prefix="/performance", tags=["performance"])

# Templates directory - adjust path as needed
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def performance_dashboard(request: Request, _auth: Any = Depends(AUTH_DEP)):
    """Serve the performance monitoring dashboard."""
    return templates.TemplateResponse(
        "performance_dashboard.html",
        {"request": request, "title": "Performance Dashboard"},
    )

@router.get("/api/database/stats")
async def get_database_stats(
    db_path: Optional[str] = None, _auth: Any = Depends(AUTH_DEP)
):
    """Get database performance statistics."""
    if not db_path:
        # Try to get default database path
        try:
            from piwardrive.core.persistence import _db_path

            db_path = _db_path()
        except Exception:
            return JSONResponse(
                {"error": "Database path not specified"}, status_code=400
            )

    try:
        optimizer = DatabaseOptimizer(db_path)

        # Get basic stats
        table_stats = await optimizer.get_table_stats()
        query_analysis = await optimizer.analyze_query_performance()
        missing_indexes = await optimizer.analyze_missing_indexes()

        return {
            "timestamp": time.time(),
            "database_path": db_path,
            "table_stats": table_stats,
            "query_analysis": query_analysis,
            "missing_indexes": [
                {
                    "table": idx.table,
                    "columns": idx.columns,
                    "reason": idx.reason,
                    "benefit": idx.estimated_benefit,
                }
                for idx in missing_indexes
            ],
            "summary": {
                "total_tables": len(table_stats),
                "total_rows": sum(stats["row_count"] for stats in table_stats.values()),
                "total_size_mb": sum(
                    stats["size_mb"] for stats in table_stats.values()
                ),
                "missing_indexes_count": len(missing_indexes),
            },
        }

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@router.get("/api/async/stats")
async def get_async_stats(_auth: Any = Depends(AUTH_DEP)):
    """Get async performance statistics."""
    try:
        monitor = get_global_monitor()
        summary = monitor.get_performance_summary()

        return {"timestamp": time.time(), "performance_summary": summary}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@router.get("/api/realtime/stats")
async def get_realtime_stats(_auth: Any = Depends(AUTH_DEP)):
    """Get real-time update performance statistics."""
    try:
        optimizer = get_global_optimizer()
        stats = optimizer.get_performance_stats()

        return {"timestamp": time.time(), "realtime_stats": stats}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@router.get("/api/comprehensive")
async def get_comprehensive_stats(
    db_path: Optional[str] = None, _auth: Any = Depends(AUTH_DEP)
):
    """Get comprehensive performance statistics."""
    if not db_path:
        try:
            from piwardrive.core.persistence import _db_path

            db_path = _db_path()
        except Exception:
            db_path = None

    stats = {"timestamp": time.time(), "collection_time": datetime.now().isoformat()}

    # Database stats
    if db_path:
        try:
            optimizer = DatabaseOptimizer(db_path)
            _tablestats = await optimizer.get_table_stats()

            stats["database"] = {
                "table_count": len(table_stats),
                "total_rows": sum(stats["row_count"] for stats in table_stats.values()),
                "total_size_mb": sum(
                    stats["size_mb"] for stats in table_stats.values()
                ),
                "tables": table_stats,
            }
        except Exception as e:
            stats["database"] = {"error": str(e)}

    # Async stats
    try:
        monitor = get_global_monitor()
        async_summary = monitor.get_performance_summary()
        stats["async"] = async_summary
    except Exception as e:
        stats["async"] = {"error": str(e)}

    # Real-time stats
    try:
        optimizer = get_global_optimizer()
        _realtimestats = optimizer.get_performance_stats()
        stats["realtime"] = realtime_stats
    except Exception as e:
        stats["realtime"] = {"error": str(e)}

    return stats

@router.post("/api/database/optimize")
async def optimize_database(
    db_path: Optional[str] = None,
    create_indexes: bool = True,
    _auth: Any = Depends(AUTH_DEP),
):
    """Optimize database performance."""
    if not db_path:
        try:
            from piwardrive.core.persistence import _db_path

            db_path = _db_path()
        except Exception:
            return JSONResponse(
                {"error": "Database path not specified"}, status_code=400
            )

    try:
        from piwardrive.performance.db_optimizer import apply_performance_optimizations

        results = await apply_performance_optimizations(db_path, create_indexes)

        return {
            "timestamp": time.time(),
            "optimization_results": results,
            "success": True,
        }

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@router.get("/api/performance/history")
async def get_performance_history(hours: int = 24, _auth: Any = Depends(AUTH_DEP)):
    """Get performance metrics history."""
    # This would require implementing performance data storage
    # For now, return sample data structure

    end_time = datetime.now()
    start_time = end_time - timedelta(hours=hours)

    # Generate sample historical data
    history = {
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "interval_minutes": 5,
        "metrics": {
            "database_query_time": [],
            "async_operations_per_second": [],
            "websocket_connections": [],
            "sse_streams": [],
            "memory_usage_mb": [],
            "cpu_usage_percent": [],
        },
    }

    # Generate sample data points
    current_time = start_time
    while current_time < end_time:
        timestamp = current_time.isoformat()

        # Sample metrics (in real implementation, this would come from stored data)
        history["metrics"]["database_query_time"].append(
            {
                "timestamp": timestamp,
                "value": 50 + (hash(timestamp) % 100),  # Sample data
            }
        )

        history["metrics"]["async_operations_per_second"].append(
            {"timestamp": timestamp, "value": 100 + (hash(timestamp) % 200)}
        )

        history["metrics"]["websocket_connections"].append(
            {"timestamp": timestamp, "value": max(0, 10 + (hash(timestamp) % 50))}
        )

        current_time += timedelta(minutes=5)

    return history

@router.get("/api/performance/alerts")
async def get_performance_alerts(_auth: Any = Depends(AUTH_DEP)):
    """Get performance alerts and recommendations."""
    alerts = []

    try:
        # Check async performance
        monitor = get_global_monitor()
        async_summary = monitor.get_performance_summary()

        if "slow_operations" in async_summary and async_summary["slow_operations"] > 10:
            alerts.append(
                {
                    "type": "warning",
                    "category": "async",
                    "message": f"High number of slow operations: {async_summary['slow_operations']}",
                        
                    "recommendation": "Review async operation performance and consider optimization",
                        
                }
            )

        # Check real-time performance
        optimizer = get_global_optimizer()
        realtime_stats = optimizer.get_performance_stats()

        ws_stats = realtime_stats.get("websocket_stats", {})
        if ws_stats.get("errors", 0) > 100:
            alerts.append(
                {
                    "type": "error",
                    "category": "websocket",
                    "message": f"High WebSocket error count: {ws_stats['errors']}",
                    "recommendation": "Check WebSocket connection stability and error handling",
                        
                }
            )

        # Check database performance (if available)
        try:
            from piwardrive.core.persistence import _db_path

            db_path = _db_path()

            db_optimizer = DatabaseOptimizer(db_path)
            missing_indexes = await db_optimizer.analyze_missing_indexes()

            if len(missing_indexes) > 5:
                alerts.append(
                    {
                        "type": "info",
                        "category": "database",
                        "message": f"Multiple missing indexes detected: {len(missing_indexes)}",
                            
                        "recommendation": "Consider creating recommended indexes to improve query performance",
                            
                    }
                )

        except Exception:
            pass  # Database not available

    except Exception as e:
        alerts.append(
            {
                "type": "error",
                "category": "monitoring",
                "message": f"Error collecting performance data: {str(e)}",
                "recommendation": "Check performance monitoring system configuration",
            }
        )

    return {"timestamp": time.time(), "alerts": alerts, "alert_count": len(alerts)}

@router.get("/api/performance/recommendations")
async def get_performance_recommendations(
    db_path: Optional[str] = None, _auth: Any = Depends(AUTH_DEP)
):
    """Get performance optimization recommendations."""
    recommendations = []

    # Database recommendations
    if not db_path:
        try:
            from piwardrive.core.persistence import _db_path

            db_path = _db_path()
        except Exception:
            db_path = None

    if db_path:
        try:
            optimizer = DatabaseOptimizer(db_path)
            missing_indexes = await optimizer.analyze_missing_indexes()
            table_stats = await optimizer.get_table_stats()

            if missing_indexes:
                recommendations.append(
                    {
                        "category": "database",
                        "priority": "high",
                        "title": "Create Missing Indexes",
                        "description": f"Found {len(missing_indexes)} missing indexes that could improve query performance",
                            
                        "action": "Run database optimization to create recommended indexes",
                            
                        "estimated_impact": "20-50% query performance improvement",
                    }
                )

            # Check for large tables without recent vacuum
            large_tables = [
                name for name, stats in table_stats.items() if stats["size_mb"] > 100
            ]
            if large_tables:
                recommendations.append(
                    {
                        "category": "database",
                        "priority": "medium",
                        "title": "Vacuum Large Tables",
                        "description": f"Found {len(large_tables)} large tables that may benefit from VACUUM",
                            
                        "action": "Run VACUUM on large tables to reclaim space and improve performance",
                            
                        "estimated_impact": "10-30% space reduction,
                            improved query performance",
                            
                    }
                )

        except Exception:
            pass  # Database recommendations not available

    # Async recommendations
    try:
        monitor = get_global_monitor()
        async_summary = monitor.get_performance_summary()

        if "operation_summary" in async_summary:
            slow_operations = [
                op
                for op, stats in async_summary["operation_summary"].items()
                if stats.get("avg_time", 0) > 0.1  # 100ms
            ]

            if slow_operations:
                recommendations.append(
                    {
                        "category": "async",
                        "priority": "medium",
                        "title": "Optimize Slow Async Operations",
                        "description": f"Found {len(slow_operations)} operations with high average execution time",
                            
                        "action": "Review and optimize slow async operations: "
                        + ", ".join(slow_operations[:3]),
                        "estimated_impact": "Improved application responsiveness",
                    }
                )

    except Exception:
        pass  # Async recommendations not available

    # Real-time recommendations
    try:
        optimizer = get_global_optimizer()
        realtime_stats = optimizer.get_performance_stats()

        ws_stats = realtime_stats.get("websocket_stats", {})
        if ws_stats.get("active_connections", 0) > 500:
            recommendations.append(
                {
                    "category": "realtime",
                    "priority": "high",
                    "title": "High WebSocket Connection Count",
                    "description": f"Currently handling {ws_stats['active_connections']} WebSocket connections",
                        
                    "action": "Consider implementing connection pooling or load balancing",
                        
                    "estimated_impact": "Improved connection stability and resource usage",
                        
                }
            )

    except Exception:
        pass  # Real-time recommendations not available

    # General recommendations
    recommendations.append(
        {
            "category": "general",
            "priority": "low",
            "title": "Enable Performance Monitoring",
            "description": "Set up continuous performance monitoring and alerting",
            "action": "Configure automated performance alerts and regular optimization tasks",
                
            "estimated_impact": "Proactive performance issue detection and resolution",
        }
    )

    return {
        "timestamp": time.time(),
        "recommendations": recommendations,
        "recommendation_count": len(recommendations),
    }

# WebSocket endpoint for real-time performance updates
@router.websocket("/ws/performance")
async def performance_websocket(websocket):
    """WebSocket endpoint for real-time performance updates."""
    await websocket.accept()

    try:
        while True:
            # Collect current performance data
            stats = await get_comprehensive_stats()

            # Send updates to client
            await websocket.send_json(
                {"type": "performance_update", "timestamp": time.time(), "data": stats}
            )

            # Wait before next update
            await asyncio.sleep(5)  # Update every 5 seconds

    except Exception as e:
        print(f"Performance WebSocket error: {e}")
    finally:
        await websocket.close()

# Include the router in your main application:
# app.include_router(router)
