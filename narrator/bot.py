# from asyncio.log import logger
import logging
import tempfile
import os
from typing import Callable, Dict, Any, Awaitable

from aiogram import Dispatcher, BaseMiddleware, Bot
from aiogram.types import ContentType, Message, FSInputFile, TelegramObject
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

from .reader import url as r_url
from .reader import file as r_file
from .speaker import Speaker
import narrator.config as conf

logger = logging.getLogger(__name__)


narrator_bot = Bot(token=conf.bot.token)
mem_storage = MemoryStorage()
dispatcher = Dispatcher(storage=mem_storage)


@dispatcher.message(Command(commands=["about"]))
async def cmd_test(message: Message):
    await message.answer("🤖: ...")


@dispatcher.message(content_types=ContentType.DOCUMENT)
async def take_document(message: Message):
    logger.info(
        f'{message.from_user.id}: file(id={message.document.file_id}, name="{message.document.file_name}",) {message.text}'
    )
    if not r_file.is_readable_ext(message.document.file_name):
        await message.answer(
            f"🤖: No reader matches the file: {message.document.file_name}"
        )
        return
    with tempfile.TemporaryDirectory() as temp_dir_path:
        file_path = os.path.join(temp_dir_path, message.document.file_name)
        await narrator_bot.download(message.document, file_path)
        path_to_audio = Speaker.narrate_from_txt_to_file(file_path)
        tf = FSInputFile(path_to_audio)
        await message.answer_document(tf)


@dispatcher.message(content_types=ContentType.TEXT)
async def take_text(message: Message):
    if r_url.is_url(message.text):
        article = r_url.read_text(message.text)
        with tempfile.TemporaryDirectory() as temp_dir_path:
            file_path = article.save_to_txt(temp_dir_path)
            path_to_audio = Speaker.narrate_from_txt_to_file(file_path)
            tf = FSInputFile(path_to_audio)
            await message.answer_document(tf)
    else:
        await take_else(message)


@dispatcher.message(content_types=ContentType.ANY)
async def take_else(message: Message):
    user = message.from_user.id

    logger.info(f"{user}: {message.text}")
    await message.answer("🤖: Please, send me a file or a link")


############################################################


class Authorizer(BaseMiddleware):
    WHITELIST: list[str] = conf.bot.allowed_usernames

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if event.from_user.username in Authorizer.WHITELIST:
            return await handler(event, data)


dispatcher.message.middleware(Authorizer())


############################################################

narrator_bot = Bot(token=conf.bot.token)

__all__ = [dispatcher, narrator_bot]
