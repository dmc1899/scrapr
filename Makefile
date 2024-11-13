###############################################################################
## This makefile provides a standardised way to execute shell and other
## command line utilities.
##
## Usage:
## To run a single target called install packages:
##		make install-packages
##
## To get help use
##	make help
##
## Limitations:
## There are issues redirecting output from datacontract
## commands used to generate large documents. For example, the HTML output
## requires post-processing to remove line breaks.  Please be wary of this
## and test any new commands carefully.
###############################################################################

.PHONY: print-python-env
print-python-env: ## Prints python env details
	@echo "Python version: `which python; python --version`"
	@echo "Poetry version: `poetry --version`"
	@echo "Poetry env:"
	@poetry env info
	@echo "Creating virtual environment using Python poetry"

.PHONY: install
install: ## Create a Python Poetry environment and install all dependencies.
	@echo "Display current version of Python"
	@which python && python --version
	@echo "Lock Poetry dependencies"
	@poetry lock
	@echo "Creating virtual environment using Python poetry"
	@poetry install --with dev


.PHONY: check
check:
	@echo "🚀 Static type checking: Running mypy"
	@poetry run mypy
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@poetry run deptry .
	@echo "🚀 Formatting code: Running black"
	@poetry run black .
	@echo "🚀 Checking code errors: Running pylint"
	@poetry run pylint .
	@echo "🚀 Checking PEP style adherence: Running flake8"
	@poetry run flake8 .
	@echo "🚀 Checking for security issues: Running bandit"
	@poetry run bandit .

.PHONY: clean-build
clean-build: clean ## Destroy distributable directory and create new Python package using Poetry.
	@echo "🚀 Creating wheel file"
	@poetry build

.PHONY: clean
clean: ## Destroy distributable directory.
	@echo "Cleaning distributable directory"
	@rm -rf dist

.PHONY: test
test: ## Test the application code using pytest
	@echo "Testing code: Running pytest with code coverage"
	@poetry run pytest --cov --cov-config=pyproject.toml --cov-report=xml --cov-report=html

.PHONY: test-verbose
test-verbose: ## Test the application code using pytest with verbose output
	@echo "Testing code: Running pytest with code coverage and verbose output"
	@poetry run pytest -s -v --cov --cov-config=pyproject.toml --cov-report=html

.PHONY: format-code
format-code: ## Format code.
	@echo "🚀 Running black formatter"
	@poetry run python -m black .

.PHONY: version-bump-patch
version-bump-patch: ## Increment the patch version number.
	@echo "🚀 Bumping version by incrementing patch number"
	@echo "Current version is"
	@poetry version
	@echo "Updating patch number"
	@poetry version patch
	@echo "Updated version is"
	@poetry version

.PHONY: version-bump-minor
version-bump-minor: ## Increment the minor version number.
	@echo "🚀 Bumping version by incrementing minor number"
	@echo "Current version is"
	@poetry version
	@echo "Updating minor number"
	@poetry version minor
	@echo "Updated version is"
	@poetry version

.PHONY: version-bump-major
version-bump-major: ## Increment the major version number.
	@echo "🚀 Bumping version by incrementing major number"
	@echo "Current version is"
	@poetry version
	@echo "Updating major number"
	@poetry version major
	@echo "Updated version is"
	@poetry version

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
