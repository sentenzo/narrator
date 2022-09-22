import subprocess

from narrator.utils import add_suffix
import narrator.config

conf = narrator.config.thirdparty


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

    blb2txt_path = conf.blb2txt.path
    blb2txt_args = [blb2txt_path]
    blb2txt_args.extend(["-f", from_file])
    blb2txt_args.extend(["-out", to_file])
    blb2txt_args.extend(["-e", "utf8"])

    subprocess.run(blb2txt_args)

    return to_file
