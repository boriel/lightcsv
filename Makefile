.PHONY: lint
lint:
	flake8
	black . --check
	mypy

.PHONY: format
format:
	black .
