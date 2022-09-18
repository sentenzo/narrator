import os

from ..article import Article

import narrator.sub_utils as utils


class Speaker:
    @staticmethod
    def narrate_from_txt_to_file(path_to_txt_file: str):

        # balcon.exe only works with UTF-8-BOM (or "utf-8-sig")
        text = open(path_to_txt_file, encoding="utf-8").read()
        open(path_to_txt_file, mode="w", encoding="utf-8-sig").write(text)

        path_to_wav = utils.balcon(path_to_txt_file)
        path_to_mp3 = utils.ffmpeg__to_mp3(path_to_wav, 48)
        return path_to_mp3
