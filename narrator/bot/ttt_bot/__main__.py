import os
import asyncio

from aiogram import Bot

from narrator.bot.ttt_bot.tic_tac_toe.dispatcher import TIC_TAC_TOE_DISPATCHER


async def main():
    dp = TIC_TAC_TOE_DISPATCHER
    bot = Bot(token=os.environ["BOT_TOKEN"])
    await dp.start_polling(bot)


asyncio.run(main())
