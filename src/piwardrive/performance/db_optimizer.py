"""
Database performance optimization utilities for PiWardrive.

This module provides tools for optimizing SQLite and PostgreSQL performance,
including query analysis, index recommendations, and connection monitoring.
"""

import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import aiosqlite

logger = logging.getLogger(__name__)


@dataclass
class QueryMetrics:
    """Metrics for database query performance."""

    query: str
    execution_time: float
    row_count: int
    timestamp: float

    @property
    def is_slow(self) -> bool:
        """Check if query is considered slow (>100ms)."""
        return self.execution_time > 0.1


@dataclass
class IndexRecommendation:
    """Recommendation for database index creation."""

    table: str
    columns: List[str]
    reason: str
    estimated_benefit: str

    @property
    def create_sql(self) -> str:
        """Generate SQL for creating the recommended index."""
        index_name = f"idx_{self.table}_{'_'.join(self.columns)}"
        columns_str = ", ".join(self.columns)
        return f"CREATE INDEX IF NOT EXISTS {index_name} ON {self.table}({columns_str})"


class DatabaseOptimizer:
    """Database performance optimization and monitoring."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.query_metrics: List[QueryMetrics] = []
        self.max_metrics = 10000  # Keep last 10k queries

    async def analyze_query_performance(self, days: int = 7) -> Dict[str, Any]:
        """Analyze query performance over the specified period."""
        cutoff_time = time.time() - (days * 24 * 3600)
        recent_metrics = [m for m in self.query_metrics if m.timestamp > cutoff_time]

        if not recent_metrics:
            return {"message": "No recent query data available"}

        slow_queries = [m for m in recent_metrics if m.is_slow]

        analysis = {
            "total_queries": len(recent_metrics),
            "slow_queries": len(slow_queries),
            "slow_query_percentage": (len(slow_queries) / len(recent_metrics)) * 100,
            "average_execution_time": sum(m.execution_time for m in recent_metrics)
            / len(recent_metrics),
            "slowest_queries": sorted(
                slow_queries, key=lambda x: x.execution_time, reverse=True
            )[:10],
        }

        return analysis

    async def get_table_stats(self) -> Dict[str, Any]:
        """Get table statistics for performance analysis."""
        stats = {}

        async with aiosqlite.connect(self.db_path) as db:
            # Get table sizes
            cursor = await db.execute(
                """
                SELECT name, sql FROM sqlite_master
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """
            )
            tables = await cursor.fetchall()

            for table_name, create_sql in tables:
                # Get row count
                cursor = await db.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = (await cursor.fetchone())[0]

                # Get table size (approximate)
                cursor = await db.execute(
                    f"SELECT SUM(pgsize) FROM dbstat WHERE name='{table_name}'"
                )
                size_result = await cursor.fetchone()
                size_bytes = size_result[0] if size_result and size_result[0] else 0

                stats[table_name] = {
                    "row_count": row_count,
                    "size_bytes": size_bytes,
                    "size_mb": size_bytes / (1024 * 1024) if size_bytes else 0,
                    "create_sql": create_sql,
                }

        return stats

    async def analyze_missing_indexes(self) -> List[IndexRecommendation]:
        """Analyze query patterns and recommend missing indexes."""
        recommendations = []

        # Common patterns that benefit from indexes
        patterns = [
            # WiFi detection queries
            {
                "table": "wifi_detections",
                "columns": ["scan_session_id", "detection_timestamp"],
                "reason": "Frequent queries by session and time range",
                "benefit": "Faster session-based queries",
            },
            {
                "table": "wifi_detections",
                "columns": ["bssid", "signal_strength_dbm"],
                "reason": "BSSID lookups with signal filtering",
                "benefit": "Faster access point analysis",
            },
            {
                "table": "wifi_detections",
                "columns": ["latitude", "longitude"],
                "reason": "Location-based queries",
                "benefit": "Faster geographic queries",
            },
            # Bluetooth detection queries
            {
                "table": "bluetooth_detections",
                "columns": ["scan_session_id", "detection_timestamp"],
                "reason": "Session-based Bluetooth queries",
                "benefit": "Faster session analysis",
            },
            {
                "table": "bluetooth_detections",
                "columns": ["mac_address", "rssi_dbm"],
                "reason": "MAC address lookups with signal filtering",
                "benefit": "Faster device analysis",
            },
            # GPS track queries
            {
                "table": "gps_tracks",
                "columns": ["scan_session_id", "timestamp"],
                "reason": "GPS track queries by session",
                "benefit": "Faster location tracking",
            },
            {
                "table": "gps_tracks",
                "columns": ["latitude", "longitude"],
                "reason": "Spatial queries on GPS data",
                "benefit": "Faster geographic analysis",
            },
            # Scan session queries
            {
                "table": "scan_sessions",
                "columns": ["device_id", "started_at"],
                "reason": "Device-based session queries",
                "benefit": "Faster device history",
            },
            {
                "table": "scan_sessions",
                "columns": ["scan_type", "started_at"],
                "reason": "Scan type filtering with time",
                "benefit": "Faster scan analysis",
            },
        ]

        async with aiosqlite.connect(self.db_path) as db:
            # Check which tables exist
            cursor = await db.execute(
                """
                SELECT name FROM sqlite_master
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
            """
            )
            existing_tables = {row[0] for row in await cursor.fetchall()}

            # Check existing indexes
            cursor = await db.execute(
                """
                SELECT name, tbl_name, sql FROM sqlite_master
                WHERE type='index' AND sql IS NOT NULL
            """
            )
            existing_indexes = await cursor.fetchall()
            existing_index_columns = set()

            for index_name, table_name, index_sql in existing_indexes:
                # Simple parsing to extract columns (could be improved)
                if index_sql and "(" in index_sql:
                    cols_part = index_sql.split("(")[1].split(")")[0]
                    cols = [col.strip() for col in cols_part.split(",")]
                    existing_index_columns.add((table_name, tuple(cols)))

            # Generate recommendations for missing indexes
            for pattern in patterns:
                table = pattern["table"]
                columns = pattern["columns"]

                if table in existing_tables:
                    index_key = (table, tuple(columns))
                    if index_key not in existing_index_columns:
                        recommendations.append(
                            IndexRecommendation(
                                table=table,
                                columns=columns,
                                reason=pattern["reason"],
                                estimated_benefit=pattern["benefit"],
                            )
                        )

        return recommendations

    async def optimize_sqlite_pragmas(self) -> Dict[str, Any]:
        """Apply SQLite performance optimizations."""
        optimizations = {
            "journal_mode": "WAL",
            "synchronous": "NORMAL",
            "cache_size": 10000,
            "temp_store": "MEMORY",
            "mmap_size": 268435456,  # 256MB
            "optimize": None,  # Run PRAGMA optimize
        }

        results = {}

        async with aiosqlite.connect(self.db_path) as db:
            for pragma, value in optimizations.items():
                try:
                    if value is not None:
                        await db.execute(f"PRAGMA {pragma} = {value}")
                    else:
                        await db.execute(f"PRAGMA {pragma}")

                    # Verify the setting
                    if pragma != "optimize":
                        cursor = await db.execute(f"PRAGMA {pragma}")
                        result = await cursor.fetchone()
                        results[pragma] = result[0] if result else "applied"
                    else:
                        results[pragma] = "executed"

                except Exception as e:
                    results[pragma] = f"error: {e}"
                    logger.warning(f"Failed to apply pragma {pragma}: {e}")

        return results

    async def vacuum_database(self) -> Dict[str, Any]:
        """Vacuum the database to reclaim space and improve performance."""
        start_time = time.time()

        # Get size before vacuum
        try:
            import os

            size_before = os.path.getsize(self.db_path)
        except Exception:
            size_before = 0

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("VACUUM")
            await db.commit()

        # Get size after vacuum
        try:
            size_after = os.path.getsize(self.db_path)
        except Exception:
            size_after = 0

        duration = time.time() - start_time

        return {
            "duration_seconds": duration,
            "size_before_bytes": size_before,
            "size_after_bytes": size_after,
            "size_reduction_bytes": size_before - size_after,
            "size_reduction_percent": (
                ((size_before - size_after) / size_before * 100)
                if size_before > 0
                else 0
            ),
        }

    async def create_recommended_indexes(
        self, recommendations: List[IndexRecommendation]
    ) -> Dict[str, Any]:
        """Create the recommended indexes."""
        results = {}

        async with aiosqlite.connect(self.db_path) as db:
            for rec in recommendations:
                try:
                    start_time = time.time()
                    await db.execute(rec.create_sql)
                    await db.commit()
                    duration = time.time() - start_time

                    results[f"{rec.table}_{'_'.join(rec.columns)}"] = {
                        "status": "created",
                        "duration_seconds": duration,
                        "sql": rec.create_sql,
                    }

                except Exception as e:
                    results[f"{rec.table}_{'_'.join(rec.columns)}"] = {
                        "status": "error",
                        "error": str(e),
                        "sql": rec.create_sql,
                    }

        return results

    def record_query_metrics(self, query: str, execution_time: float, row_count: int):
        """Record query metrics for analysis."""
        metric = QueryMetrics(
            query=query,
            execution_time=execution_time,
            row_count=row_count,
            timestamp=time.time(),
        )

        self.query_metrics.append(metric)

        # Keep only recent metrics
        if len(self.query_metrics) > self.max_metrics:
            self.query_metrics = self.query_metrics[-self.max_metrics :]

        # Log slow queries
        if metric.is_slow:
            logger.warning(
                f"Slow query detected: {execution_time:.3f}s, "
                f"{row_count} rows: {query[:200]}..."
            )


class OptimizedSQLiteConnection:
    """SQLite connection with performance optimizations and monitoring."""

    def __init__(self, db_path: str, optimizer: Optional[DatabaseOptimizer] = None):
        self.db_path = db_path
        self.optimizer = optimizer
        self.connection = None

    async def __aenter__(self):
        self.connection = await aiosqlite.connect(self.db_path)

        # Apply performance pragmas
        pragmas = {
            "journal_mode": "WAL",
            "synchronous": "NORMAL",
            "cache_size": 10000,
            "temp_store": "MEMORY",
            "mmap_size": 268435456,
        }

        for pragma, value in pragmas.items():
            await self.connection.execute(f"PRAGMA {pragma} = {value}")

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            await self.connection.close()

    async def execute(self, query: str, parameters: Tuple = ()) -> Any:
        """Execute query with performance monitoring."""
        start_time = time.time()

        cursor = await self.connection.execute(query, parameters)
        result = await cursor.fetchall()

        execution_time = time.time() - start_time

        # Record metrics if optimizer is available
        if self.optimizer:
            self.optimizer.record_query_metrics(query, execution_time, len(result))

        return result

    async def execute_many(self, query: str, parameters_list: List[Tuple]) -> None:
        """Execute many queries with performance monitoring."""
        start_time = time.time()

        await self.connection.executemany(query, parameters_list)
        await self.connection.commit()

        execution_time = time.time() - start_time

        # Record metrics if optimizer is available
        if self.optimizer:
            self.optimizer.record_query_metrics(
                query, execution_time, len(parameters_list)
            )


async def run_performance_analysis(db_path: str) -> Dict[str, Any]:
    """Run a comprehensive performance analysis on the database."""
    optimizer = DatabaseOptimizer(db_path)

    # Gather performance data
    analysis = {
        "database_path": db_path,
        "analysis_timestamp": time.time(),
        "table_stats": await optimizer.get_table_stats(),
        "query_analysis": await optimizer.analyze_query_performance(),
        "missing_indexes": await optimizer.analyze_missing_indexes(),
        "pragma_optimizations": await optimizer.optimize_sqlite_pragmas(),
    }

    return analysis


async def apply_performance_optimizations(
    db_path: str, create_indexes: bool = True
) -> Dict[str, Any]:
    """Apply performance optimizations to the database."""
    optimizer = DatabaseOptimizer(db_path)

    results = {
        "database_path": db_path,
        "optimization_timestamp": time.time(),
        "pragma_results": await optimizer.optimize_sqlite_pragmas(),
    }

    if create_indexes:
        recommendations = await optimizer.analyze_missing_indexes()
        if recommendations:
            results["index_creation"] = await optimizer.create_recommended_indexes(
                recommendations
            )
            results["indexes_created"] = len(recommendations)
        else:
            results["indexes_created"] = 0
            results["message"] = "No missing indexes found"

    # Run vacuum for space reclamation
    results["vacuum_results"] = await optimizer.vacuum_database()

    return results


if __name__ == "__main__":
    import sys

    async def main():
        if len(sys.argv) < 2:
            print("Usage: python db_optimizer.py <database_path> [analyze|optimize]")
            sys.exit(1)

        db_path = sys.argv[1]
        action = sys.argv[2] if len(sys.argv) > 2 else "analyze"

        if action == "analyze":
            results = await run_performance_analysis(db_path)
            print("Performance Analysis Results:")
            print(f"Database: {results['database_path']}")
            print(f"Tables: {len(results['table_stats'])}")
            print(f"Missing indexes: {len(results['missing_indexes'])}")

            for rec in results["missing_indexes"]:
                print(f"  - {rec.table}: {', '.join(rec.columns)} ({rec.reason})")

        elif action == "optimize":
            results = await apply_performance_optimizations(db_path)
            print("Optimization Results:")
            print(f"Database: {results['database_path']}")
            print(f"Indexes created: {results.get('indexes_created', 0)}")

            vacuum_results = results.get("vacuum_results", {})
            if vacuum_results:
                print(f"Vacuum duration: {vacuum_results['duration_seconds']:.2f}s")
                print(
                    f"Size reduction: {vacuum_results['size_reduction_percent']:.1f}%"
                )

        else:
            print("Unknown action. Use 'analyze' or 'optimize'")

    asyncio.run(main())
