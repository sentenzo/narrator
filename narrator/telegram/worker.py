import os
from typing import NamedTuple

from aiogram import Bot
from aiogram.types import Message, Document

from narrator.exceptions import UrlParserException
import narrator.text.web_parser as web_parser
from narrator.text.text import Text
from narrator.utils import make_filename


class ValidityCheckResult(NamedTuple):
    is_valid: bool
    description: str | None = None
    user_description: str | None = None


class BaseWorker:
    def __init__(self, bot: Bot, message: Message) -> None:
        self._bot = bot
        self._message = message

    def check_validity(self) -> ValidityCheckResult:
        raise NotImplemented()

    async def produce_audio_file(self, directory: str) -> str:
        raise NotImplemented()


class UrlWorker(BaseWorker):
    def __init__(self, bot: Bot, message: Message) -> None:
        super().__init__(bot, message)
        self._url = web_parser.Url(self._message.text)

    def check_validity(self) -> ValidityCheckResult:
        url: web_parser.Url = self._url
        if not url.is_valid:
            description = "Not a valid url"
            return ValidityCheckResult(False, description, description)
        elif not url.is_reachable:
            description = "The URL is unreachable (can't open the web page)"
            return ValidityCheckResult(False, description, description)
        try:
            url.parse()
        except UrlParserException as ex:
            description = str(ex)
            user_description = "Faild to parse the web page"
            return ValidityCheckResult(False, description, user_description)
        except Exception as ex:
            description = str(ex)
            user_description = "Something went terribly wrong"
            return ValidityCheckResult(False, description, user_description)
        return ValidityCheckResult(True)

    async def produce_audio_file(self, directory: str) -> str:
        text: Text = self._url.parse()
        mp3_path = text.save_to_mp3(directory)
        return mp3_path


class DocWorker(BaseWorker):
    @staticmethod
    def _bytes_to_mib_str(bytes: int, ndigits: int = 2):
        if ndigits < 0:
            raise ValueError
        r = round(bytes / 2**20, ndigits)
        fstr = "{" + f"0:0.{ndigits}f" + "}"
        return fstr.format(r)

    def __init__(self, bot: Bot, message: Message) -> None:
        super().__init__(bot, message)
        self._doc: Document = self._message.document

    def check_validity(self) -> ValidityCheckResult:
        doc = self._doc
        if not Text.has_proper_extention(doc.file_name):
            description = "The file extention is not supported"
            user_description = "The file extention is not supported\n"
            user_description += "List of supported extentions:\n"
            user_description += "  " + ", ".join(Text.INPUT_FORMATS)
            return ValidityCheckResult(False, description, user_description)
        elif doc.file_size > Text.MAX_INPUT_SIZE:
            s_cur_mib = DocWorker._bytes_to_mib_str(doc.file_size)
            s_max_mib = DocWorker._bytes_to_mib_str(Text.MAX_INPUT_SIZE)
            description = f"The file is too big: the file size is {s_cur_mib} MiB, and the max size allowed is {s_max_mib} MiB)"
            return ValidityCheckResult(False, description, description)
        return ValidityCheckResult(True)

    async def produce_audio_file(self, directory: str) -> str:
        filename = make_filename(self._doc.file_name)
        file_path = os.path.join(directory, filename)
        await self._bot.download(self._doc, file_path)
        text = Text.from_file(file_path)
        mp3_path = text.save_to_mp3(directory)
        return mp3_path
