#!/bin/bash

# PiWardrive Advanced Features Installation Script
# This script installs the advanced features and dependencies

set -e

echo "===================================================================================="
echo "PiWardrive Advanced Features Installation Script"
echo "===================================================================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}$1${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root. Please run as a normal user."
   exit 1
fi

print_header "Step 1: System Requirements Check"
echo

# Check OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    print_status "Linux detected"
    
    # Check for Raspberry Pi
    if [[ -f /proc/device-tree/model ]] && grep -q "Raspberry Pi" /proc/device-tree/model; then
        print_status "Raspberry Pi detected"
        IS_RPI=true
    else
        print_status "Standard Linux system detected"
        IS_RPI=false
    fi
else
    print_warning "Non-Linux system detected. Some features may not work correctly."
    IS_RPI=false
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.8.0"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    print_status "Python version $PYTHON_VERSION is supported"
else
    print_error "Python 3.8 or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

# Check available memory
MEMORY_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
MEMORY_GB=$((MEMORY_KB / 1024 / 1024))

if [[ $MEMORY_GB -lt 2 ]]; then
    print_warning "Low memory detected (${MEMORY_GB}GB). 4GB or more is recommended for optimal performance."
else
    print_status "Memory: ${MEMORY_GB}GB"
fi

print_header "Step 2: Installing System Dependencies"
echo

# Update package lists
print_status "Updating package lists..."
sudo apt update -qq

# Install required system packages
SYSTEM_PACKAGES=(
    "python3-pip"
    "python3-venv"
    "python3-dev"
    "build-essential"
    "git"
    "cmake"
    "pkg-config"
    "libjpeg-dev"
    "libtiff5-dev"
    "libjasper-dev"
    "libpng-dev"
    "libavcodec-dev"
    "libavformat-dev"
    "libswscale-dev"
    "libv4l-dev"
    "libxvidcore-dev"
    "libx264-dev"
    "libgtk-3-dev"
    "libatlas-base-dev"
    "gfortran"
    "libhdf5-dev"
    "wireless-tools"
    "iw"
    "gpsd"
    "gpsd-clients"
    "libgps-dev"
)

# Add Raspberry Pi specific packages
if [[ "$IS_RPI" == true ]]; then
    SYSTEM_PACKAGES+=(
        "i2c-tools"
        "python3-rpi.gpio"
        "python3-smbus"
        "python3-spidev"
        "libraspberrypi-dev"
        "raspberrypi-kernel-headers"
    )
fi

print_status "Installing system packages..."
for package in "${SYSTEM_PACKAGES[@]}"; do
    if ! dpkg -l | grep -q "^ii  $package "; then
        print_status "Installing $package..."
        sudo apt install -y "$package" > /dev/null 2>&1
    else
        print_status "$package already installed"
    fi
done

print_header "Step 3: Creating Python Virtual Environment"
echo

# Create virtual environment
VENV_DIR="$HOME/piwardrive-env"

if [[ ! -d "$VENV_DIR" ]]; then
    print_status "Creating virtual environment at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
else
    print_status "Virtual environment already exists at $VENV_DIR"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1

print_header "Step 4: Installing Python Dependencies"
echo

# Install wheel for faster compilation
print_status "Installing wheel..."
pip install wheel > /dev/null 2>&1

# Core dependencies
print_status "Installing core dependencies..."
pip install -q numpy scipy matplotlib seaborn pandas scikit-learn

# Visualization dependencies
print_status "Installing visualization dependencies..."
pip install -q plotly reportlab

# Hardware dependencies
print_status "Installing hardware dependencies..."
pip install -q pyserial pyusb

# Only install OpenCV if not on Raspberry Pi (due to compilation time)
if [[ "$IS_RPI" != true ]]; then
    print_status "Installing OpenCV..."
    pip install -q opencv-python
else
    print_warning "Skipping OpenCV installation on Raspberry Pi. Install manually if needed."
fi

# Web framework dependencies
print_status "Installing web framework dependencies..."
pip install -q flask flask-socketio

# Geospatial dependencies
print_status "Installing geospatial dependencies..."
pip install -q geojson

# Raspberry Pi specific dependencies
if [[ "$IS_RPI" == true ]]; then
    print_status "Installing Raspberry Pi specific dependencies..."
    pip install -q RPi.GPIO smbus2 spidev
    
    # Try to install picamera
    if pip install -q picamera > /dev/null 2>&1; then
        print_status "PiCamera installed successfully"
    else
        print_warning "PiCamera installation failed. Install manually if using camera module."
    fi
fi

print_header "Step 5: Setting Up PiWardrive"
echo

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIWARDRIVE_DIR="$(dirname "$SCRIPT_DIR")"

# Install PiWardrive in development mode
print_status "Installing PiWardrive in development mode..."
cd "$PIWARDRIVE_DIR"
pip install -e .

# Create configuration directory
CONFIG_DIR="$HOME/.config/piwardrive"
if [[ ! -d "$CONFIG_DIR" ]]; then
    print_status "Creating configuration directory..."
    mkdir -p "$CONFIG_DIR"
fi

# Create data directory
DATA_DIR="$HOME/.local/share/piwardrive"
if [[ ! -d "$DATA_DIR" ]]; then
    print_status "Creating data directory..."
    mkdir -p "$DATA_DIR"
fi

# Create logs directory
LOG_DIR="$HOME/.local/share/piwardrive/logs"
if [[ ! -d "$LOG_DIR" ]]; then
    print_status "Creating logs directory..."
    mkdir -p "$LOG_DIR"
fi

