import random

from narrator.text.language import ALPHABETS

RAND_STR_LEN = 8
RAND_STR_POPULATION = "0123456789ABCDEF"


def rand_str(k=RAND_STR_LEN):
    return "".join(random.choices(RAND_STR_POPULATION, k=k))


def crop_suffix(file_path):
    from os.path import dirname, basename, join, splitext

    d, f = dirname(file_path), basename(file_path)
    f, e = splitext(f)
    if len(f) > (RAND_STR_LEN + 1) and f[-(RAND_STR_LEN + 1)] == "_":
        rstr = f[-RAND_STR_LEN:]
        if all(c in RAND_STR_POPULATION for c in rstr):
            f = f[:~RAND_STR_LEN]
    return join(d, f + e)


def add_suffix(file_path, ext=None):
    file_path = crop_suffix(file_path)

    from os.path import dirname, basename, join, splitext

    new_filename = [dirname(file_path)]
    old_filename, old_ext = splitext(basename(file_path))
    ext = ext or old_ext or ""
    new_filename.append(f"{old_filename}_{rand_str()}{ext}")
    return join(*new_filename)


def make_filename(file_name: str):
    """
    Removes all the symbols from the given string which are not in allowed in filenames.
    The name of the file is chosen based on the source content. It initially can have any symbols like ':' or '/'.
    """
    all_lang_alphabets = "".join(ALPHABETS.values())
    alphabet = all_lang_alphabets + "0123456789 _-&%@#!()."
    file_name = "".join([c for c in file_name if c in alphabet])
    return file_name
