.PHONY: lint test docs

lint:
	pre-commit run --all-files

test:
	pytest -q

docs:
	sphinx-build -W -b html docs docs/_build/html
