import os

import narrator.config
from narrator.sub_utils import blb2txt

conf = narrator.config.to_txt

INPUT_FORMATS = [".epub", ".fb2", ".fb3", ".md", ".txt", ".doc", ".docx", ".rtf"]

MAX_INPUT_SIZE = conf.max_input_size


def has_proper_extention(filename):
    ext = os.path.splitext(filename)[1]
    return ext.lower() in INPUT_FORMATS


def to_txt(source, dest_directory) -> str:
    return blb2txt(source)
