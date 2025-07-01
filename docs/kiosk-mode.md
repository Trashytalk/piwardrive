# PiWardrive Kiosk Mode Configuration

## Table of Contents
- [Overview](#overview)
- [Quick Setup](#quick-setup)
- [Hardware Requirements](#hardware-requirements)
- [Kiosk Configuration](#kiosk-configuration)
- [Display Setup](#display-setup)
- [Touch Screen Configuration](#touch-screen-configuration)
- [Auto-Start Configuration](#auto-start-configuration)
- [Browser Optimization](#browser-optimization)
- [Security Considerations](#security-considerations)
- [Power Management](#power-management)
- [Remote Management](#remote-management)
- [Troubleshooting](#troubleshooting)
- [Performance Optimization](#performance-optimization)

## Overview

Kiosk mode transforms your Raspberry Pi into a dedicated PiWardrive terminal with a full-screen web interface. This mode is ideal for:

- **Permanent installations** in vehicles or fixed locations
- **Public demonstrations** and trade shows
- **Dedicated monitoring stations** for network security
- **Portable field units** with touch screen interfaces
- **Unattended operation** with automatic recovery

### Features

- **Full-screen web interface** with no browser chrome
- **Automatic startup** and crash recovery
- **Touch screen optimization** with gesture support
- **Auto-refresh** and connection monitoring
- **Screen blanking** and power management
- **Remote configuration** and monitoring
- **Security hardening** for public access

## Quick Setup

### One-Command Kiosk Setup

```bash
# Download and run kiosk setup script
curl -fsSL https://raw.githubusercontent.com/username/piwardrive/main/scripts/setup-kiosk.sh | sudo bash

# Or with custom options
curl -fsSL https://raw.githubusercontent.com/username/piwardrive/main/scripts/setup-kiosk.sh -o setup-kiosk.sh
chmod +x setup-kiosk.sh
sudo ./setup-kiosk.sh --touchscreen --auto-start --secure
```

### Manual Quick Setup

```bash
# Install kiosk dependencies
sudo apt update && sudo apt install -y \
    xorg \
    chromium-browser \
    unclutter \
    x11-xserver-utils

# Configure auto-login
sudo raspi-config nonint do_boot_behaviour B4

# Set up kiosk user
sudo useradd -m -s /bin/bash kiosk
echo 'kiosk:piwardrive' | sudo chpasswd

# Configure X11 auto-start
sudo mkdir -p /home/kiosk/.config/autostart
sudo tee /home/kiosk/.config/autostart/piwardrive-kiosk.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=PiWardrive Kiosk
Exec=/home/kiosk/start-kiosk.sh
Hidden=false
X-GNOME-Autostart-enabled=true
EOF

# Create kiosk startup script
sudo tee /home/kiosk/start-kiosk.sh << 'EOF'
#!/bin/bash
export DISPLAY=:0
chromium-browser --kiosk --no-sandbox --disable-infobars http://localhost:8000
EOF

sudo chmod +x /home/kiosk/start-kiosk.sh
sudo chown -R kiosk:kiosk /home/kiosk
```

## Hardware Requirements

### Recommended Hardware

| Component | Specification | Notes |
|-----------|---------------|-------|
| **Display** | 7" - 24" touchscreen | Official Pi touchscreen recommended |
| **Pi Model** | Pi 4 (4GB+) or Pi 5 | Pi 3 minimum for basic functionality |
| **Storage** | 32GB+ microSD or SSD | SSD recommended for reliability |
| **Power** | 5V 3A+ official supply | Stable power critical for displays |
| **Case** | Touchscreen-compatible | Consider cooling for enclosed setups |

### Tested Displays

#### Official Raspberry Pi Displays
```bash
# 7" Official Touchscreen
- Resolution: 800x480
- Interface: DSI
- Touch: Capacitive (10-point)
- Power: Via GPIO
- Mounting: VESA compatible
```

#### HDMI Displays
```bash
# Generic HDMI monitors
- Resolution: 1920x1080 recommended
- Interface: HDMI
- Touch: USB (if supported)
- Power: External
- Mounting: Standard VESA
```

#### USB Touch Displays
```bash
# Portable USB displays
- Resolution: 1024x600 to 1920x1080
- Interface: USB-C or USB-A
- Touch: Integrated USB HID
- Power: USB powered
- Mounting: Varies by model
```

## Kiosk Configuration

### System Configuration

#### 1. Configure Boot Behavior

```bash
# Enable auto-login to desktop (Pi 4/5)
sudo raspi-config nonint do_boot_behaviour B4

# Or auto-login to console (Pi 3)
sudo raspi-config nonint do_boot_behaviour B2

# Disable splash screen
echo 'disable_splash=1' | sudo tee -a /boot/firmware/config.txt

# Reduce boot time
echo 'boot_delay=0' | sudo tee -a /boot/firmware/config.txt
echo 'initial_turbo=60' | sudo tee -a /boot/firmware/config.txt
```

#### 2. Install Desktop Environment

```bash
# Minimal desktop for kiosk mode
sudo apt install -y \
    xserver-xorg \
    xinit \
    openbox \
    chromium-browser \
    unclutter \
    x11-xserver-utils \
    xdotool

# Optional: Install lightweight desktop
sudo apt install -y lxde-core

# Remove unnecessary packages
sudo apt purge -y \
    wolfram-engine \
    libreoffice* \
    scratch* \
    minecraft-pi \
    sonic-pi
sudo apt autoremove -y
```

#### 3. Create Kiosk User

```bash
# Create dedicated kiosk user
sudo useradd -m -G video,audio,input,netdev -s /bin/bash kiosk

# Set password
echo 'kiosk:piwardrive123' | sudo chpasswd

# Configure sudo access (if needed)
echo 'kiosk ALL=(ALL) NOPASSWD: /sbin/reboot, /sbin/shutdown' | sudo tee /etc/sudoers.d/kiosk

# Set up user directories
sudo -u kiosk mkdir -p /home/kiosk/{.config/autostart,.local/bin,scripts}
```

### Display Configuration

#### 1. Screen Resolution and Rotation

```bash
# Set resolution for HDMI displays
echo 'hdmi_group=2' | sudo tee -a /boot/firmware/config.txt
echo 'hdmi_mode=82' | sudo tee -a /boot/firmware/config.txt  # 1920x1080 60Hz

# Rotate display (if needed)
echo 'display_rotate=1' | sudo tee -a /boot/firmware/config.txt  # 90 degrees

# Force HDMI output
echo 'hdmi_force_hotplug=1' | sudo tee -a /boot/firmware/config.txt
```

#### 2. Touchscreen Configuration

```bash
# Official 7" touchscreen setup
echo 'dtoverlay=rpi-ft5406' | sudo tee -a /boot/firmware/config.txt

# Rotate touch input to match display
sudo tee /usr/share/X11/xorg.conf.d/40-libinput.conf << 'EOF'
Section "InputClass"
    Identifier "libinput touchscreen catchall"
    MatchIsTouchscreen "on"
    MatchDevicePath "/dev/input/event*"
    Driver "libinput"
    Option "TransformationMatrix" "0 1 0 -1 0 1 0 0 1"
EndSection
EOF
```

## Touch Screen Configuration

### Calibration and Optimization

#### 1. Touch Calibration

```bash
# Install calibration tools
sudo apt install -y xinput-calibrator

# Run calibration (on the Pi with display attached)
xinput_calibrator

# Apply calibration results
sudo tee /usr/share/X11/xorg.conf.d/99-calibration.conf << 'EOF'
Section "InputClass"
    Identifier "calibration"
    MatchProduct "ADS7846 Touchscreen"
    Option "Calibration" "3919 209 3775 296"
    Option "SwapAxes" "1"
EndSection
EOF
```

#### 2. Touch Gestures and Multi-touch

```bash
# Configure touch gestures for web interface
sudo tee /home/kiosk/.config/touchegg/touchegg.conf << 'EOF'
<touchégg>
    <settings>
        <property name="animation_delay">150</property>
        <property name="action_execute_threshold">20</property>
        <property name="color">auto</property>
        <property name="borderColor">auto</property>
    </settings>
    
    <application name="All">
        <gesture type="SWIPE" direction="LEFT" fingers="2">
            <action type="SEND_KEYS">
                <repeat>false</repeat>
                <keys>Alt+Right</keys>
            </action>
        </gesture>
        
        <gesture type="SWIPE" direction="RIGHT" fingers="2">
            <action type="SEND_KEYS">
                <repeat>false</repeat>
                <keys>Alt+Left</keys>
            </action>
        </gesture>
        
        <gesture type="PINCH" direction="IN" fingers="2">
            <action type="SEND_KEYS">
                <repeat>false</repeat>
                <keys>Control+minus</keys>
            </action>
        </gesture>
        
        <gesture type="PINCH" direction="OUT" fingers="2">
            <action type="SEND_KEYS">
                <repeat>false</repeat>
                <keys>Control+plus</keys>
            </action>
        </gesture>
    </application>
</touchégg>
EOF

# Install and start touchegg
sudo apt install -y touchegg
sudo systemctl enable touchegg
```

#### 3. Virtual Keyboard

```bash
# Install on-screen keyboard
sudo apt install -y onboard

# Configure auto-start for touch-only setups
sudo tee /home/kiosk/.config/autostart/onboard.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Onboard
Exec=onboard --startup-delay=3
Hidden=false
X-GNOME-Autostart-enabled=true
EOF
```

## Auto-Start Configuration

### X11 Auto-Start

#### 1. Openbox Configuration

```bash
# Configure Openbox for kiosk mode
sudo -u kiosk mkdir -p /home/kiosk/.config/openbox

sudo -u kiosk tee /home/kiosk/.config/openbox/autostart << 'EOF'
#!/bin/bash

# Hide cursor after 1 second of inactivity
unclutter -idle 1 -root &

# Disable screen blanking
xset s off
xset -dpms
xset s noblank

# Set desktop wallpaper (optional)
# feh --bg-scale /home/kiosk/wallpaper.jpg &

# Start PiWardrive kiosk
/home/kiosk/scripts/start-piwardrive-kiosk.sh &
EOF

chmod +x /home/kiosk/.config/openbox/autostart
```

#### 2. Kiosk Startup Script

```bash
# Create main kiosk startup script
sudo -u kiosk tee /home/kiosk/scripts/start-piwardrive-kiosk.sh << 'EOF'
#!/bin/bash

# PiWardrive Kiosk Mode Startup Script
export DISPLAY=:0

# Configuration
PIWARDRIVE_URL="http://localhost:8000"
BROWSER_USER_DATA="/home/kiosk/.config/chromium-kiosk"
RESTART_DELAY=5
MAX_RESTARTS=10
LOG_FILE="/home/kiosk/kiosk.log"

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Wait for PiWardrive to be available
wait_for_piwardrive() {
    log "Waiting for PiWardrive service..."
    while ! curl -s "$PIWARDRIVE_URL/health" > /dev/null 2>&1; do
        sleep 2
    done
    log "PiWardrive service is available"
}

# Clean up browser data on startup
cleanup_browser() {
    log "Cleaning up browser data..."
    rm -rf "$BROWSER_USER_DATA/Singleton*"
    rm -rf "$BROWSER_USER_DATA/SingletonSocket"
}

# Start browser in kiosk mode
start_browser() {
    log "Starting browser in kiosk mode..."
    
    chromium-browser \
        --kiosk \
        --no-sandbox \
        --disable-web-security \
        --disable-features=VizDisplayCompositor \
        --disable-infobars \
        --disable-restore-session-state \
        --disable-session-crashed-bubble \
        --disable-component-update \
        --disable-background-timer-throttling \
        --disable-backgrounding-occluded-windows \
        --disable-renderer-backgrounding \
        --disable-field-trial-config \
        --disable-ipc-flooding-protection \
        --no-first-run \
        --fast \
        --fast-start \
        --aggressive-cache-discard \
        --user-data-dir="$BROWSER_USER_DATA" \
        --app="$PIWARDRIVE_URL" \
        --window-position=0,0 \
        --start-fullscreen \
        --check-for-update-interval=31536000 \
        "$PIWARDRIVE_URL" \
        2>&1 | tee -a "$LOG_FILE"
}

# Main loop with restart capability
main() {
    log "Starting PiWardrive kiosk mode"
    
    restart_count=0
    
    while [ $restart_count -lt $MAX_RESTARTS ]; do
        # Wait for service
        wait_for_piwardrive
        
        # Clean up
        cleanup_browser
        
        # Start browser
        start_browser
        
        # Browser exited, increment restart counter
        restart_count=$((restart_count + 1))
        log "Browser exited. Restart attempt $restart_count/$MAX_RESTARTS"
        
        if [ $restart_count -lt $MAX_RESTARTS ]; then
            log "Restarting in $RESTART_DELAY seconds..."
            sleep $RESTART_DELAY
        fi
    done
    
    log "Maximum restart attempts reached. Rebooting system..."
    sudo reboot
}

# Start main function
main
EOF

chmod +x /home/kiosk/scripts/start-piwardrive-kiosk.sh
```

#### 3. Auto-Login Configuration

```bash
# Configure auto-login for kiosk user
sudo tee /etc/systemd/system/getty@tty1.service.d/autologin.conf << 'EOF'
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin kiosk --noclear %I $TERM
EOF

sudo systemctl daemon-reload
sudo systemctl enable getty@tty1.service
```

#### 4. X11 Session Configuration

```bash
# Configure .xinitrc for automatic X11 startup
sudo -u kiosk tee /home/kiosk/.xinitrc << 'EOF'
#!/bin/bash

# Load X resources
xrdb -merge ~/.Xresources 2>/dev/null || true

# Start window manager
exec openbox-session
EOF

chmod +x /home/kiosk/.xinitrc

# Configure automatic X11 startup
sudo -u kiosk tee -a /home/kiosk/.profile << 'EOF'

# Auto-start X11 session if on tty1
if [ -z "$DISPLAY" ] && [ "$XDG_VTNR" = 1 ]; then
    exec startx
fi
EOF
```

### Systemd Service (Alternative)

```bash
# Create systemd service for kiosk mode
sudo tee /etc/systemd/system/piwardrive-kiosk.service << 'EOF'
[Unit]
Description=PiWardrive Kiosk Mode
After=piwardrive.service
Wants=piwardrive.service
Conflicts=getty@tty1.service

[Service]
Type=simple
User=kiosk
Environment=DISPLAY=:0
ExecStartPre=/bin/bash -c 'while ! curl -s http://localhost:8000/health; do sleep 2; done'
ExecStart=/usr/bin/startx /home/kiosk/scripts/start-piwardrive-kiosk.sh -- :0 vt1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable piwardrive-kiosk.service
```

## Browser Optimization

### Chromium Configuration

#### 1. Performance Optimization

```bash
# Create optimized Chromium preferences
sudo -u kiosk mkdir -p /home/kiosk/.config/chromium-kiosk/Default

sudo -u kiosk tee /home/kiosk/.config/chromium-kiosk/Default/Preferences << 'EOF'
{
   "browser": {
      "show_home_button": false,
      "check_default_browser": false
   },
   "bookmark_bar": {
      "show_on_all_tabs": false
   },
   "distribution": {
      "skip_first_run_ui": true,
      "import_bookmarks": false,
      "import_history": false,
      "import_search_engine": false,
      "make_chrome_default": false,
      "make_chrome_default_for_user": false
   },
   "first_run_tabs": [
      "http://localhost:8000"
   ],
   "homepage": "http://localhost:8000",
   "homepage_is_newtabpage": false,
   "session": {
      "restore_on_startup": 4,
      "startup_urls": [
         "http://localhost:8000"
      ]
   }
}
EOF
```

#### 2. Memory Management

```bash
# Create memory optimization script
sudo -u kiosk tee /home/kiosk/scripts/memory-cleanup.sh << 'EOF'
#!/bin/bash

# Memory cleanup for long-running kiosk
while true; do
    sleep 300  # Every 5 minutes
    
    # Get memory usage
    MEMORY_USAGE=$(free | grep '^Mem:' | awk '{print ($3/$2) * 100.0}')
    
    # If memory usage > 80%, restart browser
    if (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
        echo "$(date): High memory usage ($MEMORY_USAGE%), restarting browser"
        pkill chromium-browser
        sleep 5
        /home/kiosk/scripts/start-piwardrive-kiosk.sh &
    fi
done
EOF

chmod +x /home/kiosk/scripts/memory-cleanup.sh
```

#### 3. Browser Extensions (Kiosk Mode)

```bash
# Install kiosk-specific extensions
sudo -u kiosk mkdir -p /home/kiosk/.config/chromium-kiosk/External\ Extensions

# Auto-refresh extension configuration
sudo -u kiosk tee '/home/kiosk/.config/chromium-kiosk/External Extensions/auto-refresh.json' << 'EOF'
{
   "external_crx": "/home/kiosk/extensions/auto-refresh.crx",
   "external_version": "1.0"
}
EOF
```

## Security Considerations

### System Hardening

#### 1. User Restrictions

```bash
# Restrict kiosk user capabilities
sudo tee /etc/security/limits.d/kiosk.conf << 'EOF'
kiosk soft nproc 50
kiosk hard nproc 100
kiosk soft nofile 1024
kiosk hard nofile 2048
EOF

# Disable unnecessary services for kiosk user
sudo -u kiosk tee /home/kiosk/.bashrc << 'EOF'
# Minimal bash configuration for kiosk mode
export HISTSIZE=0
export HISTFILESIZE=0
unset HISTFILE

# Restrict commands
alias rm='echo "rm disabled"'
alias mv='echo "mv disabled"'
alias cp='echo "cp disabled for system files"'
EOF
```

#### 2. Network Security

```bash
# Configure firewall for kiosk mode
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 8000/tcp  # PiWardrive web interface
sudo ufw allow 22/tcp    # SSH (if needed)

# Restrict local access
sudo tee /etc/hosts.deny << 'EOF'
ALL: ALL EXCEPT 127.0.0.1
EOF
```

#### 3. File System Protection

```bash
# Mount sensitive directories as read-only
sudo tee -a /etc/fstab << 'EOF'
tmpfs /tmp tmpfs defaults,nodev,nosuid,size=100M 0 0
tmpfs /var/tmp tmpfs defaults,nodev,nosuid,size=50M 0 0
EOF

# Protect configuration files
sudo chmod 600 /etc/piwardrive/piwardrive.yaml
sudo chown root:root /etc/piwardrive/piwardrive.yaml
```

### Kiosk Security

#### 1. Disable Browser Features

```bash
# Create secure browser startup script
sudo -u kiosk tee /home/kiosk/scripts/secure-browser.sh << 'EOF'
#!/bin/bash

# Secure kiosk browser configuration
chromium-browser \
    --kiosk \
    --no-sandbox \
    --disable-dev-shm-usage \
    --disable-extensions \
    --disable-plugins \
    --disable-java \
    --disable-pdf-extension \
    --disable-background-mode \
    --disable-background-networking \
    --disable-sync \
    --disable-translate \
    --disable-suggestions-service \
    --disable-save-password-bubble \
    --disable-session-crashed-bubble \
    --disable-infobars \
    --disable-web-security \
    --no-first-run \
    --incognito \
    --user-data-dir=/tmp/chromium-kiosk \
    --app=http://localhost:8000
EOF

chmod +x /home/kiosk/scripts/secure-browser.sh
```

#### 2. Physical Security

```bash
# Disable virtual terminals access
sudo systemctl mask getty@tty2.service
sudo systemctl mask getty@tty3.service
sudo systemctl mask getty@tty4.service
sudo systemctl mask getty@tty5.service
sudo systemctl mask getty@tty6.service

# Disable keyboard shortcuts
sudo -u kiosk tee /home/kiosk/.config/openbox/rc.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<openbox_config xmlns="http://openbox.org/3.4/rc" xmlns:xi="http://www.w3.org/2001/XInclude">
  <keyboard>
    <!-- Disable all keyboard shortcuts -->
  </keyboard>
  <mouse>
    <dragThreshold>1</dragThreshold>
    <doubleClickTime>500</doubleClickTime>
    <screenEdgeWarpTime>0</screenEdgeWarpTime>
    <screenEdgeWarpMouse>false</screenEdgeWarpMouse>
  </mouse>
</openbox_config>
EOF
```

## Power Management

### Screen Blanking

#### 1. Intelligent Screen Blanking

```bash
# Create smart screen blanking script
sudo -u kiosk tee /home/kiosk/scripts/screen-manager.sh << 'EOF'
#!/bin/bash

# Intelligent screen management for kiosk mode
export DISPLAY=:0

BLANK_DELAY=300  # 5 minutes
SCAN_ACTIVE_CHECK_URL="http://localhost:8000/api/v1/wifi/scans/active"

while true; do
    # Check if active scan is running
    if curl -s "$SCAN_ACTIVE_CHECK_URL" | grep -q '"active":true'; then
        # Keep screen on during active scans
        xset -dpms
        xset s off
        echo "$(date): Active scan detected, keeping screen on"
        sleep 30
    else
        # Enable screen blanking when idle
        xset +dpms
        xset s "$BLANK_DELAY"
        echo "$(date): No active scan, enabling screen blanking"
        sleep 60
    fi
done
EOF

chmod +x /home/kiosk/scripts/screen-manager.sh
```

#### 2. Scheduled Screen Control

```bash
# Create scheduled screen control
sudo -u kiosk tee /home/kiosk/scripts/scheduled-screen.sh << 'EOF'
#!/bin/bash

# Schedule-based screen control
export DISPLAY=:0

CURRENT_HOUR=$(date +%H)

# Business hours: 8 AM to 6 PM
if [ "$CURRENT_HOUR" -ge 8 ] && [ "$CURRENT_HOUR" -le 18 ]; then
    # Business hours - keep screen on
    xset -dpms
    xset s off
    echo "$(date): Business hours - screen active"
else
    # After hours - allow screen blanking
    xset +dpms
    xset s 120  # 2 minutes
    echo "$(date): After hours - screen blanking enabled"
fi
EOF

chmod +x /home/kiosk/scripts/scheduled-screen.sh

# Add to crontab
(sudo -u kiosk crontab -l 2>/dev/null; echo "0 * * * * /home/kiosk/scripts/scheduled-screen.sh") | sudo -u kiosk crontab -
```

### Automatic Recovery

#### 1. Watchdog Timer

```bash
# Enable hardware watchdog
echo 'dtparam=watchdog=on' | sudo tee -a /boot/firmware/config.txt

# Install watchdog daemon
sudo apt install -y watchdog

# Configure watchdog
sudo tee /etc/watchdog.conf << 'EOF'
watchdog-device = /dev/watchdog
interval = 10
logtick = 1
realtime = yes
priority = 1

# Test conditions
loadavg-5 = 24
loadavg-15 = 18
max-load-1 = 24

# Custom test
test-binary = /home/kiosk/scripts/watchdog-test.sh
test-timeout = 60
EOF

# Create watchdog test script
sudo tee /home/kiosk/scripts/watchdog-test.sh << 'EOF'
#!/bin/bash

# Test if PiWardrive is responsive
if curl -s --max-time 10 http://localhost:8000/health > /dev/null; then
    exit 0  # Healthy
else
    exit 1  # Unhealthy
fi
EOF

chmod +x /home/kiosk/scripts/watchdog-test.sh

# Enable watchdog service
sudo systemctl enable watchdog
```

#### 2. Application Health Monitoring

```bash
# Create health monitoring script
sudo -u kiosk tee /home/kiosk/scripts/health-monitor.sh << 'EOF'
#!/bin/bash

# Application health monitoring
LOG_FILE="/home/kiosk/health.log"
RESTART_SCRIPT="/home/kiosk/scripts/restart-kiosk.sh"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Check PiWardrive service
check_piwardrive() {
    if ! curl -s --max-time 10 http://localhost:8000/health > /dev/null; then
        log "PiWardrive service not responding"
        return 1
    fi
    return 0
}

# Check browser process
check_browser() {
    if ! pgrep chromium-browser > /dev/null; then
        log "Browser process not found"
        return 1
    fi
    return 0
}

# Check X11 session
check_x11() {
    if ! pgrep Xorg > /dev/null; then
        log "X11 session not found"
        return 1
    fi
    return 0
}

# Main monitoring loop
while true; do
    if ! check_piwardrive || ! check_browser || ! check_x11; then
        log "Health check failed, restarting kiosk"
        "$RESTART_SCRIPT"
        sleep 30
    fi
    sleep 60
done
EOF

chmod +x /home/kiosk/scripts/health-monitor.sh
```

## Remote Management

### SSH Access

#### 1. Secure SSH Configuration

```bash
# Configure SSH for remote management
sudo tee -a /etc/ssh/sshd_config << 'EOF'

# Kiosk-specific SSH configuration
AllowUsers pi admin
DenyUsers kiosk
PermitRootLogin no
PasswordAuthentication yes
PubkeyAuthentication yes
X11Forwarding yes
X11UseLocalhost no
EOF

sudo systemctl restart ssh
```

#### 2. Remote Screen Access

```bash
# Install VNC server for remote access
sudo apt install -y tightvncserver

# Configure VNC for kiosk user (optional)
sudo -u kiosk tee /home/kiosk/.vnc/xstartup << 'EOF'
#!/bin/bash
xrdb $HOME/.Xresources
startx &
EOF

chmod +x /home/kiosk/.vnc/xstartup
```

### Web-Based Remote Control

#### 1. Remote Control Interface

```bash
# Create remote control script
sudo tee /opt/piwardrive/scripts/remote-control.py << 'EOF'
#!/usr/bin/env python3
"""
Remote control interface for PiWardrive kiosk mode
"""

import subprocess
import flask
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/kiosk/restart', methods=['POST'])
def restart_kiosk():
    """Restart kiosk browser"""
    try:
        subprocess.run(['pkill', 'chromium-browser'], check=False)
        subprocess.Popen(['/home/kiosk/scripts/start-piwardrive-kiosk.sh'])
        return jsonify({'status': 'success', 'message': 'Kiosk restarted'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/kiosk/screen/on', methods=['POST'])
def screen_on():
    """Turn screen on"""
    try:
        os.environ['DISPLAY'] = ':0'
        subprocess.run(['xset', '-dpms'], check=True)
        subprocess.run(['xset', 's', 'off'], check=True)
        return jsonify({'status': 'success', 'message': 'Screen activated'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/kiosk/screen/off', methods=['POST'])
def screen_off():
    """Turn screen off"""
    try:
        os.environ['DISPLAY'] = ':0'
        subprocess.run(['xset', 'dpms', 'force', 'off'], check=True)
        return jsonify({'status': 'success', 'message': 'Screen deactivated'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/kiosk/status', methods=['GET'])
def kiosk_status():
    """Get kiosk status"""
    try:
        # Check browser process
        browser_running = subprocess.run(['pgrep', 'chromium-browser'], 
                                       capture_output=True).returncode == 0
        
        # Check X11 session
        x11_running = subprocess.run(['pgrep', 'Xorg'], 
                                   capture_output=True).returncode == 0
        
        return jsonify({
            'status': 'success',
            'browser_running': browser_running,
            'x11_running': x11_running,
            'uptime': subprocess.check_output(['uptime']).decode().strip()
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=False)
EOF

chmod +x /opt/piwardrive/scripts/remote-control.py
```

#### 2. Remote Control Service

```bash
# Create systemd service for remote control
sudo tee /etc/systemd/system/piwardrive-remote.service << 'EOF'
[Unit]
Description=PiWardrive Remote Control
After=piwardrive.service

[Service]
Type=simple
User=kiosk
ExecStart=/usr/bin/python3 /opt/piwardrive/scripts/remote-control.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable piwardrive-remote.service
sudo systemctl start piwardrive-remote.service
```

## Troubleshooting

### Common Issues

#### 1. Display Not Working

```bash
# Check display connection
dmesg | grep -i display

# Test X11 configuration
sudo -u kiosk DISPLAY=:0 xrandr

# Check graphics driver
lsmod | grep vc4

# Force HDMI output
echo 'hdmi_force_hotplug=1' | sudo tee -a /boot/firmware/config.txt
```

#### 2. Touch Not Responding

```bash
# List input devices
sudo -u kiosk DISPLAY=:0 xinput list

# Test touch input
sudo -u kiosk DISPLAY=:0 evtest /dev/input/event0

# Recalibrate touch
sudo -u kiosk DISPLAY=:0 xinput_calibrator
```

#### 3. Browser Issues

```bash
# Check browser logs
tail -f /home/kiosk/kiosk.log

# Reset browser data
rm -rf /home/kiosk/.config/chromium-kiosk

# Test browser manually
sudo -u kiosk DISPLAY=:0 chromium-browser --kiosk http://localhost:8000
```

#### 4. Service Problems

```bash
# Check kiosk service status
sudo systemctl status piwardrive-kiosk.service

# Check logs
sudo journalctl -u piwardrive-kiosk.service -f

# Restart services
sudo systemctl restart piwardrive-kiosk.service
```

### Debug Mode

#### 1. Enable Debug Logging

```bash
# Create debug startup script
sudo -u kiosk tee /home/kiosk/scripts/debug-kiosk.sh << 'EOF'
#!/bin/bash

export DISPLAY=:0
export DEBUG=1

# Start with verbose logging
chromium-browser \
    --kiosk \
    --enable-logging \
    --log-level=0 \
    --v=1 \
    --app=http://localhost:8000 \
    2>&1 | tee /home/kiosk/debug.log
EOF

chmod +x /home/kiosk/scripts/debug-kiosk.sh
```

#### 2. System Monitoring

```bash
# Create monitoring script for troubleshooting
sudo tee /home/kiosk/scripts/monitor-system.sh << 'EOF'
#!/bin/bash

# System monitoring for kiosk troubleshooting
while true; do
    echo "=== $(date) ===" >> /home/kiosk/system-monitor.log
    
    # CPU and memory usage
    echo "CPU/Memory:" >> /home/kiosk/system-monitor.log
    top -bn1 | head -5 >> /home/kiosk/system-monitor.log
    
    # Disk usage
    echo "Disk Usage:" >> /home/kiosk/system-monitor.log
    df -h >> /home/kiosk/system-monitor.log
    
    # Process list
    echo "Kiosk Processes:" >> /home/kiosk/system-monitor.log
    ps aux | grep -E "(chromium|Xorg|openbox)" >> /home/kiosk/system-monitor.log
    
    echo "" >> /home/kiosk/system-monitor.log
    sleep 300  # Every 5 minutes
done
EOF

chmod +x /home/kiosk/scripts/monitor-system.sh
```

## Performance Optimization

### System Optimization

#### 1. GPU Memory Configuration

```bash
# Optimize GPU memory for display performance
echo 'gpu_mem=128' | sudo tee -a /boot/firmware/config.txt

# Enable GPU acceleration
echo 'dtoverlay=vc4-kms-v3d' | sudo tee -a /boot/firmware/config.txt

# Optimize for high-resolution displays
echo 'hdmi_enable_4kp60=1' | sudo tee -a /boot/firmware/config.txt  # Pi 4/5 only
```

#### 2. CPU Governor

```bash
# Set performance CPU governor for kiosk mode
echo 'performance' | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor

# Make permanent
echo 'GOVERNOR="performance"' | sudo tee -a /etc/default/cpufrequtils
```

#### 3. Memory Optimization

```bash
# Configure swap for kiosk mode
sudo dphys-swapfile swapoff
sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=512/' /etc/dphys-swapfile
sudo dphys-swapfile setup
sudo dphys-swapfile swapon

# Optimize memory allocation
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
```

### Browser Performance

#### 1. Hardware Acceleration

```bash
# Enable hardware acceleration in browser
sudo -u kiosk tee /home/kiosk/.config/chromium-kiosk/Local\ State << 'EOF'
{
   "browser": {
      "enabled_labs_experiments": [
         "enable-gpu-rasterization@1",
         "enable-zero-copy@1"
      ]
   }
}
EOF
```

#### 2. Cache Optimization

```bash
# Configure browser cache for performance
mkdir -p /tmp/chromium-cache
chown kiosk:kiosk /tmp/chromium-cache

# Add cache options to browser startup
CACHE_OPTIONS="--disk-cache-dir=/tmp/chromium-cache --disk-cache-size=104857600"  # 100MB
```

This comprehensive kiosk mode documentation provides everything needed to transform a Raspberry Pi into a dedicated PiWardrive terminal with full-screen operation, touch screen support, automatic recovery, and remote management capabilities.
