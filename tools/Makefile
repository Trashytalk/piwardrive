.PHONY: lint test docs coverage deps-audit deps-update deps-security deps-outdated deps-install-core deps-install-full install-minimal install-full install-full-dev

lint:
    pre-commit run --all-files

test:
    pytest -q

docs:
    sphinx-build -W -b html docs docs/_build/html

coverage:
    pytest --cov=src --cov-report=xml -q
    cd webui && npm test

# Installation Targets
install-minimal:
    @echo "Installing PiWardrive - Minimal Installation"
    @echo "This includes only core dependencies (~20 packages)"
    @bash scripts/install.sh minimal

install-full:
    @echo "Installing PiWardrive - Full Installation"
    @echo "This includes all optional features (~50-60 packages)"
    @bash scripts/install.sh full

install-full-dev:
    @echo "Installing PiWardrive - Full + Development Installation"
    @echo "This includes all features plus development tools (~70-80 packages)"
    @bash scripts/install.sh full-dev

install-help:
    @echo "PiWardrive Installation Options:"
    @echo ""
    @echo "  make install-minimal    - Install only core dependencies (~20 packages)"
    @echo "                           Best for: Production deployments, resource-constrained systems"
    @echo "                           Features: Web UI, basic mapping, GPS, database"
    @echo ""
    @echo "  make install-full       - Install all features (~50-60 packages)"
    @echo "                           Best for: Full-featured deployments, data analysis"
    @echo "                           Features: All core + scientific computing, visualization, hardware support"
    @echo ""
    @echo "  make install-full-dev   - Install all features + development tools (~70-80 packages)"
    @echo "                           Best for: Development, contributing, testing"
    @echo "                           Features: All features + linting, testing, security scanning"
    @echo ""
    @echo "After installation, activate the environment with: source venv/bin/activate"
    @echo "Then run PiWardrive with: python -m piwardrive.webui_server"

# Dependency Management Targets
deps-audit:
    @echo "Running comprehensive dependency audit..."
    python scripts/dependency_audit.py --full --output dependency_audit_report.json

deps-update:
    @echo "Checking for outdated packages..."
    python scripts/dependency_audit.py --outdated

deps-security:
    @echo "Running security vulnerability scans..."
    python scripts/dependency_audit.py --security

deps-outdated:
    @echo "Checking for outdated packages..."
    pip list --outdated

deps-install-core:
    @echo "Installing core dependencies only..."
    pip install -r requirements-core.txt

deps-install-full:
    @echo "Installing full dependencies..."
    pip install -r requirements.txt

deps-install-dev:
    @echo "Installing development dependencies..."
    pip install -r requirements-dev.txt

deps-cleanup:
    @echo "Cleaning up unused dependencies..."
    pip-autoremove -y

deps-freeze:
    @echo "Generating current dependency freeze..."
    pip freeze > requirements-frozen.txt
    @echo "Frozen dependencies saved to requirements-frozen.txt"
