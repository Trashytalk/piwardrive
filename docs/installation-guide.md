# PiWardrive Installation Guide

This guide provides detailed instructions for installing PiWardrive with different feature sets to match your specific needs.

## Installation Options Overview

| Option | Packages | Use Case | Features |
|--------|----------|----------|----------|
| **Minimal** | ~20 | Production, resource-constrained | Core web UI, mapping, GPS, database |
| **Full** | ~50-60 | Full-featured deployments | All features including analysis and visualization |
| **Full + Dev** | ~70-80 | Development, testing, contributing | All features plus development tools |

## Quick Installation

### 🚀 Option 1: Automated Installation Scripts

**Linux/macOS:**
```bash
# Clone the repository
git clone git@github.com:Trashytalk/piwardrive.git
cd piwardrive

# Choose your installation type
bash scripts/install.sh minimal      # Minimal installation
bash scripts/install.sh full         # Full installation
bash scripts/install.sh full-dev     # Full + development installation
```

**Windows:**
```powershell
# Clone the repository
git clone git@github.com:Trashytalk/piwardrive.git
cd piwardrive

# Choose your installation type
.\scripts\install.ps1 minimal      # Minimal installation
.\scripts\install.ps1 full         # Full installation
.\scripts\install.ps1 full-dev     # Full + development installation
```

### 🎯 Option 2: Make Targets

```bash
# Clone the repository
git clone git@github.com:Trashytalk/piwardrive.git
cd piwardrive

# Use make targets
make install-minimal      # Minimal installation
make install-full         # Full installation
make install-full-dev     # Full + development installation
make install-help         # Show installation options
```

### 🔧 Option 3: Manual Installation

```bash
# Clone the repository
git clone git@github.com:Trashytalk/piwardrive.git
cd piwardrive

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\Activate.ps1  # Windows

# Choose your installation type
pip install -r requirements-core.txt    # Minimal
pip install -r requirements.txt         # Full
pip install -r requirements-dev.txt     # + Development tools

# Install PiWardrive package
pip install -e .
```

### 🎨 Option 4: Feature-Specific Installation

```bash
# Install base package first
pip install piwardrive

# Then add specific features as needed
pip install piwardrive[analysis]        # Scientific computing
pip install piwardrive[visualization]   # Charts and plotting
pip install piwardrive[hardware]        # Raspberry Pi sensors
pip install piwardrive[integrations]    # External services
pip install piwardrive[performance]     # Performance optimizations
pip install piwardrive[all]             # All features
```

## Detailed Installation Options

### Minimal Installation (~20 packages)

**Best for:**
- Production deployments
- Resource-constrained systems
- Docker containers
- Basic war-driving functionality

**Includes:**
- FastAPI web framework
- SQLite/PostgreSQL database support
- GPS and location services
- Basic mapping functionality
- Core networking and HTTP clients

**Installation:**
```bash
bash scripts/install.sh minimal
```

### Full Installation (~50-60 packages)

**Best for:**
- Full-featured deployments
- Data analysis and visualization
- Advanced mapping features
- Hardware integration

**Includes:**
- All minimal features plus:
- Scientific computing (numpy, scipy, pandas, scikit-learn)
- Visualization libraries (matplotlib, plotly, folium)
- Hardware interfaces (Bluetooth, sensors)
- External service integrations (AWS, MQTT, R)

**Installation:**
```bash
bash scripts/install.sh full
```

### Full + Development Installation (~70-80 packages)

**Best for:**
- Development and testing
- Contributing to the project
- Code quality and security auditing
- Documentation generation

**Includes:**
- All full features plus:
- Development tools (pytest, pre-commit)
- Code quality tools (black, isort, flake8, mypy)
- Security scanning (bandit, pip-audit, safety)
- Documentation tools (sphinx)

**Installation:**
```bash
bash scripts/install.sh full-dev
```

## Post-Installation Setup

### Activate Environment

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```powershell
venv\Scripts\Activate.ps1
```

### Run PiWardrive

```bash
python -m piwardrive.webui_server
```

### Verify Installation

```bash
# Check installed packages
pip list

# Run dependency audit
python scripts/dependency_audit.py --outdated

# Run tests (if development installation)
pytest

# Check code quality (if development installation)
make lint
```

## System Dependencies

Some features require additional system packages:

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y \
    r-base r-base-dev \
    libdbus-1-dev libglib2.0-dev \
    build-essential python3-dev
```

### CentOS/RHEL
```bash
sudo yum install -y \
    R-core R-devel \
    dbus-devel glib2-devel \
    gcc gcc-c++ python3-devel
```

### macOS
```bash
brew install r dbus glib
```

### Windows
- Install R from [r-project.org](https://www.r-project.org/)
- Install Visual Studio Build Tools for C++ compilation

## Troubleshooting

### Common Issues

**Permission Errors:**
```bash
# Use --user flag if needed
pip install --user -r requirements.txt
```

**Build Errors:**
```bash
# Install development headers
sudo apt install python3-dev build-essential
```

**R Integration Issues:**
```bash
# Ensure R is installed and in PATH
which R
R --version
```

### Getting Help

1. Check the [FAQ](docs/faq.rst)
2. Review [troubleshooting documentation](docs/troubleshooting.md)
3. Run dependency audit: `python scripts/dependency_audit.py --full`
4. Check installation logs in `pip-log.txt`

## Dependency Management

For ongoing dependency management, see:
- [Dependency Management Strategy](docs/dependency-management.md)
- [Dependency Audit Tools](scripts/dependency_audit.py)
- [Make Targets](Makefile) for common tasks

### Useful Commands

```bash
# Check for outdated packages
make deps-outdated

# Run security scan
make deps-security

# Update dependencies
make deps-update

# Clean up unused dependencies
make deps-cleanup
```

## Environment Variables

Optional environment variables for configuration:

```bash
# Database configuration
export PIWARDRIVE_DB_URL="sqlite:///piwardrive.db"

# Redis configuration
export PIWARDRIVE_REDIS_URL="redis://localhost:6379"

# Development mode
export PIWARDRIVE_DEBUG=1

# Log level
export PIWARDRIVE_LOG_LEVEL=INFO
```

## Next Steps

After installation:

1. **Configuration**: Review [configuration documentation](docs/configuration.md)
2. **Hardware Setup**: For Raspberry Pi, see [hardware setup guide](docs/raspberry-pi-setup.md)
3. **Development**: For contributing, see [development guide](docs/development.md)
4. **Deployment**: For production, see [deployment guide](docs/deployment.rst)
