# Security Scanning Implementation Plan

## Overview

This plan outlines the implementation of comprehensive security scanning for the PiWardrive project, focusing on:

1. Dependency vulnerability scanning
2. Static code analysis
3. Container security scanning
4. Secret detection
5. Integration with CI/CD pipeline

## Phase 1: Dependency Security Scanning

### Step 1: Setup Python Dependency Scanning

Create a script to scan Python dependencies using safety and pip-audit:

```python
#!/usr/bin/env python3
"""
PiWardrive Dependency Security Scanner

This script scans all Python dependencies for known security vulnerabilities
and generates a comprehensive security report.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPORT_DIR = Path("security_reports")


def run_command(cmd, env=None):
    """Run a command and return its output."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            env=env,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        return e.stdout  # Return stdout even if command fails as it may contain scan results


def run_pip_audit(requirements_file=None):
    """Run pip-audit on the current environment or a requirements file."""
    cmd = ["pip-audit", "--format", "json"]
    
    if requirements_file:
        cmd.extend(["-r", requirements_file])
    
    output = run_command(cmd)
    
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        print("Failed to parse pip-audit output as JSON")
        return {"error": "Failed to parse output", "raw_output": output}


def run_safety_check(requirements_file=None):
    """Run safety check on the current environment or a requirements file."""
    cmd = ["safety", "check", "--json"]
    
    if requirements_file:
        cmd.extend(["-r", requirements_file])
    else:
        cmd.append("--full-report")
    
    output = run_command(cmd)
    
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        print("Failed to parse safety output as JSON")
        return {"error": "Failed to parse output", "raw_output": output}


def check_npm_dependencies():
    """Run npm audit on the package.json file."""
    if not os.path.exists("webui/package.json"):
        return {"error": "No package.json found"}
    
    os.chdir("webui")
    cmd = ["npm", "audit", "--json"]
    output = run_command(cmd)
    os.chdir("..")
    
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        print("Failed to parse npm audit output as JSON")
        return {"error": "Failed to parse output", "raw_output": output}


def generate_report(pip_audit_results, safety_results, npm_results):
    """Generate a comprehensive security report from all scan results."""
    REPORT_DIR.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORT_DIR / f"dependency_security_report_{timestamp}.json"
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "python_dependencies": {
            "pip_audit": pip_audit_results,
            "safety": safety_results,
        },
        "javascript_dependencies": npm_results,
        "summary": {
            "python_vulnerabilities": count_python_vulnerabilities(pip_audit_results, safety_results),
            "javascript_vulnerabilities": count_npm_vulnerabilities(npm_results),
        }
    }
    
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"Security report generated: {report_file}")
    return report_file


def count_python_vulnerabilities(pip_audit_results, safety_results):
    """Count the number of Python vulnerabilities."""
    count = 0
    
    # Count pip-audit vulnerabilities
    try:
        if "vulnerabilities" in pip_audit_results:
            count += len(pip_audit_results["vulnerabilities"])
    except (TypeError, KeyError):
        pass
    
    # Count safety vulnerabilities (format may vary)
    try:
        if isinstance(safety_results, list):
            count += len(safety_results)
        elif "vulnerabilities" in safety_results:
            count += len(safety_results["vulnerabilities"])
    except (TypeError, KeyError):
        pass
    
    return count


def count_npm_vulnerabilities(npm_results):
    """Count the number of npm vulnerabilities."""
    try:
        if "vulnerabilities" in npm_results:
            return len(npm_results["vulnerabilities"])
    except (TypeError, KeyError):
        pass
    return 0


def main():
    parser = argparse.ArgumentParser(description="Scan dependencies for security vulnerabilities")
    parser.add_argument("--requirements", "-r", help="Path to requirements.txt file")
    parser.add_argument("--all", "-a", action="store_true", help="Scan all requirement files")
    parser.add_argument("--npm", "-n", action="store_true", help="Include npm dependencies")
    args = parser.parse_args()
    
    pip_audit_results = {}
    safety_results = {}
    npm_results = {}
    
    if args.all:
        # Find all requirements files
        req_files = list(Path(".").glob("**/requirements*.txt"))
        for req_file in req_files:
            print(f"Scanning {req_file}...")
            pip_audit_results[str(req_file)] = run_pip_audit(req_file)
            safety_results[str(req_file)] = run_safety_check(req_file)
    else:
        # Scan current environment or specified requirements file
        print("Scanning Python dependencies with pip-audit...")
        pip_audit_results = run_pip_audit(args.requirements)
        
        print("Scanning Python dependencies with safety...")
        safety_results = run_safety_check(args.requirements)
    
    if args.npm:
        print("Scanning npm dependencies...")
        npm_results = check_npm_dependencies()
    
    report_file = generate_report(pip_audit_results, safety_results, npm_results)
    
    # Check if any vulnerabilities were found
    summary = count_python_vulnerabilities(pip_audit_results, safety_results) + \
              count_npm_vulnerabilities(npm_results)
    
    print(f"Scan complete. Found {summary} potential security issues.")
    print(f"Full report available at: {report_file}")
    
    # Return non-zero exit code if vulnerabilities were found
    return 1 if summary > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
```

