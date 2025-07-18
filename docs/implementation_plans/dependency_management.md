# Dependency Management Implementation Plan

## Overview

This document provides a comprehensive implementation plan for establishing robust dependency management practices in the PiWardrive project. This system will automate dependency updates, security vulnerability monitoring, license compliance checking, and provide comprehensive documentation for all project dependencies.

## Current State Analysis

### Existing Dependency Management

- Basic package.json for Node.js dependencies
- pyproject.toml for Python dependencies
- Manual dependency updates
- No automated security scanning
- No license compliance checking
- Limited dependency documentation

### Gap Analysis

- No automated dependency update workflow
- No vulnerability scanning in CI/CD
- No license compliance monitoring
- No dependency impact analysis
- No security advisory integration
- No automated dependency pruning

## Implementation Strategy

### Phase 1: Automated Dependency Updates (Week 1-2)

#### 1.1 Dependabot Configuration

**File: `.github/dependabot.yml`**

```yaml
version: 2
updates:
  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
    open-pull-requests-limit: 10
    reviewers:
      - "maintainer-team"
    assignees:
      - "security-team"
    commit-message:
      prefix: "deps"
      include: "scope"
    labels:
      - "dependencies"
      - "python"
    milestone: "Security Updates"
    rebase-strategy: "auto"
    target-branch: "develop"
    
  # JavaScript dependencies
  - package-ecosystem: "npm"
    directory: "/webui"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "09:00"
    open-pull-requests-limit: 10
    reviewers:
      - "frontend-team"
    assignees:
      - "security-team"
    commit-message:
      prefix: "deps"
      include: "scope"
    labels:
      - "dependencies"
      - "javascript"
    milestone: "Security Updates"
    rebase-strategy: "auto"
    target-branch: "develop"
    
  # Docker dependencies
  - package-ecosystem: "docker"
    directory: "/docker"
    schedule:
      interval: "weekly"
      day: "tuesday"
      time: "09:00"
    reviewers:
      - "devops-team"
    assignees:
      - "security-team"
    commit-message:
      prefix: "deps"
      include: "scope"
    labels:
      - "dependencies"
      - "docker"
    
  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "wednesday"
      time: "09:00"
    reviewers:
      - "devops-team"
    commit-message:
      prefix: "ci"
      include: "scope"
    labels:
      - "dependencies"
      - "github-actions"
```

#### 1.2 Dependency Update Automation Script

**File: `scripts/update_dependencies.py`**

