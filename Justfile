default: docs-help gen-init lint

build:
    rm --force --recursive dist/
    pyproject-build
    check-wheel-contents dist/*.whl
    twine check --strict dist/*

docs-help:
    typer liblaf.lime.cli utils docs --output docs/help.md
    prettier --write docs/help.md

gen-init:
    ./scripts/gen-init.sh

lint: lint-toml lint-python

lint-python:
    ruff format
    ruff check --fix

lint-toml:
    sort-toml .ruff.toml pyproject.toml

upgrade:
    uv sync --upgrade
