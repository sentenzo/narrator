import logging
import tempfile
from typing import Callable, Dict, Any, Awaitable

from aiogram import Dispatcher, BaseMiddleware, Bot
from aiogram.types import ContentType, Message, FSInputFile, TelegramObject
from aiogram.filters import Command

import narrator.config as conf
from ..exceptions import NarratorException

from .worker import BaseWorker, DocWorker, UrlWorker

logger = logging.getLogger(__name__)

narrator_bot = Bot(token=conf.bot.token)
dispatcher = Dispatcher()


@dispatcher.message(Command(commands=["about"]))
async def cmd_test(message: Message):
    await message.answer("🤖: ...")


@dispatcher.message(content_types=ContentType.ANY)
async def take_else(message: Message):
    Worker: BaseWorker | None = None
    obj_name: str | None = None

    if message.content_type == ContentType.TEXT:
        Worker = UrlWorker
        obj_name = "url"
    elif message.content_type == ContentType.DOCUMENT:
        Worker = DocWorker
        obj_name = "file"
    else:
        await message.answer("🤖: Please, send me a file or a url")
        return

    worker = Worker(narrator_bot, message)
    is_valid, description, user_description = worker.check_validity()
    if not is_valid:
        logger.info(description)
        await message.answer("🤖: " + user_description)
        return
    try:
        with tempfile.TemporaryDirectory() as temp_dir_path:
            path_to_audio = await worker.produce_audio_file(temp_dir_path)
            f_wrap = FSInputFile(path_to_audio)
            await message.answer_document(f_wrap)
    except NarratorException:
        logger.warning(f"Faild to process {obj_name}: ", exc_info=True)
        await message.answer(
            f"🤖: Something went wrong: I faild to process the {obj_name}"
        )
    except Exception:
        logger.error(f"Faild to process {obj_name}: ", exc_info=True)
        await message.answer(
            f"🤖: Something went terribly wrong: I faild to process the {obj_name}"
        )


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
