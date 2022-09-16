import os

from ..article import Article

import narrator.sub_utils as utils


class Speaker:
    @staticmethod
    def narrate_to_file(article: Article, path_to_dest_dir: str):
        """
        This is a dummy
        """
        import shutil

        path_from = os.environ["BOT_MOCK_AUDIO_FILE_PATH"]
        path_to_audio = os.path.join(path_to_dest_dir, os.path.basename(path_from))
        shutil.copy(path_from, path_to_audio)

        path_to_audio = utils.ffmpeg__to_mp3(path_to_audio, 48)
        return path_to_audio

    @staticmethod
    def narrate_from_txt_to_file(path_to_txt_file: str):

        # balcon.exe only works with UTF-8-BOM (or "utf-8-sig")
        text = open(path_to_txt_file, encoding="utf-8").read()
        open(path_to_txt_file, mode="w", encoding="utf-8-sig").write(text)

        path_to_wav = utils.balcon(path_to_txt_file)
        path_to_mp3 = utils.ffmpeg__to_mp3(path_to_wav, 48)
        return path_to_mp3
