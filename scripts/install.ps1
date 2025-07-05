# PiWardrive Installation Script for Windows
# Provides multiple installation options for different use cases

param(
    [Parameter(Position=0)]
    [ValidateSet("minimal", "full", "full-dev", "help")]
    [string]$InstallType = "help"
)

# Function to print colored output
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Function to check if command exists
function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Function to create virtual environment
function New-VirtualEnvironment {
    Write-Info "Creating virtual environment..."
    
    if (!(Test-Path "venv")) {
        python -m venv venv
        Write-Success "Virtual environment created"
    }
    else {
        Write-Info "Virtual environment already exists"
    }
    
    # Activate virtual environment
    & "venv\Scripts\Activate.ps1"
    
    # Upgrade pip
    python -m pip install --upgrade pip setuptools wheel
}

# Function for minimal installation
function Install-Minimal {
    Write-Info "Installing PiWardrive - Minimal Installation"
    Write-Info "This includes only core dependencies (~20 packages)"
    
    New-VirtualEnvironment
    
    Write-Info "Installing core dependencies..."
    pip install -r requirements-core.txt
    
    Write-Info "Installing PiWardrive package..."
    pip install -e .
    
    Write-Success "Minimal installation completed!"
    Write-Info "Activate environment with: venv\Scripts\Activate.ps1"
    Write-Info "Run with: python -m piwardrive.webui_server"
}

# Function for full installation
function Install-Full {
    Write-Info "Installing PiWardrive - Full Installation"
    Write-Info "This includes all optional features (~50-60 packages)"
    
    New-VirtualEnvironment
    
    Write-Info "Installing all dependencies..."
    pip install -r requirements.txt
    
    Write-Info "Installing PiWardrive package with all features..."
    pip install -e .[all]
    
    Write-Success "Full installation completed!"
    Write-Info "Activate environment with: venv\Scripts\Activate.ps1"
    Write-Info "Run with: python -m piwardrive.webui_server"
}

# Function for full + development installation
function Install-FullDev {
    Write-Info "Installing PiWardrive - Full + Development Installation"
    Write-Info "This includes all features plus development tools (~70-80 packages)"
    
    New-VirtualEnvironment
    
    Write-Info "Installing all dependencies..."
    pip install -r requirements.txt
    
    Write-Info "Installing development dependencies..."
    pip install -r requirements-dev.txt
    
    Write-Info "Installing PiWardrive package with all features..."
    pip install -e .[all,development]
    
    Write-Info "Setting up pre-commit hooks..."
    pre-commit install
    
    Write-Success "Full + Development installation completed!"
    Write-Info "Activate environment with: venv\Scripts\Activate.ps1"
    Write-Info "Run with: python -m piwardrive.webui_server"
    Write-Info "Development tools available: make lint, make test, make deps-audit"
}

# Function to display help
function Show-Help {
    Write-Host "PiWardrive Installation Script for Windows" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\scripts\install.ps1 [OPTION]" -ForegroundColor White
    Write-Host ""
    Write-Host "Installation Options:" -ForegroundColor White
    Write-Host "  minimal     Install only core dependencies (~20 packages)" -ForegroundColor White
    Write-Host "              Best for: Production deployments, resource-constrained systems" -ForegroundColor Gray
    Write-Host "              Features: Web UI, basic mapping, GPS, database" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  full        Install all features (~50-60 packages)" -ForegroundColor White
    Write-Host "              Best for: Full-featured deployments, data analysis" -ForegroundColor Gray
    Write-Host "              Features: All core + scientific computing, visualization, hardware support" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  full-dev    Install all features + development tools (~70-80 packages)" -ForegroundColor White
    Write-Host "              Best for: Development, contributing, testing" -ForegroundColor Gray
    Write-Host "              Features: All features + linting, testing, security scanning" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  help        Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor White
    Write-Host "  .\scripts\install.ps1 minimal      # Minimal installation" -ForegroundColor Gray
    Write-Host "  .\scripts\install.ps1 full         # Full installation" -ForegroundColor Gray
    Write-Host "  .\scripts\install.ps1 full-dev     # Full + development installation" -ForegroundColor Gray
    Write-Host ""
    Write-Host "After installation, activate the environment with:" -ForegroundColor White
    Write-Host "  venv\Scripts\Activate.ps1" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Then run PiWardrive with:" -ForegroundColor White
    Write-Host "  python -m piwardrive.webui_server" -ForegroundColor Gray
}

# Check prerequisites
function Test-Prerequisites {
    Write-Info "Checking prerequisites..."
    
    if (!(Test-Command "python")) {
        Write-Error "Python is not installed or not in PATH."
        Write-Info "Please install Python 3.10+ from https://python.org"
        exit 1
    }
    
    # Check Python version
    $pythonVersion = python --version 2>&1
    Write-Info "Found: $pythonVersion"
    
    if (!(Test-Command "pip")) {
        Write-Error "pip is not installed or not in PATH."
        Write-Info "Please ensure pip is installed with Python"
        exit 1
    }
    
    # Check if we're in the right directory
    if (!(Test-Path "requirements.txt") -or !(Test-Path "requirements-core.txt")) {
        Write-Error "Installation files not found. Please run this script from the PiWardrive project root."
        exit 1
    }
}

# Main installation logic
function Main {
    Write-Info "PiWardrive Installation Script for Windows"
    Write-Info "Current directory: $(Get-Location)"
    
    Test-Prerequisites
    
    switch ($InstallType) {
        "minimal" {
            Install-Minimal
        }
        "full" {
            Install-Full
        }
        "full-dev" {
            Install-FullDev
        }
        "help" {
            Show-Help
        }
        default {
            Write-Error "Unknown option: $InstallType"
            Show-Help
            exit 1
        }
    }
}

# Run main function
Main
