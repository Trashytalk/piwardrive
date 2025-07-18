#!/bin/bash
# Field Support Installation Script
# Installs field support tools and configurations

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "This script must be run as root"
    exit 1
fi

print_info "Installing PiWardrive Field Support Tools..."

# Create directories
print_info "Creating directories..."
mkdir -p /etc/piwardrive
mkdir -p /var/log/piwardrive
mkdir -p /var/lib/piwardrive
mkdir -p /opt/piwardrive/field-tools

# Copy configuration files
print_info "Installing configuration files..."
if [ -f "examples/problem-reporter.conf" ]; then
    cp examples/problem-reporter.conf /etc/piwardrive/
    chmod 644 /etc/piwardrive/problem-reporter.conf
fi

# Install systemd service
print_info "Installing problem reporter service..."
if [ -f "examples/piwardrive-problem-reporter.service" ]; then
    cp examples/piwardrive-problem-reporter.service /etc/systemd/system/
    systemctl daemon-reload
fi

# Install daemon service files
print_info "Installing daemon services..."
if [ -f "examples/piwardrive-field-diagnostics.service" ]; then
    cp examples/piwardrive-field-diagnostics.service /etc/systemd/system/
fi

if [ -f "examples/piwardrive-mobile-diagnostics.service" ]; then
    cp examples/piwardrive-mobile-diagnostics.service /etc/systemd/system/
fi

