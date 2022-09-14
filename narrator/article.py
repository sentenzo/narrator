class Article:
    def __init__(self):
        self.meta = {}
        self.text = []

    def __setitem__(self, key, val):
        self.meta[key] = val

    def __getitem__(self, key):
        return self.meta[key]

    def __repr__(self) -> str:
        text = self.text[0][:20] if self.text else ""
        return f'Article(text="{text}")'

    def __str__(self) -> str:
        meta_text = []
        for k, v in self.meta.items():
            meta_text.append(f"{k}:\n    {v}")
        meta_text = "\n".join(meta_text)
        text_text = "\n".join(self.text)
        return f"\n{meta_text}\n\n{text_text}\n"
