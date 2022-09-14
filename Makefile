all:

init:
	poetry install

voice:
	poetry run python narrator/speaker/voice.py

bot:
	poetry run python -m narrator.bot