# Install field diagnostic tools
print_info "Installing field diagnostic tools..."
cp scripts/field_diagnostics.py /opt/piwardrive/field-tools/
cp scripts/problem_reporter.py /opt/piwardrive/field-tools/
cp scripts/mobile_diagnostics.py /opt/piwardrive/field-tools/
chmod +x /opt/piwardrive/field-tools/*.py

# Create symbolic links for easy access
print_info "Creating command shortcuts..."
ln -sf /opt/piwardrive/field-tools/field_diagnostics.py /usr/local/bin/piwardrive-field-diag
ln -sf /opt/piwardrive/field-tools/mobile_diagnostics.py /usr/local/bin/piwardrive-mobile-diag

# Create daemon control scripts
print_info "Creating daemon control scripts..."
cat > /usr/local/bin/piwardrive-field-daemon << 'EOF'
#!/bin/bash
# PiWardrive Field Diagnostics Daemon Control Script

case "$1" in
    start)
        echo "Starting PiWardrive field diagnostics daemon..."
        systemctl start piwardrive-field-diagnostics
        ;;
    stop)
        echo "Stopping PiWardrive field diagnostics daemon..."
        systemctl stop piwardrive-field-diagnostics
        ;;
    restart)
        echo "Restarting PiWardrive field diagnostics daemon..."
        systemctl restart piwardrive-field-diagnostics
        ;;
    status)
        systemctl status piwardrive-field-diagnostics
        ;;
    enable)
        echo "Enabling PiWardrive field diagnostics daemon..."
        systemctl enable piwardrive-field-diagnostics
        ;;
    disable)
        echo "Disabling PiWardrive field diagnostics daemon..."
        systemctl disable piwardrive-field-diagnostics
        ;;
    logs)
        journalctl -u piwardrive-field-diagnostics -f
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|enable|disable|logs}"
        exit 1
        ;;
esac
EOF

chmod +x /usr/local/bin/piwardrive-field-daemon

cat > /usr/local/bin/piwardrive-mobile-daemon << 'EOF'
#!/bin/bash
# PiWardrive Mobile Diagnostics Daemon Control Script

case "$1" in
    start)
        echo "Starting PiWardrive mobile diagnostics daemon..."
        systemctl start piwardrive-mobile-diagnostics
        ;;
    stop)
        echo "Stopping PiWardrive mobile diagnostics daemon..."
        systemctl stop piwardrive-mobile-diagnostics
        ;;
    restart)
        echo "Restarting PiWardrive mobile diagnostics daemon..."
        systemctl restart piwardrive-mobile-diagnostics
        ;;
    status)
        systemctl status piwardrive-mobile-diagnostics
        ;;
    enable)
        echo "Enabling PiWardrive mobile diagnostics daemon..."
        systemctl enable piwardrive-mobile-diagnostics
        ;;
    disable)
        echo "Disabling PiWardrive mobile diagnostics daemon..."
        systemctl disable piwardrive-mobile-diagnostics
        ;;
    logs)
        journalctl -u piwardrive-mobile-diagnostics -f
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|enable|disable|logs}"
        exit 1
        ;;
esac
EOF

chmod +x /usr/local/bin/piwardrive-mobile-daemon

# Set up log rotation
print_info "Setting up log rotation..."
cat > /etc/logrotate.d/piwardrive-field-support << 'EOF'
/var/log/piwardrive-problem-reporter.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    create 644 piwardrive piwardrive
    postrotate
        systemctl reload piwardrive-problem-reporter || true
    endscript
}

/var/log/piwardrive_diagnostics.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    create 644 piwardrive piwardrive
}
EOF

# Install dependencies
print_info "Installing Python dependencies..."
if command -v pip3 >/dev/null 2>&1; then
    pip3 install psutil requests
else
    print_warning "pip3 not found, please install psutil and requests manually"
fi

# Set permissions
print_info "Setting permissions..."
chown -R piwardrive:piwardrive /var/log/piwardrive
chown -R piwardrive:piwardrive /var/lib/piwardrive
chown piwardrive:piwardrive /etc/piwardrive/problem-reporter.conf

# Enable service
print_info "Enabling problem reporter service..."
if systemctl list-unit-files | grep -q piwardrive-problem-reporter.service; then
    systemctl enable piwardrive-problem-reporter.service
    print_info "Service enabled. Start with: systemctl start piwardrive-problem-reporter"
fi

# Create desktop shortcuts for field technicians
print_info "Creating desktop shortcuts..."
cat > /usr/share/applications/piwardrive-field-diagnostics.desktop << 'EOF'
[Desktop Entry]
Name=PiWardrive Field Diagnostics
Comment=Field diagnostic tool for PiWardrive devices
Exec=gnome-terminal -- /usr/local/bin/piwardrive-field-diag
Icon=utilities-system-monitor
Terminal=false
Type=Application
Categories=System;Network;
EOF

cat > /usr/share/applications/piwardrive-mobile-diagnostics.desktop << 'EOF'
[Desktop Entry]
Name=PiWardrive Mobile Diagnostics
Comment=Mobile diagnostic tool for remote PiWardrive devices
Exec=gnome-terminal -- /usr/local/bin/piwardrive-mobile-diag
Icon=network-wired
Terminal=false
Type=Application
Categories=System;Network;
EOF

# Create field technician quick reference
print_info "Creating field technician quick reference..."
cat > /opt/piwardrive/field-tools/QUICK_REFERENCE.txt << 'EOF'
PiWardrive Field Support - Quick Reference

DIAGNOSTIC TOOLS:
- piwardrive-field-diag          : Run full diagnostics on local device
- piwardrive-field-diag --quick  : Run quick diagnostics
- piwardrive-mobile-diag -i IP   : Diagnose remote device
- piwardrive-mobile-diag --reboot: Remotely reboot device

PROBLEM REPORTING:
- systemctl status piwardrive-problem-reporter : Check reporter status
- journalctl -u piwardrive-problem-reporter    : View reporter logs
- systemctl restart piwardrive-problem-reporter: Restart reporter

COMMON ISSUES:
1. Device not responding:
   - Check power LED (should be solid green)
   - Try power cycle (unplug for 30 seconds)
   - Check network connectivity

2. No GPS data:
   - Ensure GPS antenna is connected
   - Check for clear sky view
   - Wait 5-15 minutes for GPS lock

3. High temperature:
   - Check for blocked ventilation
   - Verify cooling fan operation
   - Consider environmental conditions

4. Storage full:
   - Check available space in web interface
   - Clear old data or add storage
   - Consider automatic cleanup settings

LOG FILES:
- /var/log/piwardrive.log               : Main application logs
- /var/log/piwardrive-problem-reporter.log : Problem reporter logs
- /var/log/syslog                       : System logs

CONFIGURATION:
- /etc/piwardrive/problem-reporter.conf : Problem reporter config
- /opt/piwardrive/config/               : Main application config

DOCUMENTATION:
- /opt/piwardrive/docs/field-troubleshooting-guide.md
- /opt/piwardrive/docs/field-serviceable-components.md
EOF

print_info "Installation completed successfully!"
print_info ""
print_info "Field Support Tools Installed:"
print_info "- Field diagnostics: piwardrive-field-diag"
print_info "- Mobile diagnostics: piwardrive-mobile-diag" 
print_info "- Problem reporter service: systemctl start piwardrive-problem-reporter"
print_info "- Field daemon control: piwardrive-field-daemon"
print_info "- Mobile daemon control: piwardrive-mobile-daemon"
print_info ""
print_info "Daemon Services Available:"
print_info "- Field diagnostics daemon: systemctl start piwardrive-field-diagnostics"
print_info "- Mobile diagnostics daemon: systemctl start piwardrive-mobile-diagnostics"
print_info ""
print_info "Documentation available at:"
print_info "- /opt/piwardrive/field-tools/QUICK_REFERENCE.txt"
print_info "- /opt/piwardrive/docs/field-troubleshooting-guide.md"
print_info ""
print_info "Next steps:"
print_info "1. Configure problem reporter: edit /etc/piwardrive/problem-reporter.conf"
print_info "2. Start problem reporter: systemctl start piwardrive-problem-reporter"
print_info "3. Test diagnostics: piwardrive-field-diag --test"
print_info "4. Enable daemon mode: piwardrive-field-daemon enable"
print_info "5. Start daemon: piwardrive-field-daemon start"
print_info "6. Check daemon logs: piwardrive-field-daemon logs"