# Copy example configuration files
if [[ -f "$PIWARDRIVE_DIR/config/piwardrive.conf.example" ]]; then
    if [[ ! -f "$CONFIG_DIR/piwardrive.conf" ]]; then
        print_status "Creating default configuration..."
        cp "$PIWARDRIVE_DIR/config/piwardrive.conf.example" "$CONFIG_DIR/piwardrive.conf"
    fi
fi

print_header "Step 6: Hardware Configuration"
echo

# Check for wireless adapters
print_status "Checking for wireless adapters..."
if command -v iwconfig &> /dev/null; then
    WIRELESS_ADAPTERS=$(iwconfig 2>/dev/null | grep -c "IEEE 802.11" || echo "0")
    if [[ $WIRELESS_ADAPTERS -gt 0 ]]; then
        print_status "Found $WIRELESS_ADAPTERS wireless adapter(s)"
    else
        print_warning "No wireless adapters found. Connect USB WiFi adapters for scanning."
    fi
else
    print_warning "iwconfig not found. Install wireless-tools package."
fi

# Check for GPS devices
print_status "Checking for GPS devices..."
GPS_DEVICES=$(ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null | wc -l || echo "0")
if [[ $GPS_DEVICES -gt 0 ]]; then
    print_status "Found $GPS_DEVICES potential GPS device(s)"
else
    print_warning "No GPS devices found at /dev/ttyUSB* or /dev/ttyACM*"
fi

# Check I2C (for Raspberry Pi)
if [[ "$IS_RPI" == true ]]; then
    print_status "Checking I2C configuration..."
    if [[ -c /dev/i2c-1 ]]; then
        print_status "I2C is enabled"
    else
        print_warning "I2C is not enabled. Run 'sudo raspi-config' to enable it."
    fi
fi

print_header "Step 7: Creating Service Files"
echo

# Create systemd service file
SERVICE_FILE="/etc/systemd/system/piwardrive.service"
if [[ ! -f "$SERVICE_FILE" ]]; then
    print_status "Creating systemd service file..."
    
    sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=PiWardrive Wireless Scanner
After=network.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$PIWARDRIVE_DIR
Environment=PATH=$VENV_DIR/bin
ExecStart=$VENV_DIR/bin/python -m piwardrive.service
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    print_status "Reloading systemd daemon..."
    sudo systemctl daemon-reload
    
    print_status "Service file created. Enable with: sudo systemctl enable piwardrive"
else
    print_status "Service file already exists"
fi

# Create desktop entry
DESKTOP_FILE="$HOME/.local/share/applications/piwardrive.desktop"
if [[ ! -f "$DESKTOP_FILE" ]]; then
    print_status "Creating desktop entry..."
    
    mkdir -p "$(dirname "$DESKTOP_FILE")"
    
    cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Name=PiWardrive
Comment=Wireless Scanner and Analyzer
Exec=$VENV_DIR/bin/python -m piwardrive.ui.user_experience
Icon=$PIWARDRIVE_DIR/static/icon.png
Terminal=false
Type=Application
Categories=Network;System;
EOF
    
    print_status "Desktop entry created"
fi

print_header "Step 8: Final Configuration"
echo

# Create activation script
ACTIVATE_SCRIPT="$HOME/bin/activate-piwardrive"
mkdir -p "$(dirname "$ACTIVATE_SCRIPT")"

cat > "$ACTIVATE_SCRIPT" <<EOF
#!/bin/bash
# PiWardrive Environment Activation Script
source "$VENV_DIR/bin/activate"
cd "$PIWARDRIVE_DIR"
echo "PiWardrive environment activated"
echo "Python virtual environment: $VENV_DIR"
echo "PiWardrive directory: $PIWARDRIVE_DIR"
echo
echo "Available commands:"
echo "  python -m piwardrive.ui.user_experience    # Start web interface"
echo "  python -m piwardrive.service               # Start service"
echo "  python -m piwardrive --help                # Show help"
echo
EOF

chmod +x "$ACTIVATE_SCRIPT"

# Add to PATH if not already there
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
    print_status "Added $HOME/bin to PATH"
fi

print_header "Installation Complete!"
echo

print_status "PiWardrive Advanced Features have been successfully installed!"
echo
echo "Next steps:"
echo "1. Run: source ~/.bashrc"
echo "2. Run: activate-piwardrive"
echo "3. Run: python -m piwardrive.ui.user_experience"
echo "4. Open browser to: http://localhost:5000"
echo
echo "For system service:"
echo "  sudo systemctl enable piwardrive"
echo "  sudo systemctl start piwardrive"
echo
echo "Configuration files:"
echo "  Config: $CONFIG_DIR/piwardrive.conf"
echo "  Data:   $DATA_DIR"
echo "  Logs:   $LOG_DIR"
echo
echo "Documentation:"
echo "  Advanced Features Report: $PIWARDRIVE_DIR/ADVANCED_FEATURES_IMPLEMENTATION_REPORT.md"
echo "  User Manual: $PIWARDRIVE_DIR/docs/"
echo

if [[ "$IS_RPI" == true ]]; then
    print_warning "Raspberry Pi specific notes:"
    echo "  - Enable I2C for environmental sensors: sudo raspi-config"
    echo "  - Install camera module support: pip install picamera"
    echo "  - Consider using USB WiFi adapters for better scanning"
fi

print_status "Installation completed successfully!"
echo

# Check if reboot is needed
if [[ "$IS_RPI" == true ]] && [[ ! -c /dev/i2c-1 ]]; then
    print_warning "A reboot may be required for all hardware features to work properly."
fi

echo "===================================================================================="
echo "For support and documentation, visit: https://github.com/your-repo/piwardrive"
echo "===================================================================================="
