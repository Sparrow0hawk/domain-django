packages = mysite polls tests
bin = .venv/bin

format-check:
	$(bin)/black --check $(packages)

format:
	$(bin)/black $(packages)

ruff:
	$(bin)/ruff check

ruff-fix:
	$(bin)/ruff --fix

test:
	$(bin)/pytest

verify: format-check ruff test