### Step 2: Setup JavaScript/Frontend Dependency Scanning

Add NPM audit to package.json scripts:

```json
{
  "scripts": {
    "security-scan": "npm audit --audit-level=moderate",
    "audit-fix": "npm audit fix"
  }
}
```

## Phase 2: Static Code Analysis Setup

### Step 1: Configure Bandit for Python Code Analysis

Create a `.bandit` configuration file:

```yaml
# .bandit
exclude_dirs:
  - tests
  - docs
  - static
  - templates
  - node_modules
  - venv
  - .venv

skips:
  # Skip assert statements in tests
  - B101

# Increase severity for certain issues
any_other_function_with_shell_equals_true:
  severity: HIGH

hardcoded_bind_all_interfaces:
  severity: MEDIUM
```

### Step 2: Create Python Static Analysis Script

```python
#!/usr/bin/env python3
"""
PiWardrive Static Code Security Analyzer

This script runs multiple static code analyzers on the codebase to identify
potential security issues and code quality problems.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPORT_DIR = Path("security_reports")


def run_bandit(path="."):
    """Run Bandit static code analyzer."""
    print("Running Bandit security analyzer...")
    cmd = ["bandit", "-r", path, "-f", "json", "-c", ".bandit"]
    output = subprocess.run(cmd, capture_output=True, text=True)
    
    try:
        return json.loads(output.stdout)
    except json.JSONDecodeError:
        return {"error": "Failed to parse Bandit output", "stdout": output.stdout, "stderr": output.stderr}


def run_semgrep(path="."):
    """Run Semgrep security analysis."""
    print("Running Semgrep security analyzer...")
    cmd = [
        "semgrep", 
        "--config=p/security-audit",
        "--config=p/python",
        "--json",
        path
    ]
    
    output = subprocess.run(cmd, capture_output=True, text=True)
    
    try:
        return json.loads(output.stdout)
    except json.JSONDecodeError:
        return {"error": "Failed to parse Semgrep output", "stdout": output.stdout, "stderr": output.stderr}


def run_trufflehog(path="."):
    """Run TruffleHog to find secrets."""
    print("Running TruffleHog secret scanner...")
    cmd = ["trufflehog", "filesystem", "--json", path]
    output = subprocess.run(cmd, capture_output=True, text=True)
    
    results = []
    for line in output.stdout.strip().split("\n"):
        if line:
            try:
                results.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    
    return results


def run_eslint(path="webui"):
    """Run ESLint for JavaScript security checks."""
    if not os.path.exists(f"{path}/package.json"):
        return {"error": "No package.json found"}
    
    print("Running ESLint security rules...")
    cmd = ["npm", "run", "lint", "--", "--format=json"]
    
    os.chdir(path)
    output = subprocess.run(cmd, capture_output=True, text=True)
    os.chdir("..")
    
    try:
        return json.loads(output.stdout)
    except json.JSONDecodeError:
        return {"error": "Failed to parse ESLint output", "stdout": output.stdout, "stderr": output.stderr}


def generate_report(bandit_results, semgrep_results, trufflehog_results, eslint_results):
    """Generate a comprehensive security report from all scan results."""
    REPORT_DIR.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORT_DIR / f"static_analysis_report_{timestamp}.json"
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "bandit": bandit_results,
        "semgrep": semgrep_results,
        "trufflehog": trufflehog_results,
        "eslint": eslint_results,
        "summary": {
            "bandit_issues": count_bandit_issues(bandit_results),
            "semgrep_issues": count_semgrep_issues(semgrep_results),
            "trufflehog_issues": len(trufflehog_results),
            "eslint_issues": count_eslint_issues(eslint_results),
        }
    }
    
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"Static analysis report generated: {report_file}")
    return report_file


def count_bandit_issues(results):
    """Count the number of Bandit issues."""
    try:
        if "results" in results:
            return len(results["results"])
    except (TypeError, KeyError):
        pass
    return 0


def count_semgrep_issues(results):
    """Count the number of Semgrep issues."""
    try:
        if "results" in results:
            return len(results["results"])
    except (TypeError, KeyError):
        pass
    return 0


def count_eslint_issues(results):
    """Count the number of ESLint issues."""
    try:
        if isinstance(results, list):
            return sum(len(file_result.get("messages", [])) for file_result in results)
    except (TypeError, AttributeError):
        pass
    return 0


def main():
    parser = argparse.ArgumentParser(description="Run static code security analysis")
    parser.add_argument("--path", "-p", default=".", help="Path to analyze")
    parser.add_argument("--skip", "-s", nargs="+", choices=["bandit", "semgrep", "trufflehog", "eslint"], 
                        help="Skip specific analyzers")
    args = parser.parse_args()
    
    skip = args.skip or []
    results = {}
    
    if "bandit" not in skip:
        results["bandit"] = run_bandit(args.path)
    
    if "semgrep" not in skip:
        results["semgrep"] = run_semgrep(args.path)
    
    if "trufflehog" not in skip:
        results["trufflehog"] = run_trufflehog(args.path)
    
    if "eslint" not in skip and os.path.exists("webui"):
        results["eslint"] = run_eslint("webui")
    
    report_file = generate_report(
        results.get("bandit", {}),
        results.get("semgrep", {}),
        results.get("trufflehog", []),
        results.get("eslint", {})
    )
    
    # Check if any issues were found
    total_issues = (
        count_bandit_issues(results.get("bandit", {})) +
        count_semgrep_issues(results.get("semgrep", {})) +
        len(results.get("trufflehog", [])) +
        count_eslint_issues(results.get("eslint", {}))
    )
    
    print(f"Analysis complete. Found {total_issues} potential security issues.")
    print(f"Full report available at: {report_file}")
    
    # Return non-zero exit code if issues were found
    return 1 if total_issues > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
```

