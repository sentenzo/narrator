all:

init:
	poetry install

run:
	poetry run python -m narrator

test:
	poetry run python -m pytest --verbosity=2 --showlocals --log-level=DEBUG