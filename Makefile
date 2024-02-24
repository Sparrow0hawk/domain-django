
verify: format-check ruff test

format-check:
	.venv/bin/black --check polls mysite tests

format:
	.venv/bin/black polls mysite tests

test:
	.venv/bin/pytest

ruff:
	.venv/bin/ruff check

ruff-fix:
	.venv/bin/ruff --fix
