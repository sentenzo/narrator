import os

import narrator.config

conf = narrator.config.to_txt

INPUT_FORMATS = [".epub", ".fb2", ".fb3", ".md", ".txt", ".doc", ".docx", ".rtf"]

MAX_INPUT_SIZE = conf.max_input_size


def has_proper_extention(filename):
    return os.path.splitext(filename)[1] in INPUT_FORMATS
