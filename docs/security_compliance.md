# Security Compliance

This document describes the security standards enforced in the PiWardrive project.

## Baseline

-   All source code is scanned on every pull request using Bandit, pip-audit and Safety.
-   Dependency updates are automated via Dependabot.
-   Security scan results are uploaded in SARIF/JSON format for analysis in the GitHub Security tab.
-   Critical vulnerabilities block merges until resolved.

## Continuous Monitoring

Scheduled scans run weekly and generate historical reports. These reports are kept in the Security tab and as build artifacts.

## Incident Response

Security issues should be reported via the `Security Issue` template. The maintainers will triage and address issues according to severity.
