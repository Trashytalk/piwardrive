# Automated Setup

PiWardrive now ships with a platform-aware setup script and interactive wizard to drastically simplify installation.

## Quick Start

1. Run `scripts/setup.sh` on Ubuntu, Debian or Raspberry Pi OS. The script installs Kismet, BetterCAP, GPSD and all other dependencies, then creates a Python virtual environment.
2. Activate the environment and launch the wizard:
    ```bash
    source pw-env/bin/activate
    python -m piwardrive.setup_wizard
    ```
3. Start the full stack using Docker Compose:
    ```bash
    docker compose up -d
    ```

## Validating Configuration

Run `scripts/validate_config.py` to check any configuration file against the built‑in schema. Helpful error messages are printed if values are invalid.

See `docker-compose.yml` for the list of included services (PostgreSQL, Redis and Grafana). The compose file provides a self‑contained environment for development or production.