```python
#!/usr/bin/env python3
"""
Automated dependency update and security checking script.
"""

import subprocess
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import requests
from packaging import version

class DependencyManager:
    """Manages dependency updates and security checks."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = project_root
        self.report_data = {
            "timestamp": datetime.now().isoformat(),
            "python_updates": [],
            "javascript_updates": [],
            "security_vulnerabilities": [],
            "license_issues": []
        }
    
    def check_python_dependencies(self) -> Dict[str, Any]:
        """Check Python dependencies for updates and vulnerabilities."""
        print("Checking Python dependencies...")
        
        # Check for outdated packages
        try:
            result = subprocess.run(
                ["pip", "list", "--outdated", "--format=json"],
                capture_output=True,
                text=True,
                check=True
            )
            outdated_packages = json.loads(result.stdout)
            
            for package in outdated_packages:
                update_info = {
                    "name": package["name"],
                    "current_version": package["version"],
                    "latest_version": package["latest_version"],
                    "type": package["latest_filetype"]
                }
                self.report_data["python_updates"].append(update_info)
                
        except subprocess.CalledProcessError as e:
            print(f"Error checking Python dependencies: {e}")
        
        # Security vulnerability check
        self.check_python_vulnerabilities()
        
        return self.report_data
    
    def check_python_vulnerabilities(self):
        """Check for security vulnerabilities in Python packages."""
        try:
            result = subprocess.run(
                ["pip-audit", "--format=json"],
                capture_output=True,
                text=True,
                check=True
            )
            
            vulnerabilities = json.loads(result.stdout)
            
            for vuln in vulnerabilities:
                vuln_info = {
                    "package": vuln["name"],
                    "version": vuln["version"],
                    "vulnerability_id": vuln["id"],
                    "description": vuln["description"],
                    "severity": vuln.get("severity", "Unknown"),
                    "fixed_version": vuln.get("fix_version")
                }
                self.report_data["security_vulnerabilities"].append(vuln_info)
                
        except subprocess.CalledProcessError:
            print("pip-audit not available, skipping Python vulnerability check")
    
    def check_javascript_dependencies(self) -> Dict[str, Any]:
        """Check JavaScript dependencies for updates and vulnerabilities."""
        print("Checking JavaScript dependencies...")
        
        webui_path = os.path.join(self.project_root, "webui")
        if not os.path.exists(webui_path):
            print("WebUI directory not found, skipping JavaScript checks")
            return self.report_data
        
        # Check for outdated packages
        try:
            result = subprocess.run(
                ["npm", "outdated", "--json"],
                cwd=webui_path,
                capture_output=True,
                text=True
            )
            
            if result.stdout:
                outdated_packages = json.loads(result.stdout)
                
                for package_name, package_info in outdated_packages.items():
                    update_info = {
                        "name": package_name,
                        "current_version": package_info["current"],
                        "wanted_version": package_info["wanted"],
                        "latest_version": package_info["latest"],
                        "type": package_info.get("type", "dependency")
                    }
                    self.report_data["javascript_updates"].append(update_info)
                    
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            print("Error checking JavaScript dependencies")
        
        # Security vulnerability check
        self.check_javascript_vulnerabilities(webui_path)
        
        return self.report_data
    
    def check_javascript_vulnerabilities(self, webui_path: str):
        """Check for security vulnerabilities in JavaScript packages."""
        try:
            result = subprocess.run(
                ["npm", "audit", "--json"],
                cwd=webui_path,
                capture_output=True,
                text=True
            )
            
            if result.stdout:
                audit_result = json.loads(result.stdout)
                
                for vuln_id, vuln_info in audit_result.get("vulnerabilities", {}).items():
                    vuln_data = {
                        "package": vuln_info["name"],
                        "severity": vuln_info["severity"],
                        "description": vuln_info["title"],
                        "affected_versions": vuln_info.get("range", ""),
                        "patched_versions": vuln_info.get("fixAvailable", {}).get("version", ""),
                        "cwe": vuln_info.get("cwe", [])
                    }
                    self.report_data["security_vulnerabilities"].append(vuln_data)
                    
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            print("Error checking JavaScript vulnerabilities")
    
    def check_license_compliance(self) -> Dict[str, Any]:
        """Check license compliance for all dependencies."""
        print("Checking license compliance...")
        
        # Python license check
        try:
            result = subprocess.run(
                ["pip-licenses", "--format=json"],
                capture_output=True,
                text=True,
                check=True
            )
            
            python_licenses = json.loads(result.stdout)
            
            for package in python_licenses:
                license_name = package.get("License", "Unknown")
                if self.is_license_problematic(license_name):
                    license_issue = {
                        "package": package["Name"],
                        "version": package["Version"],
                        "license": license_name,
                        "ecosystem": "python",
                        "issue": "Potentially problematic license"
                    }
                    self.report_data["license_issues"].append(license_issue)
                    
        except subprocess.CalledProcessError:
            print("pip-licenses not available, skipping Python license check")
        
        # JavaScript license check
        webui_path = os.path.join(self.project_root, "webui")
        if os.path.exists(webui_path):
            try:
                result = subprocess.run(
                    ["npm", "ls", "--json"],
                    cwd=webui_path,
                    capture_output=True,
                    text=True
                )
                
                if result.stdout:
                    npm_tree = json.loads(result.stdout)
                    self.check_npm_licenses(npm_tree.get("dependencies", {}))
                    
            except (subprocess.CalledProcessError, json.JSONDecodeError):
                print("Error checking JavaScript licenses")
        
        return self.report_data
    
    def check_npm_licenses(self, dependencies: Dict[str, Any]):
        """Recursively check npm package licenses."""
        for package_name, package_info in dependencies.items():
            license_name = package_info.get("license", "Unknown")
            
            if self.is_license_problematic(license_name):
                license_issue = {
                    "package": package_name,
                    "version": package_info.get("version", "Unknown"),
                    "license": license_name,
                    "ecosystem": "javascript",
                    "issue": "Potentially problematic license"
                }
                self.report_data["license_issues"].append(license_issue)
            
            # Recursively check dependencies
            if "dependencies" in package_info:
                self.check_npm_licenses(package_info["dependencies"])
    
    def is_license_problematic(self, license_name: str) -> bool:
        """Check if a license is potentially problematic."""
        problematic_licenses = [
            "GPL-3.0",
            "GPL-2.0",
            "AGPL-3.0",
            "AGPL-1.0",
            "LGPL-3.0",
            "LGPL-2.1",
            "Copyleft",
            "Unknown"
        ]
        
        return any(problematic in license_name for problematic in problematic_licenses)
    
    def update_dependencies(self, auto_update: bool = False) -> bool:
        """Update dependencies based on the report."""
        print("Updating dependencies...")
        
        success = True
        
        # Update Python dependencies
        if self.report_data["python_updates"]:
            print("Updating Python dependencies...")
            for update in self.report_data["python_updates"]:
                package_name = update["name"]
                latest_version = update["latest_version"]
                
                if auto_update:
                    try:
                        subprocess.run(
                            ["pip", "install", "--upgrade", package_name],
                            check=True
                        )
                        print(f"Updated {package_name} to {latest_version}")
                    except subprocess.CalledProcessError:
                        print(f"Failed to update {package_name}")
                        success = False
                else:
                    print(f"Available update: {package_name} -> {latest_version}")
        
        # Update JavaScript dependencies
        webui_path = os.path.join(self.project_root, "webui")
        if os.path.exists(webui_path) and self.report_data["javascript_updates"]:
            print("Updating JavaScript dependencies...")
            
            if auto_update:
                try:
                    subprocess.run(
                        ["npm", "update"],
                        cwd=webui_path,
                        check=True
                    )
                    print("Updated JavaScript dependencies")
                except subprocess.CalledProcessError:
                    print("Failed to update JavaScript dependencies")
                    success = False
            else:
                for update in self.report_data["javascript_updates"]:
                    package_name = update["name"]
                    latest_version = update["latest_version"]
                    print(f"Available update: {package_name} -> {latest_version}")
        
        return success
    
    def generate_report(self) -> str:
        """Generate a comprehensive dependency report."""
        report = f"""
# Dependency Management Report

**Generated:** {self.report_data['timestamp']}

## Python Dependencies

### Updates Available ({len(self.report_data['python_updates'])})
"""
        
        for update in self.report_data["python_updates"]:
            report += f"- **{update['name']}**: {update['current_version']} → {update['latest_version']}\n"
        
        report += f"""
## JavaScript Dependencies

### Updates Available ({len(self.report_data['javascript_updates'])})
"""
        
        for update in self.report_data["javascript_updates"]:
            report += f"- **{update['name']}**: {update['current_version']} → {update['latest_version']}\n"
        
        report += f"""
## Security Vulnerabilities

### Found ({len(self.report_data['security_vulnerabilities'])})
"""
        
        for vuln in self.report_data["security_vulnerabilities"]:
            report += f"- **{vuln['package']}**: {vuln.get('severity', 'Unknown')} - {vuln.get('description', 'No description')}\n"
        
        report += f"""
## License Issues

### Found ({len(self.report_data['license_issues'])})
"""
        
        for issue in self.report_data["license_issues"]:
            report += f"- **{issue['package']}**: {issue['license']} ({issue['ecosystem']})\n"
        
        return report
    
    def save_report(self, filename: str = "dependency_report.md"):
        """Save the dependency report to a file."""
        report_content = self.generate_report()
        
        with open(filename, "w") as f:
            f.write(report_content)
        
        print(f"Report saved to {filename}")

def main():
    """Main function to run dependency management tasks."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Dependency Management Tool")
    parser.add_argument("--check", action="store_true", help="Check for updates and vulnerabilities")
    parser.add_argument("--update", action="store_true", help="Update dependencies")
    parser.add_argument("--auto-update", action="store_true", help="Automatically update dependencies")
    parser.add_argument("--licenses", action="store_true", help="Check license compliance")
    parser.add_argument("--report", action="store_true", help="Generate dependency report")
    parser.add_argument("--output", default="dependency_report.md", help="Output file for report")
    
    args = parser.parse_args()
    
    manager = DependencyManager()
    
    if args.check:
        manager.check_python_dependencies()
        manager.check_javascript_dependencies()
    
    if args.licenses:
        manager.check_license_compliance()
    
    if args.update:
        manager.update_dependencies(auto_update=args.auto_update)
    
    if args.report:
        manager.save_report(args.output)
    
    if not any([args.check, args.licenses, args.update, args.report]):
        # Default: run all checks
        manager.check_python_dependencies()
        manager.check_javascript_dependencies()
        manager.check_license_compliance()
        manager.save_report(args.output)

if __name__ == "__main__":
    main()
```

