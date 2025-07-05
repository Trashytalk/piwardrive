#!/usr/bin/env python3
"""
PiWardrive Performance Management CLI Tool

This tool provides command-line interface for performance analysis,
optimization, and monitoring of PiWardrive databases and services.
"""

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path
from typing import Dict, Any

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from piwardrive.performance.db_optimizer import (
    DatabaseOptimizer,
    run_performance_analysis,
    apply_performance_optimizations
)
from piwardrive.performance.async_optimizer import (
    AsyncPerformanceMonitor,
    get_global_monitor
)
from piwardrive.performance.realtime_optimizer import (
    get_global_optimizer
)


async def analyze_database_performance(args):
    """Analyze database performance."""
    print(f"Analyzing database performance: {args.database}")
    
    results = await run_performance_analysis(args.database)
    
    print("\n" + "="*60)
    print("DATABASE PERFORMANCE ANALYSIS")
    print("="*60)
    
    # Table statistics
    print(f"\nTable Statistics:")
    table_stats = results.get('table_stats', {})
    for table_name, stats in table_stats.items():
        print(f"  {table_name}:")
        print(f"    Rows: {stats['row_count']:,}")
        print(f"    Size: {stats['size_mb']:.2f} MB")
    
    # Query analysis
    query_analysis = results.get('query_analysis', {})
    if 'message' not in query_analysis:
        print(f"\nQuery Performance:")
        print(f"  Total queries: {query_analysis.get('total_queries', 0):,}")
        print(f"  Slow queries: {query_analysis.get('slow_queries', 0):,}")
        print(f"  Slow query %: {query_analysis.get('slow_query_percentage', 0):.1f}%")
        print(f"  Average time: {query_analysis.get('average_execution_time', 0)*1000:.1f}ms")
    
    # Missing indexes
    missing_indexes = results.get('missing_indexes', [])
    if missing_indexes:
        print(f"\nMissing Indexes ({len(missing_indexes)} found):")
        for idx in missing_indexes:
            print(f"  {idx.table}.{', '.join(idx.columns)}")
            print(f"    Reason: {idx.reason}")
            print(f"    Benefit: {idx.estimated_benefit}")
            if args.verbose:
                print(f"    SQL: {idx.create_sql}")
    else:
        print("\nNo missing indexes detected.")
    
    # PRAGMA settings
    pragma_opts = results.get('pragma_optimizations', {})
    if pragma_opts:
        print(f"\nSQLite PRAGMA Settings:")
        for pragma, value in pragma_opts.items():
            print(f"  {pragma}: {value}")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nResults saved to: {args.output}")


async def optimize_database_performance(args):
    """Optimize database performance."""
    print(f"Optimizing database performance: {args.database}")
    
    results = await apply_performance_optimizations(
        args.database, 
        create_indexes=not args.no_indexes
    )
    
    print("\n" + "="*60)
    print("DATABASE OPTIMIZATION RESULTS")
    print("="*60)
    
    # PRAGMA results
    pragma_results = results.get('pragma_results', {})
    print(f"\nPRAGMA Optimizations:")
    for pragma, result in pragma_results.items():
        status = "✓" if "error" not in str(result).lower() else "✗"
        print(f"  {status} {pragma}: {result}")
    
    # Index creation
    indexes_created = results.get('indexes_created', 0)
    print(f"\nIndexes Created: {indexes_created}")
    
    index_results = results.get('index_creation', {})
    if index_results:
        for index_name, result in index_results.items():
            status = "✓" if result['status'] == 'created' else "✗"
            duration = result.get('duration_seconds', 0)
            print(f"  {status} {index_name} ({duration:.2f}s)")
            if result['status'] != 'created':
                print(f"    Error: {result.get('error', 'Unknown')}")
    
    # Vacuum results
    vacuum_results = results.get('vacuum_results', {})
    if vacuum_results:
        print(f"\nVacuum Results:")
        print(f"  Duration: {vacuum_results['duration_seconds']:.2f}s")
        print(f"  Size reduction: {vacuum_results['size_reduction_percent']:.1f}%")
        print(f"  Space saved: {vacuum_results['size_reduction_bytes']/1024/1024:.2f} MB")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nResults saved to: {args.output}")


