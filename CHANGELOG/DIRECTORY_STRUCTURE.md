# PiWardrive Directory Structure

This document provides an overview of the reorganized PiWardrive repository structure.

## 📁 Repository Organization

```
PiWardrive/
├── 📁 benchmarks/              # Performance benchmarks and testing
├── 📁 config/                  # Configuration files and settings
│   ├── .editorconfig          # Editor configuration
│   ├── .flake8               # Python linting configuration
│   ├── .pre-commit-config.yaml # Pre-commit hooks configuration
│   ├── .pydocstyle           # Python docstring style configuration
│   ├── localization_config.json # Localization settings
│   ├── mypy.ini              # MyPy type checking configuration
│   ├── performance_config.json # Performance optimization settings
│   ├── pyproject.toml        # Python project configuration
│   ├── pyrightconfig.json    # Pyright type checker configuration
│   ├── reno.yaml             # Release notes configuration
│   ├── requirements.txt      # Python dependencies
│   ├── requirements-core.txt # Core dependencies
│   └── requirements-dev.txt  # Development dependencies
├── 📁 deploy/                  # Deployment configurations
│   ├── 📁 charts/             # Helm charts for Kubernetes
│   ├── 📁 config/             # Deployment-specific configurations
│   └── 📁 k8s/                # Kubernetes manifests
├── 📁 docker/                  # Docker and containerization
│   ├── .dockerignore         # Docker ignore file
│   ├── docker-compose.yml    # Main Docker Compose configuration
│   ├── docker-compose.aggregation.yml # Aggregation service compose
│   ├── docker-compose.grafana.yml     # Grafana monitoring compose
│   ├── docker-compose.production.yml  # Production deployment compose
│   ├── Dockerfile            # Main application Dockerfile
│   ├── Dockerfile.aggregation # Aggregation service Dockerfile
│   └── Dockerfile.webui      # Web UI Dockerfile
├── 📁 docs/                    # Technical documentation
│   ├── api.md               # API documentation
│   ├── architecture.md      # Architecture overview
│   ├── configuration.md     # Configuration guide
│   ├── deployment.rst       # Deployment guide
│   ├── installation.md      # Installation instructions
│   └── ... (additional docs)
├── 📁 documentation/           # Project documentation and reports
│   ├── ADVANCED_FEATURES_IMPLEMENTATION_REPORT.md
│   ├── CONTRIBUTING.md       # Contribution guidelines
│   ├── DATABASE_IMPROVEMENTS_SUMMARY.md
│   ├── DEPENDENCY_MANAGEMENT_IMPLEMENTATION.md
│   ├── IMPLEMENTATION_COMPLETE.md    # Complete implementation summary
│   ├── IMPLEMENTATION_PROGRESS.md   # Implementation progress tracking
│   ├── INSTALLATION_OPTIONS_SUMMARY.md
│   ├── MIGRATION.md          # Migration guide
│   ├── PERFORMANCE_IMPROVEMENTS.md
│   ├── PERFORMANCE_SCALABILITY_PLAN.md
│   ├── README_v2.md          # Legacy README
│   ├── REFERENCE.md          # Technical reference
│   ├── REPOSITORY_ASSESSMENT.md
│   ├── SECURITY.md           # Security guidelines
│   └── database_improvements.md
├── 📁 examples/                # Usage examples and samples
├── 📁 grafana/                 # Grafana dashboards and monitoring
├── 📁 locales/                 # Internationalization files
├── 📁 releasenotes/            # Release notes and changelog
├── 📁 scripts/                 # Utility scripts and automation
├── 📁 server/                  # Server-side components
├── 📁 src/                     # Source code (main application)
│   └── 📁 piwardrive/         # Core platform modules
│       ├── 📁 analysis/       # Packet analysis engine
│       ├── 📁 enhanced/       # Advanced features and enhancements
│       ├── 📁 geospatial/     # Geospatial intelligence
│       ├── 📁 integration/    # System integration and orchestration
│       ├── 📁 ml/             # Machine learning and AI
│       ├── 📁 mining/         # Advanced data mining
│       ├── 📁 navigation/     # Offline navigation system
│       ├── 📁 performance/    # Performance optimization
│       ├── 📁 plugins/        # Plugin architecture
│       ├── 📁 protocols/      # Multi-protocol support
│       ├── 📁 reporting/      # Professional reporting
│       ├── 📁 signal/         # RF spectrum analysis
│       ├── 📁 testing/        # Automated testing framework
│       ├── 📁 visualization/  # Advanced visualization
│       └── unified_platform.py # Unified platform integration
├── 📁 static/                  # Static web assets
├── 📁 templates/               # HTML templates
├── 📁 tests/                   # Test suites and test data
├── 📁 tools/                   # Utilities and helper tools
│   ├── exception_handler.py  # Exception handling utilities
│   ├── Makefile              # Build automation
│   ├── performance_demo.py   # Performance demonstration script
│   ├── setup.py              # Package setup script
│   ├── setup_performance_dashboard.py # Dashboard setup tool
│   ├── sync.py               # Synchronization utilities
│   └── sync_receiver.py      # Sync receiver component
├── 📁 web/                     # Web interface components
├── 📁 webui/                   # Web UI implementation
├── 📁 widgets/                 # UI widgets and components
├── .gitattributes             # Git attributes configuration
├── .gitignore                 # Git ignore rules
├── LICENSE                    # MIT License
├── main.py                    # Main application entry point
├── README.md                  # Project overview and quick start
└── service.py                 # Service entry point
```

