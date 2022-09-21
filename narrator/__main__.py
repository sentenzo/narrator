import asyncio

from narrator.telegram.bot import dispatcher, narrator_bot


async def main():
    await dispatcher.start_polling(narrator_bot)


asyncio.run(main())
