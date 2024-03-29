packages = mysite polls tests
bin = .venv/bin

format-check:
	$(bin)/black --check $(packages)

format:
	$(bin)/black $(packages)

mypy:
	$(bin)/mypy $(packages)

ruff:
	$(bin)/ruff check

ruff-fix:
	$(bin)/ruff check --fix

test:
	$(bin)/pytest

verify: format-check ruff mypy test
