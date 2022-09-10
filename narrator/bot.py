import os
import asyncio

import logging
from aiogram import Bot, Dispatcher, types
import dotenv

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.environ["BOT_TOKEN"])

dp = Dispatcher()


@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
