# from asyncio.log import logger
import logging
import re

from aiogram import Dispatcher
from aiogram.types import ContentType, Message
from aiogram.fsm.storage.memory import MemoryStorage

from .extractor import url as eurl
from narrator.bot.n_bot.extractor.url import is_url


logger = logging.getLogger(__name__)

mem_storage = MemoryStorage()
dispatcher = Dispatcher(storage=mem_storage)


@dispatcher.message(commands=["test"])
async def cmd_test(message: Message):
    await message.answer("🤖: ...")


@dispatcher.message(content_types=ContentType.DOCUMENT)
async def take_document(message: Message):
    logger.info(
        f'{message.from_user.id}: file(id={message.document.file_id}, name="{message.document.file_name}",) {message.text}'
    )
    await message.answer("🤖: The file is received")


@dispatcher.message(content_types=ContentType.TEXT)
async def take_text(message: Message):
    if eurl.is_url(message.text):
        await message.answer(f"🤖: {eurl.extract_text(message.text)}")
    else:
        await take_else(message)


@dispatcher.message(content_types=ContentType.ANY)
async def take_else(message: Message):
    user = message.from_user.id
    logger.info(f"{user}: {message.text}")
    await message.answer("🤖: Please, send me a file or a link")
