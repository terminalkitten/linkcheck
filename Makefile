install-dev:
	pip install '.[dev]'
	pip install '.[doc]'

lint:
	./scripts/lint.sh

format:
	./scripts/format.sh
