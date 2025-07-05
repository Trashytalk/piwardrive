# PiWardrive Installation Guide

## Table of Contents
- [Quick Start](#quick-start)
- [System Requirements](#system-requirements)
- [Installation Methods](#installation-methods)
- [Raspberry Pi Installation](#raspberry-pi-installation)
- [Manual Installation](#manual-installation)
- [Docker Installation](#docker-installation)
- [Development Installation](#development-installation)
- [Configuration](#configuration)
- [Hardware Setup](#hardware-setup)
- [Service Configuration](#service-configuration)
- [Testing Installation](#testing-installation)
- [Troubleshooting](#troubleshooting)
- [Updating](#updating)
- [Uninstallation](#uninstallation)

## Quick Start

### One-Line Installation (Raspberry Pi)

```bash
curl -fsSL https://raw.githubusercontent.com/username/piwardrive/main/scripts/install.sh | bash
```

This script will:
- Install all dependencies
- Configure services
- Set up the database
- Start the web interface
- Configure Wi-Fi adapter for monitor mode

### Access the Dashboard

After installation, access the web interface at:
- **Local**: http://localhost:8000
- **Network**: http://your-pi-ip:8000

Default credentials:
- **Username**: `admin`
- **Password**: `piwardrive123` (change on first login)

## System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Raspberry Pi OS Lite (64-bit), Ubuntu 20.04+, Debian 11+ |
| **RAM** | 2GB (4GB recommended) |
| **Storage** | 16GB (32GB+ recommended) |
| **Python** | 3.9 or higher |
| **Wi-Fi** | Monitor mode capable adapter |
| **Architecture** | ARM64, AMD64 |

### Recommended Hardware

- **Raspberry Pi 5** (8GB) or **Raspberry Pi 4** (4GB+)
- **External Wi-Fi adapter** with monitor mode support
- **SSD storage** via USB 3.0 for better performance
- **GPS module** (optional) for location tracking
- **Official touchscreen** (optional) for portable use

### Hardware Setup Overview

```mermaid
graph TB
    A[Raspberry Pi 5/4] --> B[External Wi-Fi Adapter]
    A --> C[SSD Storage]
    A --> D[GPS Module]
    A --> E[Display]
    
    B --> B1[Monitor Mode<br/>Capable]
    B --> B2[USB 3.0/2.0<br/>Connection]
    
    C --> C1[USB 3.0<br/>Connection]
    C --> C2[32GB+ Storage<br/>Recommended]
    
    D --> D1[UART/USB<br/>Connection]
    D --> D2[NMEA Protocol<br/>Support]
    
    E --> E1[Official 7"<br/>Touchscreen]
    E --> E2[HDMI Monitor<br/>or TV]
    
    F[Power Supply] --> A
    F --> F1[5V 3A<br/>USB-C]
    F --> F2[Official PSU<br/>Recommended]
    
    style A fill:#e1f5fe
    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#fce4ec
    style E fill:#f3e5f5
    style F fill:#ffebee
```

### Supported Operating Systems

#### Tested Platforms
- **Raspberry Pi OS** (64-bit) - Primary platform
- **Ubuntu 22.04 LTS** (ARM64/AMD64)
- **Debian 12** (ARM64/AMD64)
- **Ubuntu Server 20.04+** (ARM64/AMD64)

#### Compatibility Notes
- **32-bit systems**: Limited support, 64-bit recommended
- **Other distributions**: May work but not officially tested
- **Windows/macOS**: Use Docker installation method

## Installation Methods

### Installation Flow Overview

```mermaid
graph TD
    A[Choose Installation Method] --> B[Automated Script]
    A --> C[Manual Installation]
    A --> D[Docker Installation]
    A --> E[Package Installation]
    
    B --> B1[Download Script]
    B1 --> B2[Run install.sh]
    B2 --> B3[Configure Services]
    B3 --> B4[Start Dashboard]
    
    C --> C1[Clone Repository]
    C1 --> C2[Install Dependencies]
    C2 --> C3[Configure System]
    C3 --> C4[Setup Services]
    C4 --> C5[Start Application]
    
    D --> D1[Install Docker]
    D1 --> D2[Pull Images]
    D2 --> D3[Run Containers]
    D3 --> D4[Configure Networking]
    
    E --> E1[Add Repository]
    E1 --> E2[Install Package]
    E2 --> E3[Configure System]
    E3 --> E4[Enable Services]
    
    B4 --> F[Access Dashboard]
    C5 --> F
    D4 --> F
    E4 --> F
    
    style A fill:#e1f5fe
    style F fill:#e8f5e8
    style B fill:#fff3e0
    style C fill:#fce4ec
    style D fill:#f3e5f5
    style E fill:#ffebee
```

### Method 1: Automated Script (Recommended)

The automated installer handles all dependencies and configuration:

```bash
# Download and run installer
curl -fsSL https://github.com/username/piwardrive/raw/main/scripts/install.sh -o install.sh
chmod +x install.sh
sudo ./install.sh

# Or one-line installation
curl -fsSL https://github.com/username/piwardrive/raw/main/scripts/install.sh | sudo bash
```

**Installation options:**
```bash
# Interactive installation (recommended)
sudo ./install.sh

# Headless installation
sudo ./install.sh --headless

# Custom installation directory
sudo ./install.sh --install-dir /opt/piwardrive

# Skip service setup
sudo ./install.sh --no-services

# Development installation
sudo ./install.sh --dev
```

### Method 2: Manual Installation

For custom setups or troubleshooting:

```bash
# Clone repository
git clone https://github.com/username/piwardrive.git
cd piwardrive

# Run manual installation
sudo scripts/manual-install.sh
```

### Method 3: Docker Installation

For containerized deployment:

```bash
# Using Docker Compose
git clone https://github.com/username/piwardrive.git
cd piwardrive
docker compose up -d

# Using pre-built image
docker run -d --name piwardrive \
  --privileged \
  --network host \
  -v piwardrive_data:/data \
  piwardrive/piwardrive:latest
```

See [Docker Deployment Guide](docker-deployment.md) for detailed instructions.

### Method 4: Package Installation

When available from package repositories:

```bash
# Add repository
curl -fsSL https://packages.piwardrive.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/piwardrive.gpg
echo "deb [signed-by=/usr/share/keyrings/piwardrive.gpg] https://packages.piwardrive.com/apt stable main" | sudo tee /etc/apt/sources.list.d/piwardrive.list

# Install package
sudo apt update
sudo apt install piwardrive
```

## Raspberry Pi Installation

### Pre-Installation Setup

#### 1. Prepare Raspberry Pi OS

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y git curl wget vim htop

# Enable SSH (if needed)
sudo systemctl enable ssh
sudo systemctl start ssh

# Enable I2C and SPI (for sensors)
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0
```

#### 2. Configure Storage

For better performance, use SSD storage:

```bash
# Create mount point
sudo mkdir -p /mnt/ssd

# Find SSD device
lsblk

# Format SSD (replace /dev/sda1 with your device)
sudo mkfs.ext4 /dev/sda1

# Add to fstab for auto-mount
echo '/dev/sda1 /mnt/ssd ext4 defaults,nofail 0 2' | sudo tee -a /etc/fstab

# Mount SSD
sudo mount -a
```

#### 3. Configure Wi-Fi Adapter

```bash
# Check Wi-Fi adapters
ip link show

# Test monitor mode capability
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up

# Revert to managed mode
sudo ip link set wlan1 down
sudo iw dev wlan1 set type managed
sudo ip link set wlan1 up
```

### Automated Raspberry Pi Installation

```bash
#!/bin/bash
# Enhanced Pi installation script

# Download and run the installer
curl -fsSL https://raw.githubusercontent.com/username/piwardrive/main/scripts/install-pi.sh | bash

# Or with custom options
curl -fsSL https://raw.githubusercontent.com/username/piwardrive/main/scripts/install-pi.sh -o install-pi.sh
chmod +x install-pi.sh

# Interactive installation
sudo ./install-pi.sh

# Headless installation with SSD
sudo ./install-pi.sh --headless --ssd-path /mnt/ssd

# Installation with GPS support
sudo ./install-pi.sh --gps --gps-device /dev/ttyACM0
```

### Post-Installation Pi Configuration

```bash
# Configure GPU memory (for GUI use)
echo 'gpu_mem=128' | sudo tee -a /boot/firmware/config.txt

# Optimize for SSD boot (if applicable)
echo 'dtparam=sd_overclock=100' | sudo tee -a /boot/firmware/config.txt

# Enable hardware watchdog
echo 'dtparam=watchdog=on' | sudo tee -a /boot/firmware/config.txt

# Reboot to apply changes
sudo reboot
```

## Manual Installation

### Step 1: Install System Dependencies

#### Ubuntu/Debian
```bash
# Update package lists
sudo apt update

# Install Python and development tools
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    git \
    curl \
    wget

# Install Wi-Fi tools
sudo apt install -y \
    aircrack-ng \
    wireless-tools \
    iw \
    hostapd \
    dnsmasq

# Install database dependencies
sudo apt install -y \
    sqlite3 \
    libsqlite3-dev

# Install optional dependencies
sudo apt install -y \
    postgresql-client \
    redis-tools \
    gpsd \
    gpsd-clients

# Install system monitoring tools
sudo apt install -y \
    htop \
    iotop \
    netstat-nat \
    lsof
```

#### CentOS/RHEL/Fedora
```bash
# Install Python and development tools
sudo dnf install -y \
    python3 \
    python3-pip \
    python3-devel \
    gcc \
    gcc-c++ \
    make \
    git \
    curl \
    wget

# Install Wi-Fi tools
sudo dnf install -y \
    aircrack-ng \
    wireless-tools \
    iw

# Install database dependencies
sudo dnf install -y \
    sqlite \
    sqlite-devel
```

### Step 2: Create System User

```bash
# Create piwardrive user
sudo useradd -r -s /bin/bash -d /opt/piwardrive -m piwardrive

# Add to required groups
sudo usermod -a -G dialout,netdev,bluetooth piwardrive

# Create directories
sudo mkdir -p /opt/piwardrive/{data,logs,config,scripts}
sudo chown -R piwardrive:piwardrive /opt/piwardrive
```

### Step 3: Download and Install PiWardrive

```bash
# Switch to piwardrive user
sudo -u piwardrive -i

# Clone repository
cd /opt/piwardrive
git clone https://github.com/username/piwardrive.git .

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install Python dependencies
pip install -r requirements.txt

# Install optional dependencies
pip install -r requirements-optional.txt

# Install PiWardrive in development mode
pip install -e .
```

### Step 4: Database Setup

```bash
# Initialize database
cd /opt/piwardrive
source venv/bin/activate

# Run database migrations
python -m piwardrive.database.migrations init

# Create default admin user
python -m piwardrive.auth.create_user \
    --username admin \
    --password piwardrive123 \
    --role admin \
    --email admin@localhost
```

### Step 5: Configuration

```bash
# Copy configuration template
cp config/piwardrive.yaml.example config/piwardrive.yaml

# Edit configuration
nano config/piwardrive.yaml

# Set environment variables
cat >> ~/.bashrc << 'EOF'
export PIWARDRIVE_CONFIG_FILE=/opt/piwardrive/config/piwardrive.yaml
export PIWARDRIVE_DATA_DIR=/opt/piwardrive/data
export PIWARDRIVE_LOG_DIR=/opt/piwardrive/logs
EOF

source ~/.bashrc
```

## Docker Installation

### Prerequisites

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Install Docker Compose
sudo apt install docker-compose-plugin
```

### Quick Docker Setup

```bash
# Clone repository
git clone https://github.com/username/piwardrive.git
cd piwardrive

# Copy environment file
cp .env.example .env

# Edit configuration
nano .env

# Start services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

### Docker Environment Configuration

```bash
# .env file
PIWARDRIVE_API_PORT=8000
PIWARDRIVE_LOG_LEVEL=INFO
PIWARDRIVE_SECRET_KEY=your-secret-key-here
PIWARDRIVE_DATABASE_URL=sqlite:///data/piwardrive.db
PIWARDRIVE_WIFI_INTERFACE=wlan0
PIWARDRIVE_GPS_ENABLED=false
PIWARDRIVE_REDIS_ENABLED=false
```

## Development Installation

### Development Environment Setup

```bash
# Clone repository
git clone https://github.com/username/piwardrive.git
cd piwardrive

# Create development environment
python3 -m venv venv-dev
source venv-dev/bin/activate

# Install development dependencies
pip install -r requirements-dev.txt
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Start development server
python -m piwardrive.webui --dev --reload
```

### Development Dependencies

```bash
# Install additional development tools
pip install \
    pytest \
    pytest-cov \
    pytest-asyncio \
    black \
    flake8 \
    mypy \
    pre-commit \
    sphinx \
    jupyter
```

### Development Configuration

```yaml
# config/development.yaml
app:
  debug: true
  log_level: "DEBUG"
  host: "0.0.0.0"
  port: 8000

database:
  url: "sqlite:///data/dev_piwardrive.db"
  echo: true

wifi:
  mock_hardware: true
  test_data_generation: true

monitoring:
  interval: 10
```

## Configuration

### Basic Configuration

```bash
# Create configuration directory
sudo mkdir -p /etc/piwardrive

# Copy default configuration
sudo cp /opt/piwardrive/config/piwardrive.yaml.example /etc/piwardrive/piwardrive.yaml

# Edit configuration
sudo nano /etc/piwardrive/piwardrive.yaml
```

### Environment Variables

```bash
# Create environment file
sudo tee /etc/piwardrive/environment << 'EOF'
PIWARDRIVE_CONFIG_FILE=/etc/piwardrive/piwardrive.yaml
PIWARDRIVE_DATA_DIR=/var/lib/piwardrive
PIWARDRIVE_LOG_DIR=/var/log/piwardrive
PIWARDRIVE_API_PORT=8000
PIWARDRIVE_WIFI_INTERFACE=wlan0
PIWARDRIVE_SECRET_KEY=change-this-secret-key
EOF

# Set proper permissions
sudo chmod 600 /etc/piwardrive/environment
```

### Database Configuration

#### SQLite (Default)
```yaml
database:
  url: "sqlite:///var/lib/piwardrive/piwardrive.db"
  pool_size: 10
  timeout: 30
```

#### PostgreSQL (Production)
```yaml
database:
  url: "postgresql://piwardrive:password@localhost:5432/piwardrive"
  pool_size: 20
  max_overflow: 30
  timeout: 60
```

### Wi-Fi Interface Configuration

```yaml
wifi:
  interface: "wlan1"  # External adapter
  scan_interval: 60
  monitor_mode: true
  channel_hop: true
  channels:
    "2.4ghz": [1, 6, 11]
    "5ghz": [36, 40, 44, 48]
```

## Hardware Setup

### Wi-Fi Adapter Configuration

```bash
# Check available interfaces
ip link show

# Test monitor mode
sudo airmon-ng check kill
sudo airmon-ng start wlan1

# Verify monitor mode
iwconfig

# Stop monitor mode
sudo airmon-ng stop wlan1mon
```

### GPS Module Setup

```bash
# Install GPS daemon
sudo apt install gpsd gpsd-clients

# Configure GPS daemon
sudo nano /etc/default/gpsd

# Set GPS device
DEVICES="/dev/ttyACM0"
USBAUTO="true"
GPSD_OPTIONS="-n"

# Start GPS daemon
sudo systemctl enable gpsd
sudo systemctl start gpsd

# Test GPS
cgps
```

### Storage Setup

```bash
# Create data directories
sudo mkdir -p /var/lib/piwardrive/{data,database,uploads}
sudo mkdir -p /var/log/piwardrive

# Set ownership
sudo chown -R piwardrive:piwardrive /var/lib/piwardrive
sudo chown -R piwardrive:piwardrive /var/log/piwardrive

# Set permissions
sudo chmod -R 755 /var/lib/piwardrive
sudo chmod -R 755 /var/log/piwardrive
```

## Service Configuration

### Systemd Service

```bash
# Create systemd service file
sudo tee /etc/systemd/system/piwardrive.service << 'EOF'
[Unit]
Description=PiWardrive Wi-Fi Analysis System
After=network.target
Wants=network.target

[Service]
Type=notify
User=piwardrive
Group=piwardrive
WorkingDirectory=/opt/piwardrive
Environment=PYTHONPATH=/opt/piwardrive
EnvironmentFile=/etc/piwardrive/environment
ExecStart=/opt/piwardrive/venv/bin/python -m piwardrive.webui
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/piwardrive /var/log/piwardrive /tmp

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable piwardrive

# Start service
sudo systemctl start piwardrive

# Check status
sudo systemctl status piwardrive
```

### Additional Services

#### Kismet Service (Optional)
```bash
# Install Kismet
sudo apt install kismet

# Configure Kismet
sudo nano /etc/kismet/kismet.conf

# Add source
source=wlan1

# Start Kismet
sudo systemctl enable kismet
sudo systemctl start kismet
```

#### Log Rotation
```bash
# Create logrotate configuration
sudo tee /etc/logrotate.d/piwardrive << 'EOF'
/var/log/piwardrive/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    create 644 piwardrive piwardrive
    postrotate
        systemctl reload piwardrive
    endscript
}
EOF
```

## Testing Installation

### Verification Script

```bash
#!/bin/bash
# test-installation.sh

echo "Testing PiWardrive installation..."

# Test Python import
python3 -c "import piwardrive; print(f'PiWardrive version: {piwardrive.__version__}')"

# Test database connection
python3 -c "
from piwardrive.database import get_database_engine
engine = get_database_engine()
with engine.connect() as conn:
    result = conn.execute('SELECT 1')
    print('Database connection: OK')
"

# Test web server
curl -f http://localhost:8000/health && echo "Web server: OK"

# Test Wi-Fi interface
iw dev | grep Interface && echo "Wi-Fi interface: OK"

# Test permissions
sudo -u piwardrive touch /var/lib/piwardrive/test && rm /var/lib/piwardrive/test && echo "Permissions: OK"

echo "Installation test completed!"
```

### Health Check

```bash
# Check service status
sudo systemctl status piwardrive

# Check logs
sudo journalctl -u piwardrive -f

# Check listening ports
sudo netstat -tlnp | grep :8000

# Check processes
ps aux | grep piwardrive

# Test API endpoints
curl http://localhost:8000/api/v1/system/health
```

### Web Interface Test

1. Open browser to http://your-pi-ip:8000
2. Login with default credentials (admin/piwardrive123)
3. Navigate to System → Status to verify components
4. Start a Wi-Fi scan to test functionality
5. Check real-time updates and data display

## Troubleshooting

### Common Issues

#### Service Won't Start
```bash
# Check service status
sudo systemctl status piwardrive

# Check logs
sudo journalctl -u piwardrive -n 50

# Check configuration
python3 -m piwardrive.config validate

# Test manually
sudo -u piwardrive /opt/piwardrive/venv/bin/python -m piwardrive.webui --debug
```

#### Permission Errors
```bash
# Fix file permissions
sudo chown -R piwardrive:piwardrive /opt/piwardrive
sudo chown -R piwardrive:piwardrive /var/lib/piwardrive
sudo chown -R piwardrive:piwardrive /var/log/piwardrive

# Check user groups
groups piwardrive

# Add to required groups
sudo usermod -a -G dialout,netdev piwardrive
```

#### Database Issues
```bash
# Check database file
ls -la /var/lib/piwardrive/piwardrive.db

# Reset database
sudo -u piwardrive rm /var/lib/piwardrive/piwardrive.db
sudo -u piwardrive python3 -m piwardrive.database.migrations init

# Check database integrity
sudo -u piwardrive sqlite3 /var/lib/piwardrive/piwardrive.db "PRAGMA integrity_check;"
```

#### Wi-Fi Adapter Issues
```bash
# Check USB devices
lsusb

# Check Wi-Fi interfaces
ip link show

# Check for conflicts
sudo airmon-ng check

# Test monitor mode
sudo iw dev wlan1 set type monitor
```

#### Network Issues
```bash
# Check firewall
sudo ufw status

# Check listening ports
sudo netstat -tlnp

# Test local connection
curl http://localhost:8000

# Check network interfaces
ip addr show
```

### Debug Mode

```bash
# Start in debug mode
sudo -u piwardrive /opt/piwardrive/venv/bin/python -m piwardrive.webui --debug --log-level DEBUG

# Enable verbose logging
export PIWARDRIVE_LOG_LEVEL=DEBUG
sudo systemctl restart piwardrive
```

### Log Analysis

```bash
# View recent logs
sudo journalctl -u piwardrive -f

# View specific time range
sudo journalctl -u piwardrive --since "1 hour ago"

# Search for errors
sudo journalctl -u piwardrive | grep -i error

# Check system logs
sudo dmesg | grep -i usb
```

## Updating

### Automatic Updates

```bash
# Update using script
curl -fsSL https://raw.githubusercontent.com/username/piwardrive/main/scripts/update.sh | sudo bash

# Or download and run
wget https://raw.githubusercontent.com/username/piwardrive/main/scripts/update.sh
chmod +x update.sh
sudo ./update.sh
```

### Manual Updates

```bash
# Stop service
sudo systemctl stop piwardrive

# Backup configuration
sudo cp -r /etc/piwardrive /etc/piwardrive.backup.$(date +%Y%m%d)

# Update code
cd /opt/piwardrive
sudo -u piwardrive git pull

# Update dependencies
sudo -u piwardrive /opt/piwardrive/venv/bin/pip install -r requirements.txt

# Run migrations
sudo -u piwardrive /opt/piwardrive/venv/bin/python -m piwardrive.database.migrations upgrade

# Start service
sudo systemctl start piwardrive

# Check status
sudo systemctl status piwardrive
```

### Version Management

```bash
# Check current version
python3 -c "import piwardrive; print(piwardrive.__version__)"

# List available versions
git tag -l

# Switch to specific version
git checkout v1.0.0
sudo -u piwardrive /opt/piwardrive/venv/bin/pip install -r requirements.txt
sudo systemctl restart piwardrive
```

## Uninstallation

### Complete Removal

```bash
# Stop and disable service
sudo systemctl stop piwardrive
sudo systemctl disable piwardrive

# Remove service file
sudo rm /etc/systemd/system/piwardrive.service
sudo systemctl daemon-reload

# Remove user and data
sudo userdel -r piwardrive

# Remove directories
sudo rm -rf /opt/piwardrive
sudo rm -rf /var/lib/piwardrive
sudo rm -rf /var/log/piwardrive
sudo rm -rf /etc/piwardrive

# Remove packages (optional)
sudo apt remove kismet gpsd aircrack-ng

# Clean up dependencies
sudo apt autoremove
```

### Preserve Data Removal

```bash
# Stop service
sudo systemctl stop piwardrive
sudo systemctl disable piwardrive

# Backup data
sudo tar -czf piwardrive-data-backup.tar.gz \
    /var/lib/piwardrive \
    /etc/piwardrive

# Remove application only
sudo rm -rf /opt/piwardrive
sudo rm /etc/systemd/system/piwardrive.service
sudo systemctl daemon-reload
```

---

For additional help:
- **Documentation**: [docs/](../docs/)
- **Community**: [GitHub Discussions](https://github.com/username/piwardrive/discussions)
- **Issues**: [GitHub Issues](https://github.com/username/piwardrive/issues)
- **Hardware Compatibility**: [hardware-compatibility.md](hardware-compatibility.md)
- **Configuration**: [configuration.md](configuration.md)
