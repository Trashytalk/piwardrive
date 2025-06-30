# PiWardrive - Wi-Fi Analysis & IoT Monitoring System

[![Build Status](https://github.com/username/piwardrive/workflows/CI/badge.svg)](https://github.com/username/piwardrive/actions)
[![Docker Pulls](https://img.shields.io/docker/pulls/username/piwardrive)](https://hub.docker.com/r/username/piwardrive)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://python.org)
[![Node Version](https://img.shields.io/badge/node-16%2B-green)](https://nodejs.org)

## Table of Contents

- [🚀 Quick Start](#quick-start)
- [✨ Features](#features)
- [🏗️ Architecture](#architecture)
- [💾 Installation Methods](#installation)
- [🔧 Configuration](#configuration)
- [📊 Usage Examples](#usage)
- [🐳 Docker Deployment](#docker)
- [🔍 Troubleshooting](#troubleshooting)
- [📚 Documentation](#documentation)
- [🤝 Contributing](#contributing)

<div align="center">
  <img src="docs/images/piwardrive-logo.png" alt="PiWardrive Logo" width="200"/>
  
  <h3>Real-time Wi-Fi Analysis & IoT Monitoring Platform</h3>
  
  <p>Monitor wireless networks, track device connectivity, and analyze Wi-Fi environments with an intuitive web dashboard.</p>
  
  <img src="docs/images/dashboard-overview.png" alt="Dashboard Overview" width="800"/>
</div>

### Key Highlights

- 📡 **Real-time Wi-Fi Scanning** - Monitor access points and connected devices
- 📊 **Interactive Dashboard** - Customizable widgets and real-time charts
- 🌍 **GPS Integration** - Location-aware network mapping
- 🏠 **IoT Monitoring** - System health and resource tracking
- 🐳 **Easy Deployment** - Docker, systemd, or development setups

## Prerequisites

### Hardware Requirements

- **Minimum**: Raspberry Pi 3B+ or equivalent ARM/x86 device
- **Recommended**: Raspberry Pi 4 with 4GB+ RAM
- **Storage**: 8GB+ SD card or storage device
- **Network**: Wi-Fi adapter with monitor mode support

### Software Requirements

- **Operating System**: Linux (Raspberry Pi OS, Ubuntu 20.04+)
- **Python**: 3.8 or higher
- **Node.js**: 16.x or higher (for web UI development)
- **Docker**: 20.10+ (for containerized deployment)

### Network Permissions

⚠️ **Legal Notice**: Ensure you have proper authorization before scanning wireless networks in your area. Check local regulations regarding wireless monitoring.

### Supported Wi-Fi Adapters

- Ralink RT5370/RT5372
- Atheros AR9271
- Realtek RTL8188CUS
- See [Hardware Compatibility Guide](docs/hardware-compatibility.md) for full list

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/username/piwardrive.git
cd piwardrive

# Start with Docker Compose
docker-compose up -d

# Access the dashboard
open http://localhost:8080
```

### Option 2: Native Installation

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt update && sudo apt install -y python3-pip nodejs npm wireless-tools

# Clone and setup
git clone https://github.com/username/piwardrive.git
cd piwardrive

# Install Python dependencies
pip3 install -r requirements.txt

# Install and build Web UI
cd webui && npm install && npm run build && cd ..

# Run the service
python3 service.py
```

### First-Time Setup

1. Navigate to `http://localhost:8080`
2. Complete the initial configuration wizard
3. Configure your Wi-Fi adapter settings
4. Start monitoring!

### Default Credentials

- **Username**: `admin`
- **Password**: `piwardrive`
- ⚠️ **Change these immediately** in production deployments

## ✨ Features

### Wi-Fi Analysis & Monitoring

<img src="docs/images/wifi-analysis.png" alt="Wi-Fi Analysis" width="400" align="right"/>

- **Real-time Scanning**: Continuous monitoring of wireless networks
- **Signal Strength Mapping**: RSSI tracking and visualization
- **Device Detection**: Identify connected and nearby devices
- **Channel Analysis**: Frequency usage and interference detection
- **Historical Data**: Trend analysis and reporting

### System Monitoring

- **Resource Tracking**: CPU, RAM, storage, and temperature monitoring
- **Network Statistics**: Bandwidth usage and connection health
- **GPS Integration**: Location-aware data collection
- **Alert System**: Configurable notifications for anomalies

### Web Dashboard

<img src="docs/images/dashboard-widgets.png" alt="Dashboard Widgets" width="400" align="left"/>

- **Customizable Widgets**: Drag-and-drop dashboard configuration
- **Real-time Charts**: Live updating graphs and meters
- **Data Export**: CSV, JSON export capabilities
- **Multi-device Support**: Centralized monitoring of multiple sensors
- **Mobile Responsive**: Works on tablets and smartphones

### Use Cases

- **Network Administration**: Monitor enterprise Wi-Fi infrastructure
- **IoT Deployments**: Edge device monitoring and management
- **Research Projects**: Wireless environment studies
- **Home Automation**: Personal network monitoring
- **Event Monitoring**: Temporary deployment for gatherings

## 🏗️ Architecture

<div align="center">
  <img src="docs/images/architecture-diagram.png" alt="PiWardrive Architecture" width="800"/>
</div>

### System Components

#### Backend Services

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Wi-Fi Scanner │    │  System Monitor │    │   GPS Service   │
│   (Python)      │    │   (Python)      │    │   (Python)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Core Service  │
                    │ (FastAPI/ASGI)  │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Database      │
                    │   (SQLite)      │
                    └─────────────────┘
```

#### Frontend Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React App     │    │   Widget System │    │   API Client    │
│   (TypeScript)  │    │   (Components)  │    │   (Axios)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Web Server    │
                    │   (Nginx)       │
                    └─────────────────┘
```

### Data Flow

1. **Collection**: Wi-Fi scanner and system monitors collect data
2. **Processing**: Core service processes and stores data
3. **API**: REST endpoints serve data to frontend
4. **Visualization**: React dashboard displays real-time information
5. **Export**: Data can be exported or synchronized to aggregation service

### Deployment Options

- **Standalone**: Single device with web interface
- **Distributed**: Multiple sensors with central aggregation
- **Kiosk Mode**: Full-screen dashboard for dedicated displays
- **Development**: Local development with hot-reload

## 📸 Screenshots

### Main Dashboard

<img src="docs/images/main-dashboard.png" alt="Main Dashboard" width="800"/>

### Wi-Fi Analysis View

<img src="docs/images/wifi-analysis-view.png" alt="Wi-Fi Analysis" width="400"/> <img src="docs/images/signal-strength-map.png" alt="Signal Strength" width="400"/>

### System Monitoring

<img src="docs/images/system-monitoring.png" alt="System Monitoring" width="400"/> <img src="docs/images/resource-graphs.png" alt="Resource Graphs" width="400"/>

### Configuration Interface

<img src="docs/images/configuration.png" alt="Configuration" width="800"/>

## 📚 Documentation

### User Guides

- [Installation Guide](docs/installation.md) - Detailed setup instructions
- [Configuration Reference](docs/configuration.md) - All configuration options
- [User Manual](docs/user-manual.md) - Complete feature documentation
- [Hardware Compatibility](docs/hardware-compatibility.md) - Supported devices

### Deployment Guides

- [Docker Deployment](docs/docker-deployment.md) - Container setup
- [Raspberry Pi Setup](docs/raspberry-pi-setup.md) - Pi-specific instructions
- [Production Deployment](docs/production-deployment.md) - Enterprise setup
- [Kiosk Mode](docs/kiosk-mode.md) - Dedicated display setup

### Developer Resources

- [API Documentation](docs/api.md) - REST API reference
- [Development Setup](docs/development.md) - Local development guide
- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [Architecture Deep Dive](docs/architecture.md) - Detailed system design