### Phase 2: CI/CD Integration (Week 2-3)

#### 2.1 GitHub Actions Workflow

**File: `.github/workflows/dependency-management.yml`**

```yaml
name: Dependency Management

on:
  schedule:
    # Run every Monday at 9:00 AM UTC
    - cron: '0 9 * * 1'
  workflow_dispatch:
  pull_request:
    paths:
      - 'pyproject.toml'
      - 'webui/package.json'
      - 'webui/package-lock.json'

jobs:
  dependency-check:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: 'webui/package-lock.json'
      
      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pip-audit pip-licenses
          pip install -r requirements.txt
      
      - name: Install JavaScript dependencies
        run: |
          cd webui
          npm ci
      
      - name: Run dependency checks
        run: |
          python scripts/update_dependencies.py --check --licenses --report
      
      - name: Upload dependency report
        uses: actions/upload-artifact@v3
        with:
          name: dependency-report
          path: dependency_report.md
      
      - name: Security audit (Python)
        run: |
          pip-audit --format=json --output=python-audit.json
        continue-on-error: true
      
      - name: Security audit (JavaScript)
        run: |
          cd webui
          npm audit --json > ../javascript-audit.json
        continue-on-error: true
      
      - name: Upload security reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: |
            python-audit.json
            javascript-audit.json
      
      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('dependency_report.md', 'utf8');
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Dependency Management Report\n\n${report}`
            });

  license-check:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install license checker
        run: |
          python -m pip install --upgrade pip
          pip install pip-licenses
      
      - name: Check Python licenses
        run: |
          pip-licenses --format=json --output-file=python-licenses.json
      
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      - name: Install JavaScript license checker
        run: |
          npm install -g license-checker
      
      - name: Check JavaScript licenses
        run: |
          cd webui
          license-checker --json --out ../javascript-licenses.json
      
      - name: Upload license reports
        uses: actions/upload-artifact@v3
        with:
          name: license-reports
          path: |
            python-licenses.json
            javascript-licenses.json

  update-dependencies:
    runs-on: ubuntu-latest
    if: github.event_name == 'schedule'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pip-audit pip-licenses
          pip install -r requirements.txt
          cd webui && npm ci
      
      - name: Update dependencies
        run: |
          python scripts/update_dependencies.py --update --auto-update --report
      
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          commit-message: 'deps: automated dependency updates'
          title: 'Automated Dependency Updates'
          body: |
            This PR contains automated dependency updates.
            
            Please review the changes and test thoroughly before merging.
            
            ## Changes
            - Updated Python dependencies
            - Updated JavaScript dependencies
            
            ## Reports
            See the dependency report artifact for details.
          branch: dependency-updates
          delete-branch: true
