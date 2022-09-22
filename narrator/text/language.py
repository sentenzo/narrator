import string
from enum import Enum


class Language(Enum):
    RU: str = "ru"
    EN: str = "en"

    @staticmethod
    def get_val(ch: str) -> str | None:
        for lang_val in ALPHABETS:
            if ch in ALPHABETS[lang_val]:
                return lang_val
        return None


EN_ALPHABET = string.ascii_letters

RU_ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
RU_ALPHABET += RU_ALPHABET.upper()

ALPHABETS = {
    Language.RU.value: RU_ALPHABET,
    Language.EN.value: EN_ALPHABET,
}
