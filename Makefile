.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")
USING_POETRY=$(shell grep "tool.poetry" pyproject.toml && echo "yes")
VERSION=$(shell cat checkatlas/VERSION)

.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep


.PHONY: show
show:             ## Show the current environment.
	@echo "Current environment:"
	$(ENV_PREFIX)poetry env info

.PHONY: install
install:          ## Install the project in dev mode.
	@echo "Run checkatlas install - create poetrry virtual env"
	$(ENV_PREFIX)poetry install

.PHONY: fmt
fmt:              ## Format code using black & isort.
	@echo "Run project file formatting"
	$(ENV_PREFIX)poetry run isort .
	$(ENV_PREFIX)poetry run black -l 79 .

.PHONY: lint
lint:             ## Run pep8, black, mypy linters.
	@echo "Run project linting"
	$(ENV_PREFIX)poetry run flake8 checkatlas/
	$(ENV_PREFIX)poetry run black -l 79 --check checkatlas/
	$(ENV_PREFIX)poetry run black -l 79 --check tests/
	$(ENV_PREFIX)poetry run mypy --ignore-missing-imports checkatlas/

.PHONY: test
test:             ## Run tests and generate coverage report.
	$(ENV_PREFIX)poetry run pytest -v --cov-config .coveragerc --cov=checkatlas -l --tb=short --maxfail=1 tests/
	$(ENV_PREFIX)poetry run coverage xml
	$(ENV_PREFIX)poetry run coverage html

.PHONY: watch
watch:            ## Run tests on every change.
	ls **/**.py | entr $(ENV_PREFIX)pytest -s -vvv -l --tb=long --maxfail=1 tests/

.PHONY: docs
docs:             ## Build the documentation.
	@echo "Building documentation ..."
	@$(ENV_PREFIX)poetry run mkdocs build
	URL="site/index.html"; open $$URL || xdg-open $$URL || sensible-browser $$URL || x-www-browser $$URL || gnome-open $$URL

.PHONY: release
release:          ## Create a new tag for release.
	@echo "WARNING: This operation will create s version tag and push to github"
	@echo "Reading version $(VERSION) from: checkatlas/VERSION"
	@$(ENV_PREFIX)poetry run gitchangelog > HISTORY.md
	@git add checkatlas/VERSION HISTORY.md
	@git commit -m "release: version $(VERSION) 🚀"
	@echo "creating git tag : $(VERSION)"
	@git tag $(VERSION)
	@git push -u origin HEAD --tags
	@echo "Github Actions will detect the new tag and release the new version."


.PHONY: clean
clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build
