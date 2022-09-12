from __future__ import annotations
from typing import Any

import uuid

import pyttsx3


class Voice:
    _PROP_DEFAULTS = {
        "voice": pyttsx3.init().getProperty("voices")[0].id,
        "volume": 0.5,
        "rate": 100,
    }

    # works only in sync mode (TODO: make it work async)
    _current_uid: str = None

    def __init__(
        self,
    ) -> None:
        self._uid: str = uuid.uuid4().hex.upper()
        self._engine: pyttsx3.Engine = pyttsx3.init()  # this is actually a singleton
        self._properties: dict[str, Any] = {}

    def _wipe_props(self) -> None:
        for prop_name, default in Voice._PROP_DEFAULTS.items():
            self._engine.setProperty(prop_name, default)

    def _merge_props(self, props: dict[str, Any] | None = None) -> None:
        props = props or self._properties
        for prop_name, prop_value in props.items():
            self._engine.setProperty(prop_name, prop_value)

    def _switch_props(self):
        if Voice._current_uid != self._uid:
            self._wipe_props()
            self._merge_props()

    def say(self, text: str) -> None:
        self._switch_props()

        self._engine.say(text)
        self._engine.runAndWait()

    def save_to_file(self, text: str, file_name: str | None = None) -> None:
        self._switch_props()

        if not file_name:
            file_name = "".join(
                ["./audio/", text[:10], "_", uuid.uuid4().hex.upper()[:6], ".wav"]
            )
        self._engine.save_to_file(text, file_name)
        # works only if the text has no '\n's
        # 2 minutes audio == 5 Mb
        # the format is: PCM signed 16-bit little-endian
        self._engine.runAndWait()


class VoiceBuilder:
    def __init__(self) -> None:
        self._voice_properties = {}
        self._cache = {}

    def build(self) -> Voice:
        voice = Voice()
        voice._properties |= self._voice_properties
        return voice

    def voice(self, voice_name: str) -> VoiceBuilder:
        if not "voices" in self._cache:
            self._cache["voices"] = pyttsx3.init().getProperty("voices")
        voices = self._cache["voices"]
        for voice in voices:
            if voice_name.lower() in voice.id.lower():
                self._voice_properties["voice"] = voice.id
                break
        return self

    def volume(self, volume_val: float) -> VoiceBuilder:
        volume_val = max(volume_val, 0.0)
        volume_val = min(volume_val, 1.0)
        self._voice_properties["volume"] = float(volume_val)
        return self

    def rate(self, rate_val: int) -> VoiceBuilder:
        self._voice_properties["rate"] = float(rate_val)
        return self


if __name__ == "__main__":
    nar_zira = VoiceBuilder().voice("zira").rate(300).build()
    nar_irina = VoiceBuilder().voice("irina").rate(500).volume(0.8).build()

    nar_zira.say("You have selected Microsoft Zira as the computer's default voice.")
    nar_zira.say(
        "А по-русски я не умею говорить. Но ошибок не выдаю. Просто игнорирую."
    )

    nar_irina.say("Этот город боится меня. Я видел его истинное лицо.")
    # nar_irina.say("London is the capital of Great Britain")
    nar_irina.say("Let me speak from my heart!")

    text = "Лет двести тому назад ветер-сеятель принес два семечка в Блудово болото: семя сосны и семя ели."
    nar_irina.save_to_file(text + text + text + text)
