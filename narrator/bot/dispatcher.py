# from asyncio.log import logger
import logging
import tempfile
import os

from aiogram import Dispatcher
from aiogram.types import ContentType, Message, FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage

from ..reader import url as r_url
from ..reader import file as r_file
from .bot import narrator_bot as bot
from ..speaker import Speaker

logger = logging.getLogger(__name__)

mem_storage = MemoryStorage()
dispatcher = Dispatcher(storage=mem_storage)


@dispatcher.message(commands=["about"])
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
        await bot.download(message.document, file_path)
        article = r_file.read_text(file_path)
        # path_to_audio = Speaker.narrate_to_file(article, temp_dir_path)
        path_to_audio = Speaker.narrate_from_txt_to_file(file_path)
        tf = FSInputFile(path_to_audio)
        await message.answer_document(tf)


@dispatcher.message(content_types=ContentType.TEXT)
async def take_text(message: Message):
    if r_url.is_url(message.text):
        await message.answer(f"🤖: {r_url.read_text(message.text)}")
    else:
        await take_else(message)


@dispatcher.message(content_types=ContentType.ANY)
async def take_else(message: Message):
    user = message.from_user.id

    logger.info(f"{user}: {message.text}")
    await message.answer("🤖: Please, send me a file or a link")


from .authorizer import Authorizer

dispatcher.message.middleware(Authorizer())
