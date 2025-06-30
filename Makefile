.PHONY: lint test docs coverage

lint:
    pre-commit run --all-files

test:
    pytest -q

docs:
    sphinx-build -W -b html docs docs/_build/html

coverage:
    pytest --cov=src --cov-report=xml -q
    cd webui && npm test