## Phase 3: Container Security Scanning

### Step 1: Create Docker Security Scanning Script

```bash
#!/bin/bash
# Container Security Scanning Script

set -eo pipefail

REPORT_DIR="security_reports"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="${REPORT_DIR}/container_security_report_${TIMESTAMP}.json"

# Ensure report directory exists
mkdir -p "$REPORT_DIR"

# Check if required tools are installed
check_requirements() {
  local missing_tools=()
  
  if ! command -v trivy &> /dev/null; then
    missing_tools+=("trivy")
  fi
  
  if ! command -v docker &> /dev/null; then
    missing_tools+=("docker")
  fi
  
  if [ ${#missing_tools[@]} -ne 0 ]; then
    echo "Error: Required tools not found: ${missing_tools[*]}"
    echo "Please install missing tools and try again."
    exit 1
  fi
}

# Build Docker images if needed
build_images() {
  if [ "$BUILD_IMAGES" = true ]; then
    echo "Building Docker images..."
    cd docker/
    docker-compose build
    cd ..
  fi
}

# Scan Docker images with Trivy
scan_images() {
  local images
  images=$(docker images --format "{{.Repository}}:{{.Tag}}" | grep -v "<none>" | grep "piwardrive")
  
  if [ -z "$images" ]; then
    echo "No PiWardrive Docker images found. Build images first."
    exit 1
  fi
  
  echo "Found PiWardrive images: $images"
  
  local all_results=()
  
  for img in $images; do
    echo "Scanning image: $img"
    
    # Run Trivy scan and convert to JSON
    trivy_result=$(trivy image --format json --severity HIGH,CRITICAL "$img")
    
    # Add to results array
    all_results+=("\"$img\": $trivy_result")
  done
  
  # Generate final JSON report
  {
    echo "{"
    echo "  \"timestamp\": \"$(date -Iseconds)\","
    echo "  \"scan_results\": {"
    
    # Join all results with commas
    local IFS=","
    echo "    ${all_results[*]}"
    
    echo "  }"
    echo "}"
  } > "$REPORT_FILE"
  
  echo "Container security report generated: $REPORT_FILE"
}

# Main function
main() {
  # Parse arguments
  BUILD_IMAGES=false
  
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --build)
        BUILD_IMAGES=true
        shift
        ;;
      *)
        echo "Unknown option: $1"
        echo "Usage: $0 [--build]"
        exit 1
        ;;
    esac
  done
  
  check_requirements
  build_images
  scan_images
  
  echo "Container security scanning complete."
}

main "$@"
```

## Phase 4: CI/CD Integration

### Step 1: Create GitHub Actions Workflow File

```yaml
# .github/workflows/security-scan.yml
name: Security Scanning

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  schedule:
    # Run weekly on Monday at 1 AM
    - cron: '0 1 * * 1'

jobs:
  dependency-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r config/requirements-dev.txt
          pip install safety pip-audit
          
      - name: Scan Python dependencies
        run: |
          python tools/security/scan_dependencies.py --all
        continue-on-error: true
        
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install npm dependencies
        run: |
          cd webui
          npm ci
          
      - name: Scan npm dependencies
        run: |
          cd webui
          npm audit --json > ../security_reports/npm_audit_results.json || true
          
      - name: Upload scan results
        uses: actions/upload-artifact@v3
        with:
          name: dependency-scan-results
          path: security_reports/
          
  static-code-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install bandit semgrep trufflehog
          
      - name: Run static code analysis
        run: |
          python tools/security/static_analysis.py
        continue-on-error: true
        
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install npm dependencies
        run: |
          cd webui
          npm ci
          
      - name: Run ESLint
        run: |
          cd webui
          npm run lint || true
          
      - name: Upload scan results
        uses: actions/upload-artifact@v3
        with:
          name: static-analysis-results
          path: security_reports/
          
  container-scan:
    runs-on: ubuntu-latest
    needs: [dependency-scan, static-code-analysis]
    if: github.event_name != 'pull_request'
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
        
      - name: Build Docker images
        run: |
          cd docker/
          docker-compose build
          
      - name: Install Trivy
        run: |
          curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin v0.18.3
          
      - name: Scan Docker images
        run: |
          bash tools/security/scan_containers.sh
        continue-on-error: true
        
      - name: Upload scan results
        uses: actions/upload-artifact@v3
        with:
          name: container-scan-results
          path: security_reports/
          
  security-report:
    runs-on: ubuntu-latest
    needs: [dependency-scan, static-code-analysis, container-scan]
    if: always()
    steps:
      - name: Download all scan results
        uses: actions/download-artifact@v3
        with:
          path: all-security-reports
          
      - name: Generate comprehensive security report
        run: |
          echo "# PiWardrive Security Scan Report" > security_report.md
          echo "Generated on: $(date)" >> security_report.md
          echo "" >> security_report.md
          
          echo "## Dependency Scanning Results" >> security_report.md
          echo "See attached artifact for detailed results" >> security_report.md
          echo "" >> security_report.md
          
          echo "## Static Analysis Results" >> security_report.md
          echo "See attached artifact for detailed results" >> security_report.md
          echo "" >> security_report.md
          
          echo "## Container Security Results" >> security_report.md
          echo "See attached artifact for detailed results" >> security_report.md
          
      - name: Upload comprehensive report
        uses: actions/upload-artifact@v3
        with:
          name: comprehensive-security-report
          path: |
            security_report.md
            all-security-reports/
```

