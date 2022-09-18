import os

from narrator.sub_utils import add_suffix, make_filename


class Article:
    def __init__(self):
        self.title: str = ""
        self.meta = {}
        self.text: str = ""

    def __setitem__(self, key, val):
        self.meta[key] = val

    def __getitem__(self, key):
        return self.meta[key]

    def __repr__(self) -> str:
        text = self.text[:20] if self.text else ""
        return f'Article(text="{text}")'

    def save_to_txt(self, dir_path: str) -> str:
        file_name = self.title or self.text[:20]
        file_name = make_filename(file_name)
        file_name = add_suffix(file_name, ".txt")

        file_path = os.path.join(dir_path, file_name)

        text = str(self)

        with open(file_path, "wb") as txt:
            txt.write(text.encode("utf-8-sig"))

        return file_path

    def __str__(self) -> str:
        meta_text = []
        for k, v in self.meta.items():
            meta_text.append(f"{k}:\n    {v}")
        meta_text = "\n".join(meta_text)
        return f"\n{meta_text}\n\n{self.text}\n"
