#!/usr/bin/env python3
"""
Database Performance Optimization and Analysis Tools for PiWardrive

This module provides comprehensive database performance monitoring, optimization,
and analysis capabilities.
"""

import asyncio
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, asdict
import aiosqlite
from piwardrive.core.persistence import _get_conn, _db_path

logger = logging.getLogger(__name__)


@dataclass
class QueryPerformanceMetric:
    """Performance metric for a database query."""
    query_hash: str
    query_text: str
    execution_time_ms: float
    rows_examined: int
    rows_returned: int
    index_usage: bool
    timestamp: datetime
    optimization_suggestions: List[str]


@dataclass
class DatabaseHealthMetric:
    """Overall database health metrics."""
    database_size_mb: float
    table_count: int
    index_count: int
    fragmentation_ratio: float
    query_cache_hit_ratio: float
    connection_count: int
    average_query_time_ms: float
    slow_query_count: int
    last_vacuum: Optional[datetime]
    last_analyze: Optional[datetime]


class DatabaseOptimizer:
    """Database performance optimization and monitoring."""
    
    def __init__(self):
        self.slow_query_threshold_ms = 1000  # 1 second
        self.optimization_history: List[Dict[str, Any]] = []
    
    async def analyze_query_performance(self, query: str, params: tuple = ()) -> QueryPerformanceMetric:
        """Analyze performance of a specific query."""
        start_time = time.perf_counter()
        
        async with _get_conn() as conn:
            # Enable query plan analysis
            await conn.execute("PRAGMA query_only = ON")
            
            # Get query plan
            explain_cursor = await conn.execute(f"EXPLAIN QUERY PLAN {query}", params)
            query_plan = await explain_cursor.fetchall()
            
            await conn.execute("PRAGMA query_only = OFF")
            
            # Execute query and measure performance
            cursor = await conn.execute(query, params)
            rows = await cursor.fetchall()
            
            end_time = time.perf_counter()
            execution_time_ms = (end_time - start_time) * 1000
            
            # Analyze query plan for optimization opportunities
            index_usage = any("USING INDEX" in str(step) for step in query_plan)
            
            optimization_suggestions = self._analyze_query_plan(query_plan, query)
            
            return QueryPerformanceMetric(
                query_hash=hash(query),
                query_text=query[:200] + "..." if len(query) > 200 else query,
                execution_time_ms=execution_time_ms,
                rows_examined=len(query_plan),
                rows_returned=len(rows),
                index_usage=index_usage,
                timestamp=datetime.now(),
                optimization_suggestions=optimization_suggestions
            )
    
    def _analyze_query_plan(self, query_plan: List, query: str) -> List[str]:
        """Analyze query execution plan and suggest optimizations."""
        suggestions = []
        
        plan_text = " ".join(str(step) for step in query_plan)
        
        # Check for table scans
        if "SCAN TABLE" in plan_text and "USING INDEX" not in plan_text:
            suggestions.append("Consider adding an index to avoid table scan")
        
        # Check for temp B-tree usage
        if "USE TEMP B-TREE" in plan_text:
            suggestions.append("Query requires temporary sorting - consider optimizing ORDER BY or GROUP BY")
        
        # Check for multiple table scans
        scan_count = plan_text.count("SCAN TABLE")
        if scan_count > 2:
            suggestions.append("Multiple table scans detected - consider query restructuring")
        
        # Check for JOIN optimization
        if "JOIN" in query.upper() and "AUTOMATIC INDEX" in plan_text:
            suggestions.append("Automatic index created for JOIN - consider adding permanent index")
        
        # Check for LIKE patterns
        if "LIKE" in query.upper() and query.count("%") > 0:
            if query.find("%") == query.find("LIKE") + 5:  # Leading wildcard
                suggestions.append("Leading wildcard in LIKE pattern prevents index usage")
        
        return suggestions
    
    async def get_database_health(self) -> DatabaseHealthMetric:
        """Get comprehensive database health metrics."""
        async with _get_conn() as conn:
            # Database size
            size_cursor = await conn.execute("PRAGMA page_count")
            page_count = (await size_cursor.fetchone())[0]
            
            page_size_cursor = await conn.execute("PRAGMA page_size")
            page_size = (await page_size_cursor.fetchone())[0]
            
            database_size_mb = (page_count * page_size) / (1024 * 1024)
            
            # Table and index counts
            tables_cursor = await conn.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table'"
            )
            table_count = (await tables_cursor.fetchone())[0]
            
            indexes_cursor = await conn.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='index'"
            )
            index_count = (await indexes_cursor.fetchone())[0]
            
            # Fragmentation
            freelist_cursor = await conn.execute("PRAGMA freelist_count")
            freelist_count = (await freelist_cursor.fetchone())[0]
            fragmentation_ratio = freelist_count / page_count if page_count > 0 else 0
            
            # Cache stats (approximate)
            cache_cursor = await conn.execute("PRAGMA cache_size")
            cache_size = (await cache_cursor.fetchone())[0]
            
            return DatabaseHealthMetric(
                database_size_mb=database_size_mb,
                table_count=table_count,
                index_count=index_count,
                fragmentation_ratio=fragmentation_ratio,
                query_cache_hit_ratio=0.95,  # Placeholder - SQLite doesn't expose this
                connection_count=1,  # Current connection
                average_query_time_ms=0.0,  # Would need query logging
                slow_query_count=0,  # Would need query logging
                last_vacuum=None,  # Would need to track separately
                last_analyze=None   # Would need to track separately
            )
    
    async def optimize_database(self) -> Dict[str, Any]:
        """Perform comprehensive database optimization."""
        optimization_results = {
            "started_at": datetime.now().isoformat(),
            "operations": [],
            "before_metrics": {},
            "after_metrics": {},
            "improvements": {}
        }
        
        # Get baseline metrics
        before_health = await self.get_database_health()
        optimization_results["before_metrics"] = asdict(before_health)
        
        async with _get_conn() as conn:
            # 1. VACUUM to defragment database
            logger.info("Running VACUUM to defragment database...")
            start_time = time.perf_counter()
            await conn.execute("VACUUM")
            vacuum_time = time.perf_counter() - start_time
            
            optimization_results["operations"].append({
                "operation": "VACUUM",
                "duration_seconds": vacuum_time,
                "description": "Defragmented database and reclaimed space"
            })
            
            # 2. ANALYZE to update query planner statistics
            logger.info("Running ANALYZE to update statistics...")
            start_time = time.perf_counter()
            await conn.execute("ANALYZE")
            analyze_time = time.perf_counter() - start_time
            
            optimization_results["operations"].append({
                "operation": "ANALYZE",
                "duration_seconds": analyze_time,
                "description": "Updated query planner statistics"
            })
            
            # 3. Optimize specific tables
            table_optimizations = await self._optimize_tables(conn)
            optimization_results["operations"].extend(table_optimizations)
            
            # 4. Check and create missing indexes
            index_optimizations = await self._optimize_indexes(conn)
            optimization_results["operations"].extend(index_optimizations)
        
        # Get final metrics
        after_health = await self.get_database_health()
        optimization_results["after_metrics"] = asdict(after_health)
        
        # Calculate improvements
        optimization_results["improvements"] = {
            "size_reduction_mb": before_health.database_size_mb - after_health.database_size_mb,
            "fragmentation_improvement": before_health.fragmentation_ratio - after_health.fragmentation_ratio,
            "new_indexes": after_health.index_count - before_health.index_count
        }
        
        optimization_results["completed_at"] = datetime.now().isoformat()
        self.optimization_history.append(optimization_results)
        
        return optimization_results
    
    async def _optimize_tables(self, conn: aiosqlite.Connection) -> List[Dict[str, Any]]:
        """Optimize individual tables."""
        operations = []
        
        # Get list of tables
        cursor = await conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        tables = [row[0] for row in await cursor.fetchall()]
        
        for table in tables:
            # Check table statistics
            count_cursor = await conn.execute(f"SELECT COUNT(*) FROM {table}")
            row_count = (await count_cursor.fetchone())[0]
            
            if row_count > 1000:  # Only optimize larger tables
                # REINDEX for tables with many rows
                start_time = time.perf_counter()
                await conn.execute(f"REINDEX {table}")
                reindex_time = time.perf_counter() - start_time
                
                operations.append({
                    "operation": f"REINDEX {table}",
                    "duration_seconds": reindex_time,
                    "description": f"Rebuilt indexes for table {table} ({row_count} rows)"
                })
        
        return operations
    
    async def _optimize_indexes(self, conn: aiosqlite.Connection) -> List[Dict[str, Any]]:
        """Check for missing indexes and create them."""
        operations = []
        
        # Analyze common query patterns and suggest indexes
        suggested_indexes = [
            # WiFi detections table optimizations
            ("wifi_detections", "bssid_time_compound", "bssid, detection_timestamp"),
            ("wifi_detections", "location_signal_compound", "latitude, longitude, signal_strength_dbm"),
            ("wifi_detections", "vendor_encryption_compound", "vendor_name, encryption_type"),
            
            # Bluetooth detections optimizations
            ("bluetooth_detections", "mac_time_compound", "mac_address, detection_timestamp"),
            ("bluetooth_detections", "manufacturer_compound", "manufacturer_name, device_type"),
            
            # GPS tracks optimizations
            ("gps_tracks", "session_time_compound", "scan_session_id, timestamp"),
            
            # Analytics optimizations
            ("network_analytics", "suspicious_date_compound", "suspicious_score, analysis_date"),
        ]
        
        for table, index_name, columns in suggested_indexes:
            # Check if table exists
            table_cursor = await conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,)
            )
            if not await table_cursor.fetchone():
                continue
            
            # Check if index already exists
            index_cursor = await conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name=?", 
                (f"idx_{index_name}",)
            )
            if await index_cursor.fetchone():
                continue
            
            # Create index
            try:
                start_time = time.perf_counter()
                await conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{index_name} ON {table}({columns})")
                index_time = time.perf_counter() - start_time
                
                operations.append({
                    "operation": f"CREATE INDEX idx_{index_name}",
                    "duration_seconds": index_time,
                    "description": f"Created compound index on {table}({columns})"
                })
            except Exception as e:
                logger.warning(f"Failed to create index idx_{index_name}: {e}")
        
        return operations
    
    async def get_slow_queries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get slowest queries from query log (would need query logging enabled)."""
        # This is a placeholder - would need actual query logging
        return []
    
    async def analyze_table_usage(self) -> Dict[str, Dict[str, Any]]:
        """Analyze table usage patterns."""
        usage_stats = {}
        
        async with _get_conn() as conn:
            # Get list of tables
            cursor = await conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
            tables = [row[0] for row in await cursor.fetchall()]
            
            for table in tables:
                # Row count
                count_cursor = await conn.execute(f"SELECT COUNT(*) FROM {table}")
                row_count = (await count_cursor.fetchone())[0]
                
                # Table size estimation
                info_cursor = await conn.execute(f"PRAGMA table_info({table})")
                columns = await info_cursor.fetchall()
                
                usage_stats[table] = {
                    "row_count": row_count,
                    "column_count": len(columns),
                    "estimated_size_mb": row_count * len(columns) * 50 / (1024 * 1024),  # Rough estimate
                    "last_analyzed": datetime.now().isoformat()
                }
        
        return usage_stats
    
    async def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        logger.info("Generating database performance report...")
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "database_health": {},
            "table_usage": {},
            "optimization_recommendations": [],
            "recent_optimizations": self.optimization_history[-5:] if self.optimization_history else []
        }
        
        # Get database health
        health = await self.get_database_health()
        report["database_health"] = asdict(health)
        
        # Get table usage
        report["table_usage"] = await self.analyze_table_usage()
        
        # Generate recommendations
        recommendations = []
        
        if health.fragmentation_ratio > 0.1:
            recommendations.append({
                "type": "maintenance",
                "priority": "high",
                "description": "Database fragmentation is high, run VACUUM",
                "action": "Run database optimization"
            })
        
        if health.database_size_mb > 1000:  # 1GB
            recommendations.append({
                "type": "archival",
                "priority": "medium",
                "description": "Database size is large, consider archiving old data",
                "action": "Implement data archival strategy"
            })
        
        # Check for tables without recent analysis
        for table, stats in report["table_usage"].items():
            if stats["row_count"] > 10000:
                recommendations.append({
                    "type": "performance",
                    "priority": "medium",
                    "description": f"Table {table} has many rows, ensure proper indexing",
                    "action": f"Review indexes for {table}"
                })
        
        report["optimization_recommendations"] = recommendations
        
        return report


async def main():
    """Run database performance analysis and optimization."""
    optimizer = DatabaseOptimizer()
    
    print("=== PiWardrive Database Performance Analysis ===\n")
    
    # Generate performance report
    print("Generating performance report...")
    report = await optimizer.generate_performance_report()
    
    print(f"Database Health:")
    health = report["database_health"]
    print(f"  Size: {health['database_size_mb']:.2f} MB")
    print(f"  Tables: {health['table_count']}")
    print(f"  Indexes: {health['index_count']}")
    print(f"  Fragmentation: {health['fragmentation_ratio']:.2%}")
    
    print(f"\nTable Usage:")
    for table, stats in report["table_usage"].items():
        print(f"  {table}: {stats['row_count']:,} rows ({stats['estimated_size_mb']:.1f} MB)")
    
    print(f"\nRecommendations:")
    for rec in report["optimization_recommendations"]:
        print(f"  [{rec['priority'].upper()}] {rec['description']}")
    
    # Ask user if they want to run optimization
    response = input("\nRun database optimization? (y/N): ")
    if response.lower() == 'y':
        print("\nRunning database optimization...")
        optimization_results = await optimizer.optimize_database()
        
        print(f"Optimization completed in {len(optimization_results['operations'])} operations:")
        for op in optimization_results['operations']:
            print(f"  - {op['operation']}: {op['duration_seconds']:.2f}s")
        
        improvements = optimization_results['improvements']
        if improvements['size_reduction_mb'] > 0:
            print(f"  Space saved: {improvements['size_reduction_mb']:.2f} MB")
        if improvements['new_indexes'] > 0:
            print(f"  New indexes created: {improvements['new_indexes']}")


if __name__ == "__main__":
    asyncio.run(main())
