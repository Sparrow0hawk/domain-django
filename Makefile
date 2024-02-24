format-check:
	.venv/bin/black --check polls mysite tests

format:
	.venv/bin/black polls mysite tests

ruff:
	.venv/bin/ruff check

ruff-fix:
	.venv/bin/ruff --fix

test:
	.venv/bin/pytest

verify: format-check ruff test
