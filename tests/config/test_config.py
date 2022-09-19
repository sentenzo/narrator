import os

import pytest
import yaml


from narrator.config import _Config


CONF_YML_PATH = os.path.join("tests", "config", "config.yml")
CONF_YML = yaml.safe_load(open(CONF_YML_PATH))

EMPTY_ENV = {
    "NARRATOR_BOT_TOKEN": None,
    "NARRATOR_BOT_USERNAMES_WHITELIST": None,
}

MOCK_ENV = {
    "NARRATOR_BOT_TOKEN": "0123456789:abcdefghABCDEFGHIJKLMNOPQRSTUVWXYZ0",
    "NARRATOR_BOT_USERNAMES_WHITELIST": "john_johnson,peter_peterson,david_davidson",
}


@pytest.mark.parametrize("custom_env", [EMPTY_ENV], indirect=True)
def test_config_nothing(custom_env):
    conf = _Config("this_path_does_not_exist")
    assert conf.bot.token == None


@pytest.mark.parametrize("custom_env", [MOCK_ENV], indirect=True)
def test_config_env(custom_env):
    conf = _Config("this_path_does_not_exist")

    assert conf.bot.token == MOCK_ENV["NARRATOR_BOT_TOKEN"]
    usernames_whitelist = MOCK_ENV["NARRATOR_BOT_USERNAMES_WHITELIST"].split(",")
    assert sorted(conf.bot.allowed_usernames) == sorted(usernames_whitelist)


@pytest.mark.parametrize("custom_env", [EMPTY_ENV], indirect=True)
def test_config_yml(custom_env):
    conf = _Config(CONF_YML_PATH)

    assert conf.utils.balcon.path == CONF_YML["utils"]["balcon"]["path"]
    assert conf.utils.ffmpeg.path == CONF_YML["utils"]["ffmpeg"]["path"]


@pytest.mark.parametrize("custom_env", [MOCK_ENV], indirect=True)
def test_config_env_yml(custom_env):
    conf = _Config(CONF_YML_PATH)

    assert conf.bot.token == MOCK_ENV["NARRATOR_BOT_TOKEN"]

    usernames_whitelist = MOCK_ENV["NARRATOR_BOT_USERNAMES_WHITELIST"].split(",")
    usernames_whitelist.extend(CONF_YML["bot"]["allowed_usernames"])
    assert sorted(conf.bot.allowed_usernames) == sorted(usernames_whitelist)

    assert conf.utils.balcon.path == CONF_YML["utils"]["balcon"]["path"]
    assert conf.utils.ffmpeg.path == CONF_YML["utils"]["ffmpeg"]["path"]
