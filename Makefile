all:

voice:
	poetry run python narrator/voice.py

bot:
	poetry run python -m narrator.ttt_bot