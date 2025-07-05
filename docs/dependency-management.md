# Dependency Management Strategy

## Overview
This document outlines the dependency management strategy for PiWardrive to ensure security, stability, and maintainability.

## Dependency Files Structure

### Production Dependencies
- **requirements.txt**: Full dependency set including optional packages
- **requirements-core.txt**: Minimal core dependencies for lightweight deployments
- **pyproject.toml**: Organized optional dependencies via extras_require

### Development Dependencies
- **requirements-dev.txt**: Development tools, testing, and quality assurance packages

## Dependency Categories

### Core Dependencies (requirements-core.txt)
- **Security-Critical**: Packages that handle authentication, encryption, or network communication
- **Web Framework**: FastAPI, uvicorn, and related web stack  
- **Database**: SQLite, PostgreSQL, MySQL drivers
- **System Interface**: Basic system monitoring and file operations

### Optional Dependencies (pyproject.toml extras)
- **analysis**: Scientific computing and data analysis (numpy, scipy, pandas, scikit-learn)
- **visualization**: Plotting and charting libraries (matplotlib, plotly, folium)
- **hardware**: Raspberry Pi and sensor interfaces (mpu6050, pyrtlsdr, bleak)
- **integrations**: External service integrations (boto3, paho-mqtt, rpy2)
- **performance**: Performance optimizations (orjson, ujson)

### Development Dependencies (requirements-dev.txt)
- **Code Quality**: Linters, formatters, type checkers (black, isort, flake8, mypy)
- **Testing**: Test frameworks and coverage tools (pytest, pytest-cov)
- **Security**: Vulnerability scanning tools (pip-audit, safety, bandit)
- **Documentation**: Documentation generation tools (sphinx)

## Installation Options

### Minimal Installation
```bash
# Install only core dependencies
pip install -r requirements-core.txt
```

### Feature-Specific Installation
```bash
# Install with specific optional features
pip install piwardrive[analysis,visualization]
pip install piwardrive[hardware]  # For Raspberry Pi deployments
pip install piwardrive[all]       # Full installation
```

### Development Installation
```bash
# Install development dependencies
pip install -r requirements-dev.txt
pip install piwardrive[development]
```

## Pinning Strategy

### Production Dependencies
- **Security-Critical**: Pin to compatible ranges (e.g., `>=X.Y.Z,<X.Y+1.0`)
- **Core Framework**: Pin to minor versions for stability
- **Hardware-Specific**: Allow flexible versions for compatibility
- **Scientific Libraries**: Pin major versions, allow minor/patch updates

### Development Dependencies
- **Exact Versions**: Pin to specific versions for reproducible environments
- **Quality Tools**: Pin to ensure consistent formatting and linting

### Flexible Dependencies
Some packages remain unpinned for flexibility:
- `numpy` - Performance improvements in patches
- `folium` - Map visualization with regular updates
- `dronekit` - Specialized hardware compatibility
- `mpu6050` - Hardware sensor compatibility

## Update Schedule

### Automated Updates (via Dependabot)
- **Security updates**: Weekly automated patches for vulnerabilities
- **Patch updates**: Weekly automated updates for non-breaking changes
- **CI validation**: All updates must pass full test suite before merge

### Manual Updates
- **Major version updates**: Monthly review and testing cycle
- **Breaking changes**: Requires code review and migration planning
- **Hardware dependencies**: Manual testing on target hardware required

## Dependency Management Tools

### Audit and Monitoring
```bash
# Run comprehensive dependency audit
make deps-audit

# Check for outdated packages
make deps-outdated

# Run security vulnerability scans
make deps-security

# Generate dependency tree analysis
python scripts/dependency_audit.py --tree
```

### Installation Management
```bash
# Install core dependencies only
make deps-install-core

# Install full dependencies
make deps-install-full

# Install development dependencies
make deps-install-dev

# Clean up unused dependencies
make deps-cleanup
```

### Dependency Freezing
```bash
# Generate exact version freeze for reproducibility
make deps-freeze
```

## Vulnerability Management

