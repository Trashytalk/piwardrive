# Security Audit Report

The project dependencies were scanned using **bandit**, **pip-audit** and **safety**.

## Bandit

Summary:

-   59 low severity issues
-   5 medium severity issues
-   0 high severity issues

## pip-audit

`pip-audit` failed to complete due to missing build dependencies for `dbus-python`.

## safety

`safety` could not connect to the vulnerability database because of network restrictions.

These tools are executed automatically in the `Security Scan` workflow.
