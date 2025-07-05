#!/bin/bash
# Test Coverage Tracking Script for PiWardrive
# This script runs tests with coverage tracking and sends metrics to monitoring systems

set -euo pipefail

# Configuration
COVERAGE_THRESHOLD=80
COVERAGE_TARGET=90
COVERAGE_FILE="coverage.json"
COVERAGE_HTML_DIR="htmlcov"
COVERAGE_REPORT="coverage_report.txt"
MONITORING_URL="${MONITORING_URL:-}"
MONITORING_API_KEY="${MONITORING_API_KEY:-}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check if required tools are installed
check_dependencies() {
    log_step "Checking dependencies..."
    
    if ! command -v python &> /dev/null; then
        log_error "Python is not installed"
        exit 1
    fi
    
    if ! python -c "import coverage" &> /dev/null; then
        log_info "Installing coverage.py..."
        pip install coverage[toml]
    fi
    
    if ! python -c "import pytest" &> /dev/null; then
        log_info "Installing pytest..."
        pip install pytest pytest-cov
    fi
    
    log_info "All dependencies are available"
}

# Run tests with coverage
run_tests_with_coverage() {
    log_step "Running tests with coverage..."
    
    # Clean up previous coverage data
    rm -f .coverage
    rm -rf "$COVERAGE_HTML_DIR"
    
    # Run tests with coverage
    python -m pytest \
        --cov=src \
        --cov=server \
        --cov=webui \
        --cov-report=json:"$COVERAGE_FILE" \
        --cov-report=html:"$COVERAGE_HTML_DIR" \
        --cov-report=term-missing \
        --cov-report=term:skip-covered \
        --cov-fail-under="$COVERAGE_THRESHOLD" \
        tests/ \
        -v \
        --tb=short \
        --durations=10 \
        || true  # Don't exit on test failures, we want to process coverage
    
    log_info "Test execution completed"
}

