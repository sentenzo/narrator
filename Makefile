all:

voice:
	poetry run python narrator/voice.py

bot:
	poetry run python narrator/bot.py