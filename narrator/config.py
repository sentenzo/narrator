import logging
import os
from typing import Any

import dotenv
import yaml
from box import Box

dotenv.load_dotenv()

logger = logging.getLogger(__name__)

CONFIG_PATHS = ["config.yml"]


class _Config(object):
    def __init__(self, config_paths: str | list[str] = CONFIG_PATHS) -> None:
        _config = None
        if isinstance(config_paths, str):
            config_paths = [config_paths]

        for path in config_paths:
            try:
                with open(path, "r") as file:
                    _config = yaml.safe_load(file)
            except FileNotFoundError:
                logger.info(f'Faild to load from "{path}"')

        _config = _config or {}

        _config = Box(_config, default_box=True)

        _config.bot.token = os.environ.get("NARRATOR_BOT_TOKEN", None)

        if not _config.bot.token:
            logger.warning("Faild to grab bot token")

        _config.bot.allowed_usernames = _config.bot.allowed_usernames or []
        allowed_usernames = os.environ.get("NARRATOR_BOT_USERNAMES_WHITELIST", "")
        allowed_usernames = allowed_usernames.split(",")
        for username in allowed_usernames:
            if not username in _config.bot.allowed_usernames:
                _config.bot.allowed_usernames.append(username)

        # _config.setdefault(None)

        object.__setattr__(self, "_config", _config)

    def __getattr__(self, __name: str) -> Any:
        if __name == "_config":
            return object.__getattr__(self, __name)
        else:
            return self._config[__name]

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "_config":
            object.__setattr__(self, __name, __value)
        else:
            self._config[__name] = __value


_conf = _Config()


def __getattr__(__name):
    return _conf.__getattr__(__name)
