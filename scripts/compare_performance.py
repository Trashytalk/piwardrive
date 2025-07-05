#!/usr/bin/env python3
"""
Performance Comparison Script

This script compares current performance metrics with a baseline
and detects regressions or improvements.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple


class PerformanceComparator:
    """Compares performance metrics between current and baseline results."""

    def __init__(self, regression_threshold: float = 20.0):
        self.regression_threshold = regression_threshold / 100.0  # Convert to decimal
        self.improvement_threshold = 0.1  # 10% improvement threshold

    def load_results(self, file_path: str) -> Dict[str, Any]:
        """Load performance results from JSON file."""
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {file_path}: {e}")
            sys.exit(1)

    def compare_metrics(
        self, current: Dict[str, Any], baseline: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare current metrics with baseline."""
        comparison = {
            "timestamp": datetime.now().isoformat(),
            "regression_detected": False,
            "improvement_detected": False,
            "regressions": [],
            "improvements": [],
            "unchanged": [],
            "summary": {
                "total_metrics": 0,
                "regression_count": 0,
                "improvement_count": 0,
                "unchanged_count": 0,
            },
        }

        # Compare database metrics
        if self._has_benchmarks(current, baseline, "database"):
            db_comparison = self._compare_database_metrics(
                current["benchmarks"]["database"], baseline["benchmarks"]["database"]
            )
            comparison.update(
                self._merge_comparison(comparison, db_comparison, "database")
            )

        # Compare async metrics
        if self._has_benchmarks(current, baseline, "async"):
            async_comparison = self._compare_async_metrics(
                current["benchmarks"]["async"], baseline["benchmarks"]["async"]
            )
            comparison.update(
                self._merge_comparison(comparison, async_comparison, "async")
            )

        # Compare realtime metrics
        if self._has_benchmarks(current, baseline, "realtime"):
            rt_comparison = self._compare_realtime_metrics(
                current["benchmarks"]["realtime"], baseline["benchmarks"]["realtime"]
            )
            comparison.update(
                self._merge_comparison(comparison, rt_comparison, "realtime")
            )

        # Compare memory metrics
        if self._has_benchmarks(current, baseline, "memory"):
            memory_comparison = self._compare_memory_metrics(
                current["benchmarks"]["memory"], baseline["benchmarks"]["memory"]
            )
            comparison.update(
                self._merge_comparison(comparison, memory_comparison, "memory")
            )

        # Update summary
        comparison["summary"]["total_metrics"] = (
            len(comparison["regressions"])
            + len(comparison["improvements"])
            + len(comparison["unchanged"])
        )
        comparison["summary"]["regression_count"] = len(comparison["regressions"])
        comparison["summary"]["improvement_count"] = len(comparison["improvements"])
        comparison["summary"]["unchanged_count"] = len(comparison["unchanged"])

        comparison["regression_detected"] = len(comparison["regressions"]) > 0
        comparison["improvement_detected"] = len(comparison["improvements"]) > 0

        return comparison

    def _has_benchmarks(
        self, current: Dict[str, Any], baseline: Dict[str, Any], benchmark_type: str
    ) -> bool:
        """Check if both results have the specified benchmark type."""
        return (
            "benchmarks" in current
            and "benchmarks" in baseline
            and benchmark_type in current["benchmarks"]
            and benchmark_type in baseline["benchmarks"]
            and not isinstance(current["benchmarks"][benchmark_type], dict)
            or "error" not in current["benchmarks"][benchmark_type]
        )

    def _merge_comparison(
        self,
        main_comparison: Dict[str, Any],
        sub_comparison: Dict[str, Any],
        category: str,
    ) -> Dict[str, Any]:
        """Merge sub-comparison results into main comparison."""
        for regression in sub_comparison["regressions"]:
            main_comparison["regressions"].append(f"[{category}] {regression}")

        for improvement in sub_comparison["improvements"]:
            main_comparison["improvements"].append(f"[{category}] {improvement}")

        for unchanged in sub_comparison["unchanged"]:
            main_comparison["unchanged"].append(f"[{category}] {unchanged}")

        return main_comparison

    def _compare_database_metrics(
        self, current: Dict[str, Any], baseline: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare database performance metrics."""
        comparison = {"regressions": [], "improvements": [], "unchanged": []}

        # Compare query performance
        if "query_performance" in current and "query_performance" in baseline:
            query_comparison = self._compare_performance_metrics(
                current["query_performance"], baseline["query_performance"], "Query"
            )
            comparison = self._merge_metric_comparison(comparison, query_comparison)

        # Compare insert performance
        if "insert_performance" in current and "insert_performance" in baseline:
            insert_comparison = self._compare_performance_metrics(
                current["insert_performance"], baseline["insert_performance"], "Insert"
            )
            comparison = self._merge_metric_comparison(comparison, insert_comparison)

        # Compare update performance
        if "update_performance" in current and "update_performance" in baseline:
            update_comparison = self._compare_performance_metrics(
                current["update_performance"], baseline["update_performance"], "Update"
            )
            comparison = self._merge_metric_comparison(comparison, update_comparison)

        return comparison

    def _compare_async_metrics(
        self, current: Dict[str, Any], baseline: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare async performance metrics."""
        comparison = {"regressions": [], "improvements": [], "unchanged": []}

        # Compare task performance
        if "task_performance" in current and "task_performance" in baseline:
            task_comparison = self._compare_performance_metrics(
                current["task_performance"], baseline["task_performance"], "Async Task"
            )
            comparison = self._merge_metric_comparison(comparison, task_comparison)

        # Compare batch performance
        if "batch_performance" in current and "batch_performance" in baseline:
            batch_comparison = self._compare_batch_performance(
                current["batch_performance"], baseline["batch_performance"]
            )
            comparison = self._merge_metric_comparison(comparison, batch_comparison)

        return comparison

    def _compare_realtime_metrics(
        self, current: Dict[str, Any], baseline: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare realtime performance metrics."""
        comparison = {"regressions": [], "improvements": [], "unchanged": []}

        # Compare message performance
        if "message_performance" in current and "message_performance" in baseline:
            message_comparison = self._compare_performance_metrics(
                current["message_performance"],
                baseline["message_performance"],
                "Message Processing",
            )
            comparison = self._merge_metric_comparison(comparison, message_comparison)

        # Compare connection performance
        if "connection_performance" in current and "connection_performance" in baseline:
            connection_comparison = self._compare_performance_metrics(
                current["connection_performance"],
                baseline["connection_performance"],
                "Connection Handling",
            )
            comparison = self._merge_metric_comparison(
                comparison, connection_comparison
            )

        return comparison

    def _compare_memory_metrics(
        self, current: Dict[str, Any], baseline: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare memory performance metrics."""
        comparison = {"regressions": [], "improvements": [], "unchanged": []}

        # Compare memory growth
        if "memory_growth_mb" in current and "memory_growth_mb" in baseline:
            current_growth = current["memory_growth_mb"]
            baseline_growth = baseline["memory_growth_mb"]

            change_ratio = (
                (current_growth - baseline_growth) / baseline_growth
                if baseline_growth != 0
                else 0
            )

            if change_ratio > self.regression_threshold:
                comparison["regressions"].append(
                    f"Memory growth regression: {current_growth:.2f}MB vs {baseline_growth:.2f}MB baseline ({change_ratio:.1%} increase)"
                )
            elif change_ratio < -self.improvement_threshold:
                comparison["improvements"].append(
                    f"Memory growth improvement: {current_growth:.2f}MB vs {baseline_growth:.2f}MB baseline ({abs(change_ratio):.1%} decrease)"
                )
            else:
                comparison["unchanged"].append(
                    f"Memory growth unchanged: {current_growth:.2f}MB vs {baseline_growth:.2f}MB baseline"
                )

        # Compare peak memory
        if "peak_memory_mb" in current and "peak_memory_mb" in baseline:
            current_peak = current["peak_memory_mb"]
            baseline_peak = baseline["peak_memory_mb"]

            change_ratio = (
                (current_peak - baseline_peak) / baseline_peak
                if baseline_peak != 0
                else 0
            )

            if change_ratio > self.regression_threshold:
                comparison["regressions"].append(
                    f"Peak memory regression: {current_peak:.2f}MB vs {baseline_peak:.2f}MB baseline ({change_ratio:.1%} increase)"
                )
            elif change_ratio < -self.improvement_threshold:
                comparison["improvements"].append(
                    f"Peak memory improvement: {current_peak:.2f}MB vs {baseline_peak:.2f}MB baseline ({abs(change_ratio):.1%} decrease)"
                )
            else:
                comparison["unchanged"].append(
                    f"Peak memory unchanged: {current_peak:.2f}MB vs {baseline_peak:.2f}MB baseline"
                )

        return comparison

    def _compare_performance_metrics(
        self, current: Dict[str, Any], baseline: Dict[str, Any], metric_name: str
    ) -> Dict[str, Any]:
        """Compare performance metrics (mean, median, p95, etc.)."""
        comparison = {"regressions": [], "improvements": [], "unchanged": []}

        # Compare mean
        if "mean" in current and "mean" in baseline:
            current_mean = current["mean"]
            baseline_mean = baseline["mean"]

            change_ratio = (
                (current_mean - baseline_mean) / baseline_mean
                if baseline_mean != 0
                else 0
            )

            if change_ratio > self.regression_threshold:
                comparison["regressions"].append(
                    f"{metric_name} mean regression: {current_mean:.4f}s vs {baseline_mean:.4f}s baseline ({change_ratio:.1%} increase)"
                )
            elif change_ratio < -self.improvement_threshold:
                comparison["improvements"].append(
                    f"{metric_name} mean improvement: {current_mean:.4f}s vs {baseline_mean:.4f}s baseline ({abs(change_ratio):.1%} decrease)"
                )
            else:
                comparison["unchanged"].append(
                    f"{metric_name} mean unchanged: {current_mean:.4f}s vs {baseline_mean:.4f}s baseline"
                )

        # Compare P95
        if "p95" in current and "p95" in baseline:
            current_p95 = current["p95"]
            baseline_p95 = baseline["p95"]

            change_ratio = (
                (current_p95 - baseline_p95) / baseline_p95 if baseline_p95 != 0 else 0
            )

            if change_ratio > self.regression_threshold:
                comparison["regressions"].append(
                    f"{metric_name} P95 regression: {current_p95:.4f}s vs {baseline_p95:.4f}s baseline ({change_ratio:.1%} increase)"
                )
            elif change_ratio < -self.improvement_threshold:
                comparison["improvements"].append(
                    f"{metric_name} P95 improvement: {current_p95:.4f}s vs {baseline_p95:.4f}s baseline ({abs(change_ratio):.1%} decrease)"
                )
            else:
                comparison["unchanged"].append(
                    f"{metric_name} P95 unchanged: {current_p95:.4f}s vs {baseline_p95:.4f}s baseline"
                )

        # Compare P99
        if "p99" in current and "p99" in baseline:
            current_p99 = current["p99"]
            baseline_p99 = baseline["p99"]

            change_ratio = (
                (current_p99 - baseline_p99) / baseline_p99 if baseline_p99 != 0 else 0
            )

            if change_ratio > self.regression_threshold:
                comparison["regressions"].append(
                    f"{metric_name} P99 regression: {current_p99:.4f}s vs {baseline_p99:.4f}s baseline ({change_ratio:.1%} increase)"
                )
            elif change_ratio < -self.improvement_threshold:
                comparison["improvements"].append(
                    f"{metric_name} P99 improvement: {current_p99:.4f}s vs {baseline_p99:.4f}s baseline ({abs(change_ratio):.1%} decrease)"
                )
            else:
                comparison["unchanged"].append(
                    f"{metric_name} P99 unchanged: {current_p99:.4f}s vs {baseline_p99:.4f}s baseline"
                )

        return comparison

    def _compare_batch_performance(
        self, current: List[Dict[str, Any]], baseline: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compare batch performance metrics."""
        comparison = {"regressions": [], "improvements": [], "unchanged": []}

        # Create lookup maps by batch size
        current_map = {item["batch_size"]: item for item in current}
        baseline_map = {item["batch_size"]: item for item in baseline}

        # Compare common batch sizes
        common_sizes = set(current_map.keys()) & set(baseline_map.keys())

        for batch_size in common_sizes:
            current_item = current_map[batch_size]
            baseline_item = baseline_map[batch_size]

            current_time = current_item["time_per_item"]
            baseline_time = baseline_item["time_per_item"]

            change_ratio = (
                (current_time - baseline_time) / baseline_time
                if baseline_time != 0
                else 0
            )

            if change_ratio > self.regression_threshold:
                comparison["regressions"].append(
                    f"Batch processing (size {batch_size}) regression: {current_time:.4f}s vs {baseline_time:.4f}s baseline ({change_ratio:.1%} increase)"
                )
            elif change_ratio < -self.improvement_threshold:
                comparison["improvements"].append(
                    f"Batch processing (size {batch_size}) improvement: {current_time:.4f}s vs {baseline_time:.4f}s baseline ({abs(change_ratio):.1%} decrease)"
                )
            else:
                comparison["unchanged"].append(
                    f"Batch processing (size {batch_size}) unchanged: {current_time:.4f}s vs {baseline_time:.4f}s baseline"
                )

        return comparison

    def _merge_metric_comparison(
        self, main: Dict[str, Any], sub: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Merge metric comparison results."""
        main["regressions"].extend(sub["regressions"])
        main["improvements"].extend(sub["improvements"])
        main["unchanged"].extend(sub["unchanged"])
        return main

    def generate_report(self, comparison: Dict[str, Any], format: str = "text") -> str:
        """Generate a formatted report of the comparison."""
        if format == "json":
            return json.dumps(comparison, indent=2)

        # Text format
        report = []
        report.append("Performance Comparison Report")
        report.append("=" * 40)
        report.append(f"Timestamp: {comparison['timestamp']}")
        report.append(f"Regression Threshold: {self.regression_threshold:.1%}")
        report.append("")

        # Summary
        report.append("Summary:")
        report.append(f"  Total Metrics: {comparison['summary']['total_metrics']}")
        report.append(f"  Regressions: {comparison['summary']['regression_count']}")
        report.append(f"  Improvements: {comparison['summary']['improvement_count']}")
        report.append(f"  Unchanged: {comparison['summary']['unchanged_count']}")
        report.append("")

        # Overall status
        if comparison["regression_detected"]:
            report.append("🚨 REGRESSION DETECTED")
        elif comparison["improvement_detected"]:
            report.append("✅ IMPROVEMENTS DETECTED")
        else:
            report.append("➖ NO SIGNIFICANT CHANGES")
        report.append("")

        # Regressions
        if comparison["regressions"]:
            report.append("⚠️  Performance Regressions:")
            for regression in comparison["regressions"]:
                report.append(f"  - {regression}")
            report.append("")

        # Improvements
        if comparison["improvements"]:
            report.append("🎉 Performance Improvements:")
            for improvement in comparison["improvements"]:
                report.append(f"  - {improvement}")
            report.append("")

        # Unchanged (only show if verbose)
        if comparison["unchanged"]:
            report.append("➖ Unchanged Metrics:")
            for unchanged in comparison["unchanged"]:
                report.append(f"  - {unchanged}")
            report.append("")

        return "\n".join(report)


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Compare performance metrics with baseline"
    )
    parser.add_argument(
        "--current", required=True, help="Current performance results file"
    )
    parser.add_argument(
        "--baseline", required=True, help="Baseline performance results file"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=20.0,
        help="Regression threshold percentage (default: 20%)",
    )
    parser.add_argument(
        "--format", choices=["text", "json"], default="text", help="Output format"
    )
    parser.add_argument("--output", help="Output file for report")

    args = parser.parse_args()

    # Create comparator
    comparator = PerformanceComparator(regression_threshold=args.threshold)

    # Load results
    current_results = comparator.load_results(args.current)
    baseline_results = comparator.load_results(args.baseline)

    # Compare metrics
    comparison = comparator.compare_metrics(current_results, baseline_results)

    # Generate report
    report = comparator.generate_report(comparison, args.format)

    # Output report
    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"Report saved to {args.output}")
    else:
        print(report)

    # Exit with appropriate code
    if comparison["regression_detected"]:
        print(
            f"\n❌ Performance regression detected! ({comparison['summary']['regression_count']} regressions)"
        )
        return 1
    elif comparison["improvement_detected"]:
        print(
            f"\n✅ Performance improvements detected! ({comparison['summary']['improvement_count']} improvements)"
        )
        return 0
    else:
        print("\n➖ No significant performance changes detected")
        return 0


if __name__ == "__main__":
    exit(main())
