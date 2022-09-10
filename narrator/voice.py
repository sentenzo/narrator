import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty("voices")
# for voice in engine.getProperty('voices'):
#     print(voice)

# engine.setProperty('voice', voices[1].id)
engine.setProperty(
    "voice",
    "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0",
)
engine.say("You have selected Microsoft Zira as the computer's default voice.")
engine.say("Kill all humans!")
engine.say("Sorry, wrong data file.")
engine.say("А по-русски я не умею говорить. Но ошибок не выдаю. Просто игнорирую.")

engine.setProperty(
    "voice",
    "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0",
)
engine.say(
    "Притяжательные прилагательные обозначают принадлежность чего-либо лицу или животному и отвечают на вопросы чей? чья? чьё?"
)
engine.say("London is the capital of Great Britain")
engine.say("Let me speak from my heart!")

# engine.save_to_file('Hello World', 'test.mp3')

engine.runAndWait()
