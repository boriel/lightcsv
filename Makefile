.PHONY: lint
lint:
	flake8
	black . --check
	mypy

.PHONY: format
format:
	black .

.PHONY: test
test:
	python -m unittest -v
