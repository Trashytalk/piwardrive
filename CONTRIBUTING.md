# Contributing to PiWardrive

Thank you for considering contributing! The repository includes a `Makefile` that wraps common developer tasks.

## Setup

Install the development requirements and install the git hooks:

```bash
pip install -r requirements-dev.txt
pre-commit install
```

## Running checks

Use the following convenience targets during development:

- `make lint` — run pre-commit on all files.
- `make test` — run the Python test suite with pytest.
- `make docs` — build the Sphinx documentation in `docs/_build/html`.
- `make coverage` — generate combined Python and Node test coverage reports.

Contributions should pass these checks before you submit a pull request.