## Phase 5: Security Reporting Dashboard

### Step 1: Create a Security Dashboard Template

```html
<!-- templates/security_dashboard.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PiWardrive Security Dashboard</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        .vulnerability-high { color: #dc3545; }
        .vulnerability-medium { color: #fd7e14; }
        .vulnerability-low { color: #ffc107; }
        .card { margin-bottom: 20px; }
        .chart-container { height: 300px; }
    </style>
</head>
<body>
    <div class="container py-4">
        <h1 class="mb-4">PiWardrive Security Dashboard</h1>
        
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        Vulnerability Summary
                    </div>
                    <div class="card-body">
                        <canvas id="vulnerabilityChart" class="chart-container"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        Security Status
                    </div>
                    <div class="card-body">
                        <h5 id="securityStatus" class="card-title">Loading...</h5>
                        <p class="card-text">Last scan: <span id="lastScanDate">...</span></p>
                        <a href="#" class="btn btn-primary" id="runScanBtn">Run New Scan</a>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        Trends
                    </div>
                    <div class="card-body">
                        <canvas id="trendsChart" class="chart-container"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-12">
                <ul class="nav nav-tabs" id="securityTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" id="dependencies-tab" data-bs-toggle="tab" data-bs-target="#dependencies" type="button" role="tab">Dependencies</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="code-tab" data-bs-toggle="tab" data-bs-target="#code" type="button" role="tab">Code Analysis</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="container-tab" data-bs-toggle="tab" data-bs-target="#container" type="button" role="tab">Container</button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="secrets-tab" data-bs-toggle="tab" data-bs-target="#secrets" type="button" role="tab">Secrets</button>
                    </li>
                </ul>
                <div class="tab-content p-3 border border-top-0 rounded-bottom" id="securityTabContent">
                    <div class="tab-pane fade show active" id="dependencies" role="tabpanel">
                        <h4>Dependency Vulnerabilities</h4>
                        <div class="table-responsive">
                            <table class="table table-striped" id="dependencyTable">
                                <thead>
                                    <tr>
                                        <th>Package</th>
                                        <th>Version</th>
                                        <th>Severity</th>
                                        <th>Issue</th>
                                        <th>Fix Version</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td colspan="5" class="text-center">Loading data...</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="tab-pane fade" id="code" role="tabpanel">
                        <h4>Code Analysis Issues</h4>
                        <div class="table-responsive">
                            <table class="table table-striped" id="codeTable">
                                <thead>
                                    <tr>
                                        <th>File</th>
                                        <th>Line</th>
                                        <th>Issue</th>
                                        <th>Severity</th>
                                        <th>CWE</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td colspan="5" class="text-center">Loading data...</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="tab-pane fade" id="container" role="tabpanel">
                        <h4>Container Security Issues</h4>
                        <div class="table-responsive">
                            <table class="table table-striped" id="containerTable">
                                <thead>
                                    <tr>
                                        <th>Image</th>
                                        <th>CVE</th>
                                        <th>Package</th>
                                        <th>Severity</th>
                                        <th>Description</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td colspan="5" class="text-center">Loading data...</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div class="tab-pane fade" id="secrets" role="tabpanel">
                        <h4>Secret Detection</h4>
                        <div class="table-responsive">
                            <table class="table table-striped" id="secretsTable">
                                <thead>
                                    <tr>
                                        <th>File</th>
                                        <th>Line</th>
                                        <th>Type</th>
                                        <th>Risk</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td colspan="4" class="text-center">Loading data...</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="/static/js/security_dashboard.js"></script>
</body>
</html>
```

### Step 2: Create JavaScript for the Security Dashboard

