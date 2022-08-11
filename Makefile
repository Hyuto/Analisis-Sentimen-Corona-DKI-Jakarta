clean:
	find . | grep -E '(__pycache__|\.pyc|\.lprof|\.pytest_cache|\.ipynb_checkpoints|\.mypy_cache)' | \
	xargs rm -rf

format:
	poetry run isort .
	poetry run black . 

format-check:
	poetry run isort . --check-only
	poetry run black . --check

local-notebook:
	poetry run jupyter notebook --no-browser

test:
	poetry run pytest --cov=scripts/ -v

typecheck:
	poetry run mypy scripts/ --no-incremental --ignore-missing-imports

setup-dev:
	poetry install
	poetry run pre-commit install

lock-deps:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
