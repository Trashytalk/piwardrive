# Raspberry Pi Setup Guide

This guide covers setting up PiWardrive on Raspberry Pi devices, from initial OS installation to production deployment.

## Hardware Requirements

### Recommended Hardware
- **Raspberry Pi 5** (4GB or 8GB RAM)
- **Official 7" Touchscreen** (for kiosk mode)
- **High-quality microSD card** (32GB+, Class 10 or better)
- **USB Wi-Fi adapter** with monitor mode support
- **USB GPS module** (optional)
- **External antenna** (for better Wi-Fi reception)

### Minimum Hardware
- **Raspberry Pi 4** (4GB RAM minimum)
- **MicroSD card** (16GB+)
- **USB Wi-Fi adapter** with monitor mode support

### Supported Wi-Fi Adapters
- **Alfa AWUS036ACS** (Realtek RTL8812AU) - Recommended
- **Alfa AWUS036AC** (Realtek RTL8812AU)
- **Panda PAU09** (Ralink RT5372)
- **TP-Link AC600** (Realtek RTL8811AU)
- **See**: [Hardware Compatibility Guide](hardware-compatibility.md) for full list

## Operating System Setup

### Option 1: Raspberry Pi OS (Recommended)

#### 1. Download and Flash OS
```bash
# Download Raspberry Pi Imager
# https://www.raspberrypi.org/software/

# Flash Raspberry Pi OS Lite (64-bit) to SD card
# Enable SSH and Wi-Fi in imager advanced options
```

#### 2. Initial Boot Configuration
```bash
# SSH into the Pi
ssh pi@raspberrypi.local

# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y git curl wget htop vim build-essential cmake
```

#### 3. Configure Wi-Fi and SSH
```bash
# Configure Wi-Fi (if not done in imager)
sudo raspi-config
# Navigate to: System Options > Wireless LAN

# Enable SSH permanently
sudo systemctl enable ssh

# Change default password
passwd pi
```

### Option 2: Ubuntu Server (Alternative)

#### 1. Flash Ubuntu Server
```bash
# Download Ubuntu Server 22.04 LTS for ARM64
# Flash to SD card using Raspberry Pi Imager

# Enable SSH and Wi-Fi in user-data file before first boot
```

#### 2. Initial Setup
```bash
# SSH into the Pi
ssh ubuntu@ubuntu.local

# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y git curl wget htop vim build-essential cmake
```

## PiWardrive Installation

### Option 1: Automated Installation (Recommended)

```bash
# Download and run the installation script
curl -fsSL https://raw.githubusercontent.com/TrashyTalk/piwardrive/main/scripts/install.sh | bash

# Or for development installation
curl -fsSL https://raw.githubusercontent.com/TrashyTalk/piwardrive/main/scripts/install.sh | bash -s -- --dev
```

### Option 2: Manual Installation

#### 1. Install System Dependencies
```bash
# Install Python and Node.js
sudo apt install -y python3 python3-pip python3-venv nodejs npm

# Install monitoring tools
sudo apt install -y kismet bettercap gpsd

# Install hardware tools
sudo apt install -y evtest i2c-tools

# Install build dependencies
sudo apt install -y libssl-dev libffi-dev libbluetooth-dev
```

#### 2. Install PiWardrive
```bash
# Clone the repository
git clone https://github.com/TrashyTalk/piwardrive.git
cd piwardrive

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
pip install .

# Install and build WebUI
cd webui
npm install
npm run build
cd ..
```

#### 3. Configure Services
```bash
# Create systemd service
sudo cp examples/piwardrive.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable piwardrive
```

## Hardware Configuration

### Wi-Fi Adapter Setup

#### 1. Verify Adapter Recognition
```bash
# Check if adapter is detected
lsusb

# Check wireless interfaces
iwconfig

# Check monitor mode support
sudo iw dev wlan1 set type monitor
```

#### 2. Configure Monitor Mode
```bash
# Create monitor interface
sudo airmon-ng start wlan1

# Verify monitor mode
iwconfig wlan1mon
```

#### 3. Configure Kismet
```bash
# Edit Kismet configuration
sudo nano /etc/kismet/kismet.conf

# Add your Wi-Fi interface
source=wlan1mon

# Configure Kismet user
sudo usermod -a -G kismet pi
```

### GPS Module Setup

#### 1. Connect GPS Module
```bash
# USB GPS modules should be auto-detected
# Check detection
lsusb | grep -i gps

# For serial GPS modules, enable UART
sudo raspi-config
# Interface Options > Serial Port > Enable
```

