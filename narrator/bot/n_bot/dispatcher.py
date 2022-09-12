# from asyncio.log import logger
import logging

from aiogram import Dispatcher
from aiogram.types import ContentType, Message
from aiogram.fsm.storage.memory import MemoryStorage

from .extractor.url import HarbToText


logger = logging.getLogger(__name__)

mem_storage = MemoryStorage()
dispatcher = Dispatcher(storage=mem_storage)


@dispatcher.message(commands=["test"])
async def cmd_test(message: Message):
    await message.answer("🤖: ...")


@dispatcher.message(content_types=ContentType.ANY)
async def take_link(message: Message):
    user = message.from_user.id
    logger.info(f"{user}: {message.text}")
    await message.answer("🤖: " + HarbToText.url_to_txt(message.text))
