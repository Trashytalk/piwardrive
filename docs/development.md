# Development Guide

This guide covers setting up a development environment for PiWardrive and contributing to the project.

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Node.js 18.x or higher
- Git
- Docker (optional, for containerized development)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/TrashyTalk/piwardrive.git
   cd piwardrive
   ```

2. **Set up Python environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt
   pip install -e .
   ```

3. **Set up Node.js environment**
   ```bash
   cd webui
   npm install
   cd ..
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

5. **Run tests to verify setup**
   ```bash
   make test
   ```

## Development Workflow

### Development Environment Setup

```mermaid
graph TD
    A[Clone Repository] --> B[Setup Python Environment]
    B --> C[Install Dependencies]
    C --> D[Setup Node.js Environment]
    D --> E[Install Pre-commit Hooks]
    E --> F[Run Initial Tests]
    F --> G[Start Development]
    
    G --> H[Backend Development]
    G --> I[Frontend Development]
    G --> J[Full Stack Development]
    
    H --> H1[API Development]
    H --> H2[Database Models]
    H --> H3[Services & Logic]
    
    I --> I1[React Components]
    I --> I2[UI/UX Design]
    I --> I3[WebSocket Integration]
    
    J --> J1[Integration Testing]
    J --> J2[End-to-End Testing]
    J --> J3[Performance Testing]
    
    style A fill:#e1f5fe
    style G fill:#e8f5e8
    style H fill:#fff3e0
    style I fill:#fce4ec
    style J fill:#f3e5f5
```

### Development Architecture

```mermaid
graph LR
    A[Developer] --> B[IDE/Editor]
    B --> C[Git Repository]
    C --> D[Pre-commit Hooks]
    D --> E[CI/CD Pipeline]
    
    B --> F[Backend Dev Server]
    B --> G[Frontend Dev Server]
    
    F --> H[API Testing]
    G --> I[UI Testing]
    
    H --> J[Database]
    I --> K[Mock API]
    
    E --> L[Automated Tests]
    L --> M[Code Quality Checks]
    M --> N[Build & Deploy]
    
    style A fill:#e1f5fe
    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#fce4ec
    style E fill:#f3e5f5
    style F fill:#ffebee
    style G fill:#e0f2f1
```

### Running the Application

#### Development Mode (Hot Reload)
```bash
# Terminal 1: Start the backend API
uvicorn piwardrive.service:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start the frontend development server
cd webui
npm run dev
```

#### Production Mode
```bash
# Build and start the full application
cd webui
npm run build
cd ..
piwardrive-webui
```

### Code Quality

#### Linting and Formatting
```bash
# Run all linting and formatting
make lint

# Individual tools
black src/           # Python formatting
isort src/           # Python import sorting
flake8 src/          # Python linting
mypy src/            # Python type checking
cd webui && npm run lint  # JavaScript/TypeScript linting
```

#### Testing
```bash
# Run all tests
make test

# Python tests only
pytest

# JavaScript tests only
cd webui && npm test

# With coverage
make coverage
```

### Database Development

#### Database Adapters
PiWardrive supports multiple database backends through the `DatabaseAdapter` interface:

- **SQLite** (default): `src/piwardrive/db/sqlite.py`
- **PostgreSQL**: `src/piwardrive/db/postgres.py`
- **MySQL**: `src/piwardrive/db/mysql.py`

#### Migrations
```bash
# Create a new migration
piwardrive-migrate create --name "description_of_change"

# Apply migrations
piwardrive-migrate upgrade

# Rollback migrations
piwardrive-migrate downgrade
```

#### Testing with Different Databases
```bash
# SQLite (default)
pytest

# PostgreSQL
export PW_DATABASE_URL="postgresql://user:pass@localhost/piwardrive_test"
pytest

# MySQL
export PW_DATABASE_URL="mysql://user:pass@localhost/piwardrive_test"
pytest
```

### Frontend Development

#### Component Development
```bash
# Start development server with hot reload
cd webui
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Run tests with coverage
npm run test -- --coverage
```

#### Adding New Components
1. Create component in `webui/src/components/`
2. Add tests in `webui/tests/`
3. Export from `webui/src/components/index.js`
4. Register in widget system if applicable

#### Widget Development
Widgets are dynamically loaded components for the dashboard:

1. Create widget component
2. Add to `src/piwardrive/widgets/__init__.py`
3. Add tests
4. Update widget documentation

### CLI Tool Development

#### Creating New CLI Tools
1. Create script in `scripts/`
2. Add entry point in `pyproject.toml`
3. Add tests in `tests/`
4. Update documentation

Example:
```python
# scripts/my_new_tool.py
import click

@click.command()
@click.option('--option', help='Description')
def main(option):
    """My new CLI tool."""
    click.echo(f"Running with option: {option}")

if __name__ == '__main__':
    main()
```

```toml
# pyproject.toml
[project.scripts]
my-new-tool = "piwardrive.scripts.my_new_tool:main"
```

### Performance Development

#### Profiling
```bash
# Profile the application
python -m cProfile -o profile.stats scripts/performance_cli.py

# Analyze profile
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(20)"
```

#### Benchmarking
```bash
# Run benchmarks
python benchmarks/packet_parse_benchmark.py
python benchmarks/persistence_benchmark.py
```

### Documentation Development

#### Building Documentation
```bash
# Build HTML documentation
make docs

