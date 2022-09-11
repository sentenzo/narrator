import os
import asyncio
import logging

from aiogram import Bot
import dotenv

from narrator.ttt_bot.tic_tac_toe.dispatcher import TIC_TAC_TOE_DISPATCHER

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)


async def main():
    dp = TIC_TAC_TOE_DISPATCHER
    bot = Bot(token=os.environ["BOT_TOKEN"])
    await dp.start_polling(bot)


asyncio.run(main())
