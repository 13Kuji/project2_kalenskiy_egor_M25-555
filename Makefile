install:
	poetry install

project:
	poetry run project

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	poetry run pip install --force-reinstall --no-deps $$(find dist -name '*.whl' | head -1)