# Extract coverage metrics
extract_coverage_metrics() {
    log_step "Extracting coverage metrics..."
    
    if [ ! -f "$COVERAGE_FILE" ]; then
        log_error "Coverage file not found: $COVERAGE_FILE"
        return 1
    fi
    
    # Extract overall coverage percentage
    COVERAGE_PERCENT=$(python -c "
import json
with open('$COVERAGE_FILE', 'r') as f:
    data = json.load(f)
    print(f\"{data['totals']['percent_covered']:.2f}\")
")
    
    # Extract detailed metrics
    LINES_COVERED=$(python -c "
import json
with open('$COVERAGE_FILE', 'r') as f:
    data = json.load(f)
    print(data['totals']['covered_lines'])
")
    
    LINES_TOTAL=$(python -c "
import json
with open('$COVERAGE_FILE', 'r') as f:
    data = json.load(f)
    print(data['totals']['num_statements'])
")
    
    LINES_MISSING=$(python -c "
import json
with open('$COVERAGE_FILE', 'r') as f:
    data = json.load(f)
    print(data['totals']['missing_lines'])
")
    
    BRANCHES_COVERED=$(python -c "
import json
with open('$COVERAGE_FILE', 'r') as f:
    data = json.load(f)
    print(data['totals'].get('covered_branches', 0))
")
    
    BRANCHES_TOTAL=$(python -c "
import json
with open('$COVERAGE_FILE', 'r') as f:
    data = json.load(f)
    print(data['totals'].get('num_branches', 0))
")
    
    log_info "Coverage: $COVERAGE_PERCENT%"
    log_info "Lines: $LINES_COVERED/$LINES_TOTAL"
    log_info "Branches: $BRANCHES_COVERED/$BRANCHES_TOTAL"
    
    # Export for other scripts
    export COVERAGE_PERCENT
    export LINES_COVERED
    export LINES_TOTAL
    export LINES_MISSING
    export BRANCHES_COVERED
    export BRANCHES_TOTAL
}

# Generate coverage report
generate_coverage_report() {
    log_step "Generating coverage report..."
    
    cat > "$COVERAGE_REPORT" << EOF
PiWardrive Test Coverage Report
Generated: $(date)

Overall Coverage: $COVERAGE_PERCENT%
Target Coverage: $COVERAGE_TARGET%
Threshold: $COVERAGE_THRESHOLD%

Lines Coverage:
- Covered: $LINES_COVERED
- Total: $LINES_TOTAL
- Missing: $LINES_MISSING

Branch Coverage:
- Covered: $BRANCHES_COVERED
- Total: $BRANCHES_TOTAL

Status: $(if (( $(echo "$COVERAGE_PERCENT >= $COVERAGE_THRESHOLD" | bc -l) )); then echo "PASS"; else echo "FAIL"; fi)
EOF
    
    # Add file-by-file breakdown
    echo "" >> "$COVERAGE_REPORT"
    echo "File-by-file Coverage:" >> "$COVERAGE_REPORT"
    echo "=====================" >> "$COVERAGE_REPORT"
    
    python -c "
import json
with open('$COVERAGE_FILE', 'r') as f:
    data = json.load(f)
    files = data['files']
    for file_path, file_data in sorted(files.items()):
        coverage = file_data['summary']['percent_covered']
        lines = f\"{file_data['summary']['covered_lines']}/{file_data['summary']['num_statements']}\"
        print(f'{file_path}: {coverage:.1f}% ({lines})')
" >> "$COVERAGE_REPORT"
    
    log_info "Coverage report generated: $COVERAGE_REPORT"
}

# Check coverage thresholds
check_coverage_thresholds() {
    log_step "Checking coverage thresholds..."
    
    # Check overall threshold
    if (( $(echo "$COVERAGE_PERCENT >= $COVERAGE_THRESHOLD" | bc -l) )); then
        log_info "✅ Coverage threshold met: $COVERAGE_PERCENT% >= $COVERAGE_THRESHOLD%"
        THRESHOLD_STATUS="PASS"
    else
        log_error "❌ Coverage threshold not met: $COVERAGE_PERCENT% < $COVERAGE_THRESHOLD%"
        THRESHOLD_STATUS="FAIL"
    fi
    
    # Check target
    if (( $(echo "$COVERAGE_PERCENT >= $COVERAGE_TARGET" | bc -l) )); then
        log_info "🎯 Coverage target achieved: $COVERAGE_PERCENT% >= $COVERAGE_TARGET%"
        TARGET_STATUS="PASS"
    else
        log_warn "⚠️ Coverage target not achieved: $COVERAGE_PERCENT% < $COVERAGE_TARGET%"
        TARGET_STATUS="FAIL"
    fi
    
    # Check for significant changes
    if [ -f "previous_coverage.txt" ]; then
        PREVIOUS_COVERAGE=$(cat previous_coverage.txt)
        COVERAGE_CHANGE=$(echo "$COVERAGE_PERCENT - $PREVIOUS_COVERAGE" | bc -l)
        
        if (( $(echo "$COVERAGE_CHANGE < -1" | bc -l) )); then
            log_error "📉 Coverage decreased significantly: $COVERAGE_CHANGE%"
        elif (( $(echo "$COVERAGE_CHANGE > 1" | bc -l) )); then
            log_info "📈 Coverage improved: +$COVERAGE_CHANGE%"
        else
            log_info "📊 Coverage stable: $COVERAGE_CHANGE%"
        fi
    fi
    
    # Save current coverage for next run
    echo "$COVERAGE_PERCENT" > previous_coverage.txt
    
    export THRESHOLD_STATUS
    export TARGET_STATUS
}

# Send metrics to monitoring system
send_metrics_to_monitoring() {
    if [ -z "$MONITORING_URL" ]; then
        log_warn "No monitoring URL configured, skipping metrics upload"
        return 0
    fi
    
    log_step "Sending metrics to monitoring system..."
    
    # Prepare metrics payload
    TIMESTAMP=$(date +%s)
    METRICS_PAYLOAD=$(cat << EOF
{
    "timestamp": $TIMESTAMP,
    "metrics": {
        "test_coverage_percent": $COVERAGE_PERCENT,
        "test_coverage_lines_covered": $LINES_COVERED,
        "test_coverage_lines_total": $LINES_TOTAL,
        "test_coverage_lines_missing": $LINES_MISSING,
        "test_coverage_branches_covered": $BRANCHES_COVERED,
        "test_coverage_branches_total": $BRANCHES_TOTAL,
        "test_coverage_threshold_met": $(if [ "$THRESHOLD_STATUS" = "PASS" ]; then echo "1"; else echo "0"; fi),
        "test_coverage_target_met": $(if [ "$TARGET_STATUS" = "PASS" ]; then echo "1"; else echo "0"; fi)
    },
    "tags": {
        "service": "piwardrive",
        "environment": "${ENVIRONMENT:-development}",
        "branch": "$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')",
        "commit": "$(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
    }
}
EOF
)
    
    # Send to monitoring system
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST "$MONITORING_URL" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $MONITORING_API_KEY" \
        -d "$METRICS_PAYLOAD")
    
    if [ "$HTTP_STATUS" = "200" ] || [ "$HTTP_STATUS" = "201" ]; then
        log_info "✅ Metrics sent successfully to monitoring system"
    else
        log_error "❌ Failed to send metrics (HTTP $HTTP_STATUS)"
    fi
}

# Send Slack notification
send_slack_notification() {
    if [ -z "${SLACK_WEBHOOK_URL:-}" ]; then
        log_warn "No Slack webhook configured, skipping notification"
        return 0
    fi
    
    log_step "Sending Slack notification..."
    
    # Determine color based on status
    if [ "$THRESHOLD_STATUS" = "PASS" ]; then
        COLOR="good"
        EMOJI="✅"
    else
        COLOR="danger"
        EMOJI="❌"
    fi
    
    # Create Slack payload
    SLACK_PAYLOAD=$(cat << EOF
{
    "attachments": [
        {
            "color": "$COLOR",
            "title": "$EMOJI PiWardrive Test Coverage Report",
            "fields": [
                {
                    "title": "Coverage",
                    "value": "$COVERAGE_PERCENT%",
                    "short": true
                },
                {
                    "title": "Threshold",
                    "value": "$COVERAGE_THRESHOLD%",
                    "short": true
                },
                {
                    "title": "Lines Covered",
                    "value": "$LINES_COVERED/$LINES_TOTAL",
                    "short": true
                },
                {
                    "title": "Status",
                    "value": "$THRESHOLD_STATUS",
                    "short": true
                }
            ],
            "footer": "PiWardrive CI/CD",
            "ts": $(date +%s)
        }
    ]
}
EOF
)
    
    # Send to Slack
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
        -X POST "$SLACK_WEBHOOK_URL" \
        -H "Content-Type: application/json" \
        -d "$SLACK_PAYLOAD")
    
    if [ "$HTTP_STATUS" = "200" ]; then
        log_info "✅ Slack notification sent successfully"
    else
        log_error "❌ Failed to send Slack notification (HTTP $HTTP_STATUS)"
    fi
}

# Generate badge
generate_coverage_badge() {
    log_step "Generating coverage badge..."
    
    # Determine badge color
    if (( $(echo "$COVERAGE_PERCENT >= 90" | bc -l) )); then
        BADGE_COLOR="brightgreen"
    elif (( $(echo "$COVERAGE_PERCENT >= 75" | bc -l) )); then
        BADGE_COLOR="green"
    elif (( $(echo "$COVERAGE_PERCENT >= 60" | bc -l) )); then
        BADGE_COLOR="yellow"
    else
        BADGE_COLOR="red"
    fi
    
    # Generate shield.io badge URL
    BADGE_URL="https://img.shields.io/badge/Coverage-${COVERAGE_PERCENT}%25-${BADGE_COLOR}"
    
    # Save badge URL
    echo "$BADGE_URL" > coverage_badge_url.txt
    
    log_info "Coverage badge URL saved: coverage_badge_url.txt"
}

# Main execution
main() {
    log_info "Starting test coverage tracking for PiWardrive"
    
    # Check dependencies
    check_dependencies
    
    # Run tests with coverage
    run_tests_with_coverage
    
    # Extract metrics
    extract_coverage_metrics
    
    # Generate report
    generate_coverage_report
    
    # Check thresholds
    check_coverage_thresholds
    
    # Send metrics
    send_metrics_to_monitoring
    
    # Send notifications
    send_slack_notification
    
    # Generate badge
    generate_coverage_badge
    
    # Final status
    if [ "$THRESHOLD_STATUS" = "PASS" ]; then
        log_info "🎉 Coverage tracking completed successfully"
        exit 0
    else
        log_error "💥 Coverage tracking completed with failures"
        exit 1
    fi
}

# Trap signals for cleanup
trap 'log_error "Coverage tracking interrupted"; exit 1' INT TERM

# Run main function
main "$@"
