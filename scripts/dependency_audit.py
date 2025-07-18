#!/usr/bin/env python3
"""
Dependency Audit Script for PiWardrive

This script helps maintain dependency health by:
- Checking for outdated packages
- Scanning for security vulnerabilities
- Analyzing dependency sizes and complexity
- Generating dependency reports
- Sending security alerts
"""

import argparse
import json
import logging
import os
import smtplib
import subprocess
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, List

import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_command(
    cmd: List[str], capture_output: bool = True
) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            cmd, capture_output=capture_output, text=True, check=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        sys.exit(1)


def check_outdated_packages() -> Dict[str, Any]:
    """Check for outdated packages using pip list --outdated."""
    print("Checking for outdated packages...")

    result = run_command(["pip", "list", "--outdated", "--format=json"])
    outdated = json.loads(result.stdout) if result.stdout else []

    return {
        "outdated_count": len(outdated),
        "packages": outdated,
        "timestamp": datetime.now().isoformat(),
    }


def run_security_scan() -> Dict[str, Any]:
    """Run security vulnerability scans."""
    print("Running security vulnerability scans...")

    # Run pip-audit
    pip_audit_result = None
    try:
        result = run_command(["pip-audit", "--format=json"])
        pip_audit_result = json.loads(result.stdout) if result.stdout else []
    except Exception as e:
        print(f"pip-audit scan failed: {e}")
        pip_audit_result = {"error": str(e)}

    # Run safety check
    safety_result = None
    try:
        result = run_command(["safety", "check", "--json"])
        safety_result = json.loads(result.stdout) if result.stdout else []
    except Exception as e:
        print(f"safety check failed: {e}")
        safety_result = {"error": str(e)}

    return {
        "pip_audit": pip_audit_result,
        "safety": safety_result,
        "timestamp": datetime.now().isoformat(),
    }


def analyze_dependency_size() -> Dict[str, Any]:
    """Analyze dependency sizes and installation footprint."""
    print("Analyzing dependency sizes...")

    # Get package sizes using pip show
    result = run_command(["pip", "list", "--format=json"])
    packages = json.loads(result.stdout) if result.stdout else []

    package_info = []
    for pkg in packages:
        try:
            show_result = run_command(["pip", "show", pkg["name"]])
            lines = show_result.stdout.split("\n")
            info = {"name": pkg["name"], "version": pkg["version"]}

            for line in lines:
                if line.startswith("Requires:"):
                    deps = line.split(":", 1)[1].strip()
                    info["dependencies"] = deps.split(", ") if deps else []
                elif line.startswith("Required-by:"):
                    required_by = line.split(":", 1)[1].strip()
                    info["required_by"] = required_by.split(", ") if required_by else []

            package_info.append(info)
        except Exception as e:
            print(f"Failed to get info for {pkg['name']}: {e}")

    return {
        "total_packages": len(packages),
        "package_details": package_info,
        "timestamp": datetime.now().isoformat(),
    }


def generate_dependency_tree() -> Dict[str, Any]:
    """Generate dependency tree using pipdeptree."""
    print("Generating dependency tree...")

    try:
        result = run_command(["pipdeptree", "--json"])
        tree = json.loads(result.stdout) if result.stdout else []
    except Exception as e:
        print(f"pipdeptree failed: {e}")
        # Try to install pipdeptree if not available
        try:
            run_command(["pip", "install", "pipdeptree"])
            result = run_command(["pipdeptree", "--json"])
            tree = json.loads(result.stdout) if result.stdout else []
        except Exception as e2:
            print(f"Failed to install or run pipdeptree: {e2}")
            tree = {"error": str(e2)}

    return {"dependency_tree": tree, "timestamp": datetime.now().isoformat()}


def check_license_compliance() -> Dict[str, Any]:
    """Check license compatibility for all dependencies."""
    print("Checking license compliance...")

    try:
        result = run_command(["pip-licenses", "--format=json"])
        licenses = json.loads(result.stdout) if result.stdout else []
    except Exception as e:
        print(f"pip-licenses failed: {e}")
        # Try to install pip-licenses if not available
        try:
            run_command(["pip", "install", "pip-licenses"])
            result = run_command(["pip-licenses", "--format=json"])
            licenses = json.loads(result.stdout) if result.stdout else []
        except Exception as e2:
            print(f"Failed to install or run pip-licenses: {e2}")
            licenses = {"error": str(e2)}

    # Analyze license compatibility
    problematic_licenses = ["GPL", "AGPL", "LGPL"]
    license_issues = []

    if isinstance(licenses, list):
        for pkg in licenses:
            if any(
                prob in pkg.get("License", "").upper() for prob in problematic_licenses
            ):
                license_issues.append(
                    {
                        "package": pkg.get("Name"),
                        "license": pkg.get("License"),
                        "issue": "Potentially incompatible license",
                    }
                )

    return {
        "all_licenses": licenses,
        "license_issues": license_issues,
        "timestamp": datetime.now().isoformat(),
    }