#### 2. Configure GPSD
```bash
# Install GPSD if not already installed
sudo apt install -y gpsd gpsd-clients

# Edit GPSD configuration
sudo nano /etc/default/gpsd

# Configure device
DEVICES="/dev/ttyUSB0"  # or /dev/ttyAMA0 for serial
GPSD_OPTIONS="-n"
```

#### 3. Test GPS
```bash
# Start GPSD
sudo systemctl start gpsd

# Test GPS reception
gpsmon
cgps -s
```

### Touchscreen Setup (Optional)

#### 1. Official 7" Touchscreen
```bash
# Should work out of the box with recent Raspberry Pi OS
# Verify display
fbset -fb /dev/fb0 -s

# Configure screen orientation
sudo nano /boot/config.txt
# Add: lcd_rotate=2  # for 180-degree rotation
```

#### 2. Kiosk Mode Configuration
```bash
# Install display manager
sudo apt install -y lightdm

# Configure auto-login
sudo nano /etc/lightdm/lightdm.conf
# Add: autologin-user=pi

# Create kiosk startup script
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# Add: @chromium-browser --kiosk --disable-infobars http://localhost:8000
```

## Performance Optimization

### Memory Optimization

#### 1. Reduce Memory Usage
```bash
# Disable unnecessary services
sudo systemctl disable bluetooth
sudo systemctl disable avahi-daemon

# Configure GPU memory split
sudo nano /boot/config.txt
# Add: gpu_mem=64  # Reduce GPU memory for headless operation
```

#### 2. Swap Configuration
```bash
# Increase swap size
sudo dphys-swapfile swapoff
sudo nano /etc/dphys-swapfile
# Change: CONF_SWAPSIZE=2048

sudo dphys-swapfile setup
sudo dphys-swapfile swapon
```

### Storage Optimization

#### 1. Log Rotation
```bash
# Configure log rotation
sudo nano /etc/logrotate.d/piwardrive
```

```
/var/log/piwardrive/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 pi pi
}
```

#### 2. Database Optimization
```bash
# Schedule database vacuum
crontab -e
# Add: 0 2 * * * /usr/local/bin/piwardrive-vacuum
```

### Network Optimization

#### 1. Wi-Fi Power Management
```bash
# Disable Wi-Fi power management
sudo iwconfig wlan0 power off

# Make persistent
echo 'iwconfig wlan0 power off' | sudo tee -a /etc/rc.local
```

#### 2. Network Buffer Tuning
```bash
# Optimize network buffers
sudo sysctl -w net.core.rmem_max=16777216
sudo sysctl -w net.core.wmem_max=16777216

# Make persistent
echo 'net.core.rmem_max=16777216' | sudo tee -a /etc/sysctl.conf
echo 'net.core.wmem_max=16777216' | sudo tee -a /etc/sysctl.conf
```

## Production Deployment

### Security Hardening

#### 1. User Security
```bash
# Change default passwords
sudo passwd pi
sudo passwd root

# Disable root login
sudo nano /etc/ssh/sshd_config
# Change: PermitRootLogin no

# Create PiWardrive user
sudo adduser piwardrive
sudo usermod -a -G sudo,kismet,dialout piwardrive
```

#### 2. SSH Security
```bash
# Generate SSH keys
ssh-keygen -t rsa -b 4096

# Configure SSH key authentication
# Copy public key to Pi
ssh-copy-id pi@raspberrypi.local

# Disable password authentication
sudo nano /etc/ssh/sshd_config
# Change: PasswordAuthentication no
```

#### 3. Firewall Configuration
```bash
# Install and configure UFW
sudo apt install -y ufw

# Configure basic rules
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 8000/tcp  # PiWardrive web interface

# Enable firewall
sudo ufw enable
```

### Monitoring and Maintenance

#### 1. System Monitoring
```bash
# Install monitoring tools
sudo apt install -y htop iotop

# Configure system monitoring
piwardrive-service --monitor
```

#### 2. Automated Updates
```bash
# Configure automatic security updates
sudo apt install -y unattended-upgrades

sudo nano /etc/apt/apt.conf.d/20auto-upgrades
```

```
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
```

#### 3. Health Monitoring
```bash
# Schedule health checks
crontab -e
# Add: */5 * * * * /usr/local/bin/piwardrive-field-diagnostics --quiet
```

### Backup and Recovery