```

#### 2.2 Pre-commit Hooks

**File: `.pre-commit-config.yaml`**

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: debug-statements
      - id: requirements-txt-fixer
  
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3.11
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]
  
  - repo: https://github.com/pycqa/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml"]
  
  - repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.3.2
    hooks:
      - id: python-safety-dependencies-check
  
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.44.0
    hooks:
      - id: eslint
        files: \.(js|jsx|ts|tsx)$
        types: [file]
        additional_dependencies:
          - eslint@8.44.0
          - eslint-plugin-react@7.32.2
          - eslint-plugin-react-hooks@4.6.0
```

### Phase 3: Advanced Monitoring (Week 3-4)

#### 3.1 Dependency Dashboard

**File: `webui/src/components/DependencyDashboard.jsx`**

```javascript
import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Alert, AlertDescription } from './ui/alert';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { RefreshCw, AlertTriangle, CheckCircle, Package } from 'lucide-react';

const DependencyDashboard = () => {
  const [dependencyData, setDependencyData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchDependencyData = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/dependencies/status');
      if (!response.ok) {
        throw new Error('Failed to fetch dependency data');
      }
      const data = await response.json();
      setDependencyData(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDependencyData();
  }, []);

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical':
        return 'destructive';
      case 'high':
        return 'destructive';
      case 'medium':
        return 'warning';
      case 'low':
        return 'secondary';
      default:
        return 'secondary';
    }
  };

  const getLicenseColor = (license) => {
    const problematicLicenses = ['GPL-3.0', 'GPL-2.0', 'AGPL-3.0', 'Unknown'];
    return problematicLicenses.some(l => license?.includes(l)) ? 'destructive' : 'secondary';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <RefreshCw className="h-8 w-8 animate-spin" />
        <span className="ml-2">Loading dependency data...</span>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertTriangle className="h-4 w-4" />
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold">Dependency Management</h2>
        <Button onClick={fetchDependencyData} disabled={loading}>
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Dependencies</CardTitle>
            <Package className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {dependencyData?.summary?.total_dependencies || 0}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Updates Available</CardTitle>
            <RefreshCw className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {dependencyData?.summary?.updates_available || 0}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Security Issues</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {dependencyData?.summary?.security_issues || 0}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">License Issues</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {dependencyData?.summary?.license_issues || 0}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Tabs */}
      <Tabs defaultValue="updates" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="updates">Updates</TabsTrigger>
          <TabsTrigger value="security">Security</TabsTrigger>
          <TabsTrigger value="licenses">Licenses</TabsTrigger>
          <TabsTrigger value="analysis">Analysis</TabsTrigger>
        </TabsList>

        <TabsContent value="updates">
          <Card>
            <CardHeader>
              <CardTitle>Available Updates</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {dependencyData?.updates?.map((update, index) => (
                  <div key={index} className="flex items-center justify-between p-3 border rounded">
                    <div>
                      <div className="font-medium">{update.name}</div>
                      <div className="text-sm text-muted-foreground">
                        {update.current_version} → {update.latest_version}
                      </div>
                    </div>
                    <Badge variant="outline">
                      {update.ecosystem || 'Unknown'}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="security">
          <Card>
            <CardHeader>
              <CardTitle>Security Vulnerabilities</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {dependencyData?.vulnerabilities?.map((vuln, index) => (
                  <div key={index} className="p-3 border rounded">
                    <div className="flex items-center justify-between mb-2">
                      <div className="font-medium">{vuln.package}</div>
                      <Badge variant={getSeverityColor(vuln.severity)}>
                        {vuln.severity}
                      </Badge>
                    </div>
                    <div className="text-sm text-muted-foreground mb-2">
                      {vuln.description}
                    </div>
                    {vuln.fixed_version && (
                      <div className="text-sm">
                        <strong>Fixed in:</strong> {vuln.fixed_version}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="licenses">
          <Card>
            <CardHeader>
              <CardTitle>License Compliance</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {dependencyData?.license_issues?.map((issue, index) => (
                  <div key={index} className="flex items-center justify-between p-3 border rounded">
                    <div>
                      <div className="font-medium">{issue.package}</div>
                      <div className="text-sm text-muted-foreground">
                        Version: {issue.version}
                      </div>
                    </div>
                    <Badge variant={getLicenseColor(issue.license)}>
                      {issue.license}
                    </Badge>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analysis">
          <Card>
            <CardHeader>
              <CardTitle>Dependency Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-medium mb-2">Top Dependencies by Size</h4>
                    <div className="space-y-2">
                      {dependencyData?.analysis?.top_by_size?.map((dep, index) => (
                        <div key={index} className="flex justify-between text-sm">
                          <span>{dep.name}</span>
                          <span>{dep.size}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div>
                    <h4 className="font-medium mb-2">Dependency Tree Depth</h4>
                    <div className="space-y-2">
                      {dependencyData?.analysis?.tree_depth?.map((dep, index) => (
                        <div key={index} className="flex justify-between text-sm">
                          <span>{dep.name}</span>
                          <span>Level {dep.depth}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default DependencyDashboard;
```