def generate_full_report() -> Dict[str, Any]:
    """Generate a comprehensive dependency audit report."""
    print("Generating comprehensive dependency audit report...")

    report = {
        "audit_timestamp": datetime.now().isoformat(),
        "outdated_packages": check_outdated_packages(),
        "security_vulnerabilities": run_security_scan(),
        "dependency_analysis": analyze_dependency_size(),
        "dependency_tree": generate_dependency_tree(),
        "license_compliance": check_license_compliance(),
    }

    return report


def send_security_alert(vulnerabilities: List[Dict[str, Any]]):
    """Send security alert via multiple channels."""
    if not vulnerabilities:
        return

    logger.info(f"Sending security alerts for {len(vulnerabilities)} vulnerabilities")

    # Format alert message
    alert_message = format_alert_message(vulnerabilities)

    # Send to Slack
    send_slack_alert(alert_message)

    # Send email alert
    send_email_alert(vulnerabilities)

    # Send to monitoring system
    send_monitoring_alert(vulnerabilities)


def format_alert_message(vulnerabilities: List[Dict[str, Any]]) -> str:
    """Format alert message for notifications."""
    message = f"🚨 Security Alert: {len(vulnerabilities)} vulnerabilities found\n\n"

    for vuln in vulnerabilities[:5]:  # Show top 5
        package = vuln.get("package", "unknown")
        advisory = vuln.get("advisory", "No description")
        severity = vuln.get("severity", "Unknown")
        message += f"  - {package}: {advisory} (Severity: {severity})\n"

    if len(vulnerabilities) > 5:
        message += f"  ... and {len(vulnerabilities) - 5} more\n"

    message += f"\nTimestamp: {datetime.now().isoformat()}"

    return message


def send_slack_alert(message: str):
    """Send alert to Slack."""
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    if not webhook_url:
        logger.warning("Slack webhook URL not configured")
        return

    try:
        payload = {
            "text": message,
            "username": "Dependency Audit Bot",
            "icon_emoji": ":warning:",
        }

        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()

        logger.info("Slack alert sent successfully")

    except Exception as e:
        logger.error(f"Failed to send Slack alert: {e}")


def send_email_alert(vulnerabilities: List[Dict[str, Any]]):
    """Send email alert."""
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL")
    to_emails = os.getenv("SECURITY_ALERT_EMAILS", "").split(",")

    if not all([smtp_server, smtp_username, smtp_password, from_email, to_emails[0]]):
        logger.warning("Email configuration not complete")
        return

    try:
        # Create message
        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = ", ".join(to_emails)
        msg["Subject"] = f"Security Alert: {len(vulnerabilities)} vulnerabilities found"

        # Create HTML body
        html_body = create_html_report(vulnerabilities)
        msg.attach(MIMEText(html_body, "html"))

        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()

        logger.info("Email alert sent successfully")

    except Exception as e:
        logger.error(f"Failed to send email alert: {e}")