async def monitor_async_performance(args):
    """Monitor async performance."""
    print("Monitoring async performance...")
    
    monitor = get_global_monitor()
    
    # Monitor for specified duration
    duration = args.duration
    start_time = time.time()
    
    print(f"Monitoring for {duration} seconds...")
    print("Press Ctrl+C to stop early")
    
    try:
        while time.time() - start_time < duration:
            await asyncio.sleep(1)
            
            # Print live stats every 10 seconds
            if int(time.time() - start_time) % 10 == 0:
                summary = monitor.get_performance_summary()
                if 'message' not in summary:
                    print(f"\nLive Stats (after {int(time.time() - start_time)}s):")
                    print(f"  Operations: {summary['total_operations']}")
                    print(f"  Active: {summary['active_operations']}")
                    print(f"  Slow: {summary['slow_operations']}")
    
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    
    # Final summary
    summary = monitor.get_performance_summary()
    
    print("\n" + "="*60)
    print("ASYNC PERFORMANCE SUMMARY")
    print("="*60)
    
    if 'message' in summary:
        print(summary['message'])
        return
    
    print(f"Total operations: {summary['total_operations']}")
    print(f"Active operations: {summary['active_operations']}")
    print(f"Slow operations: {summary['slow_operations']}")
    
    for op_name, stats in summary.get('operation_summary', {}).items():
        print(f"\n{op_name}:")
        print(f"  Count: {stats['count']}")
        print(f"  Success rate: {stats['success_rate']:.1f}%")
        print(f"  Avg time: {stats['avg_time']*1000:.1f}ms")
        print(f"  Max time: {stats['max_time']*1000:.1f}ms")
        print(f"  Slow count: {stats['slow_count']}")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        print(f"\nResults saved to: {args.output}")


async def monitor_realtime_performance(args):
    """Monitor real-time update performance."""
    print("Monitoring real-time update performance...")
    
    optimizer = get_global_optimizer()
    
    duration = args.duration
    start_time = time.time()
    
    print(f"Monitoring for {duration} seconds...")
    
    try:
        while time.time() - start_time < duration:
            await asyncio.sleep(5)
            
            stats = optimizer.get_performance_stats()
            
            # Print live stats
            ws_stats = stats.get('websocket_stats', {})
            sse_stats = stats.get('sse_stats', {})
            
            print(f"\nLive Stats (after {int(time.time() - start_time)}s):")
            print(f"  WebSocket connections: {ws_stats.get('active_connections', 0)}")
            print(f"  WebSocket messages: {ws_stats.get('messages_sent', 0)}")
            print(f"  SSE streams: {sse_stats.get('active_streams', 0)}")
            print(f"  SSE events: {sse_stats.get('events_sent', 0)}")
    
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    
    # Final summary
    stats = optimizer.get_performance_stats()
    
    print("\n" + "="*60)
    print("REAL-TIME PERFORMANCE SUMMARY")
    print("="*60)
    
    ws_stats = stats.get('websocket_stats', {})
    sse_stats = stats.get('sse_stats', {})
    
    print(f"WebSocket Performance:")
    print(f"  Total connections: {ws_stats.get('total_connections', 0)}")
    print(f"  Active connections: {ws_stats.get('active_connections', 0)}")
    print(f"  Messages sent: {ws_stats.get('messages_sent', 0)}")
    print(f"  Bytes sent: {ws_stats.get('bytes_sent', 0):,}")
    print(f"  Errors: {ws_stats.get('errors', 0)}")
    
    print(f"\nSSE Performance:")
    print(f"  Total streams: {sse_stats.get('total_streams', 0)}")
    print(f"  Active streams: {sse_stats.get('active_streams', 0)}")
    print(f"  Events sent: {sse_stats.get('events_sent', 0)}")
    print(f"  Bytes sent: {sse_stats.get('bytes_sent', 0):,}")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(stats, f, indent=2, default=str)
        print(f"\nResults saved to: {args.output}")


