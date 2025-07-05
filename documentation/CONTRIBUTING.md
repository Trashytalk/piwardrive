# Contributing to PiWardrive

Thank you for considering contributing! The repository includes a `Makefile` that wraps common developer tasks.

## Development Setup

### Quick Development Setup

The fastest way to get started with development:

```bash
# Clone the repository
git clone git@github.com:Trashytalk/piwardrive.git
cd piwardrive

# Install with development tools
bash scripts/install.sh full-dev  # Linux/macOS
# OR
.\scripts\install.ps1 full-dev     # Windows
# OR
make install-full-dev              # Using make
```

This will install all dependencies, development tools, and set up pre-commit hooks automatically.

### Manual Development Setup

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\Activate.ps1  # Windows

# Install development dependencies
pip install -r requirements-dev.txt
pip install -r requirements.txt

# Install PiWardrive in development mode
pip install -e .[all,development]

# Set up pre-commit hooks
pre-commit install
```

## Development Workflow

1. Fork the repository and create a feature branch off of `main`.
2. Make your changes following the existing code style. Formatting is enforced with [Black](https://black.readthedocs.io/) and [isort](https://pycqa.github.io/isort/).
3. Run `pre-commit run --all-files` and `make test` to execute Python and Node tests.
4. Commit your work with descriptive messages and open a pull request on GitHub.

All new features should include accompanying tests and documentation when applicable.

## Running checks

Use the following convenience targets during development:

- `make lint` — run pre-commit on all files.
- `make test` — run the Python test suite with pytest.
- `make docs` — build the Sphinx documentation in `docs/_build/html`.
- `make coverage` — generate combined Python and Node test coverage reports.

## Dependency Management

Use these targets for dependency management during development:

- `make deps-audit` — run comprehensive dependency audit.
- `make deps-security` — run security vulnerability scans.
- `make deps-outdated` — check for outdated packages.
- `make deps-cleanup` — clean up unused dependencies.

## Installation Options

For different development scenarios:

- `make install-minimal` — minimal installation for testing core features.
- `make install-full` — full installation with all optional features.
- `make install-full-dev` — full installation with development tools.
- `make install-help` — show all installation options.

During development you can automatically restart the backend service when files
change by running `scripts/watch_service.py` (requires the `watchgod` package).

## Testing

The project includes comprehensive tests:

```bash
# Run all tests
make test

# Run specific test categories
pytest tests/unit/        # Unit tests
pytest tests/integration/ # Integration tests
pytest tests/e2e/         # End-to-end tests

# Run tests with coverage
make coverage
```

Some tests rely on additional scientific packages such as `numpy`, `pandas`
and `scikit-learn`. These are automatically installed with the full development setup.

## Code Quality

The project enforces code quality through:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **bandit**: Security linting
- **pre-commit**: Automated checks on commit

All checks are automatically run via pre-commit hooks and CI/CD.

We use the [Developer Certificate of Origin](https://developercertificate.org/). By submitting code you certify that you have the right to license it under the project's MIT terms.

Contributions should pass these checks before you submit a pull request.
