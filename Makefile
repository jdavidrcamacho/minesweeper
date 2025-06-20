.DEFAULT_GOAL := help

.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "  format-check     Check code formatting with black and isort"
	@echo "  format-fix       Auto-format code with black and isort"
	@echo "  lint-check       Run flake8 for lint checks"
	@echo "  type-check       Run mypy for static type checks"
	@echo "  docstring-check  Check for missing docstrings using pydocstyle"
	@echo "  static-check     Run all static analysis checks"

.PHONY: format-check
format-check:
	black --check src/
	isort --check-only --profile black src/

.PHONY: format-fix
format-fix:
	black src/
	isort --profile black src/

.PHONY: lint-check
lint:
	flake8 src/

.PHONY: type-check
type-check:
	mypy src/

.PHONY: docstring-check
docstring-check:
	pydocstyle src/

.PHONY: static-check
static-check: format-check lint type-check docstring-check