```javascript
// static/js/security_dashboard.js

document.addEventListener('DOMContentLoaded', function() {
    // Load security data
    fetchSecurityData();
    
    // Add event listener for scan button
    document.getElementById('runScanBtn').addEventListener('click', function(e) {
        e.preventDefault();
        runSecurityScan();
    });
});

async function fetchSecurityData() {
    try {
        const response = await fetch('/api/security/reports/latest');
        const data = await response.json();
        
        if (data.success) {
            updateDashboard(data.data);
        } else {
            showError('Failed to load security data: ' + data.error.message);
        }
    } catch (error) {
        showError('Error fetching security data: ' + error.message);
    }
}

async function runSecurityScan() {
    const button = document.getElementById('runScanBtn');
    button.disabled = true;
    button.textContent = 'Scanning...';
    
    try {
        const response = await fetch('/api/security/scan', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Security scan started. This may take several minutes.');
            
            // Poll for results
            pollScanResults(data.data.scan_id);
        } else {
            showError('Failed to start security scan: ' + data.error.message);
            button.disabled = false;
            button.textContent = 'Run New Scan';
        }
    } catch (error) {
        showError('Error starting security scan: ' + error.message);
        button.disabled = false;
        button.textContent = 'Run New Scan';
    }
}

function pollScanResults(scanId) {
    const interval = setInterval(async () => {
        try {
            const response = await fetch(`/api/security/scan/${scanId}/status`);
            const data = await response.json();
            
            if (data.success) {
                if (data.data.status === 'completed') {
                    clearInterval(interval);
                    fetchSecurityData();
                    
                    const button = document.getElementById('runScanBtn');
                    button.disabled = false;
                    button.textContent = 'Run New Scan';
                } else if (data.data.status === 'failed') {
                    clearInterval(interval);
                    showError('Security scan failed: ' + data.data.error);
                    
                    const button = document.getElementById('runScanBtn');
                    button.disabled = false;
                    button.textContent = 'Run New Scan';
                }
                // else it's still running, keep polling
            } else {
                clearInterval(interval);
                showError('Failed to check scan status: ' + data.error.message);
                
                const button = document.getElementById('runScanBtn');
                button.disabled = false;
                button.textContent = 'Run New Scan';
            }
        } catch (error) {
            clearInterval(interval);
            showError('Error checking scan status: ' + error.message);
            
            const button = document.getElementById('runScanBtn');
            button.disabled = false;
            button.textContent = 'Run New Scan';
        }
    }, 5000); // Check every 5 seconds
}

function updateDashboard(data) {
    // Update last scan date
    document.getElementById('lastScanDate').textContent = new Date(data.timestamp).toLocaleString();
    
    // Update security status
    const statusElement = document.getElementById('securityStatus');
    const criticalCount = data.summary.critical || 0;
    const highCount = data.summary.high || 0;
    
    if (criticalCount > 0) {
        statusElement.textContent = 'Critical Issues Found';
        statusElement.className = 'card-title vulnerability-high';
    } else if (highCount > 0) {
        statusElement.textContent = 'High-Risk Issues Found';
        statusElement.className = 'card-title vulnerability-high';
    } else if (data.summary.medium > 0) {
        statusElement.textContent = 'Medium-Risk Issues Found';
        statusElement.className = 'card-title vulnerability-medium';
    } else if (data.summary.low > 0) {
        statusElement.textContent = 'Low-Risk Issues Found';
        statusElement.className = 'card-title vulnerability-low';
    } else {
        statusElement.textContent = 'No Issues Found';
        statusElement.className = 'card-title text-success';
    }
    
    // Create vulnerability chart
    createVulnerabilityChart(data.summary);
    
    // Create trends chart if history data is available
    if (data.history) {
        createTrendsChart(data.history);
    }
    
    // Update tables
    updateDependencyTable(data.dependencies || []);
    updateCodeTable(data.code_analysis || []);
    updateContainerTable(data.containers || []);
    updateSecretsTable(data.secrets || []);
}

function createVulnerabilityChart(summary) {
    const ctx = document.getElementById('vulnerabilityChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Critical', 'High', 'Medium', 'Low'],
            datasets: [{
                data: [
                    summary.critical || 0,
                    summary.high || 0,
                    summary.medium || 0,
                    summary.low || 0
                ],
                backgroundColor: [
                    '#dc3545', // Critical - Red
                    '#fd7e14', // High - Orange
                    '#ffc107', // Medium - Yellow
                    '#6c757d'  // Low - Grey
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

function createTrendsChart(history) {
    const ctx = document.getElementById('trendsChart').getContext('2d');
    
    const labels = history.map(item => {
        const date = new Date(item.timestamp);
        return date.toLocaleDateString();
    });
    
    const criticalData = history.map(item => item.summary.critical || 0);
    const highData = history.map(item => item.summary.high || 0);
    const mediumData = history.map(item => item.summary.medium || 0);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Critical',
                    data: criticalData,
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    fill: true
                },
                {
                    label: 'High',
                    data: highData,
                    borderColor: '#fd7e14',
                    backgroundColor: 'rgba(253, 126, 20, 0.1)',
                    fill: true
                },
                {
                    label: 'Medium',
                    data: mediumData,
                    borderColor: '#ffc107',
                    backgroundColor: 'rgba(255, 193, 7, 0.1)',
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    precision: 0
                }
            }
        }
    });
}

function updateDependencyTable(dependencies) {
    const tableBody = document.querySelector('#dependencyTable tbody');
    tableBody.innerHTML = '';
    
    if (dependencies.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="5" class="text-center">No vulnerabilities found</td>';
        tableBody.appendChild(row);
        return;
    }
    
    dependencies.forEach(dep => {
        const row = document.createElement('tr');
        
        const severityClass = getSeverityClass(dep.severity);
        
        row.innerHTML = `
            <td>${dep.package}</td>
            <td>${dep.installed_version}</td>
            <td class="${severityClass}">${dep.severity}</td>
            <td>${dep.description}</td>
            <td>${dep.fixed_version || 'N/A'}</td>
        `;
        
        tableBody.appendChild(row);
    });
}

function updateCodeTable(issues) {
    const tableBody = document.querySelector('#codeTable tbody');
    tableBody.innerHTML = '';
    
    if (issues.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="5" class="text-center">No issues found</td>';
        tableBody.appendChild(row);
        return;
    }
    
    issues.forEach(issue => {
        const row = document.createElement('tr');
        
        const severityClass = getSeverityClass(issue.severity);
        
        row.innerHTML = `
            <td>${issue.file}</td>
            <td>${issue.line}</td>
            <td>${issue.message}</td>
            <td class="${severityClass}">${issue.severity}</td>
            <td>${issue.cwe || 'N/A'}</td>
        `;
        
        tableBody.appendChild(row);
    });
}

function updateContainerTable(vulnerabilities) {
    const tableBody = document.querySelector('#containerTable tbody');
    tableBody.innerHTML = '';
    
    if (vulnerabilities.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="5" class="text-center">No vulnerabilities found</td>';
        tableBody.appendChild(row);
        return;
    }
    
    vulnerabilities.forEach(vuln => {
        const row = document.createElement('tr');
        
        const severityClass = getSeverityClass(vuln.severity);
        
        row.innerHTML = `
            <td>${vuln.image}</td>
            <td>${vuln.cve_id}</td>
            <td>${vuln.package}</td>
            <td class="${severityClass}">${vuln.severity}</td>
            <td>${vuln.description}</td>
        `;
        
        tableBody.appendChild(row);
    });
}

function updateSecretsTable(secrets) {
    const tableBody = document.querySelector('#secretsTable tbody');
    tableBody.innerHTML = '';
    
    if (secrets.length === 0) {
        const row = document.createElement('tr');
        row.innerHTML = '<td colspan="4" class="text-center">No secrets found</td>';
        tableBody.appendChild(row);
        return;
    }
    
    secrets.forEach(secret => {
        const row = document.createElement('tr');
        
        const riskClass = getSeverityClass(secret.risk);
        
        row.innerHTML = `
            <td>${secret.file}</td>
            <td>${secret.line}</td>
            <td>${secret.type}</td>
            <td class="${riskClass}">${secret.risk}</td>
        `;
        
        tableBody.appendChild(row);
    });
}

function getSeverityClass(severity) {
    severity = severity.toLowerCase();
    
    switch (severity) {
        case 'critical':
        case 'high':
            return 'vulnerability-high';
        case 'medium':
            return 'vulnerability-medium';
        case 'low':
            return 'vulnerability-low';
        default:
            return '';
    }
}

function showError(message) {
    console.error(message);
    alert('Error: ' + message);
}
```