#### 3.2 Backend API for Dependency Data

**File: `src/piwardrive/api/dependencies.py`**

```python
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta
import json
import os
from ..services.dependency_service import DependencyService

dependency_bp = Blueprint('dependencies', __name__)
dependency_service = DependencyService()

@dependency_bp.route('/status')
def get_dependency_status():
    """Get current dependency status."""
    try:
        status = dependency_service.get_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dependency_bp.route('/updates')
def get_available_updates():
    """Get available dependency updates."""
    try:
        updates = dependency_service.get_available_updates()
        return jsonify(updates)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dependency_bp.route('/vulnerabilities')
def get_vulnerabilities():
    """Get security vulnerabilities."""
    try:
        vulnerabilities = dependency_service.get_vulnerabilities()
        return jsonify(vulnerabilities)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dependency_bp.route('/licenses')
def get_license_issues():
    """Get license compliance issues."""
    try:
        issues = dependency_service.get_license_issues()
        return jsonify(issues)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dependency_bp.route('/update', methods=['POST'])
def update_dependency():
    """Update a specific dependency."""
    try:
        data = request.json
        package_name = data.get('package')
        version = data.get('version')
        ecosystem = data.get('ecosystem', 'python')
        
        if not package_name:
            return jsonify({'error': 'Package name is required'}), 400
        
        result = dependency_service.update_package(package_name, version, ecosystem)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dependency_bp.route('/scan', methods=['POST'])
def trigger_scan():
    """Trigger a dependency scan."""
    try:
        scan_result = dependency_service.run_scan()
        return jsonify(scan_result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### Phase 4: Documentation and Maintenance (Week 4)

#### 4.1 Dependency Documentation Generator

**File: `scripts/generate_dependency_docs.py`**

```python
#!/usr/bin/env python3
"""
Generate comprehensive dependency documentation.
"""

