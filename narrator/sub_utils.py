import subprocess

import narrator.config

conf = narrator.config.utils

RSTR_LEN = 8
RSTR_POPULATION = "0123456789ABCDEF"


def rand_str(k=RSTR_LEN):
    import random

    return "".join(random.choices(RSTR_POPULATION, k=k))


def crop_suffix(file_path):
    from os.path import dirname, basename, join, splitext

    d, f = dirname(file_path), basename(file_path)
    f, e = splitext(f)
    if len(f) > (RSTR_LEN + 1) and f[-(RSTR_LEN + 1)] == "_":
        rstr = f[-RSTR_LEN:]
        if all(c in RSTR_POPULATION for c in rstr):
            f = f[:~RSTR_LEN]
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
    from string import digits, ascii_letters

    cyrilic = "абвгдеёжзиклмнопрстуфхцчшщьыъэюя"
    alphabet = digits + ascii_letters + cyrilic + cyrilic.upper() + " _-&%@#!()."
    file_name = "".join([c for c in file_name if c in alphabet])
    return file_name


def ffmpeg__to_mp3(
    from_file: str,
    bitrate: int = 96,
):
    # ffmpeg -i input.wav -vn -ar 44100 -ac 2 -b:a 192k output.mp3

    to_file = add_suffix(from_file, ".mp3")

    ffmpeg_path = conf.ffmpeg.path
    ffmpeg_args = [ffmpeg_path]
    ffmpeg_args.extend(["-i", from_file])
    ffmpeg_args.extend(["-b:a", f"{bitrate}k"])
    ffmpeg_args.append(to_file)
    subprocess.run(ffmpeg_args)

    return to_file


def balcon(from_txt_file: str, language: str = "ru"):
    to_file = add_suffix(from_txt_file, ".wav")

    lang_conf = conf.balcon.defaults[language]

    balcon_path = conf.balcon.path
    balcon_args = [balcon_path]
    balcon_args.extend(["-f", from_txt_file])
    balcon_args.extend(["-n", lang_conf.voice])
    balcon_args.extend(["-s", str(lang_conf.speed)])
    balcon_args.extend(["-p", str(lang_conf.pitch)])
    balcon_args.extend(["-v", str(lang_conf.volume)])
    balcon_args.extend(["-w", to_file])

    subprocess.run(balcon_args)

    return to_file


def blb2txt(from_file: str):
    # .\blb2txt -f tst.docx -out txt.txt -e utf8
    to_file = add_suffix(from_file, ".txt")

    blb2txt_path = conf.utils.blb2txt.path
    blb2txt_args = [blb2txt_path]
    blb2txt_args.extend(["-f", from_file])
    blb2txt_args.extend(["-out", to_file])
    blb2txt_args.extend(["-e", "utf8"])

    subprocess.run(blb2txt_args)

    return to_file
