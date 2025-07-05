# PiWardrive 📡

[![Backend Coverage](https://codecov.io/gh/TRASHYTALK/piwardrive/branch/main/graph/badge.svg?flag=backend)](https://app.codecov.io/gh/TRASHYTALK/piwardrive?flags=backend)
[![Frontend Coverage](https://codecov.io/gh/TRASHYTALK/piwardrive/branch/main/graph/badge.svg?flag=frontend)](https://app.codecov.io/gh/TRASHYTALK/piwardrive?flags=frontend)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](docker/)

> **Professional headless mapping and diagnostic suite for Raspberry Pi 5**

PiWardrive is an enterprise-grade war-driving and network analysis platform that combines the power of Kismet, BetterCAP, and custom SIGINT tools with a modern React-based web dashboard. Designed for security professionals, researchers, and network administrators.

## 🚀 Quick Start

### Option 1: Python (Recommended)
```bash
# Install dependencies
pip install -r config/requirements.txt

# Launch the application
python main.py --config config/piwardrive.json
```

### Option 2: Docker
```bash
# Build and run with Docker Compose
cd docker/
docker-compose up -d
```

### Option 3: Web Interface
```bash
# Launch the web dashboard
python -m piwardrive.webui_server
```

## 📋 System Requirements

- **Hardware**: Raspberry Pi 5 (or compatible ARM64/x86_64 system)
- **OS**: Linux (Ubuntu 20.04+ recommended)
- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 16GB minimum, 32GB+ recommended

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Dashboard │    │   Core Engine   │    │   Data Layer    │
│   (React)       │◄──►│   (Python)      │◄──►│   (SQLite)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   REST API      │    │   Kismet        │    │   Grafana       │
│   (FastAPI)     │    │   BetterCAP     │    │   (Monitoring)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 Features

### Core Capabilities
- **🔍 Network Discovery**: Automated WiFi, Bluetooth, and device scanning
- **📊 Real-time Analytics**: Live dashboard with performance metrics
- **🎯 SIGINT Tools**: Professional-grade signal intelligence suite
- **🌐 Web Interface**: Modern React-based dashboard
- **📈 Monitoring**: Integrated Grafana dashboards
- **🐳 Containerized**: Full Docker support for easy deployment

### Advanced Features
- **GPS Integration**: Location-aware scanning and mapping
- **Multi-Protocol Support**: WiFi, Bluetooth, Zigbee, and more
- **Export Capabilities**: Multiple data formats (JSON, CSV, KML)
- **API Access**: RESTful API for automation and integration
- **Performance Optimization**: Async processing and caching
- **Security**: Role-based access control and encryption

## 📁 Project Structure

```
PiWardrive/
├── 📁 config/          # Configuration files and settings
├── 📁 docker/          # Docker containers and compose files
├── 📁 documentation/   # Project documentation and guides
├── 📁 tools/           # Utility scripts and helper tools
├── 📁 src/piwardrive/  # Core application source code
├── 📁 tests/           # Test suites and validation
├── 📁 docs/            # Technical documentation
├── 📁 examples/        # Usage examples and tutorials
├── 📁 deploy/          # Deployment configurations
└── main.py            # Application entry point
```

See [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) for detailed information.

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Installation Guide](documentation/installation-guide.md) | Complete setup instructions |
| [Configuration](documentation/configuration.md) | Configuration options and examples |
| [API Documentation](documentation/api_comprehensive_documentation.md) | REST API reference |
| [Architecture Overview](documentation/architecture_overview.md) | System design and components |
| [Performance Tuning](documentation/performance_tuning.md) | Optimization guidelines |
| [Security Guide](documentation/SECURITY.md) | Security best practices |
| [Contributing](documentation/CONTRIBUTING.md) | Development guidelines |

## 🛠️ Development

### Environment Setup
```bash
# Clone the repository
git clone https://github.com/TRASHYTALK/piwardrive.git
cd piwardrive

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -r config/requirements-dev.txt

# Run tests
python -m pytest tests/
```

### Code Quality
```bash
# Type checking
mypy src/piwardrive/

# Linting
flake8 src/piwardrive/

# Formatting
black src/piwardrive/
```

## 🔧 Configuration

The application uses JSON configuration files located in the `config/` directory:

```json
{
  "database": {
    "url": "sqlite:///piwardrive.db",
    "pool_size": 10
  },
  "scanning": {
    "wifi_enabled": true,
    "bluetooth_enabled": true,
    "update_interval": 30
  },
  "webui": {
    "host": "0.0.0.0",
    "port": 8080,
    "debug": false
  }
}
```

## 🚀 Deployment

### Production Deployment
```bash
# Using Docker Compose
cd docker/
docker-compose -f docker-compose.production.yml up -d

# Or using Kubernetes
kubectl apply -f deploy/k8s/
```

### Performance Monitoring
```bash
# Start Grafana dashboard
docker-compose -f docker/docker-compose.grafana.yml up -d

# Run performance benchmarks
python tools/performance_demo.py
```

## 📊 Performance

- **Scan Rate**: 1000+ devices per minute
- **Memory Usage**: <512MB typical operation
- **CPU Usage**: <20% on Raspberry Pi 5
- **Storage**: Efficient SQLite with compression
- **Network**: Optimized for low-bandwidth environments

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guide](documentation/CONTRIBUTING.md) for details on:

- Code style and standards
- Testing requirements
- Pull request process
- Issue reporting
- Security disclosure

## 🔒 Security

Security is a top priority. Please review our [Security Policy](documentation/SECURITY.md) and report vulnerabilities responsibly.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Kismet** - Wireless network detection
- **BetterCAP** - Network attack and monitoring
- **React** - Frontend framework
- **FastAPI** - High-performance API framework
- **Grafana** - Monitoring and visualization

## 📞 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/TRASHYTALK/piwardrive/issues)
- **Discussions**: [GitHub Discussions](https://github.com/TRASHYTALK/piwardrive/discussions)
- **Wiki**: [Project Wiki](https://github.com/TRASHYTALK/piwardrive/wiki)

---

**Made with ❤️ for the security and networking community**