import json
import subprocess
from datetime import datetime
from typing import Dict, List, Any

class DependencyDocumentationGenerator:
    """Generate documentation for project dependencies."""
    
    def __init__(self, output_file: str = "docs/dependencies.md"):
        self.output_file = output_file
        self.documentation = {
            "timestamp": datetime.now().isoformat(),
            "python_dependencies": [],
            "javascript_dependencies": [],
            "system_dependencies": []
        }
    
    def generate_python_docs(self):
        """Generate documentation for Python dependencies."""
        try:
            # Get installed packages
            result = subprocess.run(
                ["pip", "freeze", "--format=json"],
                capture_output=True,
                text=True,
                check=True
            )
            
            packages = json.loads(result.stdout)
            
            for package in packages:
                self.documentation["python_dependencies"].append({
                    "name": package["name"],
                    "version": package["version"],
                    "description": self.get_package_description(package["name"]),
                    "license": self.get_package_license(package["name"]),
                    "homepage": self.get_package_homepage(package["name"])
                })
                
        except subprocess.CalledProcessError:
            print("Error generating Python dependency documentation")
    
    def generate_javascript_docs(self):
        """Generate documentation for JavaScript dependencies."""
        try:
            result = subprocess.run(
                ["npm", "ls", "--json", "--depth=0"],
                cwd="webui",
                capture_output=True,
                text=True,
                check=True
            )
            
            npm_data = json.loads(result.stdout)
            dependencies = npm_data.get("dependencies", {})
            
            for name, info in dependencies.items():
                self.documentation["javascript_dependencies"].append({
                    "name": name,
                    "version": info.get("version", "Unknown"),
                    "description": info.get("description", ""),
                    "license": info.get("license", "Unknown"),
                    "homepage": info.get("homepage", "")
                })
                
        except subprocess.CalledProcessError:
            print("Error generating JavaScript dependency documentation")
    
    def get_package_description(self, package_name: str) -> str:
        """Get package description from PyPI."""
        try:
            result = subprocess.run(
                ["pip", "show", package_name],
                capture_output=True,
                text=True,
                check=True
            )
            
            lines = result.stdout.split('\n')
            for line in lines:
                if line.startswith('Summary:'):
                    return line.replace('Summary: ', '')
            
            return "No description available"
            
        except subprocess.CalledProcessError:
            return "No description available"
    
    def get_package_license(self, package_name: str) -> str:
        """Get package license information."""
        try:
            result = subprocess.run(
                ["pip", "show", package_name],
                capture_output=True,
                text=True,
                check=True
            )
            
            lines = result.stdout.split('\n')
            for line in lines:
                if line.startswith('License:'):
                    return line.replace('License: ', '')
            
            return "Unknown"
            
        except subprocess.CalledProcessError:
            return "Unknown"
    
    def get_package_homepage(self, package_name: str) -> str:
        """Get package homepage URL."""
        try:
            result = subprocess.run(
                ["pip", "show", package_name],
                capture_output=True,
                text=True,
                check=True
            )
            
            lines = result.stdout.split('\n')
            for line in lines:
                if line.startswith('Home-page:'):
                    return line.replace('Home-page: ', '')
            
            return ""
            
        except subprocess.CalledProcessError:
            return ""
    
    def generate_markdown(self) -> str:
        """Generate markdown documentation."""
        markdown = f"""# Dependency Documentation

**Generated:** {self.documentation['timestamp']}

## Python Dependencies ({len(self.documentation['python_dependencies'])})

| Package | Version | Description | License | Homepage |
|---------|---------|-------------|---------|----------|
"""
        
        for dep in self.documentation['python_dependencies']:
            homepage = f"[Link]({dep['homepage']})" if dep['homepage'] else "N/A"
            markdown += f"| {dep['name']} | {dep['version']} | {dep['description']} | {dep['license']} | {homepage} |\n"
        
        markdown += f"""
## JavaScript Dependencies ({len(self.documentation['javascript_dependencies'])})

| Package | Version | Description | License | Homepage |
|---------|---------|-------------|---------|----------|
"""
        
        for dep in self.documentation['javascript_dependencies']:
            homepage = f"[Link]({dep['homepage']})" if dep['homepage'] else "N/A"
            markdown += f"| {dep['name']} | {dep['version']} | {dep['description']} | {dep['license']} | {homepage} |\n"
        
        markdown += """
## Maintenance Notes

### Update Schedule
- **Python Dependencies**: Weekly security updates, monthly feature updates
- **JavaScript Dependencies**: Weekly security updates, monthly feature updates

### Security Policy
- All dependencies are scanned for vulnerabilities before updates
- Critical security updates are applied immediately
- Non-critical updates are reviewed before application

### License Compliance
- All dependencies are checked for license compatibility
- Problematic licenses are flagged and alternatives are sought
- License information is maintained in this documentation

### Monitoring
- Dependency updates are monitored through GitHub Dependabot
- Security vulnerabilities are tracked through automated scanning
- License compliance is verified during CI/CD pipeline
"""
        
        return markdown
    
    def save_documentation(self):
        """Save the generated documentation to file."""
        self.generate_python_docs()
        self.generate_javascript_docs()
        
        markdown_content = self.generate_markdown()
        
        with open(self.output_file, 'w') as f:
            f.write(markdown_content)
        
        print(f"Documentation saved to {self.output_file}")

