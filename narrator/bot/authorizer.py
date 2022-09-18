import os
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

import narrator.config as conf

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