## 📋 Directory Descriptions

### Core Directories

- **`src/piwardrive/`** - Main source code with 16 advanced modules
- **`config/`** - All configuration files and settings
- **`docker/`** - Docker containers and orchestration
- **`documentation/`** - Project documentation and reports
- **`tools/`** - Utility scripts and helper tools

### Supporting Directories

- **`benchmarks/`** - Performance testing and benchmarking
- **`deploy/`** - Deployment configurations (K8s, Helm)
- **`docs/`** - Technical documentation and guides
- **`examples/`** - Usage examples and sample code
- **`tests/`** - Comprehensive test suites
- **`web/`** - Web interface and UI components

### Specialized Directories

- **`grafana/`** - Monitoring dashboards and visualizations
- **`locales/`** - Internationalization and localization
- **`releasenotes/`** - Version history and release notes
- **`scripts/`** - Automation and utility scripts
- **`server/`** - Server-side components and services

## 🎯 Key Benefits of This Organization

### 1. **Clear Separation of Concerns**
- Configuration files isolated in `config/`
- Docker files organized in `docker/`
- Documentation centralized in `documentation/`
- Tools and utilities in `tools/`

### 2. **Professional Structure**
- Follows industry best practices
- Scalable organization for large teams
- Clear development workflow
- Easy navigation and maintenance

### 3. **Development Efficiency**
- Quick access to relevant files
- Logical grouping of related components
- Reduced cognitive load for developers
- Simplified CI/CD pipeline configuration

### 4. **Enterprise Ready**
- Professional directory structure
- Clear documentation hierarchy
- Deployment configurations organized
- Monitoring and observability components separated

## 🔧 Working with the New Structure

### Configuration Changes
All configuration files are now in `config/`:
```bash
# Install dependencies
pip install -r config/requirements.txt

# Configure the application
edit config/piwardrive_config.yaml
```

### Docker Usage
Docker files are in `docker/`:
```bash
# Build and run
docker-compose -f docker/docker-compose.yml up -d
```

### Documentation Access
All documentation is in `documentation/`:
```bash
# View implementation details
cat documentation/IMPLEMENTATION_COMPLETE.md

# Check progress
cat documentation/IMPLEMENTATION_PROGRESS.md
```

### Development Tools
Tools are in `tools/`:
```bash
# Run performance demo
python tools/performance_demo.py

# Setup dashboard
python tools/setup_performance_dashboard.py
```

This reorganization provides a clean, professional, and scalable repository structure suitable for enterprise development and deployment.