### Step 3: Create API Endpoints for Security Dashboard

```python
# src/piwardrive/api/security_dashboard.py

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
import os
import json
import uuid
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from piwardrive.api.auth import AUTH_DEP

router = APIRouter(
    prefix="/security",
    tags=["Security"],
    dependencies=[Depends(AUTH_DEP)],
)

REPORT_DIR = Path("security_reports")
RUNNING_SCANS = {}

@router.get("/reports/latest")
async def get_latest_report():
    """Get the latest security report."""
    try:
        if not REPORT_DIR.exists():
            return {
                "success": False,
                "error": {
                    "message": "No security reports found"
                }
            }
        
        # Find the most recent reports of each type
        dep_reports = list(REPORT_DIR.glob("dependency_security_report_*.json"))
        static_reports = list(REPORT_DIR.glob("static_analysis_report_*.json"))
        container_reports = list(REPORT_DIR.glob("container_security_report_*.json"))
        
        if not dep_reports and not static_reports and not container_reports:
            return {
                "success": False,
                "error": {
                    "message": "No security reports found"
                }
            }
        
        # Get the most recent report of each type
        latest_dep = max(dep_reports, key=os.path.getmtime) if dep_reports else None
        latest_static = max(static_reports, key=os.path.getmtime) if static_reports else None
        latest_container = max(container_reports, key=os.path.getmtime) if container_reports else None
        
        # Load report data
        dep_data = load_json_file(latest_dep) if latest_dep else {}
        static_data = load_json_file(latest_static) if latest_static else {}
        container_data = load_json_file(latest_container) if latest_container else {}
        
        # Process and merge report data
        report = process_security_reports(dep_data, static_data, container_data)
        
        # Get historical data for trends
        history = load_historical_data()
        
        return {
            "success": True,
            "data": {
                **report,
                "history": history
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "message": str(e)
            }
        }

@router.post("/scan")
async def start_security_scan(background_tasks: BackgroundTasks):
    """Start a new security scan."""
    scan_id = str(uuid.uuid4())
    
    RUNNING_SCANS[scan_id] = {
        "status": "running",
        "started_at": datetime.now().isoformat(),
        "results": None
    }
    
    background_tasks.add_task(run_security_scan, scan_id)
    
    return {
        "success": True,
        "data": {
            "scan_id": scan_id,
            "status": "running",
            "started_at": RUNNING_SCANS[scan_id]["started_at"]
        }
    }

@router.get("/scan/{scan_id}/status")
async def get_scan_status(scan_id: str):
    """Get the status of a running security scan."""
    if scan_id not in RUNNING_SCANS:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return {
        "success": True,
        "data": RUNNING_SCANS[scan_id]
    }

def load_json_file(file_path):
    """Load and parse a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading {file_path}: {e}")
        return {}

def process_security_reports(dep_data, static_data, container_data):
    """Process and merge security report data."""
    # Get timestamp from most recent report
    timestamps = []
    if 'timestamp' in dep_data:
        timestamps.append(dep_data['timestamp'])
    if 'timestamp' in static_data:
        timestamps.append(static_data['timestamp'])
    if 'timestamp' in container_data:
        timestamps.append(container_data['timestamp'])
    
    timestamp = max(timestamps) if timestamps else datetime.now().isoformat()
    
    # Extract vulnerabilities from dependency report
    dependencies = []
    if 'python_dependencies' in dep_data:
        # Process pip-audit results
        if 'pip_audit' in dep_data['python_dependencies']:
            pip_audit = dep_data['python_dependencies']['pip_audit']
            if 'vulnerabilities' in pip_audit:
                for vuln in pip_audit['vulnerabilities']:
                    dependencies.append({
                        "package": vuln.get('package', {}).get('name', 'Unknown'),
                        "installed_version": vuln.get('package', {}).get('version', 'Unknown'),
                        "fixed_version": vuln.get('fix_version', 'Unknown'),
                        "severity": vuln.get('severity', 'Unknown'),
                        "description": vuln.get('advisory', {}).get('description', 'No description'),
                        "source": "pip-audit"
                    })
        
        # Process safety results
        if 'safety' in dep_data['python_dependencies']:
            safety = dep_data['python_dependencies']['safety']
            if isinstance(safety, list):
                for vuln in safety:
                    dependencies.append({
                        "package": vuln[0] if len(vuln) > 0 else 'Unknown',
                        "installed_version": vuln[1] if len(vuln) > 1 else 'Unknown',
                        "fixed_version": vuln[2] if len(vuln) > 2 else 'Unknown',
                        "severity": vuln[4] if len(vuln) > 4 else 'Unknown',
                        "description": vuln[3] if len(vuln) > 3 else 'No description',
                        "source": "safety"
                    })
    
    # Extract code analysis issues
    code_analysis = []
    if 'bandit' in static_data and 'results' in static_data['bandit']:
        for result in static_data['bandit']['results']:
            code_analysis.append({
                "file": result.get('filename', 'Unknown'),
                "line": result.get('line_number', 0),
                "message": result.get('issue_text', 'No description'),
                "severity": result.get('issue_severity', 'Unknown'),
                "cwe": result.get('cwe', 'N/A'),
                "source": "bandit"
            })
    
    if 'semgrep' in static_data and 'results' in static_data['semgrep']:
        for result in static_data['semgrep']['results']:
            code_analysis.append({
                "file": result.get('path', 'Unknown'),
                "line": result.get('start', {}).get('line', 0),
                "message": result.get('extra', {}).get('message', 'No description'),
                "severity": result.get('extra', {}).get('severity', 'Unknown'),
                "cwe": result.get('extra', {}).get('cwe', 'N/A'),
                "source": "semgrep"
            })
    
    # Extract container vulnerabilities
    containers = []
    if 'scan_results' in container_data:
        for image, results in container_data['scan_results'].items():
            if 'Results' in results:
                for result in results['Results']:
                    if 'Vulnerabilities' in result:
                        for vuln in result['Vulnerabilities']:
                            containers.append({
                                "image": image,
                                "cve_id": vuln.get('VulnerabilityID', 'Unknown'),
                                "package": vuln.get('PkgName', 'Unknown'),
                                "severity": vuln.get('Severity', 'Unknown'),
                                "description": vuln.get('Description', 'No description'),
                                "installed_version": vuln.get('InstalledVersion', 'Unknown'),
                                "fixed_version": vuln.get('FixedVersion', 'Unknown')
                            })
    
    # Extract secrets
    secrets = []
    if 'trufflehog' in static_data:
        for result in static_data['trufflehog']:
            secrets.append({
                "file": result.get('file', 'Unknown'),
                "line": result.get('line', 0),
                "type": result.get('type', 'Unknown'),
                "risk": result.get('risk', 'Medium'),
                "source": "trufflehog"
            })
    
    # Count issues by severity
    critical_count = sum(1 for item in dependencies if item['severity'].lower() == 'critical')
    critical_count += sum(1 for item in code_analysis if item['severity'].lower() == 'critical' or item['severity'].lower() == 'high')
    critical_count += sum(1 for item in containers if item['severity'].lower() == 'critical')
    
    high_count = sum(1 for item in dependencies if item['severity'].lower() == 'high')
    high_count += sum(1 for item in code_analysis if item['severity'].lower() == 'high')
    high_count += sum(1 for item in containers if item['severity'].lower() == 'high')
    
    medium_count = sum(1 for item in dependencies if item['severity'].lower() == 'medium')
    medium_count += sum(1 for item in code_analysis if item['severity'].lower() == 'medium')
    medium_count += sum(1 for item in containers if item['severity'].lower() == 'medium')
    medium_count += sum(1 for item in secrets if item['risk'].lower() == 'medium')
    
    low_count = sum(1 for item in dependencies if item['severity'].lower() == 'low')
    low_count += sum(1 for item in code_analysis if item['severity'].lower() == 'low')
    low_count += sum(1 for item in containers if item['severity'].lower() == 'low')
    low_count += sum(1 for item in secrets if item['risk'].lower() == 'low')
    
    return {
        "timestamp": timestamp,
        "dependencies": dependencies,
        "code_analysis": code_analysis,
        "containers": containers,
        "secrets": secrets,
        "summary": {
            "critical": critical_count,
            "high": high_count,
            "medium": medium_count,
            "low": low_count,
            "total": critical_count + high_count + medium_count + low_count
        }
    }

def load_historical_data():
    """Load historical security scan data for trends."""
    history = []
    
    # Get all dependency reports
    dep_reports = sorted(REPORT_DIR.glob("dependency_security_report_*.json"), key=os.path.getmtime)
    
    # Take up to 10 most recent reports for the trend
    for report_path in dep_reports[-10:]:
        report_data = load_json_file(report_path)
        
        # Extract summary data
        if 'python_dependencies' in report_data:
            pip_vulns = count_pip_audit_vulnerabilities(report_data['python_dependencies'].get('pip_audit', {}))
            safety_vulns = count_safety_vulnerabilities(report_data['python_dependencies'].get('safety', []))
            
            # Get npm vulnerabilities
            npm_vulns = count_npm_vulnerabilities(report_data.get('javascript_dependencies', {}))
            
            # Create summary
            timestamp = report_data.get('timestamp', '')
            history.append({
                "timestamp": timestamp,
                "summary": {
                    "critical": pip_vulns.get('critical', 0) + safety_vulns.get('critical', 0) + npm_vulns.get('critical', 0),
                    "high": pip_vulns.get('high', 0) + safety_vulns.get('high', 0) + npm_vulns.get('high', 0),
                    "medium": pip_vulns.get('medium', 0) + safety_vulns.get('medium', 0) + npm_vulns.get('medium', 0)
                }
            })
    
    return history

def count_pip_audit_vulnerabilities(pip_audit):
    """Count vulnerabilities from pip-audit by severity."""
    result = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    
    if 'vulnerabilities' in pip_audit:
        for vuln in pip_audit['vulnerabilities']:
            severity = vuln.get('severity', '').lower()
            if severity in result:
                result[severity] += 1
    
    return result

def count_safety_vulnerabilities(safety):
    """Count vulnerabilities from safety by severity."""
    result = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    
    if isinstance(safety, list):
        for vuln in safety:
            severity = vuln[4].lower() if len(vuln) > 4 else 'unknown'
            if severity in result:
                result[severity] += 1
    
    return result

def count_npm_vulnerabilities(npm_results):
    """Count vulnerabilities from npm audit by severity."""
    result = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    
    if 'vulnerabilities' in npm_results:
        for _, vuln in npm_results['vulnerabilities'].items():
            severity = vuln.get('severity', '').lower()
            if severity in result:
                result[severity] += 1
    
    return result

async def run_security_scan(scan_id):
    """Run a comprehensive security scan."""
    try:
        # Create report directory if it doesn't exist
        os.makedirs(REPORT_DIR, exist_ok=True)
        
        # Run dependency scan
        subprocess.run(
            ["python", "tools/security/scan_dependencies.py", "--all", "--npm"],
            check=True
        )
        
        # Run static code analysis
        subprocess.run(
            ["python", "tools/security/static_analysis.py"],
            check=True
        )
        
        # Run container scan if Docker is available
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
            subprocess.run(
                ["bash", "tools/security/scan_containers.sh"],
                check=True
            )
        except (subprocess.SubprocessError, FileNotFoundError):
            print("Docker not available, skipping container scan")
        
        # Update scan status
        RUNNING_SCANS[scan_id] = {
            **RUNNING_SCANS[scan_id],
            "status": "completed",
            "completed_at": datetime.now().isoformat()
        }
    except Exception as e:
        # Update scan status with error
        RUNNING_SCANS[scan_id] = {
            **RUNNING_SCANS[scan_id],
            "status": "failed",
            "error": str(e),
            "completed_at": datetime.now().isoformat()
        }
```
