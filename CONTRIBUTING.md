# Contributing to PiWardrive

Thank you for considering contributing! The repository includes a `Makefile` that wraps common developer tasks.

## Setup

Install the development requirements and install the git hooks:

```bash
pip install -r requirements-dev.txt
pre-commit install
```

1. Fork the repository and create a feature branch off of `main`.
2. Make your changes following the existing code style. Formatting is enforced with [Black](https://black.readthedocs.io/) and [isort](https://pycqa.github.io/isort/).
3. Run `pre-commit run --all-files` and `make test` to execute Python and Node tests.
4. Commit your work with descriptive messages and open a pull request on GitHub.

All new features should include accompanying tests and documentation when applicable.

Some tests rely on additional scientific packages such as `numpy`, `pandas`
and `scikit-learn`. Install them via `pip install .[tests]` (or
`pip install -r requirements.txt`) if you plan to run the full suite.

## Running checks

Use the following convenience targets during development:

- `make lint` — run pre-commit on all files.
- `make test` — run the Python test suite with pytest.
- `make docs` — build the Sphinx documentation in `docs/_build/html`.
- `make coverage` — generate combined Python and Node test coverage reports.

During development you can automatically restart the backend service when files
change by running `scripts/watch_service.py` (requires the `watchgod` package).
We use the [Developer Certificate of Origin](https://developercertificate.org/). By submitting code you certify that you have the right to license it under the project's MIT terms.

Contributions should pass these checks before you submit a pull request.