async def run_performance_benchmark(args):
    """Run performance benchmarks."""
    print("Running performance benchmarks...")
    
    results = {
        "benchmark_timestamp": time.time(),
        "database_path": args.database,
        "benchmark_results": {}
    }
    
    # Database benchmark
    if args.database:
        print("\nRunning database benchmark...")
        
        optimizer = DatabaseOptimizer(args.database)
        
        # Test query performance
        start_time = time.time()
        table_stats = await optimizer.get_table_stats()
        query_time = time.time() - start_time
        
        results["benchmark_results"]["database"] = {
            "table_count": len(table_stats),
            "total_rows": sum(stats["row_count"] for stats in table_stats.values()),
            "total_size_mb": sum(stats["size_mb"] for stats in table_stats.values()),
            "metadata_query_time": query_time
        }
        
        print(f"  Tables: {len(table_stats)}")
        print(f"  Total rows: {sum(stats['row_count'] for stats in table_stats.values()):,}")
        print(f"  Total size: {sum(stats['size_mb'] for stats in table_stats.values()):.2f} MB")
        print(f"  Metadata query time: {query_time*1000:.1f}ms")
    
    # Async benchmark
    print("\nRunning async benchmark...")
    
    monitor = AsyncPerformanceMonitor()
    
    async def test_operation(delay: float):
        await asyncio.sleep(delay)
    
    # Run test operations
    start_time = time.time()
    tasks = []
    for i in range(100):
        operation_id = monitor.start_operation("benchmark_test")
        task = asyncio.create_task(test_operation(0.01))
        task.add_done_callback(lambda t: monitor.end_operation(operation_id))
        tasks.append(task)
    
    await asyncio.gather(*tasks)
    async_time = time.time() - start_time
    
    summary = monitor.get_performance_summary()
    
    results["benchmark_results"]["async"] = {
        "operations_count": 100,
        "total_time": async_time,
        "operations_per_second": 100 / async_time,
        "performance_summary": summary
    }
    
    print(f"  Operations: 100")
    print(f"  Total time: {async_time:.3f}s")
    print(f"  Operations/sec: {100/async_time:.1f}")
    
    print("\n" + "="*60)
    print("BENCHMARK RESULTS")
    print("="*60)
    
    for category, data in results["benchmark_results"].items():
        print(f"\n{category.upper()} Benchmark:")
        for key, value in data.items():
            if key != "performance_summary":
                print(f"  {key}: {value}")
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nResults saved to: {args.output}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PiWardrive Performance Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze database performance
  python performance_cli.py analyze-db /path/to/database.db
  
  # Optimize database with indexes
  python performance_cli.py optimize-db /path/to/database.db
  
  # Monitor async performance for 60 seconds
  python performance_cli.py monitor-async --duration 60
  
  # Monitor real-time updates for 30 seconds
  python performance_cli.py monitor-realtime --duration 30
  
  # Run comprehensive benchmark
  python performance_cli.py benchmark --database /path/to/database.db
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Database analysis command
    analyze_parser = subparsers.add_parser('analyze-db', help='Analyze database performance')
    analyze_parser.add_argument('database', help='Path to database file')
    analyze_parser.add_argument('--output', '-o', help='Output file for results (JSON)')
    analyze_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    # Database optimization command
    optimize_parser = subparsers.add_parser('optimize-db', help='Optimize database performance')
    optimize_parser.add_argument('database', help='Path to database file')
    optimize_parser.add_argument('--no-indexes', action='store_true', help='Skip index creation')
    optimize_parser.add_argument('--output', '-o', help='Output file for results (JSON)')
    
    # Async monitoring command
    async_parser = subparsers.add_parser('monitor-async', help='Monitor async performance')
    async_parser.add_argument('--duration', '-d', type=int, default=30, help='Monitoring duration in seconds')
    async_parser.add_argument('--output', '-o', help='Output file for results (JSON)')
    
    # Real-time monitoring command
    realtime_parser = subparsers.add_parser('monitor-realtime', help='Monitor real-time update performance')
    realtime_parser.add_argument('--duration', '-d', type=int, default=30, help='Monitoring duration in seconds')
    realtime_parser.add_argument('--output', '-o', help='Output file for results (JSON)')
    
    # Benchmark command
    benchmark_parser = subparsers.add_parser('benchmark', help='Run performance benchmarks')
    benchmark_parser.add_argument('--database', help='Path to database file')
    benchmark_parser.add_argument('--output', '-o', help='Output file for results (JSON)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Run the appropriate command
    try:
        if args.command == 'analyze-db':
            asyncio.run(analyze_database_performance(args))
        elif args.command == 'optimize-db':
            asyncio.run(optimize_database_performance(args))
        elif args.command == 'monitor-async':
            asyncio.run(monitor_async_performance(args))
        elif args.command == 'monitor-realtime':
            asyncio.run(monitor_realtime_performance(args))
        elif args.command == 'benchmark':
            asyncio.run(run_performance_benchmark(args))
        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