def main():
    generator = DependencyDocumentationGenerator()
    generator.save_documentation()

if __name__ == "__main__":
    main()
```

## Implementation Checklist

### Week 1-2: Basic Setup

- [ ] Configure Dependabot for automated updates
- [ ] Create dependency update script
- [ ] Set up basic vulnerability scanning
- [ ] Configure license checking tools
- [ ] Create GitHub Actions workflow

### Week 2-3: CI/CD Integration

- [ ] Implement dependency checks in CI/CD
- [ ] Set up security scanning pipeline
- [ ] Configure automated PR creation
- [ ] Add pre-commit hooks for dependency checking
- [ ] Set up artifact storage for reports

### Week 3-4: Advanced Features

- [ ] Create dependency dashboard UI
- [ ] Implement backend API for dependency data
- [ ] Add dependency analysis and reporting
- [ ] Set up monitoring and alerting
- [ ] Create documentation generator

### Week 4: Documentation and Testing

- [ ] Generate comprehensive dependency documentation
- [ ] Create maintenance procedures
- [ ] Write tests for dependency management tools
- [ ] Set up monitoring dashboards
- [ ] Create user guides and documentation

## Configuration Files

### Requirements Files

**File: `requirements-dev.txt`**

```txt
pip-audit>=2.6.0
pip-licenses>=4.3.0
safety>=2.3.0
bandit>=1.7.5
pre-commit>=3.3.0
```

### Package Configuration

**File: `pyproject.toml` (additions)**

```toml
[tool.bandit]
exclude_dirs = ["tests", "venv"]
skips = ["B101", "B601"]