#### 1. Configuration Backup
```bash
# Create backup script
sudo nano /usr/local/bin/backup-piwardrive.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/piwardrive_$DATE"
mkdir -p "$BACKUP_DIR"

# Backup configuration
cp -r ~/.config/piwardrive "$BACKUP_DIR/"
cp -r /etc/piwardrive "$BACKUP_DIR/"

# Backup database
piwardrive-vacuum
cp ~/.config/piwardrive/piwardrive.db "$BACKUP_DIR/"

# Create archive
tar -czf "/backup/piwardrive_backup_$DATE.tar.gz" "$BACKUP_DIR"
rm -rf "$BACKUP_DIR"
```

#### 2. System Image Backup
```bash
# Create SD card image (from another machine)
sudo dd if=/dev/mmcblk0 of=piwardrive_backup.img bs=4M

# Compress image
gzip piwardrive_backup.img
```

## Troubleshooting

### Common Issues

#### 1. Wi-Fi Adapter Not Detected
```bash
# Check USB connection
lsusb

# Check driver installation
dmesg | grep -i wifi

# Install additional drivers if needed
sudo apt install -y firmware-realtek
```

#### 2. Monitor Mode Issues
```bash
# Kill conflicting processes
sudo airmon-ng check kill

# Reset network manager
sudo systemctl restart NetworkManager
```

#### 3. Performance Issues
```bash
# Check system resources
htop
iotop

# Check temperature
vcgencmd measure_temp

# Check for throttling
vcgencmd get_throttled
```

#### 4. Database Issues
```bash
# Check database integrity
piwardrive-vacuum --check

# Reset database if corrupted
piwardrive-migrate reset
```

### Diagnostic Tools

#### 1. Built-in Diagnostics
```bash
# Run comprehensive diagnostics
piwardrive-field-diagnostics --full-check

# Check service status
service-status

# Monitor system health
piwardrive-service --monitor
```

#### 2. Log Analysis
```bash
# View system logs
sudo journalctl -u piwardrive -f

# View application logs
tail -f ~/.config/piwardrive/logs/piwardrive.log

# Export logs for analysis
export-log-bundle
```

## Advanced Configuration

### Multi-Device Setup

#### 1. Aggregation Server
```bash
# Install aggregation service
sudo apt install -y docker.io
sudo docker run -d --name piwardrive-aggregation \
  -p 9000:9000 \
  piwardrive/aggregation:latest
```

#### 2. Remote Sync Configuration
```bash
# Configure remote sync
export PW_REMOTE_SYNC_URL="http://aggregation-server:9000/sync"
export PW_REMOTE_SYNC_INTERVAL=300  # 5 minutes
```

### Custom Hardware Integration

#### 1. LED Status Indicators
```bash
# Configure GPIO pins
sudo nano /boot/config.txt
# Add: gpio=18=op,dh  # GPIO 18 as output, default high

# Test LED control
piwardrive-field-status --enable-leds
```

#### 2. External Sensors
```bash
# Configure I2C
sudo raspi-config
# Interface Options > I2C > Enable

# Test sensor detection
i2cdetect -y 1
```

### Kiosk Mode Deployment

#### 1. Auto-Start Configuration
```bash
# Create kiosk service
sudo nano /etc/systemd/system/piwardrive-kiosk.service
```

```ini
[Unit]
Description=PiWardrive Kiosk Mode
After=graphical-session.target

[Service]
Type=simple
User=pi
Environment="DISPLAY=:0"
ExecStart=/usr/local/bin/piwardrive-kiosk
Restart=always

[Install]
WantedBy=graphical-session.target
```

#### 2. Screen Configuration
```bash
# Configure screen power management
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
# Add: @xset s noblank
# Add: @xset s off
# Add: @xset -dpms
```

## Maintenance Schedule

### Daily Tasks (Automated)
- Health checks
- Log rotation
- Database optimization

### Weekly Tasks
- Security updates
- Configuration backup
- Performance monitoring

### Monthly Tasks
- Full system backup
- Hardware inspection
- Documentation updates

## Support and Resources

### Field Support
- [Field Troubleshooting Guide](field-troubleshooting-guide.md)
- [Field Serviceable Components](field-serviceable-components.md)
- Built-in diagnostic tools

### Hardware Support
- [Hardware Compatibility Guide](hardware-compatibility.md)
- Community hardware testing
- Vendor-specific configurations

### Community Resources
- GitHub Issues and Discussions
- Discord/Slack channels
- Documentation wiki

This guide provides a comprehensive foundation for deploying PiWardrive on Raspberry Pi devices. For specific hardware configurations or advanced use cases, consult the detailed documentation and community resources.