# Build and serve locally
cd docs
python -m http.server 8080
```

#### API Documentation
API documentation is automatically generated from code:
- FastAPI automatically generates OpenAPI/Swagger docs
- Visit `/docs` or `/redoc` when running the server

### Docker Development

#### Development Container
```bash
# Build development image
docker build -t piwardrive-dev .

# Run development container
docker run -p 8000:8000 -v $(pwd):/app piwardrive-dev

# Docker Compose development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

#### Production Testing
```bash
# Build production image
docker build -t piwardrive:latest .

# Test production container
docker run -p 8000:8000 piwardrive:latest
```

## Architecture Overview

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    PiWardrive Architecture                   │
├─────────────────────────────────────────────────────────────┤
│  Web UI (React)                                             │
│  ├── Components (webui/src/components/)                     │
│  ├── Widgets (Dynamic dashboard components)                 │
│  └── Tests (webui/tests/)                                   │
├─────────────────────────────────────────────────────────────┤
│  API Layer (FastAPI)                                        │
│  ├── REST Endpoints (src/piwardrive/service.py)             │
│  ├── WebSocket Handlers (Real-time data)                    │
│  └── GraphQL API (Optional)                                 │
├─────────────────────────────────────────────────────────────┤
│  Core Logic                                                  │
│  ├── Database Layer (src/piwardrive/db/)                    │
│  ├── Scanner Services (Wi-Fi, Bluetooth, GPS)               │
│  ├── Analytics Engine (src/piwardrive/analytics/)           │
│  └── Performance Optimization (src/piwardrive/performance/) │
├─────────────────────────────────────────────────────────────┤
│  CLI Tools & Scripts                                        │
│  ├── Management Tools (50+ CLI commands)                    │
│  ├── Field Support Tools (Diagnostics, reporting)          │
│  └── Data Export Tools (GPX, Shapefile, etc.)              │
├─────────────────────────────────────────────────────────────┤
│  External Services                                           │
│  ├── Kismet (Wi-Fi scanning)                               │
│  ├── BetterCAP (Network tools)                             │
│  ├── GPSD (GPS daemon)                                      │
│  └── Hardware Interfaces (sensors, LEDs)                   │
└─────────────────────────────────────────────────────────────┘
```

### Key Design Patterns

- **Dependency Injection**: Core services use DI for testability
- **Adapter Pattern**: Database adapters for multiple backends
- **Observer Pattern**: Real-time data updates via WebSocket
- **Factory Pattern**: Widget and component creation
- **Strategy Pattern**: Different export formats and analytics

## Contributing Guidelines

### Code Style

- **Python**: Follow PEP 8, use Black for formatting
- **JavaScript/TypeScript**: Follow Airbnb style guide
- **Documentation**: Use docstrings and comments liberally
- **Commits**: Use conventional commit format

### Pull Request Process

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** with tests
4. **Run the test suite** (`make test`)
5. **Run linting** (`make lint`)
6. **Update documentation** if needed
7. **Submit a pull request**

### Testing Requirements

- **Unit Tests**: Required for all new code
- **Integration Tests**: Required for API endpoints
- **E2E Tests**: Required for critical user workflows
- **Performance Tests**: Required for performance-critical code

### Review Process

All pull requests require:
- Passing CI/CD checks
- Code review from maintainers
- Updated documentation
- Appropriate test coverage

## Debugging & Troubleshooting

### Common Issues

#### Database Connection Issues
```bash
# Check database status
piwardrive-service --check-db

# Reset database
piwardrive-migrate reset

# Vacuum database
piwardrive-vacuum
```

#### WebUI Build Issues
```bash
# Clear node_modules and rebuild
cd webui
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### Permission Issues
```bash
# Fix permissions for development
sudo chown -R $USER:$USER ~/.config/piwardrive
```

#### Type Checking
If `mypy` reports duplicate module stubs or cannot find modules, remove any redundant `.pyi` files and set `MYPYPATH=src` before running `mypy`.


### Debugging Tools

#### Python Debugging
```python
# Add breakpoints
import pdb; pdb.set_trace()

# Remote debugging
import debugpy
debugpy.listen(5678)
debugpy.wait_for_client()
```

#### JavaScript Debugging
```javascript
// Browser debugging
console.log('Debug info:', data);
debugger;

// Node.js debugging
node --inspect-brk server/index.js
```

### Performance Debugging

```bash
# Monitor system resources
piwardrive-service --monitor

# Profile specific components
python -m cProfile -o profile.stats scripts/performance_cli.py

# Memory profiling
python -m memory_profiler scripts/memory_intensive_task.py
```

## Release Process

### Version Management
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Update version in `pyproject.toml` and `webui/package.json`
- Tag releases with `git tag v1.0.0`

### Build Process
```bash
# Build Python package
python -m build

# Build WebUI
cd webui
npm run build

# Build Docker image
docker build -t piwardrive:v1.0.0 .
```

### Deployment
```bash
# Deploy to PyPI
python -m twine upload dist/*

# Deploy Docker image
docker push piwardrive:v1.0.0

# Deploy to production
./scripts/deploy.sh production
```

## Getting Help

- **Documentation**: Check `docs/` directory
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Chat**: Discord/Slack for real-time help
- **Email**: [maintainer email] for security issues

## Resources

- [API Documentation](api.md)
- [Architecture Deep Dive](architecture.md)
- [Configuration Reference](configuration.md)
- [Hardware Compatibility](hardware-compatibility.md)
- [Contributing Guidelines](../CONTRIBUTING.md)
