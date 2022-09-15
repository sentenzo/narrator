import os
import subprocess

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
            f = f[:-RSTR_LEN]
    return join(d, f + e)


def add_suffix(file_path, ext=None):
    from os.path import dirname, basename, join, splitext

    new_filename = [dirname(file_path)]
    old_filename, old_ext = splitext(basename(file_path))
    ext = ext or old_ext or ""
    if len(old_filename) > (RSTR_LEN + 1) and old_filename[-(RSTR_LEN + 1)] == "_":
        rstr = old_filename[-RSTR_LEN:]
        if all(c in RSTR_POPULATION for c in rstr):
            old_filename = old_filename[:-RSTR_LEN]
    new_filename.append(f"{old_filename}_{rand_str()}{ext}")
    return join(*new_filename)


def ffmpeg__to_mp3(
    from_file: str,
    bitrate: int,
):
    # ffmpeg -i input.wav -vn -ar 44100 -ac 2 -b:a 192k output.mp3

    to_file = add_suffix(from_file, ".mp3")

    ffmpeg_path = os.environ["BOT_FFMPEG_PATH"]
    ffmpeg_args = [ffmpeg_path]
    ffmpeg_args.extend(["-i", from_file])
    ffmpeg_args.extend(["-b:a", f"{bitrate}k"])
    ffmpeg_args.append(to_file)
    subprocess.run(ffmpeg_args)

    return to_file


def balcon(from_txt_file: str):
    to_file = add_suffix(from_txt_file, ".wav")

    balcon_path = os.environ["BOT_BALCON_PATH"]
    balcon_args = [balcon_path]
    balcon_args.extend(["-f", from_txt_file])
    balcon_args.extend(["-n", "Irina"])
    balcon_args.extend(["-s", "8"])
    balcon_args.extend(["-p", "0"])
    # balcon_args.extend(["-v", "100"])
    balcon_args.extend(["-w", to_file])

    subprocess.run(balcon_args)

    return to_file
