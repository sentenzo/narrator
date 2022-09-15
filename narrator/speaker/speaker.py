import os

from ..article import Article


class Speaker:
    @staticmethod
    def narrate_to_file(article: Article, path_to_dest_dir: str):
        """
        This is a dummy
        """
        import shutil

        path_from = os.environ["MOCK_AUDIO_FILE_PATH"]
        path_to_audio = os.path.join(path_to_dest_dir, os.path.basename(path_from))
        shutil.copy(path_from, path_to_audio)
        return path_to_audio
