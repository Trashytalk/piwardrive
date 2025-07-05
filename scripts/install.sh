#!/bin/bash
# PiWardrive Installation Script
# Provides multiple installation options for different use cases

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install system dependencies
install_system_deps() {
    print_info "Installing system dependencies..."
    
    if command_exists apt-get; then
        sudo apt-get update
        sudo apt-get install -y \
            python3 \
            python3-pip \
            python3-venv \
            python3-dev \
            build-essential \
            libdbus-1-dev \
            libglib2.0-dev \
            pkg-config \
            git
    elif command_exists yum; then
        sudo yum install -y \
            python3 \
            python3-pip \
            python3-devel \
            gcc \
            gcc-c++ \
            make \
            dbus-devel \
            glib2-devel \
            pkgconfig \
            git
    elif command_exists pacman; then
        sudo pacman -S --noconfirm \
            python \
            python-pip \
            python-virtualenv \
            base-devel \
            dbus \
            glib2 \
            pkgconf \
            git
    else
        print_warning "Package manager not recognized. Please install system dependencies manually."
        print_info "Required packages: python3, python3-pip, python3-venv, python3-dev, build-essential, libdbus-1-dev, libglib2.0-dev, pkg-config, git"
    fi
}

# Function to create virtual environment
create_venv() {
    print_info "Creating virtual environment..."
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Virtual environment created"
    else
        print_info "Virtual environment already exists"
    fi
    
    source venv/bin/activate
    pip install --upgrade pip setuptools wheel
}

# Function for minimal installation
install_minimal() {
    print_info "Installing PiWardrive - Minimal Installation"
    print_info "This includes only core dependencies (~20 packages)"
    
    create_venv
    source venv/bin/activate
    
    print_info "Installing core dependencies..."
    pip install -r requirements-core.txt
    
    print_info "Installing PiWardrive package..."
    pip install -e .
    
    print_success "Minimal installation completed!"
    print_info "Activate environment with: source venv/bin/activate"
    print_info "Run with: python -m piwardrive.webui_server"
}

# Function for full installation
install_full() {
    print_info "Installing PiWardrive - Full Installation"
    print_info "This includes all optional features (~50-60 packages)"
    
    create_venv
    source venv/bin/activate
    
    print_info "Installing all dependencies..."
    pip install -r requirements.txt
    
    print_info "Installing PiWardrive package with all features..."
    pip install -e .[all]
    
    print_success "Full installation completed!"
    print_info "Activate environment with: source venv/bin/activate"
    print_info "Run with: python -m piwardrive.webui_server"
}

# Function for full + development installation
install_full_dev() {
    print_info "Installing PiWardrive - Full + Development Installation"
    print_info "This includes all features plus development tools (~70-80 packages)"
    
    create_venv
    source venv/bin/activate
    
    print_info "Installing all dependencies..."
    pip install -r requirements.txt
    
    print_info "Installing development dependencies..."
    pip install -r requirements-dev.txt
    
    print_info "Installing PiWardrive package with all features..."
    pip install -e .[all,development]
    
    print_info "Setting up pre-commit hooks..."
    pre-commit install
    
    print_success "Full + Development installation completed!"
    print_info "Activate environment with: source venv/bin/activate"
    print_info "Run with: python -m piwardrive.webui_server"
    print_info "Development tools available: make lint, make test, make deps-audit"
}

# Function to display help
show_help() {
    echo "PiWardrive Installation Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Installation Options:"
    echo "  minimal     Install only core dependencies (~20 packages)"
    echo "              Best for: Production deployments, resource-constrained systems"
    echo "              Features: Web UI, basic mapping, GPS, database"
    echo ""
    echo "  full        Install all features (~50-60 packages)"
    echo "              Best for: Full-featured deployments, data analysis"
    echo "              Features: All core + scientific computing, visualization, hardware support"
    echo ""
    echo "  full-dev    Install all features + development tools (~70-80 packages)"
    echo "              Best for: Development, contributing, testing"
    echo "              Features: All features + linting, testing, security scanning"
    echo ""
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 minimal      # Minimal installation"
    echo "  $0 full         # Full installation"
    echo "  $0 full-dev     # Full + development installation"
    echo ""
    echo "After installation, activate the environment with:"
    echo "  source venv/bin/activate"
    echo ""
    echo "Then run PiWardrive with:"
    echo "  python -m piwardrive.webui_server"
}

# Main installation logic
main() {
    print_info "PiWardrive Installation Script"
    print_info "Current directory: $(pwd)"
    
    # Check if we're in the right directory
    if [ ! -f "requirements.txt" ] || [ ! -f "requirements-core.txt" ]; then
        print_error "Installation files not found. Please run this script from the PiWardrive project root."
        exit 1
    fi
    
    # Parse command line arguments
    case "${1:-}" in
        minimal)
            install_system_deps
            install_minimal
            ;;
        full)
            install_system_deps
            install_full
            ;;
        full-dev)
            install_system_deps
            install_full_dev
            ;;
        help|--help|-h)
            show_help
            ;;
        "")
            print_error "No installation option specified."
            echo ""
            show_help
            exit 1
            ;;
        *)
            print_error "Unknown option: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