def create_html_report(vulnerabilities: List[Dict[str, Any]]) -> str:
    """Create HTML report for email."""
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .alert {{ background-color: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px; }}
            .vulnerability {{ margin: 10px 0; padding: 10px; background-color: #fff3cd; border-left: 4px solid #ffc107; }}
            .high {{ border-left-color: #dc3545; }}
            .critical {{ border-left-color: #6f42c1; }}
        </style>
    </head>
    <body>
        <h2>🚨 Security Vulnerability Report</h2>

        <div class="alert">
            <strong>Total Vulnerabilities Found: {len(vulnerabilities)}</strong>
        </div>

        <h3>Vulnerability Details</h3>
    """

    for vuln in vulnerabilities:
        severity = vuln.get("severity", "unknown").lower()
        html += f"""
        <div class="vulnerability {severity}">
            <strong>{vuln.get('package', 'unknown')}</strong><br>
            {vuln.get('advisory', 'No description')}<br>
            <small>Severity: {vuln.get('severity', 'Unknown')}</small><br>
            <small>Vulnerability ID: {vuln.get('id', 'N/A')}</small>
        </div>
        """

    html += f"""
        <p><strong>Timestamp:</strong> {datetime.now().isoformat()}</p>
    </body>
    </html>
    """

    return html


def send_monitoring_alert(vulnerabilities: List[Dict[str, Any]]):
    """Send alert to monitoring system."""
    monitoring_url = os.getenv("MONITORING_WEBHOOK_URL")
    if not monitoring_url:
        logger.warning("Monitoring webhook URL not configured")
        return

    try:
        payload = {
            "metric": "security_vulnerabilities",
            "value": len(vulnerabilities),
            "timestamp": datetime.now().timestamp(),
            "tags": {
                "high_severity": sum(
                    1 for v in vulnerabilities if v.get("severity") == "high"
                ),
                "critical_severity": sum(
                    1 for v in vulnerabilities if v.get("severity") == "critical"
                ),
                "source": "dependency_audit",
            },
        }

        response = requests.post(monitoring_url, json=payload, timeout=10)
        response.raise_for_status()

        logger.info("Monitoring alert sent successfully")

    except Exception as e:
        logger.error(f"Failed to send monitoring alert: {e}")


def run_enhanced_security_scan() -> Dict[str, Any]:
    """Run enhanced security vulnerability scans with alerting."""
    print("Running enhanced security vulnerability scans...")

    vulnerabilities = []

    # Run pip-audit
    try:
        result = run_command(["pip-audit", "--format=json"])
        if result.stdout:
            audit_data = json.loads(result.stdout)
            if isinstance(audit_data, list):
                vulnerabilities.extend(audit_data)
    except Exception as e:
        logger.error(f"pip-audit scan failed: {e}")

    # Run safety check
    try:
        result = run_command(["safety", "check", "--json"])
        if result.stdout:
            safety_data = json.loads(result.stdout)
            if isinstance(safety_data, list):
                vulnerabilities.extend(safety_data)
    except Exception as e:
        logger.error(f"safety check failed: {e}")

    # Run bandit for source code security
    try:
        result = run_command(["bandit", "-r", "src/", "-f", "json"])
        if result.stdout:
            bandit_data = json.loads(result.stdout)
            bandit_issues = bandit_data.get("results", [])
            # Convert bandit issues to vulnerability format
            for issue in bandit_issues:
                if issue.get("issue_severity") in ["HIGH", "MEDIUM"]:
                    vulnerabilities.append(
                        {
                            "package": "source_code",
                            "advisory": issue.get(
                                "issue_text", "Security issue in source code"
                            ),
                            "severity": issue.get("issue_severity", "unknown").lower(),
                            "file": issue.get("filename", "unknown"),
                            "line": issue.get("line_number", "unknown"),
                        }
                    )
    except Exception as e:
        logger.error(f"bandit scan failed: {e}")

    # Send alerts if vulnerabilities found
    if vulnerabilities:
        send_security_alert(vulnerabilities)

    return {
        "vulnerabilities": vulnerabilities,
        "vulnerability_count": len(vulnerabilities),
        "timestamp": datetime.now().isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(description="PiWardrive Dependency Audit Tool")
    parser.add_argument(
        "--outdated", action="store_true", help="Check for outdated packages"
    )
    parser.add_argument(
        "--security", action="store_true", help="Run security vulnerability scans"
    )
    parser.add_argument(
        "--enhanced-security",
        action="store_true",
        help="Run enhanced security scans with alerting",
    )
    parser.add_argument("--size", action="store_true", help="Analyze dependency sizes")
    parser.add_argument("--tree", action="store_true", help="Generate dependency tree")
    parser.add_argument(
        "--licenses", action="store_true", help="Check license compliance"
    )
    parser.add_argument(
        "--full", action="store_true", help="Generate full audit report"
    )
    parser.add_argument(
        "--output", type=str, help="Output file for report (JSON format)"
    )
    parser.add_argument(
        "--no-alerts", action="store_true", help="Skip sending security alerts"
    )

    args = parser.parse_args()

    # Default to full report if no specific checks requested
    if not any(
        [
            args.outdated,
            args.security,
            args.enhanced_security,
            args.size,
            args.tree,
            args.licenses,
        ]
    ):
        args.full = True

    report = {}

    if args.outdated or args.full:
        report["outdated_packages"] = check_outdated_packages()

    if args.security or args.full:
        report["security_vulnerabilities"] = run_security_scan()

    if args.enhanced_security or args.full:
        # Temporarily disable alerts if requested
        if args.no_alerts:
            original_send_alert = send_security_alert
            globals()["send_security_alert"] = lambda x: None

        report["enhanced_security_scan"] = run_enhanced_security_scan()

        if args.no_alerts:
            globals()["send_security_alert"] = original_send_alert

    if args.size or args.full:
        report["dependency_analysis"] = analyze_dependency_size()

    if args.tree or args.full:
        report["dependency_tree"] = generate_dependency_tree()

    if args.licenses or args.full:
        report["license_compliance"] = check_license_compliance()

    if args.full:
        report["audit_timestamp"] = datetime.now().isoformat()

    # Output results
    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to {args.output}")
    else:
        print(json.dumps(report, indent=2))

    # Exit with error code if critical vulnerabilities found
    if "enhanced_security_scan" in report:
        critical_count = sum(
            1
            for vuln in report["enhanced_security_scan"]["vulnerabilities"]
            if vuln.get("severity") == "critical"
        )
        if critical_count > 0:
            sys.exit(1)


if __name__ == "__main__":
    main()
