import os
import asyncio

from aiogram import Bot

from narrator.bot.n_bot import dispatcher


async def main():
    bot = Bot(token=os.environ["BOT_TOKEN"])
    await dispatcher.start_polling(bot)


asyncio.run(main())