[tool.pip-audit]
require-hashes = false
vulnerability-service = "osv"
```

### Environment Variables

```bash
# .env additions
DEPENDENCY_CHECK_ENABLED=true
SECURITY_SCAN_ENABLED=true
LICENSE_CHECK_ENABLED=true
DEPENDENCY_AUTO_UPDATE=false
DEPENDENCY_NOTIFICATION_EMAIL=admin@piwardrive.com
DEPENDENCY_WEBHOOK_URL=https://hooks.slack.com/services/...
```

## Success Metrics

1. **Update Coverage**: 95% of dependencies have automated update monitoring
2. **Security Response Time**: Critical vulnerabilities addressed within 24 hours
3. **License Compliance**: 100% of dependencies have known licenses
4. **Documentation Accuracy**: Dependency documentation 90% complete and current
5. **Automation Efficiency**: 80% reduction in manual dependency management time

## Monitoring and Maintenance

### Daily Tasks

- Review dependency security alerts
- Check for critical updates
- Monitor license compliance status

### Weekly Tasks

- Review automated dependency updates
- Analyze dependency health reports
- Update documentation if needed

### Monthly Tasks

- Comprehensive dependency audit
- License compliance review
- Performance impact analysis of updates
- Update dependency management procedures

This comprehensive dependency management system will provide the PiWardrive project with automated dependency updates, security vulnerability monitoring, license compliance checking, and comprehensive documentation, significantly reducing maintenance overhead while improving security posture.
