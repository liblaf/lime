default: docs-help gen-init lint

build:
    pyproject-build
    check-wheel-contents dist/*.whl
    twine check --strict dist/*

docs-help:
    typer liblaf.lime.cli utils docs --output docs/help.md
    prettier --write docs/help.md

gen-init:
    ./scripts/gen-init.sh

lint: lint-python lint-toml

lint-python:
    ruff check --fix

lint-toml:
    sort-toml .ruff.toml pyproject.toml
