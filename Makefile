install:
	poetry install

project:
	poetry run project

run:
	poetry run database

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	poetry run pip install --force-reinstall --no-deps $$(find dist -name '*.whl' | head -1)

lint:
	poetry run ruff check .