### Scanning Tools
- **pip-audit**: CVE vulnerability scanning integrated in CI/CD
- **safety**: Python package vulnerability database checks
- **bandit**: Security linting for code patterns
- **GitHub Security Advisories**: Automated vulnerability alerts via Dependabot

### Response Process
1. **Critical vulnerabilities**: Update within 24 hours
2. **High severity**: Update within 1 week  
3. **Medium/Low severity**: Include in next scheduled update cycle
4. **Emergency patches**: Fast-track through accelerated CI/CD process

## Dependency Reduction Strategy

### Bloat Reduction
- **Optional Dependencies**: Move heavy packages to extras_require
- **Conditional Imports**: Import expensive libraries only when needed
- **Hardware-Specific**: Separate Pi-specific packages from core dependencies
- **Feature Flags**: Allow disabling features that require heavy dependencies

### Size Optimization
- **Core Installation**: ~15-20 essential packages for basic functionality
- **Full Installation**: ~50-60 packages including all optional features
- **Development**: Additional ~15-20 packages for development workflow

## Monitoring and Maintenance

### Regular Audits
- **Weekly**: Automated security and update checks via Dependabot
- **Monthly**: Manual dependency audit and major version review
- **Quarterly**: Full dependency cleanup and optimization review
- **Annually**: Complete dependency strategy and tooling review

### Metrics Tracking
- **Package Count**: Monitor total dependency count trends
- **Security Alerts**: Track vulnerability response times
- **Update Frequency**: Monitor update adoption rates
- **Build Size**: Track installation footprint changes

## Emergency Procedures

### Security Incident Response
1. **Immediate Assessment**: Evaluate vulnerability impact and affected systems
2. **Isolation Testing**: Test emergency patches in isolated environment
3. **Accelerated Deployment**: Deploy critical updates with fast-track CI/CD
4. **Monitoring**: Monitor deployment for regressions or compatibility issues
5. **Documentation**: Document incident response and lessons learned

### Rollback Procedures
1. **Version Pinning**: Maintain known-good dependency versions
2. **Rollback Testing**: Test rollback scenarios in staging environment
3. **Automated Rollback**: Implement automatic rollback on test failures
4. **Communication**: Notify stakeholders of rollback procedures and timelines

## Best Practices

### Development Workflow
- **Local Development**: Use development dependencies for consistent tooling
- **Testing**: Run dependency audits before major releases
- **Documentation**: Keep dependency changes documented in changelogs
- **Review Process**: Require review for all dependency changes

### Production Deployment
- **Staging Validation**: Test all dependency updates in staging first
- **Gradual Rollout**: Deploy dependency updates in phases
- **Monitoring**: Monitor application performance after dependency updates
- **Rollback Plan**: Maintain rollback procedures for each deployment
- **pip-audit**: CVE vulnerability scanning
- **safety**: Python package vulnerability database
- **bandit**: Security linting for code patterns
- **GitHub Security Advisories**: Automated vulnerability alerts

### Response Process
1. **Critical vulnerabilities**: Update within 24 hours
2. **High severity**: Update within 1 week
3. **Medium/Low severity**: Include in next scheduled update cycle

## Dependency Reduction

### Optional Dependencies
Mark heavy dependencies as optional where possible:
- Scientific libraries (scipy, scikit-learn) - only for analysis features
- Visualization libraries (matplotlib, plotly) - only for reporting
- Hardware interfaces (RPi.GPIO, mpu6050) - only for Raspberry Pi deployments

### Dependency Groups
Use extras_require in setup.py to group optional dependencies:
- `[analysis]` - Data analysis and machine learning
- `[visualization]` - Charts and plotting
- `[hardware]` - Raspberry Pi and sensor interfaces
- `[development]` - Development tools

## Monitoring and Maintenance

### Regular Audits
- Monthly dependency audit and update review
- Quarterly major version update assessment
- Annual full dependency review and cleanup

### Documentation
- Maintain changelog of dependency updates
- Document any known compatibility issues
- Keep security advisory responses documented

## Emergency Procedures

### Security Incident Response
1. Assess vulnerability impact
2. Test emergency patches in isolated environment
3. Deploy critical updates with accelerated review process
4. Monitor deployment for regressions
5. Document incident and response for future reference
